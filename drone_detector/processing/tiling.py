# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/10_processing.tiling.ipynb.

# %% auto 0
__all__ = ['Tiler', 'untile_raster', 'copy_sum', 'untile_vector']

# %% ../../nbs/10_processing.tiling.ipynb 3
from ..imports import *
from ..utils import *
from .postproc import *
import rasterio.mask as rio_mask
import rasterio.windows as rio_windows


# %% ../../nbs/10_processing.tiling.ipynb 5
class Tiler():
    """
    Similar functions than ´solaris.tile.raster_tile' but with more recent dependencies. 
    """
    def __init__(self, outpath, gridsize_x:int=400, gridsize_y:int=400, 
                 overlap:Tuple[int, int]=(100, 100)):
        store_attr()
        self.grid = None
        if not os.path.exists(outpath): os.makedirs(outpath)
            
        self.raster_path = f'{self.outpath}/images'
        self.vector_path = f'{self.outpath}/vectors'
        self.rasterized_vector_path = f'{self.outpath}/rasterized_vectors'
        
    def tile_raster(self, path_to_raster:str, allow_partial_data:bool=False) -> None:
        "Tiles specified raster to `self.gridsize_x` times `self.gridsize_y` grid, with `self.overlap` pixel overlap"
        names = []
        polys = []
        col_id = 0
        row_id = 0
        
        if not os.path.exists(self.raster_path): os.makedirs(self.raster_path)
        with rio.open(path_to_raster) as src:
            y, x = src.shape
            
            for (iy, dy), (ix, dx) in tqdm(itertools.product(enumerate(range(0, y, self.gridsize_y-self.overlap[1])), 
                                                             enumerate(range(0, x, self.gridsize_x-self.overlap[0])))):
                
                if dy+self.gridsize_y > y and not allow_partial_data: continue
                if dx+self.gridsize_x > x and not allow_partial_data: continue
                window = rio_windows.Window.from_slices((dy, dy+self.gridsize_y),
                                                        (dx, dx+self.gridsize_x))
                prof = src.profile.copy()
                prof.update(
                    height=window.height,
                    width=window.width,
                    transform= rio_windows.transform(window, src.transform),
                    compress='lzw',
                    predictor=2
                )
                fname = f'R{iy}C{ix}'
                data = src.read(window=window)
                if data.shape[1] < window.height or data.shape[2] < window.width:
                    newdata = np.zeros((data.shape[0], window.height, window.width))
                    newdata[:, :data.shape[1], :data.shape[2]] = data
                    data = newdata
                with rio.open(f'{self.raster_path}/{fname}.tif', 'w', **prof) as dest:
                    dest.write(data)
                    polys.append(box(*dest.bounds))
                names.append(fname)
            self.grid = gpd.GeoDataFrame({'cell': names, 'geometry':polys}, crs=src.crs)  
        return
    
    
    def tile_vector(self, path_to_vector:str, min_area_pct:float=0.0) -> None:
        """
        Tiles a vector data file into smaller tiles. Converts all multipolygons to a regular polygons. `min_area_pct` is be used to specify the minimum area for partial masks to keep. Default value 0.0 keeps all masks.
        """
        if self.grid is None:
            print('No raster grid specified, use Tiler.tile_raster to determine grid limits')
            return
        
        if not os.path.exists(self.vector_path): os.makedirs(self.vector_path)
        vector = gpd.read_file(path_to_vector)
        # God bless spatial index
        sindex = vector.sindex
        for row in tqdm(self.grid.itertuples()):
            possible_matches_index = list(sindex.intersection(row.geometry.bounds))
            tempvector = vector.iloc[possible_matches_index].copy()
            tempvector['orig_area'] = tempvector.geometry.area
            tempvector = tempvector.clip(row.geometry, keep_geom_type=True)

            if min_area_pct < 0 or min_area_pct >= 1:
                print('Invalid minimum area percentage set, defaulting to 0')
            tempvector = tempvector[tempvector.geometry.area >= tempvector.orig_area * min_area_pct]
            # No annotations -> no shapefile
            if len(tempvector) == 0: continue            
            tempvector['geometry'] = tempvector.apply(lambda row: fix_multipolys(row.geometry) 
                                                      if row.geometry.geom_type == 'MultiPolygon'
                                                      else shapely.geometry.Polygon(row.geometry.exterior), axis=1)
            

            tempvector.to_file(f'{self.vector_path}/{row.cell}.geojson', driver='GeoJSON')
        return
    
    def tile_and_rasterize_vector(self, path_to_raster:str, path_to_vector:str, column:str,
                                  keep_bg_only:bool=False) -> None:
        """Rasterizes vectors based on tiled rasters. Requires that shapefile has numeric data in `column`. By default only keeps the patches that contain polygon data, by specifying `keep_bg_only=True` saves also masks for empty patches."""
        if not os.path.exists(self.rasterized_vector_path):
            os.makedirs(self.rasterized_vector_path)
        
        vector = gpd.read_file(path_to_vector)

        with rio.open(path_to_raster) as src:
            for row in tqdm(self.grid.itertuples()):
                out_im, out_tfm = rio_mask.mask(src, [row.geometry], crop=True)
                out_meta = src.meta
                out_meta.update({'driver':'GTiff',
                                 'height': out_im.shape[1],
                                 'width': out_im.shape[2],
                                 'transform': out_tfm,
                                 'compress':'lzw',
                                 'count':1})
                tempvector = vector.clip(row.geometry, keep_geom_type=True)
                with rio.open(f'{self.rasterized_vector_path}/{row.cell}.tif', 'w+', **out_meta) as dest:
                    dest_arr = dest.read(1)
                    shapes = ((geom,value) for geom, value in zip(tempvector.geometry, tempvector[column]))
                    if len(tempvector) == 0: 
                        if keep_bg_only: dest.write_band(1, dest_arr)
                        continue
                    burned = rio.features.rasterize(shapes=shapes, fill=0, out=dest_arr, transform=dest.transform)
                    dest.write_band(1, burned)   
        return

# %% ../../nbs/10_processing.tiling.ipynb 9
def untile_raster(path_to_targets:str, outfile:str, method:str='first'):
    """Merge multiple patches from `path_to_targets` into a single raster`"""

    rasters = [f'{path_to_targets}/{f}' for f in os.listdir(path_to_targets) if f.endswith('.tif')]
    
    if method == 'sum': method = copy_sum
    
    files_to_mosaic = []
       
    for f in rasters:
        src = rio.open(f)
        files_to_mosaic.append(src)
    
    mosaic, out_tfm = rio_merge(files_to_mosaic, method=method)
    
    out_meta = src.meta.copy()
    out_meta.update({'driver': 'GTiff',
                     'height': mosaic.shape[1],
                     'width': mosaic.shape[2],
                     'transform': out_tfm,
                     'crs': src.crs})
    
    with rio.open(outfile, 'w', **out_meta) as dest: dest.write(mosaic)
    
def copy_sum(merged_data, new_data, merged_mask, new_mask, **kwargs):
    "Make new pixels have the sum of two overlapping pixels as their value. Useful with prediction data"
    newregion = merged_data + new_data
    np.copyto(merged_data, newregion)    
    
def untile_vector(path_to_targets:str, outpath:str, non_max_suppression_thresh:float=0.0, nms_criterion:str='score'):
    "Create single shapefile from a directory of predicted shapefiles"
    pred_files = [f for f in os.listdir(path_to_targets) if f.endswith(('.shp', '.geojson'))]
    gdf = None
    for p in tqdm(pred_files):
        temp_gdf = gpd.read_file(f'{path_to_targets}/{p}')
        if gdf is None: gdf = temp_gdf
        else: gdf = gdf.append(temp_gdf)
    print(f'{len(gdf)} polygons before non-max suppression')
    if non_max_suppression_thresh != 0:
        np_bounding_boxes = np.array([b.bounds for b in gdf.geometry])
        scores = gdf.score.values
        idxs = non_max_suppression_fast(np_bounding_boxes, scores, 
                                        overlap_thresh=non_max_suppression_thresh,
                                        sort_criterion=nms_criterion)
        gdf = gdf.iloc[idxs]
    print(f'{len(gdf)} polygons after non-max suppression')
    if outpath.endswith('shp'):
        gdf.to_file(outpath)
    elif outpath.endswith('geojson'):
        gdf.to_file(outpath, driver='GeoJSON')
    return
