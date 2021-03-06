# merge the two scenes for each date into one raster file for each band
import os
import sys
import subprocess
import glob
import shutil


def merge(d):
    _all = [x for x in os.listdir(d) if x.endswith(".SAFE") and "L2A" in x]

    unique_dates = []
    # get unique dates from .safe-filenames
    for i in _all:
        a =i.split("_")
        b = a[0:3]
        date = "_".join(b)[0:19]
        if date in unique_dates:
            pass
        else:
            unique_dates.append(date)

    # make a dictionary with those dates as keys
    by_date = {date: None for date in unique_dates}

    for key in by_date.keys():
        dates = []
        for f in _all:
            a = f.split("_")
            b = a[0:3]
            date = "_".join(b)[0:19]
            if date == key:
                dates.append(f)
            else:
                by_date[key] = dates

    bands = ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B11", "B12", "B8A"]


    #  make a dictionary with the bands as keys and the files to merge as values in a lis
    mergefiles = {band: None for band in bands}

    # set working directory (not good)
    os.chdir(d)


    #### MOSAICING #####
    for k,v in by_date.items():
        print(k,v)
        for key in mergefiles.keys():
            files_to_merge = []
            for safe in v:
                L2A = glob.glob(os.path.join(safe, "GRANULE", "*", "IMG_DATA", "R20m"))[0]
                bands_one_scene = [x for x in os.listdir(L2A) if x.endswith(".jp2")]
                for band in bands_one_scene:
                    if key in band:
                        files_to_merge.append(os.path.join(L2A, band))

            if len(files_to_merge) > 1:
                bands_to_string = " ".join(files_to_merge)
                command = "gdal_merge.py  -o {} -of gtiff ".format(bands_to_string.split(os.sep)[-1][7:26]+".tif") + bands_to_string
                subprocess.call(command, shell = True)
            else:
                pass

    # move data into directories with dates
    tiffs = [tif for tif in os.listdir(".") if tif.endswith(".tif")]

    for i in tiffs:
        print(i)
        date = i[0:8]
        path = os.getcwd()
        path_final = os.path.join(path, date)
        os.makedirs(path_final, exist_ok = True)
        shutil.move(i,path_final)

def main(d):
    merge(d)

if __name__ == "__main__": 
    d = sys.argv[1]
    main(d)