import gdal
import numpy as np
import subprocess
from glob import glob

def corners(filename):
    '''
    [minx, maxy, maxx, miny] = corners coords of filename
    '''
    #http://stackoverflow.com/questions/2922532/obtain-latitude-and-longitude-from-a-geotiff-file
    ds = gdal.Open(filename)
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + (height * gt[5])
    maxx = gt[0] + width*gt[1] + (height * gt[2])
    maxy = gt[3]
    return [minx, maxy, maxx, miny]



def main():
    tif_dir = input("Enter the path to the tif directory")
    tif_paths = glob(f"{tif_dir}/*.tif")
    extents = [corners(coord) for coord in tif_paths]
    # print(f"All extents: {repr(extents)}")
    new_extent = [min(x[0] for x in extents),
                  max(x[1] for x in extents),
                  max(x[2] for x in extents),
                  min(x[3] for x in extents)]
    # print(f"Corner coords for largest extent covering all images in stack: {repr(new_extent)}")

    in_files = ''
    for path in tif_paths:
        in_files = f" {in_files} {path}"

    cmd = f"gdal_merge.py -o {tif_dir}/merged.tif -ul_lr {' '.join([str(x) for x in new_extent])} -separate -tap {in_files}"
    subprocess.call(cmd, shell=True)


    print(gdal.Info(f"{tif_dir}/merged.tif", format='json')['cornerCoordinates'])

    for i in range(1, len(tif_paths)+1):
        gdal.Translate(f"{tif_dir}/merged_{i}.tif", f"{tif_dir}/merged.tif", options=gdal.TranslateOptions(bandList=np.array([1])) )



if __name__ == "__main__":
    main()




# step 2 merging


