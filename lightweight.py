import cv2
import torch
import fastai
from fastai.vision.all import *

from time import sleep
from rich import print
from rich.console import Console

import os
import pathlib # Unix -> WindowsPath
_path = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

from utils.timer import Timer

print(f'\n Fastai {fastai.__version__}\nPytorch {torch.__version__}\n OpenCV {cv2.__version__}')
try:
  print(f'    GPU {torch.cuda.get_device_name(0)}')
  torch.cuda.device(0)
except: print("No GPU detected")


# ================== OpenCV Video Capture =================== #
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('\nFrame width:', frame_width)
print('Frame height:', frame_height)
print('Capture frame rate:', cap.get(cv2.CAP_PROP_FPS), '\n')
font = cv2.FONT_HERSHEY_SIMPLEX
# =========================================================== #

_t = {'fps': Timer()}
_nn = {'fps': Timer()}
console = Console()


def load_model():
    # Initialize model weights
    nn_dir = Path('models/lw_nb02.pkl')
    net = load_learner(nn_dir)
    console.log(f"[i]{nn_dir}[/i] :thumbs_up: [green]model loaded[/green]\n")
    return net

# Initialize model
net = load_model()


while True:
    _t['fps'].tic()

    # Capture frame and mirror horizontal
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    x0, y0 = frame.shape[0], frame.shape[1]

    # nn
    preds = net.predict(frame)
    print(f'\t▷ {preds[0]} ({max(preds[2]):0.4f})')

    # Resize for output
    frame = cv2.resize(frame, None, fx=1.5, fy=1.5)

    # Render FPS
    _t['fps'].toc()
    fps = 'FPS: {:.3f}'.format(1 / _t['fps'].diff)
    cv2.putText(frame, fps, (11, 15), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
    res = 'Output-res: {}x{}'.format(frame.shape[0], frame.shape[1])
    cv2.putText(frame, res, (11, 33), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)

    
    # Display headtracking frame
    cv2.imshow('Webcam: lightweight', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # ESC TO QUIT
        break
    if k == ord('q'):  # q TO QUIT
        break
    elif k == ord('r'):   # RESET ORIENTATION
        print('Key press: R')


cap.release()
cv2.destroyAllWindows()