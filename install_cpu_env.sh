conda update conda -n base
conda create --name dronedetector-cpu python=3.9
conda activate dronedetector-cpu

conda install mamba -c conda-forge

pip install torch torchvision torchaudio
pip install fastai==2.6.3

mamba install -c fastchan nbdev
mamba install -c conda-forge geopandas rasterio
mamba install -c pyviz bokeh holoviews hvplot
mamba install -c defaults xarray
mamba install -c conda-forge jupyter_contrib_nbextensions

pip install opencv-python scikit-image pyarrow wand tensorboard captum laspy torchsummary seaborn vit-pytorch albumentations owslib openpyxl
pip install 'git+https://github.com/facebookresearch/detectron2.git'
