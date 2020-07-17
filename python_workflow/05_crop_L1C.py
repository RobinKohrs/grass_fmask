# Crop Sentinel-2 L1C scenes to AOI while maintaining .SAFE directory structure

import sys
import fiona
import rasterio
import rasterio.mask
import os
from glob import glob
import warnings

# crops given raster to the extent of a given shapefile and overwrites original jpeg2 file
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

# appends complete path to raster files and apply crop_raster function to all
def iter_crop(dir, shape):
    glob_pattern = os.path.join(dir, '*')
    files = glob(glob_pattern)
    if len(files) != 14:
        warnings.warn('Usually Sentintel 2 download contains 14 image files. There are ' + str(len(files)) +
                      ' files in the current directory: ' + dir +
                      '\n Please check if an error occured in the download etc. \n Cropping proceeds with existing files.')

    for f in files:
        crop_raster(shape, f)
    print('Successfully cropped .SAFE directory.')

# retrieves complete path to image data within .SAFE directories
def get_img_dir(input_dir):
    if input_dir.endswith('.SAFE'):
        img_dir = dir_hop(input_dir)
    else:
        in_dir = input_dir + os.sep
        safe_files = [f for f in os.listdir(in_dir) if f.endswith('.SAFE') ]
        print('There are ', len(safe_files), '.SAFE-files in the provided location: \n')
        print(safe_files)
        safe_files_full = [os.path.join(input_dir, f) for f in safe_files]
        img_dir = []
        for i in safe_files_full:
            path = dir_hop(i)
            img_dir.append(path)

    return img_dir

# hops through .SAFE directory to folder with image data
def dir_hop(safe_dir):
    gran_folder = os.path.join(safe_dir, 'GRANULE')
    sub_folder = os.listdir(gran_folder)[0]
    img_folder = os.path.join(gran_folder, sub_folder, 'IMG_DATA')
    return img_folder


def main(shape, input_dir):

    safe_dirs = get_img_dir(input_dir) # retrieve paths to image directories

    if type(safe_dirs) == list: # check if one or more .SAFE directories are given and iterate over all if necessary
        for sd in safe_dirs:
            iter_crop(sd, shape)
    else:
        iter_crop(safe_dirs, shape)


if __name__ == '__main__':
    input_dir = sys.argv[1] # first argument in commandline is path to .SAFE directories
    shape = sys.argv[2]  # second argument in commandline is path to aoi shapefile
    main(shape, input_dir)
