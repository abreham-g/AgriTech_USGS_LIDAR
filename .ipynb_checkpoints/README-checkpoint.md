# AgriTech_USGS_LIDAR
At AgriTech, we are very interested in how water flows through a maize farm field. This
knowledge will help us improve our research on new agricultural products being tested on
farms.
our work at an AgriTech, has a mix of domain experts, data scientists, data engineers.
As part of the data engineering team, we are tasked to produce an easy to use, reliable and
well designed python module that domain experts and data scientists can use to fetch,
visualise, and transform publicly available satellite and LIDAR data. In particular, our code
should interface with USGS 3DEP and fetch data using their API.
The workflow for this project is as follows
- Reading instructions and understand the business needs, the type of data available, the
    data engineering process(es) that needs to be carried out, the Workflow
    requirements, and the resources required/available to complete the project
- Planning your work and set up development environment to assist in completing the
    project
- Exploring a sample of the dataset, understand it structure, the information stored
    within and develop intuition on how it can be used
- Seting up a github repo, integrate unit testing and CICD for proper code package test
    and deployment
- Building a codebase that communicates with the provided data source and extract
    needed information based on the parameters passed
# Data Fetching and Loading
our task is to write a modular python code/package to connect to the API, query the data
model to select with a specified input and get a desired output. For example, submit a
boundary (GPS coordinates polygon) and receive back a raster of the height of the terrain
within the boundary. The expected inputs and outputs are
Inputs:
- Field boundary polygon in geopandas dataframe
    - All CRS’s (coordinate reference systems) should be accepted
- Desired output CRS
# Terrain Visualization
In this part we will Include an option to graphically display the returned elevation files as either a 3D render plot
or as a heatmap. 
#  Data Transformation
Topographic wetness index (TWI) - as an additional column returned with
geopandas dataframe
- it is a useful model to estimate where water will accumulate in an area with elevation differences. It is a function of slope and the upstream contributing area
# Standardized grid 
- A python code that takes elevation points output from the USGS
LIDAR tool and interpolates them to a grid.
# Inputs:
- A single year geopandas elevation point dataframe returned from the tool
# above.
- Desired output resolution (in meters)
# Outputs:
- An interpolated grid of points with interpolated elevation information
- An option to visualize the output grid as a 3D render or heatmap to visually
    compare to the original, un-interpolated elevation data.
