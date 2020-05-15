# Script to crop sentinel scene to AOI while maintaining .safe directory structure

import os
from glob import glob
import warnings
import sys
import fiona
import rasterio
import rasterio.mask


def crop_raster(shape, raster):
    with fiona.open(shape, 'r') as shapefile:
        shapes = [feature['geometry'] for feature in shapefile]

    with rasterio.open(raster) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({'driver': 'JP2OpenJPEG',
                     'height': out_image.shape[1],
                     'width': out_image.shape[2],
                     'transform': out_transform})

    with rasterio.open(raster, 'w', **out_meta) as dest:
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


def get_img_dir(input_dir):
    # ? add error if directory does not exist
    if input_dir.endswith('.SAFE'):
        img_dir = dir_hop(input_dir)
    else:
        in_dir = input_dir + os.sep
        safe_files = [f for f in os.listdir(in_dir) if f.endswith('.SAFE')]
        print('There are ', len(safe_files), '.SAFE-files in the provided location: \n')
        print(safe_files)
        safe_files_full = [os.path.join(input_dir, f) for f in safe_files]
        img_dir = []
        for i in safe_files_full:
            path = dir_hop(i)
            img_dir.append(path)

    return img_dir


def dir_hop(safe_dir):
    gran_folder = os.path.join(safe_dir, 'GRANULE')
    sub_folder = os.listdir(gran_folder)[0]
    img_folder = os.path.join(gran_folder, sub_folder, 'IMG_DATA')
    return img_folder


def main():
    # (how to make sure that also windows paths are accepted?)
    shape = sys.argv[1] # first argument in commandline is path to shapefile
    # shape = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/jena-roda-testsite.shp'
    input_dir = sys.argv[2] # second argument in commandline is path to safe_dir(s)
    # input_dir = '/Users/veronikagrupp/Documents/UNIVERSIDAD/Jena/wise_1920/grassgis/data/sentinel2_testdata'
    safe_dirs = get_img_dir(input_dir)

    if type(safe_dirs) == list:
        for sd in safe_dirs:
            iter_crop(sd, shape)
    else:
        iter_crop(safe_dirs, shape)


if __name__ == '__main__':
    main()