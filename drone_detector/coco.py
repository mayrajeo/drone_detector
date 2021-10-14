# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_coco.ipynb (unless otherwise specified).

__all__ = ['resize_binary_mask', 'close_contour', 'binary_mask_to_polygon', 'COCOProcessor', 'mask_preds_to_coco_anns',
           'bbox_preds_to_coco_anns']

# Cell
from .imports import *
from .utils import *
from .coordinates import *

# Cell
from .coordinates import *
from .utils import *

import datetime
from skimage import measure
from PIL import Image

# Cell
# From https://github.com/waspinator/pycococreator/blob/master/pycococreatortools/pycococreatortools.py

def resize_binary_mask(array, new_size):
    image = Image.fromarray(array.astype(np.uint8)*255)
    image = image.resize(new_size)
    return np.asarray(image).astype(np.bool_)

def close_contour(contour):
    if not np.array_equal(contour[0], contour[-1]):
        contour = np.vstack((contour, contour[0]))
    return contour

def binary_mask_to_polygon(binary_mask, tolerance=0):
    """Converts a binary mask to COCO polygon representation
    Args:
        binary_mask: a 2D binary numpy array where '1's represent the object
        tolerance: Maximum distance from original points of polygon to approximated
            polygonal chain. If tolerance is 0, the original coordinate array is returned.
    """
    polygons = []
    # pad mask to close contours of shapes which start and end at an edge
    padded_binary_mask = np.pad(binary_mask, pad_width=1, mode='constant', constant_values=0)
    contours = measure.find_contours(padded_binary_mask, 0.5)
    contours = np.subtract(contours, 1)
    for contour in contours:
        contour = close_contour(contour)
        contour = measure.approximate_polygon(contour, tolerance)
        if len(contour) < 3:
            continue
        contour = np.flip(contour, axis=1)
        segmentation = contour.ravel().tolist()
        # after padding and subtracting 1 we may get -0.5 points in our segmentation
        segmentation = [0 if i < 0 else i for i in segmentation]
        polygons.append(segmentation)

    return polygons

# Cell

from pycocotools.mask import frPyObjects

class COCOProcessor():
    "Handles Transformations from shapefiles to COCO-format and backwards"

    def __init__(self, data_path:str, outpath:str, coco_info:dict, coco_licenses:list,
                 coco_categories:list):
        store_attr()
        self.raster_path = f'{self.data_path}/raster_tiles'
        self.vector_path = f'{self.data_path}/vector_tiles'
        self.prediction_path = f'{self.data_path}/predicted_vectors'

        self.coco_dict = {
            'info': coco_info,
            'licenses': coco_licenses,
            'images': [],
            'annotations': [],
            'categories': coco_categories,
            'segment_info': []
        }
        self.categories = {c['name']:c['id'] for c in self.coco_dict['categories']}


    def shp_to_coco(self, label_col:str='label', outfile:str='coco.json'):
        "Process shapefiles from self.vector_path to coco-format and save to self.outpath/outfile"
        vector_tiles = [f for f in os.listdir(self.vector_path) if f.endswith(('.shp', '.geojson'))]
        # If no annotations are in found in raster tile then there is no shapefile for that
        raster_tiles = [f'{fname.split(".")[0]}.tif' for fname in vector_tiles]
        for i, r in enumerate(raster_tiles):
            with rio.open(f'{self.raster_path}/{r}') as im:
                h, w = im.shape
            self.coco_dict['images'].append({'file_name': raster_tiles[i],'id': i, 'height':h, 'width':w})
        ann_id = 1
        for i in tqdm(rangeof(raster_tiles)):
            gdf = gpd.read_file(f'{self.vector_path}/{vector_tiles[i]}')
            tfmd_gdf = gdf_to_px(gdf, f'{self.raster_path}/{raster_tiles[i]}', precision=None)
            for row in tfmd_gdf.itertuples():
                category_id = self.categories[getattr(row, label_col)]
                self.coco_dict['annotations'].append(_process_shp_to_coco(i, category_id, ann_id, row.geometry))
                ann_id += 1
        with open(f'{self.outpath}/{outfile}', 'w') as f: json.dump(self.coco_dict, f)

        return

    def coco_to_shp(self, coco_data:dict=None, outdir:str='predicted_vectors'):
        """Generates shapefiles from a dictionary with coco annotations.
        TODO handle multipolygons better"""

        if not os.path.exists(f'{self.outpath}/{outdir}'): os.makedirs(f'{self.outpath}/{outdir}')
        #if coco_path is None: coco_path = f'{self.outpath}/coco.json'
        #with open(coco_path) as f:
        #    coco_data = json.load(f)

        annotations = coco_data['annotations']
        images = coco_data['images']
        categories = coco_data['categories']
        for i in tqdm(images):
            anns_in_image = [a for a in annotations if a['image_id'] == i['id']]
            if len(anns_in_image) == 0: continue
            cats = []
            polys = []
            scores = []
            for a in anns_in_image:
                # No segmentations, only bounding boxes
                if a['segmentation'] is None:
                    cats.append(a['category_id'])
                    # Bbox has format xmin, ymin, xdelta, ydelta
                    polys.append(box(a['bbox'][0], a['bbox'][1], a['bbox'][2] + a['bbox'][0], a['bbox'][3]+a['bbox'][1]))
                    if 'score' in a.keys():
                        scores.append(a['score'])
                # Single polygon
                elif len(a['segmentation']) == 1:
                    cats.append(a['category_id'])
                    xy_coords = [(a['segmentation'][0][i], a['segmentation'][0][i+1])
                                 for i in range(0,len(a['segmentation'][0]),2)]
                    xy_coords.append(xy_coords[-1])
                    polys.append(Polygon(xy_coords))
                    if 'score' in a.keys():
                        scores.append(a['score'])
                # Multipolygon
                else:
                    for p in rangeof(a['segmentation']):
                        cats.append(a['category_id'])
                        xy_coords = [(a['segmentation'][p][i], a['segmentation'][p][i+1])
                                     for i in range(0,len(a['segmentation'][p]),2)]
                        xy_coords.append(xy_coords[-1])
                        polys.append(Polygon(xy_coords))
                        if 'score' in a.keys():
                            scores.append(a['score'])

            gdf = gpd.GeoDataFrame({'label':cats, 'geometry':polys})
            if len(scores) != 0: gdf['score'] = scores
            tfmd_gdf = georegister_px_df(gdf, f'{self.raster_path}/{i["file_name"]}')
            tfmd_gdf.to_file(f'{self.outpath}/{outdir}/{i["file_name"][:-4]}.geojson', driver='GeoJSON')
        return

    def results_to_coco_res(self, label_col:str='label_id', outfile:str='coco_res.json'):
        result_tiles = [f for f in os.listdir(self.prediction_path) if f.endswith(('.shp', '.geojson'))]
        # If no annotations are in found in raster tile then there is no shapefile for that
        raster_tiles = [f'{fname.split(".")[0]}.tif' for fname in result_tiles]
        results = []
        for i in tqdm(rangeof(raster_tiles)):
            for im_id, im in enumerate(self.coco_dict['images']):
                if im['file_name'] == raster_tiles[i]:
                    break
            image_id = self.coco_dict['images'][im_id]['id']
            h = self.coco_dict['images'][im_id]['height']
            w = self.coco_dict['images'][im_id]['width']
            gdf = gpd.read_file(f'{self.prediction_path}/{result_tiles[i]}')
            tfmd_gdf = gdf_to_px(gdf, f'{self.raster_path}/{raster_tiles[i]}', precision=None)
            for row in tfmd_gdf.itertuples():
                res = {'image_id': image_id,
                       'category_id': getattr(row, label_col),
                       'segmentation': None,
                       'score': np.round(getattr(row, 'score'), 5)}
                ann = _process_shp_to_coco(image_id, getattr(row, label_col), 0, row.geometry)
                res['segmentation'] = frPyObjects(ann['segmentation'], h, w)[0]
                res['segmentation']['counts'] = res['segmentation']['counts'].decode('ascii')
                results.append(res)

        with open(f'{self.outpath}/{outfile}', 'w') as f:
            json.dump(results, f)

def mask_preds_to_coco_anns(preds:list) -> dict:
    """Process list of IceVision `samples` and `preds` to COCO-annotation polygon format.
    Returns a dict with Coco-style `images` and `annotations`

    TODO replace these with functions from icevision somehow"""
    outdict = {}
    outdict['annotations'] = []
    outdict['images'] = [{'file_name': str(f'{p.ground_truth.filepath.stem}{p.ground_truth.filepath.suffix}'), 'id': p.record_id} for p in preds]
    anns = []
    for i, p in tqdm(enumerate(preds)):
        for j in rangeof(p.pred.detection.label_ids):
            anns = []
            ann_dict = {
                'segmentation': binary_mask_to_polygon(p.pred.detection.mask_array.to_mask(p.height,p.width).data[j]),
                'area': None,
                'iscrowd': 0,
                'category_id': p.pred.detection.label_ids[j].item(),
                'id': i,
                'image_id': p.record_id,
                'bbox': [p.pred.detection.bboxes[j].xmin.item(),
                         p.pred.detection.bboxes[j].ymin.item(),
                         p.pred.detection.bboxes[j].xmax.item() - p.pred.detection.bboxes[j].xmin.item(),
                         p.pred.detection.bboxes[j].ymax.item() - p.pred.detection.bboxes[j].ymin.item()],
                'score': p.pred.detection.scores[j]
            }


            anns.append(ann_dict)
            outdict['annotations'].extend(anns)

    return outdict

def bbox_preds_to_coco_anns(preds:list) -> dict:
    """Process list of IceVision `samples` and `preds` to COCO-annotation polygon format.
    Returns a dict with Coco-style `images` and `annotations`"""
    outdict = {}
    outdict['annotations'] = []
    outdict['images'] = [{'file_name': str(f'{p.ground_truth.filepath.stem}{p.ground_truth.filepath.suffix}'), 'id': p.record_id} for p in preds]

    anns = []
    for i, p in tqdm(enumerate(preds)):
        for j in rangeof(p.pred.detection.bboxes):
            anns = []
            ann_dict = {
                'segmentation': None,
                'area': None,
                'iscrowd': 0,
                'category_id': p.pred.detection.label_ids[j].item(),
                'id': i,
                'image_id': p.record_id,
                'bbox': [p.pred.detection.bboxes[j].xmin.item(),
                         p.pred.detection.bboxes[j].ymin.item(),
                         p.pred.detection.bboxes[j].xmax.item() - p.pred.detection.bboxes[j].xmin.item(),
                         p.pred.detection.bboxes[j].ymax.item() - p.pred.detection.bboxes[j].ymin.item()],
                'score': p.pred.detection.scores[j]
            }

            anns.append(ann_dict)
            outdict['annotations'].extend(anns)

    return outdict


def _process_shp_to_coco(image_id, category_id, ann_id, poly:Polygon):
    "TODO handle multipolygons"
    ann_dict = {
        'segmentation': [],
        'area': None,
        'bbox': [],
        'category_id': category_id,
        'id' : ann_id,
        'image_id': image_id,
        'iscrowd': 0,
    }
    ann_dict['bbox'] = [(poly.bounds[0]),
                        (poly.bounds[1]),
                        (poly.bounds[2]-poly.bounds[0]),
                        (poly.bounds[3]-poly.bounds[1])]
    ann_dict['area'] = poly.area
    if poly.type == 'Polygon':
        ann_dict['segmentation'] = [list(sum(poly.exterior.coords[:-1], ()))]
    elif poly.type == 'MultiPolygon':
        ann_dict['segmentation'] = [list(sum(p.exterior.coords[:-1], ())) for p in list(poly)]
    return ann_dict
