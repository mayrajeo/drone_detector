conda update conda -n base
conda create --name dronedetector-dep python=3.9
conda activate dronedetector-deploy

conda install mamba -c conda-forge

pip install torch>=1.10.1 torchvision>=0.11.2 torchaudio>=0.10.1
pip install fastai>=2.7.7

mamba install -c conda-forge geopandas>=0.11.0 rasterio>=1.3.0
mamba install -c conda-forge jupyter_contrib_nbextensions

pip install opencv-python scikit-image

pip install 'git+https://github.com/facebookresearch/detectron2.git'

pip install albumentations