#!/usr/bin/env python3

#%module
#% description: Calculate NDVI, SAVI and NDWI as Space Time Datacube (STC).
#%end

#%option G_OPT_STRDS_INPUTS
#% key: raster
#% description: b4, b8, b12 and cldmsk
#-----------------------------------------------------------------------------------------------------------
# vegetationIndices.py
#-----------------------------------------------------------------------------------------------------------
# Programm calculates the Normalized Difference Vegetation (NDVI), the Soil Adjusted Vegetation Index (SAVI)
# and the Normalized Difference Water Index (NDWI), when there are no clouds and saves them as
# Space-Time-Cube (STC).
#-----------------------------------------------------------------------------------------------------------

# Import modules
import sys
import grass.script as grass

def main():
    # Calculate NDVI, when there are no clouds
    grass.run_command('t.rast.mapcalc',
                      input= options['raster'],
                      expression = 'ndvi = if(!isnull(cldmsk), null(), float(b8 - b4) / ( b8 + b4 ))',
                      output = 'ndvi',
                      basename = 'ndvi',
                      nprocs = '3',
                      overwrite = True)
    grass.run_command('t.rast.colors',
                      input = 'ndvi',
                      color = 'ndvi') # color: ndvi


    # Calculate SAVI, when there are no clouds, with L = 0.5
    grass.run_command('t.rast.mapcalc',
                      input= options['raster'],
                      expression = 'savi = if(!isnull(cldmsk), null(), float(1.5* (b8-b4)) / ( b8+b4+0.5))',
                      output = 'savi',
                      basename = 'savi',
                      nprocs = '3',
                      overwrite = True)
    grass.run_command('t.rast.colors',
                      input = 'savi',
                      color = 'ndvi') # color set like ndvi, because there is more vegetation with raising savi.


    # Calculate NDWI after Goa (1996), when there are no clouds
    grass.run_command('t.rast.mapcalc',
                      input= options['raster'],
                      expression = 'ndwi = if(!isnull(cldmsk), null(), float(b8 - b12) / ( b8 + b12))',
                      output = 'ndwi',
                      basename = 'ndwi',
                      nprocs = '3',
                      overwrite = True)
    grass.run_command('t.rast.colors',
                      input = 'ndwi',
                      color = 'ndwi')  # color: ndwi

if __name__ == "__main__":
    options, flags = grass.parser()

    sys.exit(main())
