#!/usr/bin/env python3

#%module
#% description: Create Space Time Datacubes (STC) for Sentinel-2 channels and cloudmasks.
#%end

#%option G_OPT_F_INPUT
#% key: timestamps_raster
#% description: Name of textfile with timestamps for sentinel bands
#%end

#%option G_OPT_F_INPUT
#% key: timestamps_clouds
#% description: Name of textfile with timestamps for cloudmasks
#%end

#-----------------------------------------------------------------------------------------------------------
# STC.py
#-----------------------------------------------------------------------------------------------------------
# Programm creates and registrates a STC of rasters and cloudmasks first.
# Finally, it extracts all Sentinel-2 channels as STC.
#-----------------------------------------------------------------------------------------------------------

# Import modules
import sys
import grass.script as grass

def main():
    #Create STC of rasters
    grass.run_command('t.create',
                      output = 'Sentinel2_Raster',
                      type = 'strds',
                      semantictype = 'mean',
                      temporaltype = 'absolute',
                      title = 'Sentinel2_Raster',
                      description = 'Sentinel2_Raster',
                      overwrite=True)

    # Create STC of cloudmasks
    grass.run_command('t.create',
                      output = 'cldmsk',
                      type = 'strds',
                      semantictype = 'mean',
                      temporaltype = 'absolute',
                      title = 'cldmskk',
                      description = 'cldmsk',
                      overwrite=True)

    # Registrate the Raster-STC
    grass.run_command('t.register',
                      input = 'Sentinel2_Raster',
                      type = 'raster',
                      file = options['timestamps_raster'],
                      overwrite=True)

    # Registrate the Cloudmask-STC
    grass.run_command('t.register',
                      input = 'cldmsk',
                      type = 'raster',
                      file=options['timestamps_clouds'],
                      overwrite=True)

    # Extract all relevant Sentinel-2 channels (B2, B3, B4, B5, B6, B7, B8, B8A, B11 and B12).
    # Channel B1, B9 and B10 are not important for calculating vegetation indices later 
    # (rather for atmospherical correction).
    list = [2,3,4,5,6,7,8,11,12]
    for i in list:
        if i < 11:
            grass.run_command('t.rast.extract',
                              input = 'Sentinel2_Raster',
                              output = 'b' + str(i),
                              overwrite = True,
                              where = 'name like \'%B0' + str(i) + '%\'')
        else:
            grass.run_command('t.rast.extract',
                              input = 'Sentinel2_Raster',
                              output = 'b' + str(i),
                              overwrite = True,
                              where = 'name like \'%B' + str(i) + '%\'')

    grass.run_command('t.rast.extract',
                      input='Sentinel2_Raster',
                      output='b8A',
                      overwrite=True,
                      where='name like \'%B8A%\'')

if __name__ == "__main__":
    options, flags = grass.parser()

    sys.exit(main())
