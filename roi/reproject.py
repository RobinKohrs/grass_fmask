import geopandas as gpd
import os
import matplotlib.pyplot as plt

f = "jena.geojson"

f_aoi = gpd.read_file(f)
print("CRS")
print(f_aoi.crs)
print(" ")
print("Bounds")
print(f_aoi.total_bounds)
print("reproject data...")
f_wgs84 = f_aoi.to_crs({"init": "epsg:4326"})
print(f_wgs84.crs)

f_wgs84.to_file("jena_wgs84.geojson", driver = "GeoJSON")

fig, ax = plt.subplots(figsize=(12,9))
f_aoi.plot(cmap="Greys", ax = ax)
f_wgs84.plot(cmap="Greys", ax = ax)
plt.show()
