#
#                             WildSat
#           This script will convert .tif data to .png and 
#           combine wildfire with its binary segmentation.
#           All outputs will be saved in Wildfire_Dataset.      
#

import cv2
import numpy as np
import os
import shutil
import rasterio

IMAGE_PATH=FULL_DATASET_UNZIP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'LandSat_Dataset',"images")
MASKS_PATH=FULL_DATASET_UNZIP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'LandSat_Dataset',"masks")
OUT_PATH=os.path.join(os.path.dirname(os.path.realpath(__file__)), ".." ,'Wildfire_Dataset','MAIN_DATA')

def convert2image(path):
    MAX_PIXEL_VALUE = 65535 # Max. pixel value, used to normalize the image
    img = rasterio.open(path).read((7,6,2)).transpose((1, 2, 0))    
    img = np.float32(img)/MAX_PIXEL_VALUE
    img = np.array(img * 255, dtype=np.uint8)
    img= cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def convert2mask(path):
    mask = cv2.imread(os.path.join(MASKS_PATH,path))
    copy = mask.copy()
    height, width, depth = mask.shape
    for i in range(0, height):
        for j in range(0, width):
            if (mask[i,j,0] > 0):
                copy[i,j] = 255
    return copy



images=os.listdir(IMAGE_PATH)
masks=os.listdir(MASKS_PATH)

if  os.path.exists(OUT_PATH):
    shutil.rmtree(OUT_PATH)
    os.mkdir(os.path.join(OUT_PATH,"MAIN_DATA"))
else:
    os.mkdir(os.path.dirname(os.path.realpath(__file__)), "..","Wildfire_dataset"))
    os.mkdir(os.path.dirname(os.path.realpath(__file__)), "..","Wildfire_dataset","MAIN_DATA"))
    
# combine only images which has mask.
for i,mask_name in enumerate(masks):
    image_name=mask_name.replace("_voting","")
    print(image_name,os.path.join(IMAGE_PATH,image_name))

    if(image_name in images ):
        
        img=convert2image(os.path.join(IMAGE_PATH,image_name))
        mask=convert2mask(os.path.join(IMAGE_PATH,mask_name))

        out=np.zeros(dtype=np.uint8, shape=(256,512,3))
        out[:256,:256,:]=img
        out[:256,256:,:]=mask
        cv2.imwrite(os.path.join(OUT_PATH,str(i)+".png"),out)    
