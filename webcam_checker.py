# webcam_checker.py
# cycles through and identifies available webcams

import numpy as np
import cv2 as cv

def check_cam_by_index(i):
    cap = cv.VideoCapture(i)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv.imshow('frame',frame)
        
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


def check_multiple():
    for i in range(-1,10):
        try:
            print(f'checking camera #{i}')
            print('press q for next')
            check_cam_by_index(i)
        except:
            continue

#check_multiple() # 2 is index of OBS Virtual Camera , 0 is index of OBS-Camera

#check_cam_by_index(2) 

check_multiple()