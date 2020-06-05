#!/usr/bin/env python3
#-----------------------------------------------------------------------------------------------------------
# cloudmask_import.py
#-----------------------------------------------------------------------------------------------------------
# Programm imports all gpkg files (cloudmask) from dirpath.
# You have to set your own dirpath to gpkg files.
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
os.chdir("C:\Cloudmask")


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
    if len(sys.argv) == 1:
            import_gpkg(os.getcwd())
    else:
        import_gpkg(sys.argv[1])


if __name__ == "__main__":
    main()
