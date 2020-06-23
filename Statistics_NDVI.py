#!/usr/bin/env python3
#---------------------------------------------------------------------------------------------------------------------
# Testscript for statistical calculation of NDVI Change Indice (Summer vs. Winter 2019)
#---------------------------------------------------------------------------------------------------------------------

import sys
import grass.script as grass

from grass import parser, parse_key_val
from subprocess import PIPE


def main():

    # for ChangeIndice_NDVI_Summer_Winter_2019: divide into classes and calculate statistics
    grass.run_command('r.recode',
                      input='ChangeIndice_NDVI_Summer_Winter_2019',
                      output='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      rules='C:/Sentinel2Project/reclass.txt')

    grass.run_command('r.colors',
                      map='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      rules='C:/Sentinel2Project/colors.txt')

    grass.run_command('r.to.vect',
                      flags='s,v',
                      input='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      output='ChangeIndice_NDVI_Summer_Winter_2019_class')

    grass.run_command('v.clean',
                      input='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      output='ChangeIndice_NDVI_Summer_Winter_2019_vect',
                      tool='rmarea',
                      threshold='1600')

    # Calculation of NDVI statistics
    grass.run_command('v.rast.stats',
                      flags='c',
                      map='ChangeIndice_NDVI_Summer_Winter_2019_vect',
                      raster='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      column_prefix='statistic')

if __name__ == "__main__":
    options, flags = grass.parser()

    sys.exit(main())