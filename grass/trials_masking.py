import rasterio.features
import rasterio.mask
from rasterio.plot import show
import numpy as np
import fiona
import geopandas as gpd
import rasterio.plot
import matplotlib.pyplot as plt
import matplotlib as mpl
from descartes import PolygonPatch
import geojson as gj

input_raster = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/T32UQB_20200322T102021_B08.jp2'
clouds_raster = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/cloudmask_S2A_20200322_T32UQB_.img'
clouds_reclass = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/clouds_reclass.tif'
clouds_shape = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/clouds_reclass_shapes.shp'

with rasterio.open(clouds_reclass) as clouds:
    clouds_crs = str(clouds.crs)

    #convert to shape
    clouds_vec = rasterio.features.dataset_features(clouds, as_mask=True, geographic=False)
    #shapes = [feature['geometry'] for feature in clouds_vec]

    crs = {
        "type": "name",
        "properties": {
            "name": clouds_crs
        }
    }
    clouds_collection = gj.FeatureCollection(list(clouds_vec), crs=crs)
    print(clouds_collection)
    #print(list(clouds_vec))

    gjson = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/clouds.geojson'
    with open(gjson, 'w') as fp:
       gj.dump(clouds_collection, fp)











# with rasterio.open(clouds_reclass) as clouds, \
#         rasterio.open(input_raster) as img:
#
#     clouds_vec = rasterio.features.dataset_features(clouds, as_mask=True, geographic = False)
#     features = [feature['geometry'] for feature in clouds_vec]
#
#     rasterio.plot.show((img, 1))
#     ax = plt.gca()
#
#     patches = [PolygonPatch(feature, edgecolor="red", facecolor="none", linewidth=2) for feature in features]
#     ax.add_collection(mpl.collections.PatchCollection(patches, match_original=True))


#
#
# with rasterio.open(clouds_reclass) as clouds, \
#         rasterio.open(input_raster) as img:
#
#     trf = clouds.transform
#     cl_arr = clouds.read()
#     #clouds_vec = rasterio.features.shapes(cl_arr, transform=trf) # connectivity=4,
#     clouds_vec = rasterio.features.dataset_features(clouds, as_mask=True, geographic=False)
#     for i in clouds_vec:
#         print(rasterio.features.is_valid_geom(i))
#     #print(list(clouds_vec))
#     #shapes = [feature['geometry'] for feature in clouds_vec]

#     out_image, out_transform = rasterio.mask.mask(img, clouds_vec, invert=True, all_touched=True)
#     out_meta = img.meta
#
#     # Reclassify
#     # out_image[np.where(out_image == 11)] = 0
#     # out_image[np.where(out_image == 1)] = 0
#
#     out_meta.update({'driver': 'JP2OpenJPEG',
#                      'height': out_image.shape[1],
#                      'width': out_image.shape[2],
#                      'transform': out_transform,
#                      'nodata': 0.0})
#
# with rasterio.open(input_raster, 'w', **out_meta) as dest:
#     dest.write(out_image)
#



   #show(img)
    # convert to shape
    # clouds_vec = rasterio.features.dataset_features(clouds, as_mask=True, geographic = False)
    # #shapes = [feature['geometry'] for feature in clouds_vec]
    # shapes = [feature for feature in clouds_vec]
    # print(shapes)
    # cl_gdf = gpd.GeoDataFrame(shapes)
    # print(type(cl_gdf))
    # #print(cl_gdf.head())
    # cl_gdf.plot()

    #print(cl_gdf)
    #cl_gdf.to_file('/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/clouds_reclass_shapes.shp')
    #print(list(clouds_vec))
#
#     # shp_crs = img.crs
#     #
#     # with fiona.open(clouds_shape, 'w', driver='ESRI Shapefile', schema=shp_schema, crs = shp_crs) as dst:
#     #     dst.writerecords(clouds_vec)
#
#     # extract geometries
# #
# #
# #     # mask clouds
# #     out_image, out_transform = rasterio.mask.mask(img, shapes, invert=True, all_touched = True)
# #     out_meta = img.meta
# #
# #     # Reclassify
# #     #out_image[np.where(out_image == 11)] = 0
# #     #out_image[np.where(out_image == 1)] = 0
# #
# #     out_meta.update({'driver': 'JP2OpenJPEG',
# #                      'height': out_image.shape[1],
# #                      'width': out_image.shape[2],
# #                      'transform': out_transform,
# #                      'nodata': 0.0})
# #
# #
# # with rasterio.open(input_raster, 'w', **out_meta) as dest:
# #     dest.write(out_image)