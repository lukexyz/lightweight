import cv2
import numpy as np
import os

# Playing video from file:
filename = 'lift_lucy_01'
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
    name = f'./{filename}/frame' + str(currentFrame) + '.jpg'
    print ('Creating...' + name)
    cv2.imwrite(name, frame)

    # To stop duplicate images
    currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()