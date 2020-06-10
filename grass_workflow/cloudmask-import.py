#!/usr/bin/env python3

#%module
#% description: Import merged cloudmasks created with fmask
#%end

#%option G_OPT_M_DIR
#% description: Name of directory where merged cloud masks as geopackage files are stored
#%end

#-----------------------------------------------------------------------------------------------------------
# cloudmask_import.py
#-----------------------------------------------------------------------------------------------------------
# Programm imports all gpkg files (cloudmask) from dirpath.
#-----------------------------------------------------------------------------------------------------------

# Import modules
import sys
import os
import grass.script as grass


def cleanup():
    pass


def import_gpkg(dirpath):
    for dirpath, dirname, filenames in os.walk(dirpath):
        # Iterate through the files in the current dir returned by walk()
        for gpkg_file in filenames:
            # If the suffix is '.GPKG', process
            if gpkg_file.endswith('.gpkg'):
                # This will contain the full path to your file
                full_path = os.path.join(dirpath, gpkg_file)
                # gpkg_file will already contain the name, so you can call from here
                grass.message('Importing %s -> %s@%s...' % (full_path, gpkg_file, dirpath))

                # Import all gpkg files from dirpath
                grass.run_command('v.import',
                                  input = full_path,
                                  output = gpkg_file[:38],
                                  quiet = True,
                                  overwrite = True)

def main():

    import_gpkg(options['input'])


if __name__ == '__main__':
    options, flags = grass.parser()

    sys.exit(main())