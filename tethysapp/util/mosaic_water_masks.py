import gdal
import glob
from datetime import date
from datetime import datetime
import re


def date_from_product_name(product_name: str) -> str:
    regex = "\w[0-9]{7}T[0-9]{6}"
    results = re.search(regex, product_name)
    if results:
        return results.group(0).split('T')[0]
    else:
        return None

def seconds_from_product_name(product_name: str) -> str:
    regex = "\w[0-9]{7}T[0-9]{6}"
    results = re.search(regex, product_name)
    if results:
        date = results.group(0).split('T')[0]
        date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        return datetime.fromisoformat(date).timestamp()
    else:
        return None

def get_epsg(path):
    info = gdal.Info(path, format='json')
    info = info['coordinateSystem']['wkt']
    return info.split('ID')[-1].split(',')[1][0:-2]


paths = glob.glob('/home/alex/Documents/Watermasks_F/*.tif')
print(paths)
interval = 1296000  # 15 days as seconds
batches = [int(seconds_from_product_name(p))//interval for p in paths]
epsgs = [get_epsg(p) for p in paths]

for i, p in enumerate(paths):


# for path in paths:
#     #info = gdal.Info(path, format='json')
#     #info = info['coordinateSystem']['wkt']
#     #zone = info.split('ID')[-1].split(',')[1][0:-2]
#     #print(zone)
#
#     day = int(date_from_product_name(path)[-2:])
#     if day < 16:
#         new_path = f"{path.replace('.tif', '_batch_1.tif')}"
#         gdal.Warp(new_path , path, srcSRS='EPSG:32646', dstSRS='EPSG:4326')
#         batch_1.append(new_path)
#     else:
#         new_path = f"{path.replace('.tif', '_batch_2.tif')}"
#         gdal.Warp(new_path, path, srcSRS='EPSG:32646', dstSRS='EPSG:4326')
#         batch_2.append(new_path)
#
#
# for p in batch_1:
#     info = gdal.Info(p, format='json')
#     info = info['coordinateSystem']['wkt']
#     zone = info.split('ID')[-1].split(',')[1][0:-2]
#     print(zone)
#
# for p in batch_2:
#     info = gdal.Info(p, format='json')
#     info = info['coordinateSystem']['wkt']
#     zone = info.split('ID')[-1].split(',')[1][0:-2]
#     print(zone)
#
