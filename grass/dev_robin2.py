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
#% description: keep intermediate files
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
#% key: output_cl
#% description: Name of output cloud mask
#% required: yes
#% guisection: Output
#%end





import os
import subprocess

import grass.script as grass
from fmask import fmask as fm
from fmask import config as cfg



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



def config(sensor, refband, terminfo):
    pass



def filesnames():
    fnames = cfg.FmaskFilenames()



def main():

    try:
        from fmask import fmask as fm
    except ImportError as e:
        gs.message(_("you need to install the python fmask library first..."))
        gs.fatal(_("Module requires fmask library: {}").format(e))

    # the path to the input safedit
    safedir = options["input_dir"]

    # the path to output-rasterfile
    img_out = options["output_cl"]

    params = parameters()
    print("this is what params returns", "\n", params)
    
    cmd_string = " ".join([i for m,j in params.items() for i in [m, str(j)]])
    print("this is the concatenated list", cmd_string)
    
    cmd = f"fmask_sentinel2Stacked.py -o {img_out} {cmd_string} --safedir {safedir}"
    print(cmd)
    subprocess.call(cmd, shell=True)
    
    return 0

if __name__ == "__main__":
    options, flags = grass.parser()
    main()


