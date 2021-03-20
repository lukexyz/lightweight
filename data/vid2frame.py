"""
HOW TO USE

1. change `filename` to video path

2. > python vid2frame.py 

"""


import cv2
import numpy as np
import os

# Playing video from file:
filename = '02_luke_sunlight'
cap = cv2.VideoCapture(f'{filename}.mp4')

try:
    if not os.path.exists(filename):
        os.makedirs(filename)
except OSError:
    print ('Error: Creating directory of data')

currentFrame = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Saves image of the current frame in jpg file
    name = f'./{filename}/{filename}_frame{currentFrame}.jpg'
    print ('Creating...' + name)
    cv2.imwrite(name, frame)

    # To stop duplicate images
    currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()