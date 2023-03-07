# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_metrics.ipynb.

# %% auto 0
__all__ = ['rrmse', 'bias', 'bias_pct', 'one_error', 'adjusted_R2Score', 'label_ranking_average_precision_score',
           'label_ranking_loss', 'coverage_error', 'JaccardCoeffMulti', 'poly_IoU', 'poly_dice', 'is_true_positive',
           'is_false_positive', 'average_precision', 'average_recall', 'GisCOCOeval']

# %% ../nbs/01_metrics.ipynb 2
from .imports import *
from fastai.learner import Metric
from fastai.torch_core import *
from fastai.metrics import *
from fastai.losses import BaseLoss
import sklearn.metrics as skm
import torch
import torch.nn.functional as F

# %% ../nbs/01_metrics.ipynb 5
mk_class('ActivationType', **{o:o.lower() for o in ['No', 'Sigmoid', 'Softmax', 'BinarySoftmax']},
         doc="All possible activation classes for `AccumMetric")

# %% ../nbs/01_metrics.ipynb 6
def adjusted_R2Score(r2_score, n, k):
    "Calculates adjusted_R2Score based on r2_score, number of observations (n) and number of predictor variables(k)"
    return 1 - (((n-1)/(n-k-1)) * (1 - r2_score))


# %% ../nbs/01_metrics.ipynb 8
def _rrmse(inp, targ):
    "RMSE normalized with mean of the target"
    return torch.sqrt(F.mse_loss(inp, targ)) / targ.mean() * 100

rrmse = AccumMetric(_rrmse)
rrmse.__doc__ = "Relative RMSE. Normalized with mean of the target"

# %% ../nbs/01_metrics.ipynb 10
def _bias(inp, targ):
    "Average bias of predictions"
    inp, targ = flatten_check(inp, targ)
    return (inp - targ).sum() / len(targ)

bias = AccumMetric(_bias)
bias.__doc__ = "Average bias of predictions"

# %% ../nbs/01_metrics.ipynb 12
def _bias_pct(inp, targ):
    "Mean weighted bias"
    inp, targ = flatten_check(inp, targ)
    return 100 * ((inp-targ).sum()/len(targ)) / targ.mean()

bias_pct = AccumMetric(_bias_pct)
bias_pct.__doc__ = 'Mean weighted bias, normalized with mean of the target'

# %% ../nbs/01_metrics.ipynb 15
def label_ranking_average_precision_score(sigmoid=True, sample_weight=None):
    """Label ranking average precision (LRAP) is the average over each ground truth label assigned to each sample, 
    of the ratio of true vs. total labels with lower score."""
    activation = ActivationType.Sigmoid if sigmoid else ActivationType.No
    return skm_to_fastai(skm.label_ranking_average_precision_score, sample_weight=None, flatten=False, thresh=None, 
                         activation=activation)

# %% ../nbs/01_metrics.ipynb 20
def label_ranking_loss(sigmoid=True, sample_weight=None):
    """Compute the average number of label pairs that are incorrectly ordered given y_score 
    weighted by the size of the label set and the number of labels not in the label set."""
    activation = ActivationType.Sigmoid if sigmoid else ActivationType.No
    return skm_to_fastai(skm.label_ranking_loss, sample_weight=None, flatten=False, thresh=None, 
                         activation=activation)

# %% ../nbs/01_metrics.ipynb 22
def _one_error(inp, targ):
    max_ranks = inp.argmax(axis=1)
    faults = 0
    for i in range_of(max_ranks):
        faults += targ[i,max_ranks[i]]
    return 1 - torch.true_divide(faults, len(max_ranks))
    
one_error = AccumMetric(_one_error, flatten=False)
one_error.__doc__ = "Rate for which the top ranked label is not among ground truth"

# %% ../nbs/01_metrics.ipynb 25
def coverage_error(sigmoid=True, sample_weight=None):
    """Compute how far we need to go through the ranked scores to cover all true labels. 
    The best value is equal to the average number of labels in y_true per sample."""
    
    activation = ActivationType.Sigmoid if sigmoid else ActivationType.No
    return skm_to_fastai(skm.coverage_error, sample_weight=None, flatten=False, thresh=None, activation=activation)

# %% ../nbs/01_metrics.ipynb 28
class JaccardCoeffMulti(DiceMulti):
    "Averaged Jaccard coefficient for multiclass target in segmentation. Excludes background class"
    @property
    def value(self):
        binary_jaccard_scores = np.array([])
        for c in self.inter:
            if c > 0:
                binary_jaccard_scores = np.append(binary_jaccard_scores, self.inter[c]/(self.union[c] - self.inter[c]) if self.union[c] > 0 else np.nan)
        return np.nanmean(binary_jaccard_scores)

# %% ../nbs/01_metrics.ipynb 34
def poly_IoU(poly_1:Polygon, poly_2:Polygon) -> float:
    "IoU for polygons"
    area_intersection = poly_1.intersection(poly_2).area
    area_union = poly_1.union(poly_2).area
    iou = area_intersection / area_union
    return iou

# %% ../nbs/01_metrics.ipynb 35
def poly_dice(poly_1:Polygon, poly_2:Polygon):
    "Dice for polygons"
    area_intersection  = poly_1.intersection(poly_2).area
    area_union = poly_1.union(poly_2).area
    return (2 * area_intersection) / (poly_1.area + poly_2.area)

# %% ../nbs/01_metrics.ipynb 36
def is_true_positive(row, results:gpd.GeoDataFrame, res_sindex:gpd.sindex):
    "Check if a single ground truth mask is TP or FN with 11 different IoU thresholds"
    iou_threshs = np.arange(0.5, 1.04, 0.05)
    
    # Matching predictions using spatial index
    c = list(res_sindex.intersection(row.geometry.bounds))
    possible_matches = results.iloc[c].copy()
    
    # No masks -> False negative
    if len(possible_matches) == 0: return ['FN'] * len(iou_threshs)

    possible_matches['iou'] = possible_matches.apply(lambda pred: poly_IoU(pred.geometry, row.geometry), axis=1)
    
    retvals = []
    
    for i, iou_thresh in enumerate(iou_threshs):
        iou_thresh = np.round(iou_thresh, 2)
        possible_matches = possible_matches[possible_matches.iou >= iou_thresh]
        if len(possible_matches) == 0: return retvals + ['FN'] * (len(iou_threshs)-len(retvals))
        
        possible_matches.reset_index(inplace=True, drop=True)
        max_iou_ix = possible_matches['iou'].idxmax()
        max_score_id = possible_matches['score'].idxmax()
        
        if possible_matches.iloc[max_iou_ix].iou < iou_thresh: return ['FN'] * (len(iou_threshs) - len(retvals))
        
        if possible_matches.iloc[max_iou_ix].label != row.label: return ['FN'] * (len(iou_threshs) - len(retvals))
        
        retvals.append('TP')
    return retvals

# %% ../nbs/01_metrics.ipynb 37
def is_false_positive(row, ground_truth:gpd.GeoDataFrame, gt_sindex:gpd.sindex, 
                      results:gpd.GeoDataFrame, res_sindex:gpd.sindex):
    "Check if prediction is FP or TP for 11 different IoU thresholds"
    
    iou_threshs = np.arange(0.5, 1.04, 0.05)
    
    # First find out the matching ground truth masks
    c = list(gt_sindex.intersection(row.geometry.bounds))
    possible_gt_matches = ground_truth.iloc[c].copy()
    #possible_gt_matches = possible_matches[possible_matches.label == row.label].copy()
    possible_gt_matches = possible_gt_matches.loc[possible_gt_matches.intersects(row.geometry)]
    possible_gt_matches.reset_index(inplace=True)
    
    # No ground truth masks -> false positive
    if len(possible_gt_matches) == 0: return ['FP'] * len(iou_threshs)
    
    retvals = []
    
    # Count IoU for all possible_gt_matches
    possible_gt_matches['iou'] = possible_gt_matches.apply(lambda gt: poly_IoU(gt.geometry, row.geometry), axis=1)
    
    # Assume that largest IoU is the corresponding label
    gt_ix = possible_gt_matches['iou'].idxmax()
    
    for i, iou_thresh in enumerate(iou_threshs):
        iou_thresh = np.round(iou_thresh, 2)
        # If IoU-threshold is too low -> false positive
        if possible_gt_matches.iloc[gt_ix].iou < iou_thresh: 
            return retvals + ['FP'] * (len(iou_threshs)-len(retvals))


        # If labels don't match -> false positive:
        if possible_gt_matches.iloc[gt_ix].label != row.label: 
            return retvals + ['FP'] * (len(iou_threshs)-len(retvals))

        # Then check whether there are other predictions
        c = list(res_sindex.intersection(row.geometry.bounds))
        possible_pred_matches = results.iloc[c].copy()

        # Remove examined row from possible_matches. Assume that scores are always different (spoiler: they are not)
        possible_pred_matches = possible_pred_matches[possible_pred_matches.score != row.score]

        # No other possibilities -> not FP
        if len(possible_pred_matches) == 0: 
            retvals.append('TP')
            continue

        possible_pred_matches['iou'] = possible_pred_matches.apply(lambda pred: poly_IoU(pred.geometry, 
                                                                                         possible_gt_matches.iloc[gt_ix].geometry), 
                                                                   axis=1)

        possible_pred_matches = possible_pred_matches[possible_pred_matches.iou > iou_thresh]
        possible_pred_matches.reset_index(inplace=True)

        if len(possible_pred_matches) == 0: 
            retvals.append('TP')
            continue

        pred_max_iou_ix = possible_pred_matches['iou'].idxmax()
        pred_max_score_ix = possible_pred_matches['score'].idxmax()

        # Do any other possible predictions have larger score? If yes -> FP
        if possible_pred_matches.iloc[pred_max_score_ix].score > row.score: 
            return retvals + ['FP'] * (len(iou_threshs)-len(retvals))
        
        retvals.append('TP')
    
    return retvals

# %% ../nbs/01_metrics.ipynb 39
def average_precision(ground_truth:gpd.GeoDataFrame, preds:gpd.GeoDataFrame) -> dict:
    "Get 11-point AP score for each label separately and with all iou_thresholds"
    
    # Clip geodataframes so that they cover the same area
    preds = gpd.clip(preds, box(*ground_truth.total_bounds), keep_geom_type=True)
    ground_truth = gpd.clip(ground_truth, box(*preds.total_bounds), keep_geom_type=True)
    
    gt_sindex = ground_truth.sindex
    pred_sindex = preds.sindex
    fp_cols = [f'FP_{np.round(i, 2)}' for i in np.arange(0.5, 1.04, 0.05)]
    preds[fp_cols] = preds.apply(lambda row: is_false_positive(row, ground_truth, gt_sindex, preds, pred_sindex), 
                                 axis=1, result_type='expand')
    iou_threshs = np.arange(0.5, 1.04, 0.05)
    
    res_dict = {}
    for l in preds.label.unique():
        for iou_thresh in iou_threshs:
            iou_thresh = np.round(iou_thresh, 2)
            res_dict[f'{l}_pre_{iou_thresh}'] = []
            temp_preds = preds[preds.label == l].copy()
            num_correct = len(ground_truth[ground_truth.label == l])
            temp_preds.sort_values(by='score', ascending=False, inplace=True)
            temp_preds.reset_index(inplace=True)
            temp_preds['cumul_TP'] = 0.
            temp_preds['precision'] = 0. 
            temp_preds['recall'] = 0.
            temp_preds.loc[0, 'cumul_TP'] = 0 if temp_preds.loc[0, f'FP_{iou_thresh}'] == 'FP' else 1
            temp_preds.loc[0, 'precision'] = temp_preds.loc[0,'cumul_TP'] / 1
            temp_preds.loc[0, 'recall'] = temp_preds.loc[0,'cumul_TP'] / num_correct
            for i in range(1, len(temp_preds)):
                row_tp = 0 if temp_preds.loc[i, f'FP_{iou_thresh}'] == 'FP' else 1
                temp_preds.loc[i, 'cumul_TP'] = temp_preds.loc[i-1, 'cumul_TP'] + row_tp
                temp_preds.loc[i, 'precision'] = temp_preds.loc[i,'cumul_TP'] / (i+1)
                temp_preds.loc[i, 'recall'] = temp_preds.loc[i,'cumul_TP'] / num_correct
            recall_threshs = np.arange(0,1.04, 0.1)
            for rec_thresh in recall_threshs:
                pre = temp_preds[temp_preds.recall >= rec_thresh].precision.max()
                res_dict[f'{l}_pre_{iou_thresh}'].append(0 if not np.isfinite(pre) else pre)  
    return res_dict

# %% ../nbs/01_metrics.ipynb 40
def average_recall(ground_truth:gpd.GeoDataFrame, preds:gpd.GeoDataFrame, max_detections:int=None) -> dict:
    """Get 11-point AR score for each label separately and with all iou_thresholds. 
    If `max_detections` is not `None` evaluate with only that most confident predictions
    Seems to be still bugged, needs fixing
    """
    
    # Clip geodataframes so that they cover the same area
    preds = gpd.clip(preds, box(*ground_truth.total_bounds), keep_geom_type=True)
    ground_truth = gpd.clip(ground_truth, box(*preds.total_bounds), keep_geom_type=True)
    
    tp_cols = [f'TP_{np.round(i, 2)}' for i in np.arange(0.5, 1.03, 0.05)]
    if max_detections is not None:
        preds.sort_values(by='score', ascending=False, inplace=True)
        preds = preds[:max_detections]
        preds.reset_index(inplace=True)
    pred_sindex = preds.sindex
    ground_truth[tp_cols] = ground_truth.apply(lambda row: is_true_positive(row, preds, pred_sindex), 
                                               axis=1, result_type='expand')
    iou_threshs = np.arange(0.5, 1.04, 0.05)
    res_dict = {}
    for l in ground_truth.label.unique():
        res_dict[f'{l}_rec'] = []
        for iou_thresh in iou_threshs:
            iou_thresh = np.round(iou_thresh, 2)
            temp_gt = ground_truth[ground_truth.label == l].copy()
            res_dict[f'{l}_rec'].append(len(temp_gt[temp_gt[f'TP_{iou_thresh}'] == 'TP']) / len(temp_gt))
    return res_dict

# %% ../nbs/01_metrics.ipynb 43
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from pycocotools.mask import decode
from .processing.coco import *

# %% ../nbs/01_metrics.ipynb 44
class GisCOCOeval():
    
    def __init__(self, data_path:str, outpath:str, coco_info:dict, coco_licenses:list, coco_categories:list):
        "Initialize evaluator with data path and coco information"
        store_attr()
        self.iou_threshs = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
        self.coco_proc = COCOProcessor(data_path=self.data_path, outpath=self.outpath, coco_info=self.coco_info,
                                       coco_licenses=self.coco_licenses, coco_categories=self.coco_categories)
        
    def prepare_data(self, gt_label_col:str='label', res_label_col:str='label', rotated_bbox:bool=False):
        "Convert GIS-data predictions to COCO-format for evaluation, and save resulting files to self.outpath"
        self.coco_proc.from_shp(label_col=gt_label_col, rotated_bbox=rotated_bbox)
        self.coco_proc.to_coco_results(label_col=res_label_col, rotated_bbox=rotated_bbox)
    
    def prepare_eval(self, eval_type:str='segm'):
        """
        Prepare COCOeval to evaluate predictions with 100 and 1000 detections. AP metrics are evaluated with 1000 detections and AR with 100
        """
        self.coco = COCO(f'{self.outpath}/coco.json')
        self.coco_res = self.coco.loadRes(f'{self.outpath}/coco_res.json')
        self.coco_eval = COCOeval(self.coco, self.coco_res, eval_type)
        self.coco_eval.params.maxDets = [100, 1000]
        
    def evaluate(self):
        "Run evaluation and print metrics"
        
        for cat in self.coco_categories:
            print(f'\nEvaluating for category {cat["name"]}')
            self.coco_eval.params.catIds = [cat['id']]
            self.coco_eval.evaluate()
            self.coco_eval.accumulate()
            _summarize_coco(self.coco_eval)
        
        self.coco_eval.params.catIds = self.coco.getCatIds()
        print('\nEvaluating for full data...')

        self.coco_eval.evaluate()
        self.coco_eval.accumulate()
        _summarize_coco(self.coco_eval)
    
    def save_results(self, outpath, iou_thresh:float=0.5):
        """Saves correctly detected ground truths, correct detections missed ground truths and misclassifications with specified iou_threshold in separate files for each scene"""
        
        if not os.path.exists(f'{self.coco_proc.outpath}/{outpath}'):
            os.makedirs(f'{self.coco_proc.outpath}/{outpath}')
            os.makedirs(f'{self.coco_proc.outpath}/{outpath}/cor_gts')
            os.makedirs(f'{self.coco_proc.outpath}/{outpath}/cor_dts')
            os.makedirs(f'{self.coco_proc.outpath}/{outpath}/miss_gts')
            os.makedirs(f'{self.coco_proc.outpath}/{outpath}/miss_dts')
        
        else: 
            print('Output directory exists')
            return
        
        # Index from which get the Iou
        iou_ix = self.iou_threshs.index(iou_thresh)

        im_ids = self.coco.getImgIds()
        cat_ids = self.coco.getCatIds()
        anns = self.coco.anns
        
        cor_gt_res = {'images': self.coco.dataset['images'],
                      'categories': self.coco.cats,
                      'annotations': []}
        
        miss_gt_res = {'images': self.coco.dataset['images'],
                       'categories': self.coco.cats,
                       'annotations': []}
        
        cor_dt_res = {'images': self.coco.dataset['images'],
                      'categories': self.coco.cats,
                      'annotations': []}
        
        miss_dt_res = {'images': self.coco.dataset['images'],
                       'categories': self.coco.cats,
                       'annotations': []}
        
        # self.cocoeval.evalImgs has lenght of 4 * n_images * n_cats, and full results are in the ranges of 
        # [(4*n_images*(cat_id-1)):(4*n_images*(cat_id-1)+9)] 
        
        for im_id, cat_id in tqdm(itertools.product(im_ids, cat_ids)):
            eval_ix = 4*len(im_ids)*(cat_id-1) + im_id
            res_dict = self.coco_eval.evalImgs[eval_ix]
            
            if res_dict is None:
                continue
                
            gt_matches = np.unique(res_dict['dtMatches'][iou_ix]) # Detected ground truth ids in specified iou level
            dt_matches = np.unique(res_dict['gtMatches'][iou_ix]) # Correct detection ids in specified iou level
            gt_matches = gt_matches[gt_matches>0]
            dt_matches = dt_matches[dt_matches>0]
            
            if gt_matches is None:
                gt_matches = []
                
            gt_misses = [i for i in res_dict['gtIds'] if i not in gt_matches] # Missed ground truths
            gt_match_anns = [self.coco.anns[i] for i in gt_matches]
            gt_miss_anns = [self.coco.anns[i] for i in gt_misses]

                
            if dt_matches is None: 
                dt_matches = []
                
            dt_misses = [i for i in res_dict['dtIds'] if i not in dt_matches] # Misdetections
            dt_match_anns = [self.coco_res.anns[i] for i in dt_matches]
            dt_miss_anns = [self.coco_res.anns[i] for i in dt_misses]
            
        
            for a in gt_match_anns:
                ann = a.copy()
                ann['segmentation'] = binary_mask_to_polygon(decode(a['segmentation']))
                cor_gt_res['annotations'].append(ann)
                
            for a in dt_match_anns:
                ann = a.copy()
                ann['segmentation'] = binary_mask_to_polygon(decode(a['segmentation']))
                cor_dt_res['annotations'].append(ann)
                
            for a in gt_miss_anns:
                ann = a.copy()
                ann['segmentation'] = binary_mask_to_polygon(decode(a['segmentation']))
                miss_gt_res['annotations'].append(ann)
                
            for a in dt_miss_anns:
                ann = a.copy()
                ann['segmentation'] = binary_mask_to_polygon(decode(a['segmentation']))
                miss_dt_res['annotations'].append(ann)
               
        self.coco_proc.coco_to_shp(cor_gt_res, f'{outpath}/cor_gts/')
        self.coco_proc.coco_to_shp(cor_dt_res, f'{outpath}/cor_dts/')
        self.coco_proc.coco_to_shp(miss_gt_res, f'{outpath}/miss_gts/')
        self.coco_proc.coco_to_shp(miss_dt_res, f'{outpath}/miss_dts/')
    
def _summarize_coco(cocoeval:COCOeval): 
    """
    Compute and display summary metrics for evaluation results.
    Note this functin can *only* be applied on the default parameter setting
    """
    def _summarize(ap=1, iouThr=None, areaRng='all', maxDets=100):
        p = cocoeval.params
        iStr = ' {:<18} {} @[ IoU={:<9} | area={:>6s} | maxDets={:>3d} ] = {:0.3f}'
        titleStr = 'Average Precision' if ap == 1 else 'Average Recall'
        typeStr = '(AP)' if ap==1 else '(AR)'
        iouStr = '{:0.2f}:{:0.2f}'.format(p.iouThrs[0], p.iouThrs[-1]) \
            if iouThr is None else '{:0.2f}'.format(iouThr)

        aind = [i for i, aRng in enumerate(p.areaRngLbl) if aRng == areaRng]
        mind = [i for i, mDet in enumerate(p.maxDets) if mDet == maxDets]
        if ap == 1:
            # dimension of precision: [TxRxKxAxM]
            s = cocoeval.eval['precision']
            # IoU
            if iouThr is not None:
                t = np.where(iouThr == p.iouThrs)[0]
                s = s[t]
            s = s[:,:,:,aind,mind]
        else:
            # dimension of recall: [TxKxAxM]
            s = cocoeval.eval['recall']
            if iouThr is not None:
                t = np.where(iouThr == p.iouThrs)[0]
                s = s[t]
            s = s[:,:,aind,mind]
        if len(s[s>-1])==0:
            mean_s = -1
        else:
            mean_s = np.mean(s[s>-1])
        print(iStr.format(titleStr, typeStr, iouStr, areaRng, maxDets, mean_s))
        return mean_s
    
    def _summarizeDets():
        stats = np.zeros((12,))
        stats[0] = _summarize(1, maxDets=cocoeval.params.maxDets[1])
        stats[1] = _summarize(1, iouThr=.5, maxDets=cocoeval.params.maxDets[1])
        stats[2] = _summarize(1, iouThr=.75, maxDets=cocoeval.params.maxDets[1])
        stats[3] = _summarize(1, areaRng='small', maxDets=cocoeval.params.maxDets[1])
        stats[4] = _summarize(1, areaRng='medium', maxDets=cocoeval.params.maxDets[1])
        stats[5] = _summarize(1, areaRng='large', maxDets=cocoeval.params.maxDets[1])
        stats[6] = _summarize(0, maxDets=cocoeval.params.maxDets[0])
        stats[9] = _summarize(0, areaRng='small', maxDets=cocoeval.params.maxDets[0])
        stats[10] = _summarize(0, areaRng='medium', maxDets=cocoeval.params.maxDets[0])
        stats[11] = _summarize(0, areaRng='large', maxDets=cocoeval.params.maxDets[0])
        return stats
    
    def _summarizeKps():
        stats = np.zeros((10,))
        stats[0] = _summarize(1, maxDets=20)
        stats[1] = _summarize(1, maxDets=20, iouThr=.5)
        stats[2] = _summarize(1, maxDets=20, iouThr=.75)
        stats[3] = _summarize(1, maxDets=20, areaRng='medium')
        stats[4] = _summarize(1, maxDets=20, areaRng='large')
        stats[5] = _summarize(0, maxDets=20)
        stats[6] = _summarize(0, maxDets=20, iouThr=.5)
        stats[7] = _summarize(0, maxDets=20, iouThr=.75)
        stats[8] = _summarize(0, maxDets=20, areaRng='medium')
        stats[9] = _summarize(0, maxDets=20, areaRng='large')
        return stats
    
    if not cocoeval.eval:
        raise Exception('Please run accumulate() first')
        
    iouType = cocoeval.params.iouType
    
    if iouType == 'segm' or iouType == 'bbox':
        summarize = _summarizeDets
    elif iouType == 'keypoints':
        summarize = _summarizeKps
    cocoeval.stats = summarize()
