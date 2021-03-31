import cv2
import torch
import fastai
import fastprogress
from fastai.vision.all import *

from time import sleep
from rich import print
from rich.console import Console
from rich.live import Live
from rich.table import Table

import os
import pathlib # Unix -> WindowsPath
_path = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
os.system('cls||clear')

from utils.timer import Timer

print(f'\n Fastai {fastai.__version__}\nPytorch {torch.__version__}\n OpenCV {cv2.__version__}')
try:
  print(f'    GPU {torch.cuda.get_device_name(0)}')
  torch.cuda.device(0)
except: print("No GPU detected")


# ================== OpenCV Video Capture =================== #

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('data/02_luke_sunlight_540p.mp4')

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('\nFrame width:', frame_width)
print('Frame height:', frame_height)
print('Capture frame rate:', cap.get(cv2.CAP_PROP_FPS), '\n')
font = cv2.FONT_HERSHEY_SIMPLEX
# =========================================================== #

_t = {'fps': Timer()}
_nn = {'fps': Timer()}
ret = True
console = Console()

class progress_disabled():
    ''' Context manager to disable the progress update bar and Recorder print'''
    def __init__(self,learn:Learner):
        self.learn = learn
    def __enter__(self):
        fastprogress.fastprogress.NO_BAR = True
        # fastai.basic_train.master_bar, fastai.basic_train.progress_bar = fastprogress.force_console_behavior()
        self.learn.callback_fns[0] = partial(Recorder,add_time=True,silent=True) #silence recorder
        
        return self.learn
    
    def __exit__(self,type,value,traceback):
        # fastai.basic_train.master_bar, fastai.basic_train.progress_bar = master_bar,progress_bar
        self.learn.callback_fns[0] = partial(Recorder,add_time=True)

df = pd.DataFrame(columns=['pred', 'conf', 'time'])


def load_model():
    # Initialize model weights
    nn_dir = Path('models/lw_nb02.pkl')
    net = load_learner(nn_dir)
    net.recorder.silent = True
    net.no_bar()
    net.no_logging()
    console.log(f"[i]{nn_dir}[/i] [green]> model loaded[/green] :heavy_check_mark: \n")
    return net

net = load_model()

with Live(console=console) as live_table:
    while ret == True:
        _t['fps'].tic()

        # Capture frame and mirror horizontal
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        x0, y0 = frame.shape[0], frame.shape[1]

        # nn
        preds = net.predict(frame)


        pose = preds[0]
        conf = f'{max(preds[2]):0.4f}'
        delta_t = 1000*round(_t['fps'].toc(), 4)
        #print(f'\t▷ {pose} ({conf})')
        
        df.loc[len(df.index)] = [pose, conf, delta_t]  # adds row at end (not performant)

        # Live table
        table = Table('pred', 'conf', 'process_ms')
        table.add_row(f"▷ {pose}", f"{conf}", f"{delta_t:0.1f}")
        live_table.update(table)


        # Resize for video output
        frame = cv2.resize(frame, None, fx=1, fy=1)

        # Render Overlay
        _t['fps'].toc()
        fps = 'FPS: {:.3f}'.format(1 / _t['fps'].diff)
        cv2.putText(frame, fps, (11, 15), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
        res = 'Output-res: {}x{}'.format(frame.shape[0], frame.shape[1])
        cv2.putText(frame, res, (11, 33), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f'{pose} ({conf})', (11, 50), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.putText(frame, f'>{pose}', (11, 120), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

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