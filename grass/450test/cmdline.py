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


#%flag
#% key: v
#% description: print informative messages
#% guisection: flags
#%end

#%flag
#% key: i
#% description: keep intermediate filesT
#% guisection: flags
#%end

#%option G_OPT_M_DIR
#% key: temp_out_dir
#% type: string
#% description: path to directory where to store temporary output
#% required: no
#% guisection: values
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
#% guisection: values
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
#% guisection: values
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
#% guisection: values
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
#% guisection: values
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
#% guisection: values
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
#% guisection: values
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
#% guisection: values
#%end

#%flag
#% key: p
#% description: parallax-test
#% guisection: flags
#%end


#%option G_OPT_BIN_OUTPUT
#% key: output
#% description: Name of output cloud mask
#% required: yes
#% guisection: Output
#%end

import os
import sys
import subprocess
import numpy

import grass.script as grass

def parameters():

    # initialize empty dictionry to store the paramters
    params = dict()

    # cmd-input for verbose output
    if flags['v']:
        params[""] = "-v"


    # cmd input for intermediate files
    if flags["i"]:
        # check if intermediate directory is also provided
        try:
            temp_dir = options["temp_out_dir"]
            params["-k"] = temp_dir
        except NameError as n:
            print("no valid directory provided. Continue without saving temporary files")
    
    # output pixel size
    if flags["j"]:
        params["--pixelsize"] = options["pixelsize"]

    # mincloudsize
    if flags["m"]:
        params["--mincloudsize"] = options["mincloud"]

    # cloudbufferdistance
    if flags["c"]:
        params["--cloudbufferdistance"] = options["cloudbuffer"]


    # shadowbufferdistance
    if flags["s"]:
        params["--shadowbufferdistance"] = options["shadowbuffer"]

    # couldprobtreshold
    if flags["t"]:
        params["--cloudprobthreshold"] = options["prob"]

    # nir reflectanve
    if flags["n"]:
        params["--nirsnowthreshold"] = options["nir"]

    # greensnowthreshold
    if flags["s"]:
        params["--greensnowthreshold"] = options["green"]

    if flags["p"]:
        params["--parallaxtest"] = None

    return params



def main():

    # get parameters from User
    params = parameters()
    print("this is what params returns")
    print(params)
    print(" ")

    # print safe-files
    print(".SAFE-files in the provided location are:")

    if not options["input_dir"].endswith(".SAFE"):
        input_dir = options["input_dir"] + "/"

        safe_files = [f for f in os.listdir(input_dir) if f.endswith(".SAFE") ]
        for i in safe_files:
            print(i)


        for i in safe_files:
            # make output cloudmask
            parts = i.split("_")
            out_file = parts[0] + "_" + parts[2][0:7] + "_" + options["output"] + "_cloudmask" + ".img"

            # parse options from dictionary
            cmd_string = " ".join([i for m,j in params.items() for i in [m, str(j)]])
            cmd = f"fmask_sentinel2Stacked.py -o {out_file} {cmd_string} --safedir {i}"

            print("CMDCALL")
            print(cmd)

            #subprocess.call(cmd, shell=True)
    else:
        safe_file = options["input_dir"]
        parts = safe_file.split("_")
        out_file = parts[0] + "_" + parts[2][0:7] +"_" + options["output"] + ".img"
        print(safe_file)
        print(out_file)
        cmd_string = " ".join([i for m,j in params.items() for i in [m, str(j)]])
        cmd = f"fmask_sentinel2Stacked.py -o {out_file} {cmd_string} --safedir {safe_file}"
        print(cmd)
        #subprocess.call(cmd, shell = True)
    return 0

if __name__ == "__main__":
    
    # add path to miniconda binary to PATH
    import pprint
    env = os.environ
    os.environ["PATH"] += os.pathsep + "/home/robin/miniconda3/bin"
    os.environ["PYTHONPATH"] += os.pathsep + "/home/robin/miniconda3/bin/python"
    pprint.pprint(dict(env), depth = 1) 
    options, flags = grass.parser()
    main()


