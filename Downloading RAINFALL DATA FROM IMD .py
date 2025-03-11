#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Connect Google drive with Google colab
from google.colab import drive
drive.mount('/content/drive')


# In[2]:


pip install imdlib


# In[ ]:


# Download the IMD raw data into the google drive
import imdlib as imd
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

path = "/content/drive/MyDrive/Colab Notebooks"

start_yr = 2019
end_yr = 2021
variable = 'rain' # other options are ('tmin'/ 'tmax')

imd.get_data(variable, start_yr, end_yr, fn_format='yearwise', file_dir=path)
data = imd.open_data(variable, start_yr, end_yr,'yearwise', path)
ds = data.get_xarray()
print(ds)


# In[ ]:


# Provide the alttitude & Longitude of a point for which the data is required
#  And save the data into CSV file

lat = 20.03 #lattitude of point
lon = 77.23 #longitude of point
data.to_csv('data.csv', lat, lon, path)


# In[ ]:


# Save CSV files for multiple points

# Provide lat and long in a list
latLong = [[20.3,77.23],[23.5,72.5],[26.0,77,1]]

for points in latLong:
  lat = points[0]
  lon = points[1]

  data.to_csv('test.csv', lat, lon, path)
  print ("data save for ",points)


# In[ ]:


#  Provide the Geojson file of a catchment or polygon to dowlnaod all the gridded data lying into that polygon

geojson_file = '/content/drive/MyDrive/IMD/Test_geojson.geojson'


url="https://drive.google.com/file/d/111XvmUzvTlhY2lbFMseGVhZQh4pisFXQ/view?usp=sharing"
url2='https://drive.google.com/uc?id=' + url.split('/')[-2]
points_df = pd.read_csv(url2)


geometry = [Point(xy) for xy in zip(points_df['Long'], points_df['Lat'])]

# Creating the GeoDataFrame
gdf_points = gpd.GeoDataFrame(points_df, geometry=geometry)

# Set a CRS (coordinate reference system), EPSG:4326 is WGS84 Lat/Long
gdf_points.set_crs(epsg=4326, inplace=True)


gdf_polygon = gpd.read_file(geojson_file)

# Ensure both GeoDataFrames use the same CRS
if gdf_points.crs != gdf_polygon.crs:
    gdf_points = gdf_points.to_crs(gdf_polygon.crs)

gdf_list = []
for row in range (len(gdf_polygon)):
    points_in_polygon = gdf_points[gdf_points.within(gdf_polygon.iloc[row].geometry)]
    gdf_list.append(points_in_polygon)

final_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))

final_df = final_gdf[["Name","Lat","Long"]]
final_df.to_csv("Master_file.csv")

for index, row in final_df.iterrows():
    lat = row['Lat']
    lon = row['Long']
    data.to_csv('test.csv', lat, lon, path)
    print ("data save for " + str(lat)+ "_" +str(lon))

