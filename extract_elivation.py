import numpy as np
# import laspy as lp
from shapely.geometry import box, Point, Polygon
# from laspy.file import File
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import fetch_data
import geopandas as gpd
from shapely.geometry import Polygon, Point

input_path = "laz/"
dataname = "SoPlatte"
region = "IA_FullState"
bound = "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])"

def elevation(x, y, z):
    
    
    
    
#     point=lp.read(input_path+dataname+".laz")
    #
#     las = laspy.create(point_format=2, file_version='1.2')
    #np.vstack must be changed to geopanda dataframe
    points = np.vstack((x, y, z)).transpose()
    print(points)
    geometry = [Point(xyz) for xyz in zip(points[:, 0],points[:, 1],points[:, 2])]

    
    
    df = GeoDataFrame(points, geometry = geometry)
    df.columns = ['0', '1', 'Elevation', 'geometry']
    dataframe = df.iloc[:,[2,3]]
    
      
   #df = get_elevation(region,bound)
    
    return dataframe

def get_elevation(polygon: Polygon, crs: int, REGION:str = region):
    
    data = fetch_data.get_raster_terrain(polygon=polygon, crs=crs, region=region)[0]
    x, y, z = np.array(data["X"]), np.array(data["Y"]), np.array(data["Z"])
    
    
    df = elevation(x,y,z)
    return df

def plot_terrain_3d( gdf: gpd.GeoDataFrame, fig_size: tuple=(12, 10), size: float=0.01):

        fig, ax = plt.subplots(1, 1, figsize=fig_size)
        ax = plt.axes(projection='3d')
        ax.scatter(gdf.geometry.x, gdf.geometry.y, gdf.Elevation, s=size)
        plt.show()
def subsample(gdf: gpd.GeoDataFrame, res: int = 3):
    """
    This method subsamples the points in a point cloud data using some resolution.

    Args:
        gdf (gpd.GeoDataFrame): [a geopandas dataframe containing points in the geometry column and height in the elevation column.]
        res (int, optional): [resolution]. Defaults to 3.

    Returns:
        [Geopandas.GeoDataFrame]: [a geopandas dataframe]
    """

    points = np.vstack((gdf.geometry.x, gdf.geometry.y, gdf.Elevation)).transpose()
    voxel_size=res
    non_empty_voxel_keys, inverse, nb_pts_per_voxel = np.unique(((points - np.min(points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
    idx_pts_vox_sorted=np.argsort(inverse)
    voxel_grid={}
    grid_barycenter=[]
    last_seen=0
    for idx,vox in enumerate(non_empty_voxel_keys):
        voxel_grid[tuple(vox)]= points[idx_pts_vox_sorted[
        last_seen:last_seen+nb_pts_per_voxel[idx]]]
        grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
        last_seen+=nb_pts_per_voxel[idx]

    sub_sampled =  np.array(grid_barycenter)
    df_subsampled = gpd.GeoDataFrame(columns=["Elevation", "geometry"])

    geometry = [Point(x, y) for x, y in zip( sub_sampled[:, 0],  sub_sampled[:, 1])]

    df_subsampled['Elevation'] = sub_sampled[:, 2]
    df_subsampled['geometry'] = geometry

    return df_subsampled



