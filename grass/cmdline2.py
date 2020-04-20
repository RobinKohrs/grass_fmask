#!/usr/bin/env python3
#
##############################################################################
#
# MODULE:       r.fmask
#
# AUTHOR(S):    Veronica Grupp
#               Florian 
#               Robin Kohrs
#
# PURPOSE:      Implement fmask algorithm for cloud detection in GRASS GIS
#
# DATE:         Sat Mar  7 
#
##############################################################################

#%module
#% description: fmask-algorithm for cloud detection in GRASS GIS
#% keyword: raster
#% keyword: fmask
#% keyword: cloud detection
#%end

#%option G_OPT_M_DIR
#% key: input_dir
#% type: string
#% description: path to directory (.save), where sentinel scenes are stored
#% required: yes
#%end

#%option
#% key: output_name
#% type: string
#% description: Name of output image(s) 
#% required: yes
#%end

#%option G_OPT_M_DIR
#% key: output_dir
#% description: Location of output cloud mask
#% required: yes
#%end


#%options
#% key: conda
#% type: string
#% description: choose if you use anaconda(a) or miniconda(m)
#% required: yes
#%end


#%flag
#% key: p
#% description: print informative overwiev
#% guisection: print
#%end

#%flag
#% key: i
#% description: keep intermediate files
#% guisection: flags
#%end

#%option G_OPT_M_DIR
#% key: temp_out_dir
#% type: string
#% description: path to directory where to store temporary output
#% required: no
#% guisection: parameters
#%end

#%flag
#% key: j
#% description: output pixel size in metres
#% guisection: flags
#%end

#%option
#% key: pixelsize
#% type: integer
#% description: output pixel size in metres
#% answer: 20
#% guisection: parameters
#%end

#%flag
#% key: m
#% description: mincloudsize in pixels
#% guisection: flags
#%end

#%option
#% key: mincloud
#% type: integer
#% description: mincloudsize in pixels
#% answer: 0
#% guisection: parameters
#%end

#%flag
#% key: c
#% description: cloudbufferdistance in metres 
#% guisection: flags
#%end

#%option
#% key: cloudbuffer
#% type: integer
#% description: cloudbufferdistance in metres 
#% answer: 150
#% guisection: parameters
#%end

#%flag
#% key: s
#% description: shadow buffer distance in metres
#% guisection: flags
#%end

#%option
#% key: shadowbuffer
#% type: integer
#% description: shadow buffer distance in metres
#% answer: 300
#% guisection: parameters
#%end


#%flag
#% key: t
#% description: cloud probability threshold
#% guisection: flags
#%end

#%option
#% key: prob
#% type: integer
#% description: cloud probability threshold (*1/100)
#% answer: 20
#% guisection: parameters
#%end

#%flag
#% key: n
#% description: threshold for nir reflectance 
#% guisection: flags
#%end

#%option
#% key: nir
#% type: integer
#% description: threshold for nir reflectance (*1/100)
#% answer: 11 
#% guisection: parameters
#%end

#%flag
#% key: g
#% description: threshold for green-band reflectance 
#% guisection: flags
#%end

#%option
#% key: green
#% type: integer
#% description: threshold for green-band reflectance (*1/100)
#% answer: 10
#% guisection: parameters
#%end

#%flag
#% key: t
#% description: parallax-test
#% guisection: flags
#%end


import os
import glob
import sys
import subprocess
import numpy
import time

import grass.script as grass


class FmaskSentinel():

    def __init__(self, input_dir, output_dir, output_name):

        # check if input directory exists
        self.input_dir = input_dir
        if not os.path.exists(input_dir):
            gs.fatal(_('Input directory <{}> does not exist').format(input_dir))

        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            gs.fatal(_('Directory <{}> does not exist').format(output_dir))

        self.output_name = output_name


    def parameters(self):
        args = dict()

        if flags["i"]:
            # check if intermediate directory is also provided
            try:
                temp_dir = options["temp_out_dir"]
                args["-k"] = temp_dir
            except NameError as n:
                print("no valid directory provided. Continue without saving temporary files")
        
        # output pixel size
        if flags["j"]:
            args["--pixelsize"] = options["pixelsize"]

        # mincloudsize
        if flags["m"]:
            args["--mincloudsize"] = options["mincloud"]

        # cloudbufferdistance
        if flags["c"]:
            args["--cloudbufferdistance"] = options["cloudbuffer"]


        # shadowbufferdistance
        if flags["s"]:
            args["--shadowbufferdistance"] = options["shadowbuffer"]

        # couldprobtreshold
        if flags["t"]:
            args["--cloudprobthreshold"] = options["prob"]

        # nir reflectanve
        if flags["n"]:
            args["--nirsnowthreshold"] = options["nir"]

        # greensnowthreshold
        if flags["s"]:
            args["--greensnowthreshold"] = options["green"]

        if flags["p"]:
            args["--parallaxtest"] = None

        self._args = args

    def findconda(self):

        if  options["conda"] == "m":
            conda = "miniconda?"
            miniconda_path = glob.glob(os.path.expanduser("~") + os.sep + conda)[0]

            # get miniconda binary and add it to path
            conda_bin = os.path.join(miniconda_path, "bin" + os.sep) 
            os.environ["PATH"] = conda_bin + os.pathsep + os.getenv("PATH")
            print("your current PATH-Variable looks like:")
            print("Either the '/bin' of miniconda or anaconda should be at the beginning")
            print(os.environ["PATH"])

            # set proj
            proj = os.path.join(miniconda_path, "share", "proj")
            os.environ["PROJ_LIB"] = proj
            print(" ")
            print("your current path to the 'proj'-library looks like:")
            print(os.getenv("PROJ_LIB"))
        elif options["conda"] == "a":
            conda = "anaconda?"

        else:
            print("either use miniconda or anaconda")

    def printproducts(self):

        if not self.input_dir.endswith(".SAFE"):
            # print safe-files
            print(".SAFE-file(s) in the provided location are:")
            # get all .safe-files in a list
            safe_files = [f for f in os.listdir(self.input_dir) if f.endswith(".SAFE") ]
            for i in safe_files:
                print(i)
            print(" ")

            # print the cmd-call for each
            for counter, i in enumerate(safe_files):

                # make output cloudmask
                output_dir = self.output_dir
                if self.output_name.endswith(".img"):
                    outfile = self.output_name
                else:
                    outfile = self.output_name + ".img"

                # get the date of the product
                parts = i.split("_")
                out_file = parts[0] + "_" + parts[2][0:7] + "_" + outfile
                out_file = output_dir + out_file

                # make input absolut path
                i_abs = self.input_dir + i

                # parse options from dictionary
                cmd_string = " ".join([i for m,j in self._args.items() for i in [m, str(j)]])
                cmd = f"fmask_sentinel2Stacked.py -o {out_file} {cmd_string} --safedir {i_abs}"

                print("CMDCALL", counter +1)
                print(cmd)

        # if single file
        else:
            safe_file = options["input_dir"]
            parts = safe_file.split("_")
            out_file = parts[0] + "_" + parts[2][0:7] + options["output"] + ".img"
            print(safe_file)
            print(out_file)
            cmd_string = " ".join([i for m,j in args.items() for i in [m, str(j)]])
            cmd = f"fmask_sentinel2Stacked.py -o {out_file} {cmd_string} --safedir {safe_file}"
            print(cmd)

    # make cloudmasks
    #def cloudmask(self):
        
        # if not options["input_dir"].endswith(".SAFE"):
        #     # get all the .safe files in the input_dir
        #     safe_files = [f for f in os.listdir(self.input_dir) if f.endswith(".SAFE") ]
            
        #     # run fmask on every .safe directory
        #     for counter, i in enumerate(safe_files):

        #         # make output cloudmask
        #         output_dir = self.output_dir + os.sep
        #         if self.output_name.endswith(".img"):
        #             outfile = self.output_name
        #         else:
        #             outfile = self.output_name + ".img"
        #         parts = i.split("_")
        #         out_file = parts[0] + "_" + parts[2][0:7] + "_" + outfile
        #         out_file = output_dir + out_file

        #         # make input absolut path
        #         i_abs = self.input_dir + i
        #         print("ABSOLUTEPATH")
        #         print(i_abs)

        #         # parse options from dictionary
        #         cmd_string = " ".join([i for m,j in self._args.items() for i in [m, str(j)]])
        #         cmd = f"fmask_sentinel2Stacked.py -o {out_file} {cmd_string} --safedir {i_abs}"

        #         print("CMDCALL", counter +1)
        #         print(cmd)

        #         #subprocess.call(cmd, shell=True)

        # # single cloudsmask        
        # else:
        #     safe_file = self.input_dir
        #     parts = safe_file.split("_")
        #     out_file = parts[0] + "_" + parts[2][0:7] + self.output_name + ".img"
        #     print(safe_file)
        #     print(out_file)
        #     cmd_string = " ".join([i for m,j in params.items() for i in [m, str(j)]])
        #     cmd = f"fmask_sentinel2Stacked.py -o {out_file} {cmd_string} --safedir {safe_file}"
        #     print(cmd)
        #     #subprocess.call(cmd, shell = True)


def main():
    fmask = FmaskSentinel(options["input_dir"], options["output_dir"], options["output_name"])
    fmask.parameters()
    fmask.findconda()
    if flags["p"]:
        fmask.printproducts()
        return 0
    else:
        fmask.cloudmask()


if __name__ == "__main__":
    options, flags = grass.parser()
    sys.exit(main())


