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
#% key: pr
#% description: print informative messages
#% guisection: flags
#%end


#%flag
#% key: m
#% description: mincloudsize in pixels
#% answer: 0
#% guisection: flags
#%end

#%flag
#% key: c
#% description: cloudbufferdistance in metres 
#% answer: 150
#% guisection: flags
#%end

#%flag
#% key: s
#% description: shadow buffer distance in metres
#% answer: 300
#% guisection: flags
#%end

#%flag
#% key: t
#% description: cloud probability threshold
#% answer: 0.2
#% guisection: flags
#%end


#%flag
#% key: n
#% description: threshold for nir reflectance (0-1)
#% answer: 0.11
#% guisection: flags
#%end


#%flag
#% key: g
#% description: threshold for green-band reflectance (0-1)
#% answer: 0.1
#% guisection: flags
#%end

#%flag
#% key: p
#% description: parallax-test
#% answer: no
#% guisection: flags
#%end

#%option
#% key: cloudbuffer
#% type: integer
#% description: size of buffer in shadowlayer (in number of pixels)
#% required: no
#% answer: 10
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

               

def config(sensor, refband, terminfo):

    """[create a function that creates an instance of a class FmaskConfig]
    
    Arguments:
        sensor {integer} -- [either 1 or 2 for Landsat8 or Sentinel]
    """ 
    # create instance of that class
    conf = cfg.FmaskConfig(sensor)

    # set all the attributes
    conf.setReflectiveBand = refband
    self.toa_file = os.path.join(self.tmp_dir, "toa.tif")

    




def filesnames():

    fnames = cfg.FmaskFilenames()



def main():

    img  = options['input_dir']   # name of input directory
    print("This is the input-dir:", img)
    img_out = options['output_cl']  # name of output image 
    print("This is the output-file:", img_out)

    try:
        from fmask import fmask as fm
    except ImportError as e:
        gs.message(_("you need to install the python fmask library first..."))
        gs.fatal(_("Module requires fmask library: {}").format(e))
    
    cmd = f"fmask_sentinel2Stacked.py -o {img_out} --safedir {img}"
    print(cmd)
    subprocess.call(cmd, shell=True)
    
    return 0

if __name__ == "__main__":
    options, flags = grass.parser()
    main()


