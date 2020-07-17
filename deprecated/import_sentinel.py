#!/usr/bin/env python3
#-----------------------------------------------------------------------------------------------------------
# sentinel_import.py
#-----------------------------------------------------------------------------------------------------------
# Programm imports all tif files (uncropped merged S2MSL2A Sentinel-2 channels (B2 - B8, B8A, B11 and B12))
# from dirpath and testsite (jena_roda_testsite).
# You have to set your own dirpath to tif files and rename testsite.
#-----------------------------------------------------------------------------------------------------------

# Import modules
import sys
import os
from subprocess import PIPE
from grass.script import parser, parse_key_val
import grass.script as grass


def cleanup():
    pass

# Set your own dirpath
os.chdir("C:\Sentinel")


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

    # Import testsite map (vector)
    # You have to rename "jena-roda-testsite" into "jena_roda_testsite"
    grass.run_command('v.import',
                      input = "C:\Sentinel\Site\jena_roda_testsite.shp",
                      layer = "jena_roda_testsite",
                      output = "jena_roda_testsite",
                      overwrite = True)

def main():
    if len(sys.argv) == 1:
            import_tifs(os.getcwd())
    else:
        import_tifs(sys.argv[1])


if __name__ == "__main__":
    main()
