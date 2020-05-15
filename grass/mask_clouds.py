# script to overlay a sentinel scene with a cloud mask and assign NoData to the raster cells below clouds

import rasterio.features
import rasterio.mask
import numpy as np
import os
import geojson as gj

# define path for result raster of fmask algorithm
clouds_raster = '...img'
#clouds_raster = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/cloudmask_S2A_20200322_T32UQB_.img'

# define target file for reclassfied cloud mask
clouds_reclass = '.../clouds_reclass.tif'
#clouds_reclass = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/clouds_reclass.tif'

# define input directory with image data (one or multiple) in jp2 format (not yet safe directory...!)
#in_dir = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/IMG_DATA'
in_dir = '...'
input_raster = [os.path.join(in_dir, f) for f in os.listdir(in_dir) if f.endswith(".jp2")]

# optional: define geojson file to extract cloud polygons for visualization and checking in QGIS or others
#clouds_gj = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/cloud_mask_examp/clouds.geojson'
#clouds_gj = '.../clouds.geojson'


#create reclassified cloud mask
with rasterio.open(clouds_raster) as src:
    # Read as numpy array
    reclass = src.read()
    profile = src.profile # save metadata for file creation/writing

    # Reclassify, only cells with clouds or cloud shadow will be kept
    reclass[np.where(reclass < 2)] = 0
    reclass[np.where(reclass == 2)] = 1
    reclass[np.where(reclass == 3)] = 1
    reclass[np.where(reclass > 3)] = 0


with rasterio.open(clouds_reclass, 'w', **profile) as dst:
    # Write reclassfied raster to disk
    dst.write(reclass)


# open reclassified cloud mask
with rasterio.open(clouds_reclass) as clouds:
    # convert to shapes
    clouds_vec = rasterio.features.dataset_features(clouds, as_mask=True, geographic=False) # as_mask=True only converts cells with valid values/ not null
    shapes = [feature['geometry'] for feature in clouds_vec]


    # optionally create gjson:
    # *********************************
    # clouds_crs = str(clouds.crs)
    # crs = {
    #     "type": "name",
    #     "properties": {
    #         "name": clouds_crs
    #     }
    # }
    # clouds_collection = gj.FeatureCollection(list(clouds_vec), crs=crs)
    # with open(clouds_gj, 'w') as f:
    #    gj.dump(clouds_collection, f)
    # *********************************

    # each image file in input directory will be masked
    for i in input_raster:
        out_name = i.replace('.jp2', '.tif') # create new filename to save to tif, we could also overwrite jp2 data like we did with the cropping, depends on workflow and memory
        with rasterio.open(i) as img:

            # mask clouds
            out_image, out_transform = rasterio.mask.mask(img, shapes, invert=True, all_touched = True)
            out_profile = img.profile

            # out_profile.update({'driver': 'JP2OpenJPEG'  # only neccessary if we want to overwrite file and keep jp2
            #                     'transform': out_transform, # doesn't seem to be neccessary
            #                     'nodata': 0.0}) # doesn't seem to be neccessary


        with rasterio.open(out_name, 'w', **out_profile) as dest:
            dest.write(out_image)