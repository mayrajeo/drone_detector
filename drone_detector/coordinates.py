# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_coordinates.ipynb (unless otherwise specified).

__all__ = ['convert_poly_coords', 'affine_transform_gdf', 'gdf_to_px', 'georegister_px_df']

# Cell
from .imports import *
from .utils import *

# Cell

def convert_poly_coords(geom:shape, raster_src:str=None, affine_obj:affine.Affine=None,
                        inverse:bool=False, precision=None) -> shape:
    "Adapted from solaris. Converts georeferenced coordinates to pixel coordinates and vice versa"
    if not raster_src and not affine_obj:
        raise ValueError("Either raster_src or affine_obj must be provided.")

    if raster_src is not None:
        affine_xform = get_geo_transform(raster_src)
    else:
        if isinstance(affine_obj, affine.Affine):
            affine_xform = affine_obj
        else:
            # assume it's a list in either gdal or "standard" order
            # (list_to_affine checks which it is)
            if len(affine_obj) == 9:  # if it's straight from rasterio
                affine_obj = affine_obj[0:6]
            affine_xform = list_to_affine(affine_obj)

    if inverse:  # geo->px transform
        affine_xform = ~affine_xform

    if isinstance(geom, str):
        # get the polygon out of the wkt string
        g = shapely.wkt.loads(geom)
    elif isinstance(geom, shapely.geometry.base.BaseGeometry):
        g = geom
    else:
        raise TypeError('The provided geometry is not an accepted format. '
                        'This function can only accept WKT strings and '
                        'shapely geometries.')

    xformed_g = shapely.affinity.affine_transform(g, [affine_xform.a,
                                                      affine_xform.b,
                                                      affine_xform.d,
                                                      affine_xform.e,
                                                      affine_xform.xoff,
                                                      affine_xform.yoff])
    if isinstance(geom, str):
        # restore to wkt string format
        xformed_g = shapely.wkt.dumps(xformed_g)
    if precision is not None:
        xformed_g = _reduce_geom_precision(xformed_g, precision=precision)

    return xformed_g

def affine_transform_gdf(gdf:gpd.GeoDataFrame, affine_obj:affine.Affine, inverse:bool=False,
                         geom_col:str='geometry', precision:int=None) -> gpd.GeoDataFrame:
    """Adapted from solaris, transforms all geometries in GeoDataFrame to pixel coordinates from
    Georeferced coordinates and vice versa"""
    if 'geometry' not in gdf.columns: gdf = gdf.rename(columns={geom_col: 'geometry'})
    gdf["geometry"] = gdf["geometry"].apply(convert_poly_coords,
                                            affine_obj=affine_obj,
                                            inverse=inverse)
    if precision is not None:
        gdf['geometry'] = gdf['geometry'].apply(
            _reduce_geom_precision, precision=precision)

    # the CRS is no longer valid - remove it
    gdf.crs = None

    return gdf


def gdf_to_px(gdf:gpd.GeoDataFrame, im_path, geom_col:str='geometry', precision:int=None,
              outpath=None, override_crs=False) -> gpd.GeoDataFrame:
    "Adapted from https://solaris.readthedocs.io/en/latest/_modules/solaris/vector/polygon.html#geojson_to_px_gdf"

    with rio.open(im_path) as im:
        affine_obj = im.transform

    transformed_gdf = affine_transform_gdf(gdf, affine_obj=affine_obj,
                                           inverse=True, precision=precision,
                                           geom_col=geom_col)

    transformed_gdf['image_fname'] = os.path.split(im_path)[1]

    if outpath is not None:
        if outpath.lower().endswith('json'):
            transformed_gdf.to_file(outpath, driver='GeoJSON')
        else:
            transformed_gdf.to_csv(outpath, index=False)
    return transformed_gdf

def georegister_px_df(df:pd.DataFrame, im_path=None, affine_obj:affine.Affine=None, crs=None,
                      geom_col:str='geometry', precision:int=None, output_path=None) -> gpd.GeoDataFrame:
    with rio.open(im_path) as im:
        affine_obj = im.transform
        crs = im.crs

    tmp_df = affine_transform_gdf(df, affine_obj, geom_col=geom_col,
                                  precision=precision)
    result = gpd.GeoDataFrame(tmp_df, crs='epsg:' + str(crs.to_epsg()))

    if output_path is not None:
        if output_path.lower().endswith('json'):
            result.to_file(output_path, driver='GeoJSON')
        else:
            result.to_csv(output_path, index=False)

    return result