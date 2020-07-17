# Download corresponding L1C scenes for existing L2A scenes

import os
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import numpy as np
import zipfile

# path to directory where downloaded L2A scenes are stored
L2Ascenes_dir = sys.argv[1]

# request user credentials for Sentinel Download
user = input('Enter your Copernicus Open Access Hub Username: ')
password = input('Password: ')
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
# path to area of interest defined by user on the command line
aoi = sys.argv[2]
footprint = geojson_to_wkt(read_geojson(aoi)) # define aoi for search of scenes
ro = 65 # set relative orbit number

# list dates of L2A data
dates = os.listdir(L2Ascenes_dir)
print('L1C Scenes for the following date will be searched and downloaded:')
print(dates)

# path to folder where downloaded scenes will be stored defined by user on the command line
out_dir = sys.argv[3]

# iterate over dates and for every date search products, check if there are two available and if they are in
# relative orbit 65, if so download them
for d in dates:
    y = int(d[:4])
    m = int(d[4:6])
    day = int(d[6:8])
    products = api.query(footprint,
                     date = (date(y, m, day), date(y, m, day+1)),
                     producttype = 'S2MSI1C',
                     platformname = 'Sentinel-2')

    print(type(products))
    products_df = api.to_dataframe(products)
    cond1 = len(products_df.index) == 2
    cond2 = np.all(products_df.loc[:, 'relativeorbitnumber'].values == np.asarray([ro, ro]))
    if cond1 and cond2:
        print('There are two scenes of relative Orbit 65 available:')
        print(products_df)
        print('Scenes will be downloaded...')
        api.download_all(products,
                         directory_path= out_dir)
    else:
        print('For date ' + str(d) + ' conditions are not met. Following scenes are available:')
        print(products_df)
        print('Will continue with next date...')
        continue

# extract all downloaded data
l1cs = os.listdir(out_dir)
print(l1cs)
for s in l1cs:
    file = os.path.join(out_dir, s)
    with zipfile.ZipFile(file, 'r') as f:
        f.extractall(path= out_dir)
    print(s + ' was successfully extracted.')
    os.remove(file)