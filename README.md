# Automatic deadwood detection from RGB UAV imagery



`drone_detector`is a python package for automatic deadwood detection or segmentation from RGB UAV imagery. It utilizes [IceVision](https://airctic.com) for object detection and instance segmentation, and [fastai](https://docs.fast.ai) for semantic segmentation. 

## Installation

Use `conda` to create environment from `environment.yml` with

```
conda env create -f environment.yml
```

This will install all otherwise difficult to install dependencies like gdal. At the moment `rtree` conda installation doesn't work properly with python 3.8 or newer, but if you wish to use that then you need to manually install `libspatialindex-dev` to your machine.

 ### Running with Singularity
 
 Use provided `dronecontainer.def` definition file to build Singularity container. Follow instructions on [https://cloud.sylabs.io/builder](https://cloud.sylabs.io/builder) and build the image with
 
 ```
 singularity build --remote dronecontainer.sif dronecontainer.der
 ```

### Running with Docker

TODO

## Usage

`drone_detector` provides several utilities, like tiling raster and vector files into smaller patches with overlap, and untiling them back to a larger tiles.

Examples are added as the package develops.
