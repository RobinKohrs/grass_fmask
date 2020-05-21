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
from shapely.geometry import shape, MultiPolygon
from shapely.ops import unary_union
import geopandas as gpd
import fiona

clr1 = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/cloudmask_S2A_20200322_T32UPB_.img'
clr2 = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/cloudmask_S2A_20200322_T32UQB_.img'
clouds_reclass1 = clr1.replace('.img', '.tif')
clouds_reclass2 = clr2.replace('.img', '.tif')
#clouds_gp = clr1.replace('.img', '.gpkg')
#
# def binary_reclass(cloudmask):
#     cloudmask[np.where(cloudmask < 2)] = 0
#     cloudmask[np.where(cloudmask == 2)] = 1
#     cloudmask[np.where(cloudmask == 3)] = 1
#     cloudmask[np.where(cloudmask > 3)] = 0
#     return cloudmask
#
#
# with rasterio.open(clr1) as clouds1, \
#      rasterio.open(clr2) as clouds2:
#
#      reclass1 = clouds1.read()
#      reclass2 = clouds2.read()
#      profile1 = clouds1.profile  # save metadata for file creation/writing
#      profile2 = clouds2.profile  # save metadata for file creation/writing
#      clouds_crs = str(clouds1.crs)
#
#      # Reclassify, only cells with clouds or cloud shadow will be kept
#      reclass1 = binary_reclass(reclass1)
#      reclass2 = binary_reclass(reclass2)
#
#      with rasterio.open(clouds_reclass1, 'w', **profile1) as dst:
#          # Write reclassfied raster to disk
#          dst.write(reclass1)
#      with rasterio.open(clouds_reclass2, 'w', **profile2) as dst:
#          # Write reclassfied raster to disk
#          dst.write(reclass2)

def binary_to_vector(binary_raster):
    vector = rasterio.features.dataset_features(binary_raster, as_mask=True, geographic=False)
    shapes = MultiPolygon([shape(feature['geometry']).buffer(0) for feature in vector])
    return shapes


def reclass_to_mergedvector(clouds_reclass): # list of the two reclassified rasters of one date

    with rasterio.open(clouds_reclass[0]) as clouds_rc1, \
            rasterio.open(clouds_reclass[1]) as clouds_rc2:

        clouds_crs = str(clouds_rc1.crs)

        cl_shp1 = binary_to_vector(clouds_rc1)
        cl_shp2 = binary_to_vector(clouds_rc2)

        clouds_gpd = gpd.GeoDataFrame(geometry=[
            cl_shp1, cl_shp2
        ])

        geoms = clouds_gpd.geometry.unary_union
        clouds_vec = gpd.GeoDataFrame(geometry=[geoms])
        clouds_vec.crs = clouds_crs

        dir = clouds_reclass[0].split('/')
        names = dir[-1].split('_')
        #names = clouds_reclass[-1].split('_')
        clouds_gp = '_'.join(names[:3])
        clouds_gp += '.gpkg'
        #clouds_gp += '.geojson'
        clouds_gp_path = os.path.join(*dir[:-1], clouds_gp)
        clouds_vec.to_file(clouds_gp_path, driver='GPKG')

        #with fiona.open(clouds_gp_path, 'w', driver='GPKG') as f:
         #   f.to_file(clouds_gp_path, driver='GPKG')

        # seems like i cannot save file to other directory than my working directory... ??
        # wobei es im data Ordner gespeichert wurde als es geklappt hat?? Häääää...

clouds_reclass = [clouds_reclass1, clouds_reclass2]
reclass_to_mergedvector(clouds_reclass)



