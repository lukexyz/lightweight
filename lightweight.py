'''
Usage
> python lightwieght.py -h

'''


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
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.align import Align
from fastcore.script import *

import os
from typing import Dict, List, Tuple
import pathlib # Unix -> WindowsPath
_path = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
os.system('cls||clear')

from utils.timer import Timer

@call_parse
def main(vid:Param("Use video sample?", store_true),
         saveframe:Param("Save output frames?", store_true)):
    "Print `sample`, video input source: webcam or video sample"

    if vid: start_text = 'sample video'
    else: start_text = 'webcam'

    # ==================== Fastai and GPU ===================== #
    console = Console()
    console.log(Panel(f"Starting program with [green][{start_text}][/green]", title="💪😬💪 lightweight 💪🤪💪"))
    console.log(f'\n Fastai {fastai.__version__}\nPytorch {torch.__version__}\n OpenCV {cv2.__version__}')
    try:
        console.log(f' GPU [green]:heavy_check_mark:[/green] {torch.cuda.get_device_name(0)}')
        torch.cuda.device(0)
    except: console.log("No GPU detected")

    # ================== OpenCV Video Capture =================== #
    if vid:
        cap = cv2.VideoCapture('data/AlphaPose_squat_loop_540p.mp4')
        cap = cv2.VideoCapture('data/girl.gif')
        # or 'data/squat_loop_540p.mp4'
        # or 'data/02_luke_sunlight_540p.mp4'
    else:
        cap = cv2.VideoCapture(0)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    console.log('\nFrame width:', frame_width)
    console.log('Frame height:', frame_height)
    console.log('Capture frame rate:', cap.get(cv2.CAP_PROP_FPS), '\n')
    font = cv2.FONT_HERSHEY_SIMPLEX
    # =========================================================== #

    _t = {'fps': Timer()}
    _nn = {'fps': Timer()}
    ret = True
    fastprogress.fastprogress.NO_BAR = True
    fastprogress.fastprogress.FLUSH = False
    pose_dict: Dict[Tuple[str, str], [float, float]] = {}
    buffer_length = 10
    n = 0
    atg, squats = 0, 0

    def load_model():
        # Initialize model weights
        nn_dir = Path('models/lw_nb04_ap2.pkl')  # previously lw_nb02.pkl
        net = load_learner(nn_dir)
        console.log(f"[i]{nn_dir}[/i] [green]> model loaded[/green] :heavy_check_mark: \n")
        return net

    console.log(Rule("load model"))
    net = load_model()
    console.log(Rule("run"))

    with Live(console=console) as live_table:
        while ret == True:
            _t['fps'].tic()
            n += 1

            # Capture frame and mirror horizontal
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)
            x0, y0 = frame.shape[0], frame.shape[1]

            # nn
            preds = net.predict(frame)
            pose = preds[0]
            conf = max(preds[2])
            delta_t = 1000*round(_t['fps'].toc(), 4)

            # =============== table ===============
            if len(pose_dict) > buffer_length - 1:
                pose_dict.pop(list(pose_dict.keys())[0])

            pose_dict[(f'{n}', pose)] = [conf, delta_t]

            table = Table(title="Pose Estimation")
            table.add_column("frame")
            table.add_column("pose")
            table.add_column("conf")
            table.add_column("process_ms")
            for ((n_frame, pred), [conf, delta_t]) in pose_dict.items():
                table.add_row(n_frame,
                            Text(f'▷{pred}'),
                            Text(f"{conf:.4f}", 
                                    style="white" if conf < 0.8 else "green"),
                            Text(f'{delta_t:.0f}'),
                            )

            live_table.update(Align.center(table))

            # ============= Squat Counter =============
            if pose == '07_squatDown': 
                atg += 1
            if (pose == '05_frontUp') & (atg >= 3):  # 3 frames of atg (error correction)
                squats += 1
                atg = 0

            # ============= Output Frame =============
            # Resize for video output
            frame = cv2.resize(frame, None, fx=1, fy=1)

            # Render Overlay
            _t['fps'].toc()
            fps = f'({n}) FPS: {1/_t["fps"].diff:.03f}'
            cv2.putText(frame, fps, (11, 15), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
            in_res = f'Intput res: {frame.shape[1]}x{frame.shape[0]}'
            cv2.putText(frame, in_res, (11, 33), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
            out_res = f'Output res: {frame_width}x{frame_height}'
            cv2.putText(frame, out_res, (11, 51), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f'{pose} ({conf:0.4})', (11, 70), font, 0.35, (0, 255, 0), 1, cv2.LINE_AA)

            # --> (pose label) Big text 
            cv2.putText(frame, f'>{pose}', (11, frame_height-20), font, 1.5, (5, 10, 5), 6, cv2.LINE_AA)
            cv2.putText(frame, f'>{pose}', (11, frame_height-20), font, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
            # --> (squat counter)
            cv2.putText(frame, f'Squats: {squats}', (11, frame_height-80), font, 2, (5, 10, 5), 6, cv2.LINE_AA)
            cv2.putText(frame, f'Squats: {squats}', (11, frame_height-80), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
            if (n > 192) & (n< 205): 
                cv2.putText(frame, f'lightweight baby', (375, 215), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            if (pose == '06_overheadPress') & (n > 339) & (n < 380): 
                cv2.putText(frame, f'nothing but a peanut', (150, 200), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


            # OpenCV Show frame
            cv2.imshow('Webcam: lightweight', frame)

            if saveframe:
                cv2.imwrite(f"data/saveframe_demo/{n:06d}_frame.jpg", frame)

            k = cv2.waitKey(1) & 0xFF
            if k == 27:  # ESC TO QUIT
                break
            if k == ord('q'):  # q TO QUIT
                break
            elif k == ord('r'):   # RESET ORIENTATION
                print('Key press: R')

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()