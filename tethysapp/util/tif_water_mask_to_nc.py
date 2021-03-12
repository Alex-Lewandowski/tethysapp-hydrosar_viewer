"""
Script to covert Sentinel-1 Surface Water Extent GeoTIFF into netCDF for THREDDS
"""
import netCDF4 as nc
import xarray as xr
from datetime import datetime, timezone

# specify filepaths
tiff_path = "/home/alex/Documents/demo_tethys/tethysapp-hydrosar_viewer/data/thredds/2020_watermask/batch_1_merged_aligned.tif"
nc_path = '/home/alex/Documents/demo_tethys/tethysapp-hydrosar_viewer/data/thredds/2020_watermask/merged_1.nc'


# figure out dates
tiff_datetime = datetime(2020, 7, 15)
tiff_date_unix = tiff_datetime.replace(tzinfo=timezone.utc).timestamp()
print(type(tiff_date_unix))

# read tiff to array
a = xr.open_rasterio(tiff_path, 'r')
print(type(a.values))

# a tuple showing the dimensions of the geotiff data (# of bands, # of latitude steps, # of longitude steps)
shape = a.values.shape

# for help with the following code, consult: https://unidata.github.io/netcdf4-python/netCDF4/index.html
# create the new netcdf
f = nc.Dataset(filename=nc_path, mode='w')

f.Conventions = 'CF-1.7'

# create netCDF dimensions
f.createDimension('time', size=1)
f.createDimension('lat', size=shape[1])
f.createDimension('lon', size=shape[2])

# create netCDF variables
f.createVariable('time', datatype='int', dimensions=('time',))
f['time'].standard_name = 'time'
f['time'].long_name = 'time'
f['time'].units = 'seconds since 1970-01-01 00:00:00'
f['time'].calendar = 'gregorian'

f.createVariable('lat', datatype='float', dimensions=('lat',))
f['lat'].standard_name = 'latitude'
f['lat'].units = 'degrees_north'

f.createVariable('lon', datatype='float', dimensions=('lon',))
f['lon'].standard_name = 'longitude'
f['lon'].units = 'degrees_east'

f.createVariable('S1_SWE', datatype='byte', dimensions=('time', 'lat', 'lon'), fill_value=0)
f['S1_SWE'].long_name = 'Sentinel-1 Surface Water Extent'
f['S1_SWE'].units = '1'

# populate time, lon, lat variables

f['time'][:] = tiff_date_unix
f['lat'][:] = a.y.values
f['lon'][:] = a.x.values

print(f['time'][0])


f['S1_SWE'][:] = a.values
# print(f['S1_SWE']._FillValue)
# write data to and close the new netcdf
f.sync()
f.close()
