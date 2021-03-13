"""
Script to covert Sentinel-1 Surface Water Extent GeoTIFF into netCDF for THREDDS
"""
import argparse
import glob
import netCDF4 as nc
import os
import xarray as xr

def geotiff_to_thredds_compatible_nc(src_dir):
    paths = glob.glob(f"{src_dir}/*.tif")
    nc_dir = f"{src_dir}/netcdf_mosaics"
    os.makedirs(nc_dir, exist_ok=True)

    for p in paths:
        time = os.path.basename(p).split('.')[0]

        # read tiff to array
        a = xr.open_rasterio(p, 'r')
        print(type(a.values))

        # a tuple showing the dimensions of the geotiff data (# of bands, # of latitude steps, # of longitude steps)
        shape = a.values.shape

        # create the new netcdf
        f = nc.Dataset(filename=f'{nc_dir}/{time}.nc', mode='w')

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
        f['time'][:] = time
        f['lat'][:] = a.y.values
        f['lon'][:] = a.x.values
        f['S1_SWE'][:] = a.values

        # write data to and close the new netcdf
        f.sync()
        f.close()

def main():
    parser = argparse.ArgumentParser(description='convert geotiff to Thredds wms compatible netcdf')
    parser.add_argument(dest='src_dir', metavar='src_dir')
    args = parser.parse_args()

    geotiff_to_thredds_compatible_nc(args.src_dir)

if __name__ == "__main__":
    main()