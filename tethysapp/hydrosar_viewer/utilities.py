import glob
import string
import random
import re
import datetime

class DateRangeNotInFilename(Exception):
    """
    Raised when the expected date range formatted YYMMDD_YYMMDD is not found where expected
    """
    pass

def new_id():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for i in range(10))


def date_string(yymmdd: str) -> str:
    try:
        date = datetime.datetime(int(yymmdd[:4]), int(yymmdd[4:6]), int(yymmdd[6:9]))
    except ValueError:
        raise

    return f'{date.strftime("%B")} {int(yymmdd[6:9])} {yymmdd[:4]}'


def event_name_from_filename(path: str) -> str:
    """
    Takes a path to a file containing a date range formatted YYMMDD_YYMMDD
    Returns a menu ready, pretty print of the date range

    Ex. "20200716_20200731_watermask.nc4" -> "July 16 2020 - July 31 2020"
    """
    regex = '(19|20)[0-9]{2}(0|1)[0-9][0-3][0-9]_(19|20)[0-9]{2}(0|1)[0-9][0-3][0-9]'
    date_range = re.search(regex, path)
    if date_range:
        date_range = date_range.group(0).split('_')
    else:
        raise DateRangeNotInFilename('Filename must contain a date range formatted YYMMDD_YYMMDD')

    return f"{date_string(date_range[0])} - {date_string(date_range[1])}"


def update_ncml(data_dir: str):
    """
    Takes a path to a data dir containing netCDFs and
    creates an ncml containing an aggregation of all
    netCDF locations
    """
    paths = glob.glob(f"{data_dir}/*.nc4")
    netcdf_aggregation = ""
    for path in paths:
        netcdf_aggregation = (f'{netcdf_aggregation}\n'
                              f'        <netcdf location="{path}"/>')

    ncml = (f'<netcdf xmlns="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2">\n'
            f'    <variable name="time" type="int" shape="time">\n'
            f'        <attribute name="units" value="Bi-weekly periods since 2019-01-01 00:00"/>\n'
            f'        <attribute name="_CoordinateAxisType" value="Time" />\n'
            f'            <values start="0" increment="1" />\n'
            f'    </variable>\n'
            f'    <aggregation dimName="time" type="joinExisting" recheckEvery="1 day">'
            f'{netcdf_aggregation}\n'
            f'    </aggregation>\n'
            f'</netcdf>\n')

    with open(f'{data_dir}{data_dir.split("/")[-2]}.ncml', "w") as f:
        f.write(ncml)