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
def main(vid:Param("Use video sample?", store_true)):
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

            # ----------- table --------------
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

            # Resize for video output
            frame = cv2.resize(frame, None, fx=1, fy=1)

            # Render Overlay
            _t['fps'].toc()
            fps = 'FPS: {:.3f}'.format(1 / _t['fps'].diff)
            cv2.putText(frame, fps, (11, 15), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
            res = 'Output-res: {}x{}'.format(frame.shape[0], frame.shape[1])
            cv2.putText(frame, res, (11, 33), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f'{pose} ({conf})', (11, 50), font, 0.35, (255, 255, 255), 1, cv2.LINE_AA)

            # --> Big text
            cv2.putText(frame, f'>{pose}', (11, 120), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # OpenCV Show frame
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

if __name__ == '__main__':
    main()