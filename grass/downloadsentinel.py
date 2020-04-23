import matplotlib
import numpy
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

# connect to the API
api = SentinelAPI("roko93", "Rotole11", 'https://scihub.copernicus.eu/dhus')

# dowload_scenes by date and polygon
footprint = geojson_to_wkt(read_geojson("./../geodata/jena_roda.json"))
print(type(footprint))
