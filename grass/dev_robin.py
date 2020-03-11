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
#% key: input
#% description: path to directory (.save), where sentinel scenes are stored
#% required: yes
#%end

#%option
#% key: sensor
#% type: integer
#% description: Either Landsat8(1) or Sentinel2(2)
#% options: 1,2
#% required: yes
#%end

#%option
#% key: cloudbuffer
#% type: integer
#% description: size of buffer in cloudlayer (in number of pixels)
#% required: no
#% answer: 5
#%end

#%option
#% key: cloudbuffer
#% type: integer
#% description: size of buffer in shadowlayer (in number of pixels)
#% required: no
#% answer: 10
#%end

#%flag
#% key: v
#% description: print informative messages
#%end

#%option G_OPT_R_OUTPUT
#% key: output_cl
#% description: Name of output cloud mask
#% required: yes
#% guisection: Output
#%end

#%option G_OPT_R_OUTPUT
#% key: output_sh
#% description: Name of output shadow mask
#% required: yes
#% guisection: Output
#%end





import os

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
    conf.setThermalInfo = terminfo

    




def filesnames():

    fnames = cfg.FmaskFilenames()



def main():

    img  = options['input']   # name of input image
    img_out = options['output_cl']  # name of output image 

    try:
        from fmask import fmask as fm
    except ImportError as e:
        gs.message(_("you need to install the python fmask library first..."))
        gs.fatal(_("Module requires fmask library: {}").format(e))
    
    
    return 0

if __name__ == "__main__":
    options, flags = grass.parser()
    main()


