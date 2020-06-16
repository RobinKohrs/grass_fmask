#!/usr/bin/env python3

#%module
#% description: Create Space Time Datacubes for sentinel data and cloudmasks
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
# S-T-C.py
#-----------------------------------------------------------------------------------------------------------
# Programm creates and registrates a S-T-C of rasters and cloudmasks first. Then it extracts all Sentinel-2
# channels. Finally it calculates the NDVI, when there are no clouds, and an example change indice.
#-----------------------------------------------------------------------------------------------------------

# Import modules
import sys
import grass.script as grass


def main():
    #Create S-T-C of rasters
    grass.run_command('t.create',
                      output = 'Sentinel2_Raster',
                      type = 'strds',
                      semantictype = 'mean',
                      temporaltype = 'absolute',
                      title = 'Sentinel2_Raster',
                      description = 'Sentinel2_Raster',
                      overwrite=True)

    # Create S-T-C of cloudmasks
    grass.run_command('t.create',
                      output = 'Sentinel2_Cloudmask',
                      type = 'strds',
                      semantictype = 'mean',
                      temporaltype = 'absolute',
                      title = 'Sentinel2_Cloudmask',
                      description = 'Sentinel2_Cloudmask',
                      overwrite=True)

    # Registrate the Raster S-T-C
    grass.run_command('t.register',
                      input = 'Sentinel2_Raster',
                      type = 'raster',
                      # Link your timestamp for rasters
                      file = options['timestamps_raster'],
                      overwrite=True)

    # Registrate the Cloudmask S-T-C
    grass.run_command('t.register',
                      input = 'Sentinel2_Cloudmask',
                      type = 'raster',
                      # Link your timestamp for cloudmasks
                      file = options['timestamps_clouds'],
                      overwrite=True)

if __name__ == "__main__":
    options, flags = grass.parser()

    sys.exit(main())
