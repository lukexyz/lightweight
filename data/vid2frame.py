import cv2
import numpy as np
import os

# Playing video from file:
path = 'C:/Python/lightweight/data/04_saturday_sesh/'
filename = '04_saturday_sesh_charlotte' #no .mp4
output_folder = 'C:/Python/lightweight/data/04_saturday_sesh/raw'
cap = cv2.VideoCapture(path+filename+'.mp4')

try:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
except OSError:
    print ('Error: Creating directory of data')

currentFrame = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Saves image of the current frame in jpg file
    name = f'{output_folder}/{filename}_frame{currentFrame}.jpg'
    print ('Saving file:' + name)
    cv2.imwrite(name, frame)

    # To stop duplicate images
    currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()