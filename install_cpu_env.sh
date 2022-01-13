conda update conda -n base
conda create --name dronedetector-cpu python=3.9
conda activate dronedetector-cpu

conda install mamba -c conda-forge

pip install torch==1.10.1+cpu torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
pip install fastai==2.5.3

mamba install -c fastchan nbdev
mamba install -c conda-forge geopandas rasterio
mamba install -c pyviz bokeh holoviews hvplot
mamba install -c defaults xarray
mamba install -c conda-forge jupyter_contrib_nbextensions

pip install opencv-python scikit-image pyarrow wand tensorboard captum laspy torchsummary seaborn
pip install git+https://github.com/airctic/icevision.git#egg=icevision[all] --upgrade
pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html
