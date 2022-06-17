# Automatic deadwood detection from RGB UAV imagery



`drone_detector` was originally a python package for automatic deadwood detection or segmentation from RGB UAV imagery. It contains functions and helpers to use various GIS data with fastai and Detectron2.

icevision support will be added once it supports pytorch 1.11 and fastai 2.6 or newer.

## Installation

Installing the required packages is fairly tricky, because some of them are easiest to install via conda (`geopandas` and `GDAL`), some via pip (`pytorch`) and for `detectron2` it is required to specify which prebuilt package to use. 

Repository contains two installation scripts, one for CPU environment and other for GPU environment with cudatoolkit 11.3. Install miniconda and run `bash -i install_cpu_env.sh` for CPU environment and `bash -i install_gpu_env.sh`. If you have different cudatoolkit, modify `pytorch` and `detectron2` urls. 

Afterwards install library with `pip install . -e`.

### Running with Singularity
  
Use provided `dronecontainer.def` definition file to build Singularity container. Follow instructions on [https://cloud.sylabs.io/builder](https://cloud.sylabs.io/builder) and build the image with
 
```
singularity build --remote dronecontainer.sif dronecontainer.def
```

## Training

Examples need to be updated, stay tuned!

## CLI Usage

### fastai

`predict_segmentation_fastai` runs pretrained U-Net model for larger image. So far we support only models saved with `learner.export()`.

### Detectron2

`predict_bboxes_detectron2` and `predict_instance_masks_detectron2` work identically with icevision CLI commands, but use Detectron2 instead. 

# Citations

## Publications using this repository

Nothing so far, but soon!

## Other people's work applied in this repository

This repository contains parts from 

* [Solaris](https://github.com/CosmiQ/solaris) by CosmiQ Works
* [pycococreator](https://github.com/waspinator/pycococreator) by waspinator, [https://doi.org/10.5281/zenodo.4627206](https://doi.org/10.5281/zenodo.4627206)
