import pdal
import json
import geopandas as gpd
from shapely.geometry import Polygon, Point

#region = 'USGS_LPC_CO_SoPlatteRiver_Lot5_2013_LAS_2015/'
#bound = "([-93.756155, 41.918015], [-93.747334, 41.921429])"
#public_access_path = data_path + region + "ept.json"
#Data_Path = "https://s3-us-west-2-amazonaws.com/usgs-lidar-public"

Data_Path = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
REGION= "IA_FullState"
BOUND = "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])"
output_flename_laz = "SoPlatte"
output_flename_tif = "Platte"
pipeline_path = "./fetch_data.json"


def prep_input(polygon: Polygon, output_epsg):
    polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])
    polygon_df.set_crs(epsg=output_epsg, inplace=True)
    polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=3857)
    minx, miny, maxx, maxy = polygon_df['geometry'][0].bounds

    polygon_input = 'POLYGON(('
    xcords, ycords = polygon_df['geometry'][0].exterior.coords.xy
    for x, y in zip(list(xcords), list(ycords)):
        polygon_input += f'{x} {y}, '
        
    polygon_input = polygon_input[:-2]
    polygon_input += '))'

    print(polygon_input)
    print(f"({[minx, maxx]},{[miny,maxy]})")

    return f"({[minx, maxx]},{[miny,maxy]})", polygon_input

def get_raster_terrain(
                       crs,
                       polygon: Polygon,
                    #    bounds:str = BOUND,
                       region:str = REGION,
                       public_access_path: str = Data_Path,
                       OUTPUT_FILENAME_LAZ:str = output_flename_laz,
                       OUTPUT_FILENAME_TIF:str = output_flename_tif,
                       PIPLINE_PATH:str = pipeline_path 
                    )->None:

            bounds2, polygon2 = prep_input(polygon, crs)
            with open(pipeline_path) as json_file:
                the_json = json.load(json_file)
                the_json['pipeline'][0]['filename']= public_access_path + region + "/ept.json"
                the_json['pipeline'][0]['bounds']= bounds2
                the_json['pipeline'][1]['polygon']= polygon2
                the_json['pipeline'][3]['out_srs']=  f"EPSG:{crs}"
                the_json['pipeline'][4]['filename']=  "laz/" + OUTPUT_FILENAME_LAZ + ".laz"
                the_json['pipeline'][5]['filename']= "tif/" + OUTPUT_FILENAME_TIF + ".tif"

   # pipline = pdal.pipeline(json.dumps(the_json))
                pipline = pdal.Pipeline(json.dumps(the_json))

            try:
                res = pipline.execute()
                metadata = pipline.metadata
                # print('metadata: ', metadata)
                log = pipline.log
                # print("logs: ", log)
                return pipline.arrays
            except RuntimeError as e:
             print(e)





