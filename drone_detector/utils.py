# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_utils.ipynb (unless otherwise specified).

__all__ = ['rangeof', 'cone_v', 'cut_cone_v']

# Cell

from .imports import *

# Cell

def rangeof(iterable):
    "Equivalent for range(len(iterable))"
    return range(len(iterable))

# Cell

def cone_v(r:float, h:float) -> float:
    "V = (Ah)/3"
    A = np.pi * r**2
    V = (A * h) / 3
    return V

def cut_cone_v(r_1:float, r_2:float, h:float):
    "V = (h(A + sqrt(A*A') + A))/3"
    A_1 = np.pi * r_1**2
    A_2 = np.pi * r_2**2
    V = (h*(A_1 + np.sqrt(A_1 * A_2) + A_2))/3
    return V
