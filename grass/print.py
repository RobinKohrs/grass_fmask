import matplotlib
import numpy
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd


# connect to the API
api = SentinelAPI("roko93", "Rotole11", 'https://scihub.copernicus.eu/dhus')

# dowload_scenes by date and polygon
footprint = geojson_to_wkt(read_geojson("../roi/jena_wgs84.geojson"))
products = api.query(footprint,
                     date = (date(2018,4,1), date(2020,4,10)),
                     producttype = 'S2MSI1C',
                     platformname = 'Sentinel-2',
                     cloudcoverpercentage=(0, 30))

# convert to Pandas Dataframe
products_df = api.to_dataframe(products)

# print all the column names
#for col in products_df:
#    print(col)

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

print(df_new.head(), df_new.tail())
print(" ")
print("Unique Tiles intersecting the area are: ")
print(df_new.tile.unique())
print(" ")
print("all in all there are {} scenes to download".format(len(df_new.index)))

# only print the index in pandas
#print(df_overview.index)
