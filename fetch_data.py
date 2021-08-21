import pdal
import json

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

def get_raster_terrain(bounds:str = BOUND,
                       region:str = REGION,
                       public_access_path: str = Data_Path,
                       OUTPUT_FILENAME_LAZ:str = output_flename_laz,
                       OUTPUT_FILENAME_TIF:str = output_flename_tif,
                       PIPLINE_PATH:str = pipeline_path 
                    )->None:

    with open(pipeline_path) as json_file:
        the_json = json.load(json_file)

    the_json['pipeline'][0]['bounds']= bounds
    the_json['pipeline'][0]['filename']= public_access_path + region + "/ept.json"
    the_json['pipeline'][3]['filename']=  "laz/" + OUTPUT_FILENAME_LAZ + ".laz"
    the_json['pipeline'][4]['filename']= "tif/" + OUTPUT_FILENAME_TIF + ".tif"

   # pipline = pdal.pipeline(json.dumps(the_json))
    pipline = pdal.Pipeline(json.dumps(the_json))

    try:
        res = pipline.execute()
        metadata = pipline.metadata
        print('metadata: ', metadata)
        log = pipline.log
        print("logs: ", log)
        return pipline.arrays
    except RuntimeError as e:
        print(e)



get_raster_terrain()

