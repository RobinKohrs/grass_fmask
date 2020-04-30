import os
import glob
from osgeo import gdal

_all = [x for x in os.listdir(".") if x.endswith(".SAFE") and "L1C" in x]

unique_dates = []
for i in _all:
    a =i.split("_")
    b = a[0:3]
    date = "_".join(b)[0:19]
    if date in unique_dates:
        pass
    else:
        unique_dates.append(date)

by_date = {date: None for date in unique_dates}

for key in by_date.keys():
    dates = []
    for f in _all:
        a = f.split("_")
        b = a[0:3]
        date = "_".join(b)[0:19]
        if date == key:
            dates.append(f)
    by_date[key] = dates


bands = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09",
         "B10", "B11", "B12", "B8A"]
mergefiles = {band: None for band in bands}

#### MOSAICING #####
for k,v in by_date.items():
    for key in mergefiles.keys():
        files_to_merge = []
        for safe in v:
            L1C = glob.glob(os.path.join(safe, "GRANULE", "*", "IMG_DATA"))[0]
            bands_one_scene = [x for x in os.listdir(L1C) if x.endswith(".jp2")]
            for band in bands_one_scene:
                if key in band:
                    files_to_merge.append(os.path.join(L1C, band))
        bands_to_string = " ".join(files_to_merge)
        # all same bands for one date in one string
        #print(bands_to_string)
        #print(" ")
        #print(type(bands_to_string))
        command = "gdal_merge.py  -o {} -of gtiff ".format(bands_to_string.split(os.sep)[-1][0:26]+".tif") + bands_to_string 
        print(command)
        print(" ")
        #subprocess.call(command, shell = True)
            


