import logging
import subprocess
from datetime import datetime
import os
import numpy.f2py as f2py

# __author__ = 'Trond Kristiansen'
__author__ = 'Joe McGovern, Irish Marine Institute'
# __email__ = 'me@trondkristiansen.com'
__email__ = 'joe.mcgovern@marine.ie'
__created__ = datetime(2009, 11, 11)
# __modified__ = datetime(2018, 4, 5)
__modified__ = datetime(2021, 11, 29)
__version__ = "1.0"
__status__ = "Development, 11.11.2009, 14.3.2012, 31.5.2012, 5.4.2018, 29.11.2021"


def help():
    """
    @compile This is a simple script to call for automatic compiling of all
    fortran files necessary to run the soda2roms package. This is turned on in
    main.py with the compileAll=True

    Call this from command line using python compile.py

    NOTE!
    To run this on Hecxagon do this first:
    module swap PrgEnv-pgi PrgEnv-gnu
    module unload notur
    Then remove the -fcompiler=intelem command

    NOTE: cleanarray.f90 is no longer used as fill.90 has better fill options
    using Laplace equation. 
    """


def compileallifort(log):

    logging.info("[M2R_compile] Compiling barotropic.f90 to create ==> barotropic.so")
    proc = subprocess.Popen(
        'f2py --verbose --fcompiler=intelem -c -m barotropic barotropic.f90 --f90flags="-no-heap-arrays"',
        shell=True, stdout=log, )
    stdout_value = proc.communicate()
    log.writelines(repr(stdout_value))

    logging.info("[M2R_compile] Compiling interpolation.f90 to create ==> interpolation.so")
    proc = subprocess.Popen(
        'f2py --verbose --fcompiler=intelem -c -m interpolation interpolation.f90 --f90flags="-no-heap-arrays"',
        shell=True, stdout=log, )
    stdout_value = proc.communicate()[0]
    log.writelines(repr(stdout_value))

    logging.info("[M2R_compile] Compiling fill.f90 to create ==> extrapolate.so")
    proc = subprocess.Popen(
        'f2py --verbose --fcompiler=intelem -c -m extrapolate fill.f90 --f90flags="-no-heap-arrays"',
        shell=True, stdout=log, )
    stdout_value = proc.communicate()[0]
    log.writelines(repr(stdout_value))

    log.close()


def compileallgfortran(log):

    logging.info("[M2R_compile] Compiling barotropic.f90 to create ==> barotropic.so")
    proc = subprocess.Popen('f2py -c -m barotropic barotropic.f90',
                            shell=True, stdout=log,)
    stdout_value = proc.communicate()
  #  log.writelines(repr(stdout_value))

    logging.info("[M2R_compile] Compiling interpolation.f90 to create ==> interpolation.so")
    proc = subprocess.Popen('f2py -c -m interpolation interpolation.f90',
                            shell=True, stdout=log,)
    stdout_value = proc.communicate()[0]
   # log.writelines(repr(stdout_value))

    logging.info("[M2R_compile] Compiling fill.f90 to create ==> extrapolate.so")
    proc = subprocess.Popen('f2py -c -m extrapolate fill.f90',
                            shell=True, stdout=log,)
    stdout_value = proc.communicate()[0]
   # log.writelines(repr(stdout_value))
    log.close()


def compilefortran(compiler):

    logfile = "compile.log"
    if os.path.exists(logfile):
        os.remove(logfile)
    log = open(logfile, 'a')

    logging.info("[M2R_compile] Adding LDFALGS required for Python 3")
    proc = subprocess.Popen('export LDFLAGS="-undefined dynamic_lookup -bundle"',
                            shell=True, stdout=log, )
    if compiler == "gfortran":
        compileallgfortran(log)

    elif compiler == "ifort":
        compileallifort(log)
    else:
        raise Exception("No compiler selected - aborting the compilation")

    logging.info("[M2R_compile] Compilation finished and results written to file => %s" % logfile)
    logging.info("[M2R_compile] ===================================================================")

if __name__ == "__main__":

    compilefortran("gfortran")

