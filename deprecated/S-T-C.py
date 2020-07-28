#!/usr/bin/env python3

#%module
#% description: Create Space Time Datacubes for sentinel data and cloudmasks and calculate ndvi
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
                      file = options['timestamps_raster'],
                      overwrite=True)

    # Registrate the Cloudmask S-T-C
    grass.run_command('t.register',
                      input = 'Sentinel2_Cloudmask',
                      type = 'raster',
                      file=options['timestamps_clouds'],
                      overwrite=True)

    # extract all Sentinel-2 channels
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

    # calculate NDVI, when there are no clouds
    grass.run_command('t.rast.mapcalc',
                      input='b4,b8,Sentinel2_Cloudmask',
                      expression = 'ndvi = if(!isnull(Sentinel2_Cloudmask), null(), float(b8 - b4) / ( b8 + b4 ))',
                      output = 'ndvi',
                      basename = 'ndvi',
                      nprocs = '3',
                      overwrite = True)

    #grass.run_command('t.rast.colors',
         #             color = 'ndvi',
          #            map = 'ndvi')

    # create one average raster of summer 2019
    grass.run_command('t.rast.series',
                      input = 'ndvi',
                      output = 'ndvi_summer2019',
                      method = 'average',
                      where = 'start_time > \'2019-06-21\' and end_time < \'2019-09-22\'',
                      overwrite = True)

    grass.run_command('r.colors',
                      color = 'ndvi',
                      map = 'ndvi_summer2019')

    # create one average raster of autumn 2019
    grass.run_command('t.rast.series',
                      input = 'ndvi',
                      output = 'ndvi_autumn2019',
                      method = 'average',
                      where = 'start_time > \'2019-09-23\' and end_time < \'2019-12-21\'',
                      overwrite = True)

    grass.run_command('r.colors',
                      color = 'ndvi',
                      map = 'ndvi_autumn2019')

    # create one average raster of winter 2019
    grass.run_command('t.rast.series',
                      input = 'ndvi',
                      output = 'ndvi_winter2019',
                      method = 'average',
                      where = 'start_time > \'2019-12-22\' and end_time < \'2020-03-19\'',
                      overwrite = True)

    grass.run_command('r.colors',
                      color = 'ndvi',
                      map = 'ndvi_winter2019')

    # create one average raster of spring 2020
    grass.run_command('t.rast.series',
                      input = 'ndvi',
                      output = 'ndvi_spring2020',
                      method = 'average',
                      where = 'start_time > \'2020-03-20\' and end_time < \'2020-06-19\'',
                      overwrite = True)

    grass.run_command('r.colors',
                      color = 'ndvi',
                      map = 'ndvi_spring2020')

    # example: Change Indice: NDVI Winter - Summer 2019
    grass.run_command('r.mapcalc',
                      expression = 'ChangeIndice_NDVI_Summer_Winter_2019 = abs(ndvi_winter2019 - ndvi_summer2019)',
                      overwrite = True)

    grass.run_command('r.colors',
                      color = 'ndvi',
                      map = 'ChangeIndice_NDVI_Summer_Winter_2019')


if __name__ == "__main__":
    options, flags = grass.parser()

    sys.exit(main())

