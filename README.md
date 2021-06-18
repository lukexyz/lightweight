
# `lightweight` 💪🎯💪

<p align="center">
  <img src="https://raw.githubusercontent.com/lukexyz/lightweight/master/media/ronnie_catchphrase.JPG">
</p>

A squat dectector algorithm running on [`fastai`](https://github.com/fastai/fastai) and [`alphapose`](https://github.com/MVIG-SJTU/AlphaPose). 

The classifier uses the AlphaPose network as an itermediate step, and trains quickly using a pretrained `resnet34` couretesy of `fastai v2`. Each frame is classified as one of 7 labels that I made up from my exercise routine. 

</br>  

![image](https://github.com/lukexyz/lightweight/blob/master/media/lw_demo_small.gif?raw=true)
💪😬💪 💪😙💪 💪🤪💪
</br>  
</br>  

## Dataset and Training


![image](https://github.com/lukexyz/lightweight/blob/master/media/training_results.JPG?raw=true)


## Run
```sh
> conda activate lightweight
# webcam
> python lightweight.py 
# sample vid 
> python lightweight.py --vid --saveframe
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

### AlphaPose Installation
[MVIG-SJTU/AlphaPose](https://github.com/MVIG-SJTU/AlphaPose/blob/master/docs/INSTALL.md)
```sh
# 1. New conda env
conda create -n alphapose python=3.6 pip jupyter -y
conda activate alphapose

# 2. Install PyTorch
conda install pytorch==1.1.0 torchvision==0.3.0
```

### Get AlphaPose
```sh
git clone https://github.com/MVIG-SJTU/AlphaPose.git
# git pull origin pull/592/head if you use PyTorch>=1.5
cd AlphaPose

# 4. install
-- export PATH=/usr/local/cuda/bin/:$PATH
-- export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:$LD_LIBRARY_PATH
python -m pip install cython
```
