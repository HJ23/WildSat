#
#                                 WildSat
#           This script will download extract and convert .tif data to .png
#           As mask and image patch.
#           This script is designed to be used with the landsat_download.py
#           *Script will extract only voted masks. 
#


import zipfile
from glob import glob
import os
import shutil


FULL_DATASET_ZIPS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'LandSat')
FULL_DATASET_UNZIP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'LandSat_Dataset')

print('Unziping Full Dataset...')

if not os.path.exists(FULL_DATASET_UNZIP_PATH):
    os.makedirs(FULL_DATASET_UNZIP_PATH)


images_output = os.path.join(FULL_DATASET_UNZIP_PATH, 'images')
if(not os.path.exists(images_output)):
    os.makedirs(images_output)
masks_output = os.path.join(FULL_DATASET_UNZIP_PATH, 'masks')
if(not os.path.exists(masks_output)):
    os.makedirs(masks_output)

zips_continents = glob(os.path.join(FULL_DATASET_ZIPS_PATH, '*.zip'))
    
tmp_dir = os.path.join(FULL_DATASET_UNZIP_PATH, 'tmp')
tmp_derivates = os.path.join(FULL_DATASET_UNZIP_PATH, 'tmp_derivates')
   
print('Unzip images to {}'.format(images_output))
print('Unzip masks to {}'.format(masks_output))
total_files = 0
for zip_continent in zips_continents:
    print('Unziping: {}'.format(zip_continent))
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    with zipfile.ZipFile(zip_continent, 'r') as zip_ref:
        print('Num ziped Files: {}'.format(len(zip_ref.namelist())))
        zip_ref.extractall(tmp_dir)

    patches_zips = glob(os.path.join(tmp_dir, '*.zip'))
    print('Num. of zips unpacked: {}'.format(len(patches_zips)))

    print('Unziping patches...')
    num_files = 0
    for patches_zip in patches_zips:
        output_dir = images_output

        if patches_zip.endswith('masks_derivates.zip'):
            with zipfile.ZipFile(patches_zip, 'r') as zip_ref:
                zip_ref.extractall(tmp_derivates)
                num_files += len(zip_ref.namelist())
                
            derivate_patches = glob(os.path.join(tmp_derivates, '*.tif'))

            for derivate_patch in derivate_patches:
                if '_voting_' in derivate_patch.lower():
                    shutil.move(derivate_patch, derivate_patch.replace(tmp_derivates, masks_output))
                    
            shutil.rmtree(tmp_derivates)
            continue
        elif(not  "masks" in patches_zip):
            with zipfile.ZipFile(patches_zip, 'r') as zip_ref:
                zip_ref.extractall(images_output)
                num_files += len(zip_ref.namelist())

    print('Zip: {} - Patches: {}'.format(zip_continent, num_files))
    shutil.rmtree(tmp_dir)

    print('Total files unziped: {}'.format(total_files))
    print('Done!')
    
