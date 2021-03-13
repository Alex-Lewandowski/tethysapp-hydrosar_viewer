"""
batch_mosaic_water_masks.py
Alex Lewandowski
Alaska Satellite Facility
2021-3-12

Takes a path to a directory holding water masked scenes (geotiffs),
each containing its acquisition timestamp in its filename,
formatted YYYYMMDDTHHMMSS

Takes an optional time interval (int seconds, default=1296000) for merging tifs by date range
Images are batched for merging in UNIX time (seconds since 1970-01-01 00:00:00)

Reprojects all geotiffs to epsg arg (default=4326 for Thredds)
Reprojections saved in "batches" subdirectory

Mosaics batched geotiffs
Each mosaic named by the end of its time interval in UNIX seconds (i.e. 1592784000.tif)
"""

import argparse
from datetime import datetime
import glob
import os
import re
import subprocess

import numpy as np
from osgeo import gdal

from tif_water_mask_to_nc import geotiff_to_thredds_compatible_nc


def seconds_from_filename(product_name: str) -> float:
    regex = "\w[0-9]{7}T[0-9]{6}"
    results = re.search(regex, product_name)
    if results:
        date = results.group(0).split('T')[0]
        date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        return datetime.fromisoformat(date).timestamp()
    else:
        return None


def seconds_from_batch(batch, interval):
    return batch * interval


def batch_from_seconds(path, interval):
    return int(seconds_from_filename(path)) // interval


def get_epsg(path):
    info = gdal.Info(path, format='json')
    info = info['coordinateSystem']['wkt']
    return info.split('ID')[-1].split(',')[1][0:-2]


def corners(filename):
    '''
    http://stackoverflow.com/questions/2922532/obtain-latitude-and-longitude-from-a-geotiff-file
    [minx, maxy, maxx, miny] = corners coords of filename
    '''
    ds = gdal.Open(filename)
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width * gt[4] + (height * gt[5])
    maxx = gt[0] + width * gt[1] + (height * gt[2])
    maxy = gt[3]
    return [minx, maxy, maxx, miny]


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_cover_all_corner_coords(paths):
    extents = [corners(coord) for coord in paths]
    return [min(x[0] for x in extents),
            max(x[1] for x in extents),
            max(x[2] for x in extents),
            min(x[3] for x in extents)]


def main():
    # argument parsing
    parser = argparse.ArgumentParser(description='batch and mosaic geotiffs by date range')
    parser.add_argument(dest='src_dir', metavar='src_dir')
    parser.add_argument('-ul_lr', dest='ul_lr',
                        action='store', default="88.0069826 28.5101134 92.2258500 20.4043523",
                        help='Area of Interest upper-left and lower-right corner coords "ulx uly lrx lry" default="88.0069826 28.5101134 92.2258500 20.4043523"')
    parser.add_argument('-e', '--epsg', dest='epsg',
                        action='store', default='4326',
                        help='reprojection epsg, default=4326')
    parser.add_argument('-i', '--interval', dest='interval',
                        action='store', default=1296000,
                        help='time range length in seconds, default=1296000')
    parser.add_argument('-c', '--cover_all', dest='cover_all',
                        type=str2bool, default=False,
                        help='Use the AOI needed to cover every pixel val == 1 in the stack')
    args = parser.parse_args()

    # collect paths to tiffs and create directory to hold reprojected tifs, labeled by batch #
    paths = sorted(glob.glob(f'/{args.src_dir}/*.tif'))
    batch_dir = f"{args.src_dir}/batches"
    os.makedirs(batch_dir, exist_ok=True)

    # sort images into batches (default == 1296000 seconds == 15 days)
    batches = [batch_from_seconds(p, int(args.interval)) for p in paths]
    epsg = [get_epsg(p) for p in paths]

    # reproject all images to epsg (default=4326), saving them to "batches" subdirectory
    for i, p in enumerate(paths):
        new_path = f"{batch_dir}/{os.path.basename(p.replace('.tif', f'_{batches[i]}.tif'))}"
        gdal.Warp(new_path, p, srcSRS=f'EPSG:{epsg[i]}', dstSRS=f'EPSG:{args.epsg}')

    # collect paths to the batched tifs
    paths = sorted(glob.glob(f'{batch_dir}/*.tif'))

    # build space separated string of tif paths in each batch, store in dict
    batch_dict = {key: "" for key in set(batches)}
    print(batch_dict)
    for p in paths:
        batch = int(p.split('_')[-1].split('.')[0])
        batch_dict.update({batch: f'{batch_dict[batch]} {p}'})

    # create directory to hold mosaics
    mosaic_dir = f"{args.src_dir}/mosaics"
    os.makedirs(mosaic_dir, exist_ok=True)

    # merge tifs by batch, saving them to "mosaics" subdirectory
    for batch in batch_dict:
        dest_path = f"{mosaic_dir}/{seconds_from_batch(batch, int(args.interval))}.tif"
        print(dest_path)
        merge_cmd = f"gdal_merge.py -o {dest_path} {batch_dict[batch]}"
        subprocess.call(merge_cmd, shell=True)

    # collect paths to mosacis and list them in a space separated string
    paths = sorted(glob.glob(f'{mosaic_dir}/*.tif'))
    in_files = ''
    for p in paths:
        in_files = f" {in_files} {p}"

    # merge mosaics into a temporary multi-band geotiff, subset by ul_lr corner coords
    # this will prevent off-by-one pixel errors in the final, single-band mosaic stack
    temp_merged = f"{mosaic_dir}/merged.tif"
    if args.cover_all:
        args.ul_lr = ' '.join(map(str, get_cover_all_corner_coords(paths)))
    cmd = f"gdal_merge.py -o {temp_merged} -ul_lr {args.ul_lr} -separate -tap {in_files}"
    subprocess.call(cmd, shell=True)

    # create single-band mosaics from multi-band mosaic, overwriting the originals
    for i in range(1, len(paths) + 1):
        gdal.Translate(f"{mosaic_dir}/{os.path.basename(paths[i - 1])}", f"{mosaic_dir}/merged.tif",
                       options=gdal.TranslateOptions(bandList=np.array([i])))
        print(gdal.Info(f"{mosaic_dir}/{os.path.basename(paths[i - 1])}", format='json')['cornerCoordinates'])

    # delete the temporary multi-band mosaic
    try:
        os.remove(temp_merged)
    except FileNotFoundError:
        raise

    geotiff_to_thredds_compatible_nc(mosaic_dir)

    print(f'\nPath to Geotiff Mosaics: {mosaic_dir}')


if __name__ == "__main__":
    main()
