# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/41_engines.detectron2.training.ipynb (unless otherwise specified).

__all__ = ['Trainer', 'transform_rotated_annotations', 'RotatedDatasetMapper', 'RotatedTrainer']

# Cell
from ...imports import *
from ...utils import *

from .augmentations import *

import detectron2
from detectron2.engine import DefaultTrainer
from detectron2.evaluation import COCOEvaluator, DatasetEvaluators, RotatedCOCOEvaluator
from detectron2.data import build_detection_train_loader, DatasetMapper, MetadataCatalog
from detectron2.data import detection_utils as utils
from detectron2.utils.visualizer import Visualizer
from detectron2.data import transforms as T
from detectron2.structures import BoxMode
import torch


# Cell

class Trainer(DefaultTrainer):
    """
    Trainer class for training detectron2 models, using default augmentations
    """

    def __init__(self, cfg):
        super().__init__(cfg)

    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        return DatasetEvaluators([COCOEvaluator(dataset_name, output_dir=output_folder)])

    @classmethod
    def build_train_loader(cls, cfg):
        return build_detection_train_loader(cfg, mapper=DatasetMapper(cfg, is_train=True,
                                                                      augmentations=build_aug_transforms(cfg)))

# Cell

def transform_rotated_annotations(annotation, transforms, image_size, *, keypoint_hflip_indices=None):
    if annotation["bbox_mode"] == BoxMode.XYWHA_ABS:
        annotation["bbox"] = transforms.apply_rotated_box(np.asarray([annotation["bbox"]]))[0]
    else:
        bbox = BoxMode.convert(annotation["bbox"], annotation["bbox_mode"], BoxMode.XYXY_ABS)
        # Note that bbox is 1d (per-instance bounding box)
        annotation["bbox"] = transforms.apply_box([bbox])[0]
        annotation["bbox_mode"] = BoxMode.XYXY_ABS

    return annotation

class RotatedDatasetMapper(DatasetMapper):
    def _transform_annotations(self, dataset_dict, transforms, image_shape):
        for anno in dataset_dict["annotations"]:
            if not self.use_instance_mask:
                anno.pop("segmentation", None)
            if not self.use_keypoint:
                anno.pop("keypoints", None)

        annos = [
            transform_rotated_annotations(
                obj, transforms, image_shape, keypoint_hflip_indices=self.keypoint_hflip_indices
            )
            for obj in dataset_dict.pop("annotations")
            if obj.get("iscrowd", 0) == 0
        ]

        instances = utils.annotations_to_instances_rotated(
            annos, image_shape
        )
        if self.recompute_boxes:
            instances.gt_boxes = instances.gt_masks.get_bounding_boxes()
        dataset_dict["instances"] = utils.filter_empty_instances(instances)


    def __call__(self, dataset_dict):
        for a in dataset_dict['annotations']:
            a['bbox_mode'] = BoxMode.XYWHA_ABS # Ensure that boxmode is correct
        image = utils.read_image(dataset_dict['file_name'])
        utils.check_image_size(dataset_dict, image)
        aug_input = T.AugInput(image)
        transforms = self.augmentations(aug_input)
        image = aug_input.image

        image_shape = image.shape[:2]

        dataset_dict['image'] = torch.as_tensor(np.ascontiguousarray(image.transpose(2,0,1)))

        if not self.is_train:
            dataset_dict.pop('annotations', None)
            dataset_dict.pop('sem_seg_file_name', None)
            return dataset_dict

        if 'annotations' in dataset_dict:
            self._transform_annotations(dataset_dict, transforms, image_shape)
        return dataset_dict

# Cell

class RotatedTrainer(DefaultTrainer):

    def __init__(self, cfg):
        super().__init__(cfg)


    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        evaluators = [RotatedCOCOEvaluator(dataset_name, output_folder)]
        return DatasetEvaluators(evaluators)

    @classmethod
    def build_train_loader(cls, cfg):
        return build_detection_train_loader(cfg, mapper=RotatedDatasetMapper(cfg, is_train=True,
                                                                             augmentations=build_aug_transforms(cfg)))