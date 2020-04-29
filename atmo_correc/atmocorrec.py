import os
import argparse
import sys
import subprocess

def main():
    # excute the sen2cor algorithm
    if _input.endswith(".SAFE") or _input.endswith(".SAFE/"):
        cmd = "L2A_Process --resolution 20 {}".format(single_file)
        subprocess.call(cmd, shell = True)
    else:
        print("Process multiple files")
        for safe in safe_dirs:
            print(safe)
            if not safe.endswith("/"):
                safe = safe + "/"
            safe = os.path.join(_input, safe)
            cmd ="L2A_Process --resolution 20 {}".format(safe)
            subprocess.call(cmd, shell = True)


if __name__ == "__main__":
    _input = sys.argv[1]
    if _input.endswith(".SAFE/") or _input.endswith(".SAFE"):
        single_file = _input
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
            safe_dirs = [x for x in os.listdir(_input) if x.endswith(".SAFE")]
            print("the following .SAFE-direcotries will be corrected")
            for i in safe_dirs:
                print(i)
    main()
