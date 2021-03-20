import cv2
# from glob import glob  
# from collections import OrderedDict
# import os, pathlib
import torch


from utils.timer import Timer
print('torch version:', torch.__version__)

# ================== OpenCV Video Capture =================== #
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('Frame width:', frame_width)
print('Frame height:', frame_height)
print('Capture frame rate:', cap.get(cv2.CAP_PROP_FPS))
font = cv2.FONT_HERSHEY_SIMPLEX
# =========================================================== #

_t = {'fps': Timer()}
_nn = {'fps': Timer()}


while True:
    _t['fps'].tic()

    # Capture frame and mirror horizontal
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Crop image to central/top area
    # (optimises foward-pass speed and overall FPS)
    c1 = frame_height * 1  # % Keep from top
    c2 = frame_width * 0.2   # % removed from each side
    y1, y2 = 0, int(c1)
    x1, x2 = int(c2), int(frame_width - c2)
    frame = cv2.resize(frame[y1:y2, x1:x2], None, fx=0.8, fy=0.8)


    outframe = cv2.resize(frame, None, fx=1.2, fy=1.2)

    # Render FPS
    _t['fps'].toc()
    fps = 'FPS: {:.3f}'.format(1 / _t['fps'].diff)
    cv2.putText(outframe, fps, (11, 15), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
    res = 'NN-res: {}x{}'.format(frame.shape[0], frame.shape[1])
    cv2.putText(outframe, res, (11, 33), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)

    
    # Display headtracking frame
    cv2.imshow('Headtracking', outframe)


    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # ESC TO QUIT
        break
    elif k == ord('r'):   # RESET ORIENTATION
        print('Key press: R')


cap.release()
cv2.destroyAllWindows()