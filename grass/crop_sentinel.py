# Script to try cropping of sentinel scene to AOI while maintaining .safe directory structure


# import rasterio
# from rasterio.mask import mask
#
# band1 = rasterio.open('/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/sentinel2_testdata/S2B_MSIL1C_20200327T101629_N0209_R065_T32UPB_20200327T123753.SAFE/GRANULE/L1C_T32UPB_A015964_20200327T101842/IMG_DATA/T32UPB_20200327T101629_B01.jp2',
#                       driver='JP2OpenJPEG')
# band1_crop = mask(band1, shapes='/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/jena-roda-testsite.geojson',
#                   all_touched=True,
#                   crop=True)


import fiona
import rasterio
import rasterio.mask


with fiona.open("/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/jena-roda-testsite.shp",
                "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

with rasterio.open(
        "/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/sentinel2_testdata/S2B_MSIL1C_20200327T101629_N0209_R065_T32UPB_20200327T123753.SAFE/GRANULE/L1C_T32UPB_A015964_20200327T101842/IMG_DATA/T32UPB_20200327T101629_B01.jp2") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta

out_meta.update({"driver": "JP2OpenJPEG",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/sentinel2_testdata/S2B_MSIL1C_20200327T101629_N0209_R065_T32UPB_20200327T123753.SAFE/GRANULE/L1C_T32UPB_A015964_20200327T101842/IMG_DATA/T32UPB_20200327T101629_B01.jp2",
                   "w", **out_meta) as dest:
    dest.write(out_image)
