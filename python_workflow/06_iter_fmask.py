import os
import sys

from rios import fileinfo
from fmask import fmask
from fmask import config
from fmask.cmdline.sentinel2Stacked import makeStackAndAngles, checkAnglesFile


def main():

    # create directory for cloudmasks
    if _input.endswith(".SAFE/"):
        paths = _input.split(os.sep)
        cloudmaskdir = os.path.join(os.sep, *paths[0:-2], "cloudmasks")
        os.makedirs(cloudmaskdir, exist_ok=True)
        
    elif _input.endswith(".SAFE"):
        paths = _input.split(os.sep)
        cloudmaskdir = os.path.join(os.sep, *paths[0:-1], "cloudmasks")
        os.makedirs(cloudmaskdir, exist_ok=True)
    else:
        cloudmaskdir = os.path.join(_input, "cloudmasks")
        os.makedirs(cloudmaskdir, exist_ok=True)

    # a dictionary containing all the default arguments from the argument parser
    args = {'safedir': None,
            'granuledir': None,
            'toa': None,
            'anglesfile': None,
            'output': None,
            'verbose': True,
            'pixsize': 20,
            'keepintermediates': False,
            'tempdir': '.',
            'mincloudsize': 0,
            'cloudbufferdistance': 150.0,
            'shadowbufferdistance': 300.0,
            'cloudprobthreshold': 100 * config.FmaskConfig.Eqn17CloudProbThresh,
            'nirsnowthreshold': config.FmaskConfig.Eqn20NirSnowThresh,
            'greensnowthreshold': config.FmaskConfig.Eqn20GreenSnowThresh,
            'parallaxtest': False}                                       
    
    
    # a helper class so that the arguments can be called with args.argument instead of args['argument']
    class Cmdargs(object):
        def __init__(self, args):
            for key, value in args.items():
                setattr(self, key, value)
    
    for i in safe_dir:
        cmdargs = Cmdargs(args)
        if not i.endswith(os.sep):
            safe = i.split(os.sep)[-1]
        else:
            safe = i.split(os.sep)[-2]
        names = safe.split("_")
        out_name = "cloudmask_" + names[0] + "_" + names[2] + "_" + names[5] + "_.img"
        print(os.path.join(cloudmaskdir, out_name))
        cmdargs.output = os.path.join(cloudmaskdir, out_name)
        cmdargs.safedir = i
        

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
    _input = sys.argv[1] # .SAFE directory or directory with several L1C .SAFE directories
    if _input.endswith(".SAFE/") or _input.endswith(".SAFE"):
        safe_dir_file = _input
        safe_dir = []
        safe_dir.append(safe_dir_file)
        print("You provided one file:")
        print(safe_dir)
    else:
        if not _input.endswith(".SAFE/"):
            if os.path.isdir(_input):
                print("provided directory input")
            else:
                print("directory '{}' does not exists".format(_input))
                sys.exit(1)
        if len([x for x in os.listdir(_input) if x.endswith(".SAFE")]) < 1:
            print("in the provided path are no .safe directories")
            sys.exit(1)
        else:
            safe_dir = [_input + x for x in os.listdir(_input) if x.endswith(".SAFE")]
            print("for the following directories a cloudmask will be computed")
            for i in safe_dir:
                print(i)
    main()
