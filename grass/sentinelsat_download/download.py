import matplotlib
from collections import OrderedDict
import numpy
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas as pd


# connect to the API
api = SentinelAPI("roko93", "Rotole11", 'https://scihub.copernicus.eu/dhus')

# tiles
tiles = ["32UPB", "32UQB"]

query_kwargs = {
    'date': ('NOW-12DAYS', 'NOW'),
    'platformname': 'Sentinel-2',
    'producttype': 'S2MSI1C'}

products = OrderedDict()

for tile in tiles:
    kw = query_kwargs.copy()
    kw['tileid'] = tile # products after 2017-03-31
    pp = api.query(**kw)
    df = api.to_dataframe(pp)
    print(df["title"].to_string(index = False))
    products.update(pp)


api.download_all(products, directory_path = "/home/robin/projects/geodata/rasterdata/satellitedata/sentinel2/geo450/jena_roda")

