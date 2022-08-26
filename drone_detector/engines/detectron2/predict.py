# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../nbs/40_engines.detectron2.predict.ipynb.

# %% auto 0
__all__ = ['predict_bboxes', 'predict_bboxes_detectron2', 'predict_instance_masks', 'predict_instance_masks_detectron2']

# %% ../../../nbs/40_engines.detectron2.predict.ipynb 2
from ...imports import *
from ...processing.all import *
from .tta import *
from ...metrics import *
from ...utils import *

import detectron2
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
import cv2
import torch
from shutil import rmtree

from fastcore.foundation import *
from fastcore.script import *

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# %% ../../../nbs/40_engines.detectron2.predict.ipynb 3
def predict_bboxes(path_to_model_files:str,
                   path_to_image:str,
                   outfile:str,
                   processing_dir:str='temp',
                   tile_size:int=400,
                   tile_overlap:int=100,
                   coco_set:str=None,
                   use_tta:bool=True,
                   postproc_results:bool=True):
    "Detect bounding boxes from a new image using a pretrained model"
    
    if os.path.exists(processing_dir): 
        print('Processing folder exists')
        return
    os.makedirs(processing_dir)
    print(f'Reading and tiling {path_to_image} to {tile_size}x{tile_size} tiles with overlap of {tile_overlap}px')
    tiler = Tiler(outpath=processing_dir, gridsize_x=int(tile_size), gridsize_y=int(tile_size), 
                  overlap=(int(tile_overlap), int(tile_overlap)))
    tiler.tile_raster(path_to_image)
    
    # Check whether is possible to use gpu
    device = 'cpu' if not torch.cuda.is_available() else f'cuda:{torch.cuda.current_device()}'
    
        # Loading pretrained model
    print('Loading model')
    
    cfg = get_cfg()
    cfg.merge_from_file(f'{path_to_model_files}/config.yaml')
    cfg.DEVICE = device
    
    print('Starting predictions')
    image_files = os.listdir(f'{processing_dir}/raster_tiles')
    #else:
    
    cfg.MODEL.WEIGHTS = os.path.join(path_to_model_files, 'model_final.pth')
    predictor = DefaultPredictor(cfg)    
    if use_tta:
        cfg.TEST.AUG.MIN_SIZES = (cfg.INPUT.MIN_SIZE_TEST-200, cfg.INPUT.MIN_SIZE_TEST, cfg.INPUT.MIN_SIZE_TEST+200,)
        predictor = TTAPredictor(cfg)
    images = []
    preds = []

    for i in tqdm(rangeof(image_files)):
        img = cv2.imread(f'{processing_dir}/raster_tiles/{image_files[i]}')
        pred = predictor(img)
        images.append({'file_name': image_files[i],
                       'width': img.shape[0],
                       'height': img.shape[0],
                       'id': i+1})
        preds.append(pred)
        
    preds_coco = detectron2_bbox_preds_to_coco_anns(images, preds)
    try:
        with open(coco_set) as coco:
            cats = json.load(coco)['categories']
    except:
        print('No categories found, defaulting to dummy classes')
        cats = [{'supercategory': 'dummy', 'id':i+1, 'name': f'class_{i+1}'}
                for i in range(cfg.ROI_HEADS.NUM_CLASSES)]
            
                        
    # Process preds to shapefiles
    coco_proc = COCOProcessor(data_path=processing_dir, 
                              outpath=processing_dir,
                              coco_info=None, coco_licenses=None,
                              coco_categories=cats)
    preds_coco['categories'] = cats
    
    coco_proc.coco_to_shp(preds_coco, downsample_factor=1)
    
    if postproc_results:
        # Drop all polygons whose centroid is not within thresholded cell.
        # Thresholded cell is constructed by eroding it by half the overlap area.
        grid = tiler.grid
        grid = grid.to_crs('EPSG:3067')
        num_polys = 0
        for cell in grid.itertuples():
            if not os.path.isfile(f'{processing_dir}/predicted_vectors/{cell.cell}.geojson'): continue
            pred_shp = gpd.read_file(f'{processing_dir}/predicted_vectors/{cell.cell}.geojson')
            num_polys += len(pred_shp)
            orig_crs = pred_shp.crs
            pred_shp = pred_shp.to_crs('EPSG:3067')
            cell_px = (cell.geometry.bounds[2] - cell.geometry.bounds[0]) / tile_size
            cell_geom = cell.geometry.buffer(-(cell_px * tile_overlap/2)) 
            pred_shp['to_drop'] = pred_shp.apply(lambda row: 0 if row.geometry.centroid.within(cell_geom) else 1, axis=1)
            pred_shp = pred_shp[pred_shp.to_drop == 0]
            pred_shp = pred_shp.to_crs(orig_crs)
            pred_shp.drop(columns=['to_drop'], inplace=True)
            if len(pred_shp) > 0: pred_shp.to_file(f'{processing_dir}/predicted_vectors/{cell.cell}.geojson')
            else: os.remove(f'{processing_dir}/predicted_vectors/{cell.cell}.geojson')

        # Collate shapefiles
        print(f'{num_polys} polygons before edge area removal')
    # Collate shapefiles
    untile_vector(path_to_targets=f'{processing_dir}/predicted_vectors', outpath=outfile)
    
    print('Removing intermediate files')
    rmtree(processing_dir)
    return

# %% ../../../nbs/40_engines.detectron2.predict.ipynb 4
@call_parse
def predict_bboxes_detectron2(path_to_model_files:str, #Path to the folder containing config and weights
                              path_to_image:str, #Path to image to annotate
                              outfile:str, #Path and filename for output raster
                              processing_dir:str='temp', #Directory to save the intermediate tiles. Deleted after use.
                              tile_size:int=400, #Tile size to use. Default 400x400px tiles
                              tile_overlap:int=100, #Tile overlap to use. Default 100px
                              coco_set:str=None, #Path to json file for the coco dataset the model was trained on. None defaults to dummy classes
                              use_tta:bool=False, #Use test-time augmentation? 
                              postproc_results:bool=False): #Filter predicted masks
                             
    "CLI for bbox prediction with detectron2"
    predict_bboxes(path_to_model_files,
                   path_to_image,
                   outfile,
                   processing_dir,
                   tile_size,
                   tile_overlap,
                   use_tta,
                   postproc_results,
                   smooth_preds)

# %% ../../../nbs/40_engines.detectron2.predict.ipynb 5
def predict_instance_masks(path_to_model_files:str,
                           path_to_image:str,
                           outfile:str,
                           processing_dir:str='temp',
                           tile_size:int=400,
                           tile_overlap:int=100,
                           coco_set:str=None,
                           use_tta:bool=False,
                           postproc_results:bool=False,
                           smooth_preds:bool=False):
    "Segment instance masks from a new image using a pretrained model"
    
    if os.path.exists(processing_dir): 
        print('Processing folder exists')
        return
    os.makedirs(processing_dir)
    print(f'Reading and tiling {path_to_image} to {tile_size}x{tile_size} tiles with overlap of {tile_overlap}px')
    tiler = Tiler(outpath=processing_dir, gridsize_x=int(tile_size), gridsize_y=int(tile_size), 
                  overlap=(int(tile_overlap), int(tile_overlap)))
    tiler.tile_raster(path_to_image)
    
    # Check whether is possible to use gpu
    device = 'cpu' if not torch.cuda.is_available() else f'cuda:{torch.cuda.current_device()}'
    
        # Loading pretrained model
    print('Loading model')
    
    cfg = get_cfg()
    cfg.merge_from_file(f'{path_to_model_files}/config.yaml')
    cfg.DEVICE = device
    
    print('Starting predictions')
    image_files = os.listdir(f'{processing_dir}/raster_tiles')
    
    cfg.MODEL.WEIGHTS = os.path.join(path_to_model_files, 'model_final.pth')
    predictor = DefaultPredictor(cfg)    
    if use_tta:
        cfg.TEST.AUG.MIN_SIZES = (cfg.INPUT.MIN_SIZE_TEST-200, cfg.INPUT.MIN_SIZE_TEST, cfg.INPUT.MIN_SIZE_TEST+200,)
        predictor = TTAPredictor(cfg)
    images = []
    preds = []

    for i in tqdm(rangeof(image_files)):
        img = cv2.imread(f'{processing_dir}/raster_tiles/{image_files[i]}')
        pred = predictor(img)
        images.append({'file_name': image_files[i],
                       'width': img.shape[0],
                       'height': img.shape[0],
                       'id': i+1})
        preds.append(pred)

    # Mask postprocessing:
    if smooth_preds:
        print('Not yet implemented')
        #preds = fill_holes(preds)
        #preds = dilate_erode(preds)
        
    preds_coco = detectron2_mask_preds_to_coco_anns(images, preds)
    try:
        with open(coco_set) as coco:
            cats = json.load(coco)['categories']
    except:
        print('No categories found, defaulting to dummy classes')
        cats = [{'supercategory': 'dummy', 'id':i+1, 'name': f'class_{i+1}'}
                for i in range(cfg.ROI_HEADS.NUM_CLASSES)] 

    # Process preds to shapefiles
    coco_proc = COCOProcessor(data_path=processing_dir, 
                              outpath=processing_dir,
                              coco_info=None, coco_licenses=None,
                              coco_categories=cats)
    
    preds_coco['categories'] = cats
    coco_proc.coco_to_shp(preds_coco, downsample_factor=1)
    
    if postproc_results:
        # Drop all polygons whose centroid is not within thresholded cell.
        # Thresholded cell is constructed by eroding it by half the overlap area.
        grid = tiler.grid
        grid = grid.to_crs('EPSG:3067')
        num_polys = 0
        for cell in grid.itertuples():
            if not os.path.isfile(f'{processing_dir}/predicted_vectors/{cell.cell}.geojson'): continue
            pred_shp = gpd.read_file(f'{processing_dir}/predicted_vectors/{cell.cell}.geojson')
            num_polys += len(pred_shp)
            orig_crs = pred_shp.crs
            pred_shp = pred_shp.to_crs('EPSG:3067')
            cell_px = (cell.geometry.bounds[2] - cell.geometry.bounds[0]) / tile_size
            cell_geom = cell.geometry.buffer(-(cell_px * tile_overlap/2)) 
            pred_shp['to_drop'] = pred_shp.apply(lambda row: 0 if row.geometry.centroid.within(cell_geom) else 1, axis=1)
            pred_shp = pred_shp[pred_shp.to_drop == 0]
            pred_shp = pred_shp.to_crs(orig_crs)
            pred_shp.drop(columns=['to_drop'], inplace=True)
            if len(pred_shp) > 0: pred_shp.to_file(f'{processing_dir}/predicted_vectors/{cell.cell}.geojson')
            else: os.remove(f'{processing_dir}/predicted_vectors/{cell.cell}.geojson')

        # Collate shapefiles
        print(f'{num_polys} polygons before edge area removal')
    untile_vector(path_to_targets=f'{processing_dir}/predicted_vectors', outpath=outfile)
    
    print('Removing intermediate files')
    rmtree(processing_dir)
    return

# %% ../../../nbs/40_engines.detectron2.predict.ipynb 6
@call_parse
def predict_instance_masks_detectron2(path_to_model_files:str, #Path to the folder containing config and weights
                                      path_to_image:str, #Path to image to annotate
                                      outfile:str, #Path and filename for output raster
                                      processing_dir:str='temp', #Directory to save the intermediate tiles. Deleted after use
                                      tile_size:int=400, #Tile size to use. Default 400x400px tiles
                                      tile_overlap:int=100, #Tile overlap to use. Default 100px
                                      coco_set:str=None, #Path to json file for the coco dataset the model was trained on. None defaults to dummy classes
                                      use_tta:bool=False, #Use test-time augmentation? 
                                      postproc_results:bool=False, #Filter predicted masks
                                      smooth_preds:bool=False): #Run fill_holes and dilate_erode to masks. Not implemented yet
                                     
    "CLI for instance segmentation with detectron2"
    predict_instance_masks(path_to_model_files,
                           path_to_image,
                           outfile,
                           processing_dir,
                           tile_size,
                           tile_overlap,
                           coco_set,
                           use_tta,
                           postproc_results,
                           smooth_preds)
