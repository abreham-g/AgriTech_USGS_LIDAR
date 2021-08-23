import numpy as np
# import laspy as lp
from shapely.geometry import box, Point, Polygon
# from laspy.file import File
from geopandas import GeoDataFrame
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
    





