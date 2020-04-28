# Script to crop sentinel scene to AOI while maintaining .safe directory structure

import fiona
import rasterio
import rasterio.mask
import os
from glob import glob
import warnings


def crop_raster(shape, raster):
    with fiona.open(shape, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    with rasterio.open(raster) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "JP2OpenJPEG",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    with rasterio.open(raster, "w", **out_meta) as dest:
        dest.write(out_image)

def iter_crop(dir, shape):
    glob_pattern = os.path.join(dir, '*')
    files = glob(glob_pattern)
    if len(files) != 14:
        warnings.warn('Usually Sentintel 2 download contains 14 image files. There are ' + str(len(files)) +
                      ' files in the current directory: ' + dir +
                      '\n Please check if an error occured in the download etc. \n Cropping proceeds with existing files.')

    for f in files:
        crop_raster(shape, f)


def crop_within_safe(safe_dir, shape):
    # error if directory does not exist

    gran_folder = os.path.join(safe_dir, 'GRANULE')
    sub_folder = os.listdir(gran_folder)[0]
    img_folder = os.path.join(gran_folder, sub_folder, 'IMG_DATA')
    iter_crop(img_folder, shape)

    # LATER: check if it's one or more safe_dirs, adaption for more than one .safe directory


def main():
    shape = input('Please enter the path to the shapefile of your AOI: '
    #safe_dir = input('Please enter the path to your .safe directory or a directory containing multiple .safe directories: ')
    safe_dir = input('Please enter the path to your .safe directory: ')
    crop_within_safe(safe_dir, shape)

if __name__ == '__main__':
    main()
