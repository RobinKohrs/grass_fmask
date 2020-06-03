import matplotlib
from collections import OrderedDict
import numpy
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd
import time


# connect to the API
api = SentinelAPI("roko93", "Rotole11", 'https://scihub.copernicus.eu/dhus')

# tiles
tiles = ["32UPB", "32UQB"]

query_kwargs = {
    'date': ('20190518', date(2020,5,18)),
    'platformname': 'Sentinel-2',
    'producttype': 'S2MSI2A',
    'relativeorbitnumber': '65',
    'cloudcoverpercentage': ('0','10')}

products = OrderedDict()

for tile in tiles:
    kw = query_kwargs.copy()
    kw['tileid'] = tile # products after 2017-03-31
    pp = api.query(**kw)
    df = api.to_dataframe(pp)
    #print(df["title"].to_string(index = False))
    products.update(pp)

print(products)


api.download_all(products, directory_path = "/home/robin/geodata/rasterdata/satellitedata/sentinel2/geo450/jena_roda")

