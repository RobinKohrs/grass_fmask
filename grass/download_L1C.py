# Download corresponding L1C scenes for our L2A scenes

import os
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import numpy as np
import zipfile

# list dates for L2A data in our STC
L2Ascenes_dir = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/S2MSI2A_cropped_20m_data'
out_dir = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/L1C_scenes'
dates = os.listdir(L2Ascenes_dir)
print('L1C Scenes for the following date will be searched and downloaded:')
print(dates)
ro = 65
api = SentinelAPI('vroni-g', 'Sigsig-21', 'https://scihub.copernicus.eu/dhus')
aoi = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/jena-roda-testsite.geojson'
footprint = geojson_to_wkt(read_geojson(aoi))

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

# check if this works:
l1cs = os.listdir(out_dir)
print(l1cs)
for s in l1cs:
    file = os.path.join(out_dir, s)
    with zipfile.ZipFile(file, 'r') as f:
        f.extractall(path= out_dir)
    print(s + ' was successfully extracted.')
    os.remove(file)
