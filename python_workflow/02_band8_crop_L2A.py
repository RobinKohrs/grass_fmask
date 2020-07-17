# Resample and move band 8 to 20m (folder) then crop sentinel scenes to AOI while maintaining .safe directory structure

import fiona
import rasterio
import rasterio.mask
import os
from glob import glob
import sys
import shutil
import zipfile

# Unzips all the downloaded .SAFE-directories
def unzip(dirs):
    # get all files in input dir
    files = [file for file in os.listdir(dirs)]
    # check if there are already unzipped files
    for file in files:
        if file.endswith(".SAFE"):
            print("The files are already unzipped")
            return None

    # if not unzip them
    zips = [x for x in os.listdir(dirs) if x.endswith(".zip") and "L2A" in x]
    for file in zips:
        with zipfile.ZipFile( dirs + os.sep + file, "r") as src:
            src.extractall(dirs)
        os.remove(file)

# band 8 is only available in 10m resolution but needed for NDVI
# therefore resample band 8 to 20m resolution and move it into the R20 directory
def resample_and_move_band8(dirs):
    _all = [x for x in os.listdir(dirs) if x.endswith(".SAFE") and "L2A" in x]
    for dir in _all:
        band08_list = glob(os.path.join(dirs, dir, "GRANULE", "*", "IMG_DATA", "R10m", "*B08*"))
        pathb08 = band08_list[0]
        tiff = pathb08.replace("R10m", "R20m").replace("_10m", "_20m")
        cmd = "gdal_translate -tr 20 -20 {inp} {out}".format(inp=pathb08, out=tiff)
        os.system(cmd)

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

# append complete path to raster files and apply crop_raster function to all
def iter_crop(dir, shape):
    glob_pattern = os.path.join(dir, '*')
    files = glob(glob_pattern)

    for f in files:
        crop_raster(shape, f)

# retrieve complete path to image data within .SAFE directories
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

# hop through .SAFE directories to folder with 20m resolution data
def dir_hop(safe_dir):
    gran_folder = os.path.join(safe_dir, 'GRANULE')
    sub_folder = os.listdir(gran_folder)[0]
    resolution_folder = os.listdir(os.path.join(gran_folder, sub_folder, "IMG_DATA"))
    print("dirs with spatial resolution to remove")
    print(resolution_folder)
    dirs_to_remove = [x for x in os.listdir(os.path.join(gran_folder, sub_folder, "IMG_DATA")) if "R20m" not in x]
    for i in dirs_to_remove:
        shutil.rmtree(os.path.join(gran_folder, sub_folder,"IMG_DATA", i))
    r20 = os.path.join(gran_folder, sub_folder,'IMG_DATA', "R20m")
    return r20


def main(input_dir, aoi):
    unzip(input_dir)
    resample_and_move_band8(input_dir)
    safe_dirs = get_img_dir(input_dir)
    if type(safe_dirs)==list:
        for sd in safe_dirs:
            iter_crop(sd, aoi)
    else:
        iter_crop(safe_dirs, aoi)


if __name__ == '__main__':
    input_dir = sys.argv[1]
    aoi = sys.argv[2]
    main(input_dir, aoi)
