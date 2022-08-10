conda update conda -n base
conda create --name dronedetector-dev python=3.9
conda activate dronedetector-dev

conda install mamba -c conda-forge

mamba install -c fastchan fastai

mamba install -c conda-forge geopandas rasterio
mamba install -c conda-forge xarray
mamba install -c conda-forge jupyter_contrib_nbextensions

pip install opencv-python scikit-image pyarrow captum wandb tensorboard
pip install laspy torchsummary seaborn owslib openpyxl

pip install 'git+https://github.com/facebookresearch/detectron2.git'

pip install albumentations 
pip install timm
pip install nbdev

pip install -e .

nbdev_test --skip_file_re examples
