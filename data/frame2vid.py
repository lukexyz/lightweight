import cv2
import numpy as np
import os
from tqdm import tqdm

# Combine image folder into video
img_path = 'D:/python/lightweight/data/saveframe_demo/'
filename = 'lw_demo01' #no .mp4
output_folder = 'D:/python/lightweight/data'
fps_out = 24

img_list=[x for x in os.listdir(img_path) if 'jpg' in x or 'JPEG' in x]
print(f'{len(img_list)} images found')

img_array = []
for f in tqdm(img_list):
    img = cv2.imread(f'{img_path}/{f}')
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)

out = cv2.VideoWriter(f'{filename}.mp4', cv2.VideoWriter_fourcc(*"mp4v"), fps_out, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

print(f'\nsaved {output_folder}/{filename}.mp4\n')