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
#% description: Implement fmask algorithm for cloud detection in GRASS GIS
#% keyword: raster
#% keyword: fmask
#% keyword: cloud detection
#%end
#%option G_OPT_F_INPUT
#% key: settings
#% label: full path to fmask paramters
#%end
#%option
#% key: sensor
#% type: integer
#% description: Either Landsat8(1) or Sentinel2(2)
#% options: 1,2
#% required: no
#%end
#%option G_OPT_R_OUTPUT
#% key: output
#% description: Name of output image 
#% required: yes
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

    print("im in main")

    try:
        from fmask import fmask as fm
    except ImportError as e:
         gs.fatal(_("Module requires sentinelsat library: {}").format(e))
    try:
        from fmask import config as cfg
    except ImportError as e:
        gs.fatal(_("Module requires pandas library: {}").format(e))
    



    
    return 0

if __name__ == "__main__":
    options, flags = grass.parser()
    main()


