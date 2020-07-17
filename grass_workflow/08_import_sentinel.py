#!/usr/bin/env python3
#%module
#% description: Import cropped, merged and resampled S2MSL2A Sentinel-2 channels (B2 - B8, B8A, B11 and B12)
#%end

#%option G_OPT_M_DIR
#% key: input_dir_ras
#% description: Name of directory where sentinel 2 raster files are stored sorted by date
#%end

#%option G_OPT_F_INPUT
#% key: input_aoi_vec
#% description: Name of input vector file of AOI
#%end

#-----------------------------------------------------------------------------------------------------------
# Programm imports all tif files (cropped merged S2MSL2A Sentinel-2 channels (B2 - B8, B8A, B11 and B12))
# from dirpath and testsite (jena_roda_testsite).
#-----------------------------------------------------------------------------------------------------------


# Import modules
import sys
import os
import grass.script as grass


def cleanup():
    pass

def import_tifs(dirpath):
    for dirpath, dirname, filenames in os.walk(dirpath):
        # Iterate through the files in the current dir returned by walk()
        for tif_file in filenames:
            # If the suffix is '.TIF', process
            if tif_file.endswith('.tif'):
                # This will contain the full path to your file
                full_path = os.path.join(dirpath, tif_file)
                # tif_file will already contain the name, so you can call from here
                grass.message('Importing %s -> %s@%s...' % (full_path, tif_file, dirpath))

                # Import all tif files from dirpath
                grass.run_command('r.in.gdal',
                                  flags = 'o',
                                  input = full_path,
                                  output = tif_file,
                                  quiet = True,
                                  overwrite = True)

def import_aoi_vector(aoi_vec):
    # Import testsite map (vector)
    grass.run_command('v.import',
                      input = aoi_vec,
                      overwrite = True)

def main():

    import_tifs(options['input_dir_ras'])
    import_aoi_vector(options['input_aoi_vec'])


if __name__ == '__main__':
    options, flags = grass.parser()

    sys.exit(main())