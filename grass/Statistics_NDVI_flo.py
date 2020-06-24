#!/usr/bin/env python3

#%module
#% description: Testscript for statistical calculation of NDVI Change Indice (Summer vs. Winter 2019)
#%end

#%option G_OPT_F_INPUT
#% key: reclass
#% description: Name of textfile with reclassification rules
#%end

#%option G_OPT_F_INPUT
#% key: color
#% description: Name of textfile with color assignment
#%end

import sys
import grass.script as grass

def main():

    # for ChangeIndice_NDVI_Summer_Winter_2019: divide into classes and calculate statistics
    grass.run_command('r.recode',
                      input='ChangeIndice_NDVI_Summer_Winter_2019',
                      output='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      rules=options['reclass'],
                      overwrite = True)

    grass.run_command('r.colors',
                      map='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      rules=options['color'])

    grass.run_command('r.to.vect',
                      flags='sv',
                      input='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      output='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      type = 'area',
                      overwrite = True)

    grass.run_command('v.clean',
                      input='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      output='ChangeIndice_NDVI_Summer_Winter_2019_vect',
                      tool='rmarea',
                      threshold='1600',
                      overwrite = True)

    # Calculation of NDVI statistics
    grass.run_command('v.rast.stats',
                      flags='c',
                      map='ChangeIndice_NDVI_Summer_Winter_2019_vect',
                      raster='ChangeIndice_NDVI_Summer_Winter_2019_class',
                      column_prefix='statistic')

if __name__ == "__main__":
    options, flags = grass.parser()

    sys.exit(main())
