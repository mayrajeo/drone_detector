
# Automatic deadwood detection from RGB UAV imagery



`drone_detector` was originally a python package for automatic deadwood detection or segmentation from RGB UAV imagery. It contains functions and helpers to use various GIS data with fastai, icevision and Detectron2.

## Installation

NEEDS UPDATING

Use `conda` to create environment from `environment.yml` with

```
conda env create -f environment.yml
```

After that change directory to `drone_detector` and run `pip install -e .` to get CLI commands to work.

### Running with Singularity
 
NEEDS UPDATING
 
Use provided `dronecontainer.def` definition file to build Singularity container. Follow instructions on [https://cloud.sylabs.io/builder](https://cloud.sylabs.io/builder) and build the image with
 
```
singularity build --remote dronecontainer.sif dronecontainer.der
```

### Running with Docker

TODO

## CLI Usage

### icevision

`predict_bboxes_icevision` and `predict_instance_masks_icevision` process large image, tile them to `--tile_size` sized patches with `--tile_overlap` pixel overlap. The parameters for the models are read from config files described in `drone_detector.engines.icevision.models`.

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
* [pycococreator](https://github.com/waspinator/pycococreator) by waspinator, [https://doi.org/10.5281/zenodo.4627206]
