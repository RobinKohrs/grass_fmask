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
#% key: temp_dir
#% type: string
#% description: path to directory where to store temporary output
#% required: no
#% guisection: flags
#%end

#%option
#% key: pixsize
#% type: integer
#% description: output pixel size in metres
#% answer: 20
#%end

#%option
#% key: mincloud
#% type: integer
#% description: mincloudsize in pixels
#% answer: 0
#%end

#%option
#% key: cloudbuffer
#% type: integer
#% description: cloudbufferdistance in metres 
#% answer: 150
#%end

#%option
#% key: shadowbuffer
#% type: integer
#% description: shadow buffer distance in metres
#% answer: 300
#%end

#%option
#% key: prob
#% type: integer
#% description: cloud probability threshold (*1/100)
#% answer: 20
#%end

#%option
#% key: nir
#% type: integer
#% description: threshold for nir reflectance (*1/100)
#% answer: 11 
#%end

#%option
#% key: green
#% type: integer
#% description: threshold for green-band reflectance (*1/100)
#% answer: 10
#%end

#%flag
#% key: p
#% description: parallax-test
#% guisection: flags
#%end


#%option G_OPT_BIN_OUTPUT
#% key: outfile
#% description: Name of output cloud mask
#% required: yes
#%end


import os
import sys
import pprint

print("os.environ")
os.environ["GRASS_PYTHON"] = "/home/robin/miniconda3/envs/fmask/bin/python"
os.environ["PYTHONPATH"] = "/home/robin/miniconda3/envs/fmask/lib/python3.8/site-packages"
env = os.environ
pprint.pprint(dict(env), width = 1)

print("SYS PATH")
for i in sys.path:
    print(i)

print("SYS EXECUTABLE")
print(sys.executable)


import grass.script as grass
from rios import fileinfo
from fmask import fmask
from fmask import config
from fmask.cmdline.sentinel2Stacked import makeStackAndAngles, checkAnglesFile



def main():

    safedir = options["input_dir"]
    outfile = options["outfile"]

    if flags["v"]:
        verbose = True
    else:
        verbose = False

    if flags["i"]:
        keep = True
    else:
        keep = False
    
    if flags["p"]:
        parallax = True
    else:
        parallax = False

    temp = options["temp_dir"]    
    pixsize = options["pixsize"]
    mincloud = options["mincloud"]
    cloudbuffer = options["cloudbuffer"]
    shadowbuffer = options["shadowbuffer"]
    prob = options["prob"]
    nir = options["nir"]
    green = options["green"]

    # a dictionary containing all the default arguments from the argument parser
    args = {'safedir': safedir,
            'granuledir': None,
            'toa': None,
            'anglesfile': None,
            'output': outfile,
            'verbose': verbose,
            'pixsize': pixsize,
            'keepintermediates': keep,
            'tempdir': 'tempdir',
            'mincloudsize': mincloud,
            'cloudbufferdistance': cloudbuffer,
            'shadowbufferdistance': shadowbuffer,
            'cloudprobthreshold': 100 * prob,
            'nirsnowthreshold': 100 / nir,
            'greensnowthreshold': 100 / green,
            'parallaxtest': parallax}
 
    
    # a helper class so that the arguments can be called with args.argument instead of args['argument']
    class Cmdargs(object):
        def __init__(self, args):
            for key, value in args.items():
                setattr(self, key, value)
    
    cmdargs = Cmdargs(args)
    
    tempStack = False
    if cmdargs.safedir is not None or cmdargs.granuledir is not None:
        tempStack = True
        resampledBands = makeStackAndAngles(cmdargs)
    
    anglesfile = checkAnglesFile(cmdargs.anglesfile, cmdargs.toa)
    anglesInfo = config.AnglesFileInfo(anglesfile, 3, anglesfile, 2, anglesfile, 1, anglesfile, 0)
    
    fmaskFilenames = config.FmaskFilenames()
    fmaskFilenames.setTOAReflectanceFile(cmdargs.toa)
    fmaskFilenames.setOutputCloudMaskFile(cmdargs.output)
    
    fmaskConfig = config.FmaskConfig(config.FMASK_SENTINEL2)
    fmaskConfig.setAnglesInfo(anglesInfo)
    fmaskConfig.setKeepIntermediates(cmdargs.keepintermediates)
    fmaskConfig.setVerbose(cmdargs.verbose)
    fmaskConfig.setTempDir(cmdargs.tempdir)
    fmaskConfig.setTOARefScaling(10000.0)
    fmaskConfig.setMinCloudSize(cmdargs.mincloudsize)
    fmaskConfig.setEqn17CloudProbThresh(cmdargs.cloudprobthreshold / 100)  # Note conversion from percentage
    fmaskConfig.setEqn20NirSnowThresh(cmdargs.nirsnowthreshold)
    fmaskConfig.setEqn20GreenSnowThresh(cmdargs.greensnowthreshold)
    fmaskConfig.setSen2displacementTest(cmdargs.parallaxtest)
    
    # Work out a suitable buffer size, in pixels, dependent on the resolution of the input TOA image
    toaImgInfo = fileinfo.ImageInfo(cmdargs.toa)
    fmaskConfig.setCloudBufferSize(int(cmdargs.cloudbufferdistance / toaImgInfo.xRes))
    fmaskConfig.setShadowBufferSize(int(cmdargs.shadowbufferdistance / toaImgInfo.xRes))
    
    fmask.doFmask(fmaskFilenames, fmaskConfig)
    
    if anglesfile != cmdargs.anglesfile:
        # Must have been a temporary, so remove it
        os.remove(anglesfile)
    
    if tempStack and not cmdargs.keepintermediates:
        for fn in [cmdargs.toa, cmdargs.anglesfile]:
            if os.path.exists(fn):
                os.remove(fn)


if __name__ == '__main__':
    options, flags = grass.parser()
    main()
