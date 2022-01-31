from datetime import datetime

from netCDF4 import MFDataset, date2index, num2date


# # __author__ = 'Trond Kristiansen'
# # __email__ = 'trond.kristiansen@niva.no'
# __author__ = 'Joe McGovern, Irish Marine Institute'
# __email__ = 'joe.mcgovern@marine.ie'
# # __created__ = datetime(2008, 8, 15)
# __modified__ = datetime(2021, 11, 29)
# __version__ = "1.X"
# __status__ = "Development, most recent update 29.11.2021"


# Main function called from model2roms
def get_filename(confM2R, year, month, day, defaultvar):
    if confM2R.ocean_indata_type == 'SODA3':
        if defaultvar is None:
            defaultvar = "salinity"
        filenamein = getSODA3filename(confM2R, year, month, day, defaultvar)
    if confM2R.ocean_indata_type == 'SODA3_5DAY':
        if defaultvar is None:
            defaultvar = "salinity"
        filenamein = getSODA3_5DAYfilename(confM2R, year, month, day, defaultvar)
    if confM2R.ocean_indata_type == 'NORESM':
        if defaultvar is None:
            defaultvar = "grid"
        filenamein = getNORESMfilename(confM2R, year, month, defaultvar)
    if confM2R.ocean_indata_type == 'GLORYS':
        if defaultvar is None:
            defaultvar = "So"
        filenamein = get_GLORYS_filename(confM2R, year, month, defaultvar)
    if confM2R.ocean_indata_type == 'IBI':
        if defaultvar is None:
            defaultvar = "so"
        filenamein = get_IBI_filename(confM2R, year, month, day, defaultvar)
    return filenamein


# private functions called from within module
def get_IBI_filename(confM2R, year, month, day, varname):
    # return "{}{}/CMEMS_{}_monthly_MERCATOR_{}-{}.nc".format(confM2R.ocean_forcing_path, varname.lower(),
    #                                                         varname.capitalize(),
    #                                                         year, str(month).zfill(2))
    # e.g. CMEMS_v5r1_IBI_BIO_MY_PdE_01dav_20180101_20180101_R20201201_RE01.nc
    #      "CMEMS_v5r1_IBI_PHY_MY_PdE_01dav_{}{}{}_{}{}{}_R20201201_RE01.nc"
    return "{}/CMEMS_v5r1_IBI_PHY_MY_PdE_01dav_{}{}{}_{}{}{}_R20201201_RE01.nc".format(confM2R.ocean_forcing_path,
                                                                                       year, str(month).zfill(2),
                                                                                       str(day).zfill(2),
                                                                                       year, str(month).zfill(2),
                                                                                       str(day).zfill(2))


# private functions called from within module
def get_GLORYS_filename(confM2R, year, month, varname):
    return "{}{}/CMEMS_{}_monthly_MERCATOR_{}-{}.nc".format(confM2R.ocean_forcing_path, varname.lower(),
                                                            varname.capitalize(),
                                                            year, str(month).zfill(2))


def getNORESMfilename(confM2R, year, month, myvar):
    if myvar == 'grid':
        filename = confM2R.ocean_forcing_path + 'grid_gx1v6.nc'
    else:
        if myvar in ['iage', 'uvel', 'vvel', 'aice', 'hi', 'hs']:
            filename = confM2R.ocean_forcing_path + 'ICE/NRCP45AERCN_f19_g16_CLE_01.cice.h.' + str(year) + '.nc'

        elif myvar in ['dissic', 'talk', 'po4', 'no3', 'si', 'o2']:
            filename = confM2R.ocean_forcing_path + "BCG_NRCP85BPRPEX_01.micom.hbgcmlvl.2006-2050.nc"

        elif myvar in ['templvl', 'salnlvl', 'sealv', 'uvellvl', 'vvellvl']:
            if myvar in ['salnlvl', 'templvl']:
                filename = confM2R.ocean_forcing_path + "TS_NRCP85BPRPEX_01.micom.2006-2100.nc"
            else:
                filename = confM2R.ocean_forcing_path + "VEL_NRCP85BPRPEX_01.micom.hmlvl.2006-2100.nc"
    return filename


def getSODA3filename(confM2R, year, month, day, myvar):
    if (myvar in ['cn', 'hi', 'hs']):
        return confM2R.ocean_forcing_path + "soda3.3.1_mn_ice_reg_" + str(year) + ".nc"
    else:
        return confM2R.ocean_forcing_path + "soda3.3.1_mn_ocean_reg_" + str(year) + ".nc"


def getSODA3_5DAYfilename(confM2R, year, month, day, myvar):
    if len(confM2R.time_object) == 0:
        mcdf = MFDataset(confM2R.ocean_forcing_path + "*.nc")
        confM2R.time_object = mcdf.variables["time"]

    # print("Loaded all timesteps: {}".format(confM2R.time_object[:]))
    index = date2index(datetime(year, month, day, 0, 0), confM2R.time_object, calendar=confM2R.time_object.calendar,
                       select="nearest")
    seldate = num2date(confM2R.time_object[index], units=confM2R.time_object.units,
                       calendar=confM2R.time_object.calendar)

    if (myvar in ['cn', 'hi', 'hs']):
        return '{}soda3.3.2_5dy_ocean_ice_{:04}_{:02}_{:02}.nc'.format(confM2R.ocean_forcing_path, seldate.year,
                                                                       seldate.month, seldate.day)
    else:
        return '{}soda3.3.2_5dy_ocean_reg_{:04}_{:02}_{:02}.nc'.format(confM2R.ocean_forcing_path, seldate.year,
                                                                       seldate.month, seldate.day)
