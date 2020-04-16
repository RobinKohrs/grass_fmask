#!/usr/bin/env python3


import os
import sys
import subprocess
import numpy

import grass.script as grass

def main():
    pass



if __name__ == "__main__":
    
    # add path to miniconda binary to PATH
    import pprint
    env = os.environ
    os.environ["PATH"] = "/home/robin/450test/link" + os.pathsep + os.getenv("PATH")
    #os.environ["PYTHONPATH"] += os.pathsep + "/home/robin/miniconda3/envs/fmask/lib/python3.8/site-packages"
    pprint.pprint(dict(env), depth = 1)

    import sys
    for i in sys.path:
        print(i) 
    
    import fmask

    
    options, flags = grass.parser()
    main()






