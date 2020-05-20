# script to convert fmask results to binary raster and then to vector, merge two scenes, either as raster or vector

# load raster with same date
# list all files that end with '.img'
# detect the same ones, load them
# put vector data and tifs in separate folders

import rasterio.features
import rasterio.mask
import numpy as np
import os
import geojson as gj

clr1 = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/cloudmask_S2A_20200322_T32UPB_.img'
clr2 = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/cloudmask_S2A_20200322_T32UQB_.img'
clouds_reclass1 = clr1.replace('.img', '.tif')
clouds_reclass2 = clr2.replace('.img', '.tif')
clouds_gj = clr1.replace('.img', '.geojson')

def binary_reclass(cloudmask):
    cloudmask[np.where(cloudmask < 2)] = 0
    cloudmask[np.where(cloudmask == 2)] = 1
    cloudmask[np.where(cloudmask == 3)] = 1
    cloudmask[np.where(cloudmask > 3)] = 0
    return cloudmask


with rasterio.open(clr1) as clouds1, \
     rasterio.open(clr2) as clouds2:

     reclass1 = clouds1.read()
     reclass2 = clouds2.read()
     profile1 = clouds1.profile  # save metadata for file creation/writing
     profile2 = clouds2.profile  # save metadata for file creation/writing
     clouds_crs = str(clouds1.crs)

     # Reclassify, only cells with clouds or cloud shadow will be kept
     reclass1 = binary_reclass(reclass1)
     reclass2 = binary_reclass(reclass2)

     with rasterio.open(clouds_reclass1, 'w', **profile1) as dst:
         # Write reclassfied raster to disk
         dst.write(reclass1)
     with rasterio.open(clouds_reclass2, 'w', **profile2) as dst:
         # Write reclassfied raster to disk
         dst.write(reclass2)

with rasterio.open(clouds_reclass1) as clouds_rc1, \
    rasterio.open(clouds_reclass2) as clouds_rc2:

    clouds_vec1 = rasterio.features.dataset_features(clouds_rc1, as_mask=True, geographic=False)
    clouds_vec2 = rasterio.features.dataset_features(clouds_rc2, as_mask=True, geographic=False)
    crs = {
        "type": "name",
        "properties": {
         "name": clouds_crs
        }
     }
    clouds_collection = gj.FeatureCollection(list(clouds_vec1)+list(clouds_vec2), crs=crs)

    #https://shapely.readthedocs.io/en/latest/manual.html#shapely.ops.unary_union
    #https://stackoverflow.com/questions/34325030/merging-two-geojson-polygons-in-python
    # convert to shapely polygons and unite..?


    with open(clouds_gj, 'w') as f:
        gj.dump(clouds_collection, f)


