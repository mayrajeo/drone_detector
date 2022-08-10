conda update conda -n base
conda create --name dronedetector-deploy python=3.9
conda activate dronedetector-deploy

conda install mamba -c conda-forge

mamba install -c fastchan fastai

mamba install -c conda-forge geopandas rasterio

pip install opencv-python scikit-image

pip install 'git+https://github.com/facebookresearch/detectron2.git'

pip install albumentations
pip install nbdev
pip install -e .

nbdev_test --skip_file_re examples
