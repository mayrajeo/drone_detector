import sys, os, re, shutil, typing, itertools, operator, math, warnings, json, random
from fastcore.foundation import *
from fastcore.basics import *

import numpy as np
import pandas as pd
from copy import copy, deepcopy

from pathlib import Path
from tqdm.auto import tqdm

from functools import partial, reduce
from typing import *

from types import (
    BuiltinFunctionType,
    BuiltinMethodType,
    MethodType,
    FunctionType,
    SimpleNamespace,
)

import json


import geopandas as gpd
import shapely
from shapely.geometry import Point, Polygon, box, shape
import rasterio as rio
from rasterio.merge import merge as rio_merge
import affine

import matplotlib.pyplot as plt