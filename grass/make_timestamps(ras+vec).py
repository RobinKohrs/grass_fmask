#!/usr/bin/env python3

#%module
#% description: Retrieve timestamps from Sentinel bands and cloudmasks from current mapset.
#%end
#%option G_OPT_F_OUTPUT
#% description: Name of output timestamps file for raster data (sentinel bands)
#%end
#%option G_OPT_F_OUTPUT
#% description: Name of output timestamps file for vector data (cloudmasks)
#%end

# PyGrass Skript to retrieve timestamps for satellite data (raster) and cloudmasks (vector), save them to a textfile
# files will be used to space-time-datacube creation

import sys
import os
from datetime import datetime, timedelta

import grass.script as gs

from grass.pygrass.gis import Mapset



import os

# get directories with raster and vector (cloudmasks) data
raster_dir = sys.argv[1]
vector_dir = sys.argv[2]


# raster time stamps
scene_dirs = [os.path.join(raster_dir, x) for x in os.listdir(raster_dir) if len(x) == 10 and os.path.isdir(x)]

# select band 2 in each directory
band2 = open("band2.txt","w+")
for i in realpaths:
    files = [x for x in os.listdir(i)]
    for band in files:
        if "B02" in band:
            date = band.split("_")[1]
            year = date[0:4]
            month = date[4:6]
            day = date[6:8]
            band2.write(band[0:-4] + "@" + mapset + "|" + year + "-" + month + "-" + day+ "\n")