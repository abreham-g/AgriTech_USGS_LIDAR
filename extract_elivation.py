import numpy as np
import laspy as lp
from shapely.geometry import box, Point, Polygon
from laspy.file import File
from geopandas import GeoDataFrame
import fetch_data

input_path = "10acadamy/AgriTech_USGS_LIDAR/laz"
dataname = "SoPlatte"
region = "IA_FullState"
bound = "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])"

def elevation(INPUT_PATH: str = input_path,
               DATANAMES:str = dataname):
    
    
    
    
    point=lp.file.File(input_path+dataname+".laz", mode="r")
    
    #np.vstack must be changed to geopanda dataframe
    points = np.vstack((point.x, point.y, point.z)).transpose()
    geometry = [Point(xyz) for xyz in zip(point.x,point.y,point.z)]
    df = GeoDataFrame(points, crs = crs, geometry = geometry)

    
    return df

def get_elevation(BOUND:str = bound,
               REGION:str = region):
    
    fetch_data.get_raster_terrain(bound, region)
    
    
    df = elevation(input_path, dataname)
    return df
    





