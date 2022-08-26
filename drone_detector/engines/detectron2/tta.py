# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../nbs/43_engines.detectron2.tta.ipynb.

# %% auto 0
__all__ = ['DatasetMapperTTAFlip', 'TTAPredictor']

# %% ../../../nbs/43_engines.detectron2.tta.ipynb 2
from detectron2.data.transforms import RandomFlip, ResizeShortestEdge, ResizeTransform, apply_augmentations 
from detectron2.config import configurable
from copy import deepcopy
from fvcore.transforms import VFlipTransform, HFlipTransform, NoOpTransform
from detectron2.modeling import GeneralizedRCNNWithTTA, build_model
from detectron2.data import MetadataCatalog
from detectron2.checkpoint import DetectionCheckpointer
import torch
from ...imports import *

from detectron2.modeling.roi_heads.rotated_fast_rcnn import fast_rcnn_inference_single_image_rotated
from detectron2.modeling.roi_heads.fast_rcnn import fast_rcnn_inference_single_image
from detectron2.structures import Boxes, Instances

from itertools import count

# %% ../../../nbs/43_engines.detectron2.tta.ipynb 3
class DatasetMapperTTAFlip:
    """
    Implement test-time augmentation for detection data. Modified to implement both horizontal and vertical flip
    It is a callable which takes a dataset dict from a detection dataset,
    and returns a list of dataset dicts where the images
    are augmented from the input image by the transformations defined in the config.
    This is used for test-time augmentation.
    """

    @configurable
    def __init__(self, min_sizes: List[int], max_size: int, flip: bool):
        """
        Args:
            min_sizes: list of short-edge size to resize the image to
            max_size: maximum height or width of resized images
            flip: whether to apply flipping augmentation
        """
        self.min_sizes = min_sizes
        self.max_size = max_size
        self.flip = flip

    @classmethod
    def from_config(cls, cfg):
        return {
            "min_sizes": cfg.TEST.AUG.MIN_SIZES,
            "max_size": cfg.TEST.AUG.MAX_SIZE,
            "flip": cfg.TEST.AUG.FLIP,
        }

    def __call__(self, dataset_dict):
        """
        Args:
            dict: a dict in standard model input format. See tutorials for details.
        Returns:
            list[dict]:
                a list of dicts, which contain augmented version of the input image.
                The total number of dicts is ``len(min_sizes) * (2 if flip else 1)``.
                Each dict has field "transforms" which is a TransformList,
                containing the transforms that are used to generate this image.
        """
        numpy_image = dataset_dict["image"].permute(1, 2, 0).numpy()
        shape = numpy_image.shape
        orig_shape = (dataset_dict["height"], dataset_dict["width"])
        if shape[:2] != orig_shape:
            # It transforms the "original" image in the dataset to the input image
            pre_tfm = ResizeTransform(orig_shape[0], orig_shape[1], shape[0], shape[1])
        else:
            pre_tfm = NoOpTransform()

        # Create all combinations of augmentations to use
        aug_candidates = []  # each element is a list[Augmentation]
        for min_size in self.min_sizes:
            resize = ResizeShortestEdge(min_size, self.max_size)
            aug_candidates.append([resize])
            if self.flip:
                hflip = RandomFlip(prob=1.0, horizontal=True, vertical=False)
                aug_candidates.append([resize, hflip])
                vflip =  RandomFlip(prob=1.0, horizontal=False, vertical=True)
                aug_candidates.append([resize, vflip])

        # Apply all the augmentations
        ret = []
        for aug in aug_candidates:
            new_image, tfms = apply_augmentations(aug, np.copy(numpy_image))
            torch_image = torch.from_numpy(np.ascontiguousarray(new_image.transpose(2, 0, 1)))

            dic = deepcopy(dataset_dict)
            dic["transforms"] = pre_tfm + tfms
            dic["image"] = torch_image
            ret.append(dic)
        return ret

# %% ../../../nbs/43_engines.detectron2.tta.ipynb 4
@patch_to(GeneralizedRCNNWithTTA)
def _reduce_pred_masks(self, outputs, tfms):
    "Invert vflip and hflip transforms"
    for output, tfm in zip(outputs, tfms):
        if any(isinstance(t, HFlipTransform) for t in tfm.transforms):
            output.pred_masks = output.pred_masks.flip(dims=[3])
        if any(isinstance(t, VFlipTransform) for t in tfm.transforms):
            output.pred_masks = output.pred_masks.flip(dims=[2])
    all_pred_masks = torch.stack([o.pred_masks for o in outputs], dim=0)
    avg_pred_masks = torch.mean(all_pred_masks, dim=0)
    return avg_pred_masks

@patch_to(GeneralizedRCNNWithTTA)
def _merge_detections(self, all_boxes, all_scores, all_classes, shape_hw):
    # select from the union of all results
    num_boxes = len(all_boxes)
    num_classes = self.cfg.MODEL.ROI_HEADS.NUM_CLASSES
    # +1 because fast_rcnn_inference expects background scores as well
    all_scores_2d = torch.zeros(num_boxes, num_classes + 1, device=all_boxes.device)
    for idx, cls, score in zip(count(), all_classes, all_scores):
        all_scores_2d[idx, cls] = score

    if all_boxes.size()[-1] == 5:
        merged_instances, _ = fast_rcnn_inference_single_image_rotated(
            all_boxes,
            all_scores_2d,
            shape_hw,
            1e-8,
            self.cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST,
            self.cfg.TEST.DETECTIONS_PER_IMAGE,
        )

    else:
        merged_instances, _ = fast_rcnn_inference_single_image(
            all_boxes,
            all_scores_2d,
            shape_hw,
            1e-8,
            self.cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST,
            self.cfg.TEST.DETECTIONS_PER_IMAGE,
        )

    return merged_instances

@patch_to(GeneralizedRCNNWithTTA)
def _rescale_detected_boxes(self, augmented_inputs, merged_instances, tfms):
    augmented_instances = []
    for input, tfm in zip(augmented_inputs, tfms):
        # Transform the target box to the augmented image's coordinate space
        pred_boxes = merged_instances.pred_boxes.tensor.cpu().numpy()
        if pred_boxes.shape[-1] == 5:
            pred_boxes = torch.from_numpy(tfm.apply_rotated_box(pred_boxes))
        else:
            pred_boxes = torch.from_numpy(tfm.apply_box(pred_boxes))

        aug_instances = Instances(
            image_size=input["image"].shape[1:3],
            pred_boxes=Boxes(pred_boxes),
            pred_classes=merged_instances.pred_classes,
            scores=merged_instances.scores,
        )
        augmented_instances.append(aug_instances)
    return augmented_instances

@patch_to(GeneralizedRCNNWithTTA)
def _get_augmented_boxes(self, augmented_inputs, tfms):
    # 1: forward with all augmented images
    outputs = self._batch_inference(augmented_inputs)
    # 2: union the results
    all_boxes = []
    all_scores = []
    all_classes = []
    for output, tfm in zip(outputs, tfms):
        # Need to inverse the transforms on boxes, to obtain results on original image
        pred_boxes = output.pred_boxes.tensor
        if pred_boxes.size()[-1] == 5:
            original_pred_boxes = tfm.inverse.apply_rotated_box(pred_boxes.cpu().numpy())
        else:
            original_pred_boxes = tfm.inverse().apply_box(pred_boxes.cpu().numpy())
        all_boxes.append(torch.from_numpy(original_pred_boxes).to(pred_boxes.device))

        all_scores.extend(output.scores)
        all_classes.extend(output.pred_classes)
    all_boxes = torch.cat(all_boxes, dim=0)
    return all_boxes, all_scores, all_classes

# %% ../../../nbs/43_engines.detectron2.tta.ipynb 5
class TTAPredictor:
    """DefaultPredictor that implements TTA
    """
    
    def __init__(self, cfg):
        self.cfg = cfg.clone()  # cfg can be modified by model
        self.model = build_model(self.cfg)
        checkpointer = DetectionCheckpointer(self.model)
        checkpointer.load(cfg.MODEL.WEIGHTS)
        self.model = GeneralizedRCNNWithTTA(cfg, self.model, tta_mapper=DatasetMapperTTAFlip(cfg))
        self.model.eval()
        if len(cfg.DATASETS.TEST):
            self.metadata = MetadataCatalog.get(cfg.DATASETS.TEST[0])

        self.aug = ResizeShortestEdge(
            [cfg.INPUT.MIN_SIZE_TEST, cfg.INPUT.MIN_SIZE_TEST], cfg.INPUT.MAX_SIZE_TEST
        )

        self.input_format = cfg.INPUT.FORMAT
        assert self.input_format in ["RGB", "BGR"], self.input_format

    def __call__(self, original_image):
        """
        Args:
            original_image (np.ndarray): an image of shape (H, W, C) (in BGR order).

        Returns:
            predictions (dict):
                the output of the model for one image only.
                See :doc:`/tutorials/models` for details about the format.
        """
        with torch.no_grad():  # https://github.com/sphinx-doc/sphinx/issues/4258
            # Apply pre-processing to image.
            if self.input_format == "RGB":
                # whether the model expects BGR inputs or RGB
                original_image = original_image[:, :, ::-1]
            height, width = original_image.shape[:2]
            image = self.aug.get_transform(original_image).apply_image(original_image)
            image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1))

            inputs = {"image": image, "height": height, "width": width}
            predictions = self.model([inputs])[0]
            return predictions
