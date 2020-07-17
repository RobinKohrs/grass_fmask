import sys
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd

# path to area of interest defined by user on the command line
aoi = sys.argv[1]

# request user credentials for Sentinel Download
user = input('Enter your Copernicus Open Access Hub Username: ')
password = input('Password: ')

# connect to the API
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

# request overview of scenes filtered by date, region, cloud cover etc.
footprint = geojson_to_wkt(read_geojson(aoi))
products = api.query(footprint,
                     date = (date(2019,8,18), date(2020,5,18)), # time span for search (only last year to avoid long term archive)
                     producttype = 'S2MSI2A', # define processing level
                     platformname = 'Sentinel-2',
                     relativeorbitnumber = 65, # orbit number for our aoi
                     cloudcoverpercentage=(0, 10)) # up to 10 % cloud cover allowed

# convert result to Pandas Dataframe
products_df = api.to_dataframe(products)

# create dataframe only for overview
df_overview = products_df[["title"]]
df_string = df_overview.to_string(index = False).split()[1:]
df_new = pd.DataFrame(df_string, columns = ["Product"])

# make dates column
dates = df_new["Product"].str[11:19]
dt_series = pd.to_datetime(dates)
df_new["dates"] = dt_series
df_new.sort_values(by = ["dates"], inplace = True)

# make tiles column
tiles = df_new["Product"].str[39:44]
df_new["tile"] = tiles
print(df_new)

# request confirmation for download of filtered scenes
proceed = input('Do you want to proceed with the download of the selected scenes? [y/n] ')

if proceed == 'y':
    # path to folder where downloaded scenes will be stored defined by user on the command line
    download_folder = sys.argv[2]
    # actual download of filtered scenes
    api.download_all(products, directory_path = download_folder)
else:
    sys.exit()

