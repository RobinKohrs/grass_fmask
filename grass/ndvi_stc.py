# SCRIPT NOT YET WORKING!!!


#!/usr/bin/env python3

#%module
#% description: Compute NDVI from Space Time Datacubes for cloudfree areas
#%end

#%option G_OPT_STDS_INPUT
#% key: stc_ras
#% description: Name of space time datacube of sentinel bands
#%end

#%option G_OPT_STDS_INPUT
#% key: stc_clouds
#% description: Name of space time datacube of cloudmasks
#%end

# Import modules
import sys
import grass.script as grass


def main():
    # extract all Sentinel-2 channels

    list = [2, 3, 4, 5, 6, 7, 8, 11, 12]
    for i in list:
        if i < 11:
            grass.run_command('t.rast.extract',
                              input=options['stc_ras'],
                              output='b' + str(i),
                              overwrite=True,
                              where='name like \'%B0' + str(i) + '%\'')
        else:
            grass.run_command('t.rast.extract',
                              input=options['stc_ras'],
                              output='b' + str(i),
                              overwrite=True,
                              where='name like \'%B' + str(i) + '%\'')

    grass.run_command('t.rast.extract',
                      input=options['stc_ras'],
                      output='b8A',
                      overwrite=True,
                      where='name like \'%B8A%\'')

    # calculate NDVI, when there are no clouds
    b4_b8_clouds = 'b4,b8,' + options['stc_clouds']
    ndvi = 'ndvi = if(!isnull(' + options['stc_clouds'] + '), null(), float(b8 - b4) / ( b8 + b4 ))'

    grass.run_command('t.rast.mapcalc',
                      input=b4_b8_clouds,
                      expression=ndvi,
                      output='ndvi',
                      basename='ndvi',
                      nprocs='3',
                      overwrite=True)

    grass.run_command('t.rast.colors',
                      color='ndvi',
                      input='ndvi')

    # create one average raster of summer 2019
    grass.run_command('t.rast.series',
                      input='ndvi',
                      output='ndvi_summer2019',
                      method='average',
                      where='start_time > \'2019-06-21\' and end_time < \'2019-09-22\'',
                      overwrite=True)

    grass.run_command('r.colors',
                      color='ndvi',
                      input='ndvi_summer2019')

    # create one average raster of autumn 2019
    grass.run_command('t.rast.series',
                      input='ndvi',
                      output='ndvi_autumn2019',
                      method='average',
                      where='start_time > \'2019-09-23\' and end_time < \'2019-12-21\'',
                      overwrite=True)

    grass.run_command('r.colors',
                      color='ndvi',
                      input='ndvi_autumn2019')

    # create one average raster of winter 2019
    grass.run_command('t.rast.series',
                      input='ndvi',
                      output='ndvi_winter2019',
                      method='average',
                      where='start_time > \'2019-12-22\' and end_time < \'2020-03-19\'',
                      overwrite=True)

    grass.run_command('r.colors',
                      color='ndvi',
                      input='ndvi_winter2019')

    # create one average raster of spring 2020
    grass.run_command('t.rast.series',
                      input='ndvi',
                      output='ndvi_spring2020',
                      method='average',
                      where='start_time > \'2020-03-20\' and end_time < \'2020-06-19\'',
                      overwrite=True)

    grass.run_command('r.colors',
                      color='ndvi',
                      input='ndvi_spring2020')

    # example: Change Indice: NDVI Winter - Summer 2019
    grass.run_command('r.mapcalc',
                      expression='"ChangeIndice_NDVI_Summer_Winter_2019 = abs(ndvi_winter2019 - ndvi_summer2019)"')

    grass.run_command('r.colors',
                      color='ndvi',
                      input='ChangeIndice_NDVI_Summer_Winter_2019')


if __name__ == "__main__":
    options, flags = grass.parser()

    sys.exit(main())
