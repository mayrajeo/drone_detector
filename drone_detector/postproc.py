# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_postprocessing.ipynb (unless otherwise specified).

__all__ = ['poly_IoU', 'poly_intersection_over_area']

# Cell
from .imports import *

# Cell

def poly_IoU(poly_1:Polygon, poly_2:Polygon) -> float:
    "IoU for polygons"
    area_intersection = poly_1.intersection(poly_2).area
    area_union = poly_1.union(poly_2).area
    iou = area_intersection / area_union
    return iou

def poly_intersection_over_area(poly_1:Polygon, poly_2:Polygon) -> float:
    "How much of smaller polygon is contained within larger"
    if poly_1.area > poly_2.area:
        smaller = poly_2
        larger = poly_1
    else:
        smaller = poly_1
        larger = poly_2
    area_intersection = larger.intersection(smaller).area
    intersection_over_area = area_intersection / smaller.area
    return intersection_over_area