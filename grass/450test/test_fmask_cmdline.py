import os
import sys
import subprocess


def main():
    subprocess.call("fmask_sentinel2Stacked.py -o out.img -v --safedir /home/robin/450test/S2B_MSIL1C_20200213T101029_N0209_R022_T32TQR_20200213T122453.SAFE", shell = True)

if __name__ == "__main__":
    os.environ["PROJ_LIB"] = "/home/robin/miniconda3/share/proj"
    main()
