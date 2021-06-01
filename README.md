
# 💪😬💪 `light`  💪🤪💪  `weight`  💪😙💪

</br>  

![image](https://user-images.githubusercontent.com/13252029/114288591-56985700-9a69-11eb-8509-988707672256.png)

## Run
```sh
> conda activate lightweight
# webcam
> python lightweight.py 
# sample vid
> python lightweight.py --vid
```


## Installation

```
> conda create -n lightweight python=3.8 pip jupyter
> conda activate lightweight
> conda install -c fastai -c pytorch -c anaconda fastai gh anaconda
> pip install -r requirements.txt
```





## OpenPose Installation

[CMU-Perceptual-Computing-Lab/openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md#operating-systems-requirements-and-dependencies)

## AlphaPose Installation
[MVIG-SJTU/AlphaPose](https://github.com/MVIG-SJTU/AlphaPose/blob/master/docs/INSTALL.md)
```sh
# 1. New conda env
conda create -n alphapose python=3.6 pip jupyter -y
conda activate alphapose

# 2. Install PyTorch
conda install pytorch==1.1.0 torchvision==0.3.0
```

# 3. Get AlphaPose
```sh
git clone https://github.com/MVIG-SJTU/AlphaPose.git
# git pull origin pull/592/head if you use PyTorch>=1.5
cd AlphaPose

# 4. install
-- export PATH=/usr/local/cuda/bin/:$PATH
-- export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:$LD_LIBRARY_PATH
python -m pip install cython
```

## tf-Openpose Installation
```sh
git clone https://github.com/infocom-tpo/tf-openpose.git
cd tf-openpose

conda create -n tf-openpose python=3.6 pip jupyter
conda activate tf-openpose
pip install tensorflow==1.3.0
pip install opencv-python==3.4.3.18
pip install -r requirements.txt

# might need to rename model dir from here https://qiita.com/kotauchisunsun/items/bdbdca2ddb9036e29ab1
python realtime_webcam.py --camera=0 --model=mobilenet --zoom=1.0
python inference.py --model=mobilenet --imgpath=./images/golf.jpg
```
