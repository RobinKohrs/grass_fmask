# script to try download with python package sentinelsat
# 22.04.20 Vroni

# import sys
import geopandas as gpd
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt


def shp_to_geojson(shp_path):
    aoi = gpd.read_file(shp_path)
    aoi_WGS84 = aoi.to_crs('EPSG:4326')
    out_geojson = shp_path.replace('shp', 'geojson')
    aoi_WGS84.to_file(out_geojson, driver='GeoJSON')
    return out_geojson

def sentinel2_downloader(user, password, bounds):
    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    footprint = geojson_to_wkt(read_geojson(bounds))
    products = api.query(footprint,
                         date=('20190201', '20190227'),
                         platformname='Sentinel-2',
                         processinglevel = 'Level-1C',
                         cloudcoverpercentage = (0, 20)) # change this with a argument to define maximum cloud cover
    products_df = api.to_dataframe(products)
    print('These are the available Sentinel 2 Scenes for your query:\n')
    print(products_df)



if __name__ == '__main__':
    shp_path = input('Define path to shapefile: ')
    out_geojson = shp_to_geojson(shp_path)
    user = input('Please type your Copernicus Open Access Hub Username: ')
    password = input('Password: ')
    sentinel2_downloader(user, password, out_geojson)
