# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/33_engines.fastai.predict.ipynb (unless otherwise specified).

__all__ = ['predict_segmentation_fastai']

# Cell
from ...imports import *
from ...processing.all import *
from ...metrics import *
from .losses import *

from fastcore.foundation import *
from fastcore.script import *

from fastai.vision.all import *
from fastai.learner import load_learner, Learner
from shutil import rmtree
from fastai.data.load import DataLoader
from fastcore.transform import Pipeline

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Cell

@patch
def remove(self:Pipeline, t):
    "Remove an instance of `t` from `self` if present"
    for i,o in enumerate(self.fs):
        if isinstance(o, t.__class__): self.fs.pop(i)
@patch
def set_base_transforms(self:DataLoader):
    "Removes all transforms with a `size` parameter"
    attrs = ['after_item', 'after_batch']
    for i, attr in enumerate(attrs):
        tfms = getattr(self, attr)
        for j, o in enumerate(tfms):
            if hasattr(o, 'size'):
                tfms.remove(o)
        setattr(self, attr, tfms)

# Cell

@call_parse
def predict_segmentation_fastai(path_to_model:Param("Path to pretrained model file",type=str),
                               path_to_image:Param("Path to image to annotate", type=str),
                               outfile:Param('Path and filename for output raster', type=str),
                               processing_dir:Param("Directory to save the intermediate tiles. Deleted after use", type=str, default='temp'),
                               tile_size:Param("Tile size to use. Default 400x400px tiles", type=int, default=400),
                               tile_overlap:Param("Tile overlap to use. Default 100px", type=int, default=200),
                               use_tta:Param("Use test-time augmentation", store_true)=None
    ):
    """Segment image into land cover classes with a pretrained models
    TODO save also information about label and class
    TODO add test-time augmentations"""
    if os.path.exists(processing_dir):
        print('Processing folder exists')
        return
    os.makedirs(processing_dir)
    print(f'Reading and tiling {path_to_image} to {tile_size}x{tile_size} tiles with overlap of {tile_overlap}px')
    tiler = Tiler(outpath=processing_dir, gridsize_x=int(tile_size), gridsize_y=int(tile_size),
                  overlap=(int(tile_overlap), int(tile_overlap)))
    tiler.tile_raster(path_to_image)

    # Check whether is possible to use gpu
    cpu = True if not torch.cuda.is_available() else False

    # Loading pretrained model

    # PyTorch state dict TODO
    if path_to_model.endswith('.pth') or path_to_model.endswith('.pt'):
        print('Using PyTorch state dict not yet supported')
        print('Removing intermediate files')
        rmtree(processing_dir)
        return
    # fastai learn.export()
    elif path_to_model.endswith('.pkl'):
        learn = load_learner(path_to_model, cpu=cpu)
        test_files = get_image_files(f'{processing_dir}/raster_tiles')
        print('Starting prediction')
        os.makedirs(f'{processing_dir}/predicted_rasters')
        # Works with chunks of 300 patches
        for chunk in range(0, len(test_files), 300):
            test_dl = learn.dls.test_dl(test_files[chunk:chunk+300], num_workers=0, bs=1)
            test_dl.set_base_transforms()
            if use_tta:
                batch_tfms = [Dihedral()]
                item_tfms = [ToTensor(), IntToFloatTensor()]
                preds = learn.tta(dl=test_dl, batch_tfms=batch_tfms)[0]
            else:
                preds = learn.get_preds(dl=test_dl, with_input=False, with_decoded=False)[0]

            print('Rasterizing predictions')
            for f, p in tqdm(zip(test_files[chunk:chunk+300], preds)):
                #if len(p.shape) == 3: p = p[0]
                ds = gdal.Open(str(f))
                out_raster = gdal.GetDriverByName('gtiff').Create(f'{processing_dir}/predicted_rasters/{f.stem}.{f.suffix}',
                                                                  ds.RasterXSize,
                                                                  ds.RasterYSize,
                                                                  p.shape[0], gdal.GDT_Int16)
                out_raster.SetProjection(ds.GetProjectionRef())
                out_raster.SetGeoTransform(ds.GetGeoTransform())
                np_pred = p.numpy()#.argmax(axis=0)
                np_pred = np_pred.round(2)
                np_pred *= 100
                np_pred = np_pred.astype(np.int16)
                for c in range(p.shape[0]):
                    band = out_raster.GetRasterBand(c+1).WriteArray(np_pred[c])
                    band = None
                #band = out_raster.GetRasterBand(1).WriteArray(np_pred)
                out_raster = None
                ds = None

    print('Merging predictions')
    temp_full = f'{processing_dir}/full_raster.tif'
    untile_raster(f'{processing_dir}/predicted_rasters', outfile=temp_full, method='sum')

    print('Postprocessing predictions')

    raw_raster = gdal.Open(temp_full)
    processed_raster = gdal.GetDriverByName('gtiff').Create(outfile,
                                                            raw_raster.RasterXSize,
                                                            raw_raster.RasterYSize,
                                                            1, gdal.GDT_Int16)
    processed_raster.SetProjection(raw_raster.GetProjectionRef())
    processed_raster.SetGeoTransform(raw_raster.GetGeoTransform())
    raw_np = raw_raster.ReadAsArray()
    pred_np = raw_np.argmax(axis=0)
    band = processed_raster.GetRasterBand(1).WriteArray(pred_np)
    raw_raster = None
    band = None
    processed_raster = None

    print('Removing intermediate files')
    rmtree(processing_dir)
    return