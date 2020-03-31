import os

from rios import fileinfo
from fmask import fmask
from fmask import config
from fmask.cmdline.sentinel2Stacked import makeStackAndAngles, checkAnglesFile


def main():
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

    return args                                          
    
    
    # modification of the argument dictionary with custom values
    args['output'] = 'cloud.img'
    args['safedir'] = '/home/robin/uni/semester2/geo450/data/sentinel_test/s2_data/roma/S2A_MSIL1C_20200329T101021_N0209_R022_T33TTG_20200329T111343.SAFE'
    
    
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
    main()