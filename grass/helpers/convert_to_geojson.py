import sys
import geopandas as gpd


def convert():
    # convert shape to geojson 
    f = gpd.read_file(shape)
    f.to_file(out_file, driver = "GeoJSON")
    
if __name__ == "__main__":
    shape = input("path to .shp file: ") 
    out_file = input("specify the full path + '.geoson': ")
    print(shape, out_file)
    convert()

