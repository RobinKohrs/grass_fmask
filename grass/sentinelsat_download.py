# script for download with python package sentinelsat
# Author: Vroni

# import sys
import os
import geopandas as gpd
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt


def shp_to_geojson(shp_path):
    aoi = gpd.read_file(shp_path)
    aoi_WGS84 = aoi.to_crs('EPSG:4326')
    out_geojson = shp_path.replace('shp', 'geojson')
    aoi_WGS84.to_file(out_geojson, driver='GeoJSON')
    return out_geojson

#to do: make dates, max cloudcover and orbit input parameters
def sentinel2_downloader(user, password, bounds, dates, max_cloudcover):
    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    footprint = geojson_to_wkt(read_geojson(bounds))
    ccp = (0, max_cloudcover)
    products = api.query(footprint,
                         date=dates,
                         platformname='Sentinel-2',
                         processinglevel = 'Level-1C',
                         cloudcoverpercentage = ccp) # change this with a argument to define maximum cloud cover
    products_df = api.to_dataframe(products)
    print('These are the available Sentinel 2 Scenes for your query:\n')
    print(products_df)
    #down_all = input('Do you want to download all of the listed products? [y/n] ')
    #if down_all == 'y':
     #   print('Data is saved to current working directory.')
      #  api.download_all(products_df, directory_path=os.getcwd())

# then: - select and maybe sort sentinel scenes and !download them!

if __name__ == '__main__':
    shp_path = input('Define path to shapefile: ')
    #shp_path = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/jena-roda-testsite.shp'
    out_geojson = shp_to_geojson(shp_path)

    user = input('Enter your Copernicus Open Access Hub Username: ')
    #user = 'vroni-g'
    password = input('Password: ')
    #password = ''
    start = input('Enter the start date for your search in format YYYYMMDD: ')
    #start = 20190201
    end = input('Enter the end date for your search in format YYYYMMDD: ')
    #end = 20190227
    dates = (str(start), str(end))
    max_ccp = input('Define the maximum cloud cover percentage: ')
    sentinel2_downloader(user, password, out_geojson, dates, max_ccp)
