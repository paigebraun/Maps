import geopandas as gpd
import pandas
import numpy as np
import random
import matplotlib.pyplot as plt
import shapely.ops
from shapely.ops import polygonize
import os

#get current working directory
current_directory = os.getcwd()

#define relative path to shapefile data
relative_path_arterial_streets = 'kx-washington-5layers-SHP/king-county-wa-arterial-streets/king-county-wa-arterial-streets.shp'
relative_path_local_roads = 'kx-washington-5layers-SHP/king-county-wa-local-streets-and-roads/king-county-wa-local-streets-and-roads.shp'
relative_path_lake = 'kx-washington-5layers-SHP/king-county-washington-lakes-and-large-rivers/king-county-washington-lakes-and-large-rivers.shp'
relative_path_hwy = 'kx-washington-5layers-SHP/king-county-wa-freeways/king-county-wa-freeways.shp'
relative_path_watershed = 'kx-washington-5layers-SHP/king-county-wa-watershed-boundary/king-county-wa-watershed-boundary.shp'

#join current directory with relative path to create absolute path for shapefile data
absolute_path_arterial_streets = os.path.join(current_directory, relative_path_arterial_streets)
absolute_path_local_roads = os.path.join(current_directory, relative_path_local_roads)
absolute_path_lake = os.path.join(current_directory, relative_path_lake)
absolute_path_hwy = os.path.join(current_directory, relative_path_hwy)
absolute_path_watershed = os.path.join(current_directory, relative_path_watershed)

#load in shapefile data
arterial_streets = gpd.read_file(absolute_path_arterial_streets)
local_roads = gpd.read_file(absolute_path_local_roads)
lake = gpd.read_file(absolute_path_lake)
hwy = gpd.read_file(absolute_path_hwy)
watershed = gpd.read_file(absolute_path_watershed)


#custom colors
colors = ['#174d26', '#4d8657', '#311515', '#b79a8a', '#ded3ab']

arterial = gpd.GeoDataFrame(data = arterial_streets.geometry)
local = gpd.GeoDataFrame(data = local_roads.geometry)
streets = pandas.concat([arterial, local])

#create color column for each street and assign each street a random color based on our custom color list
for i in range(len(streets)):
    streets.loc[streets.index[i], "color"] = random.choice(colors)   

#create polygons from the street linestrings
union_poly = shapely.ops.unary_union(streets.geometry)
polygons = gpd.GeoSeries(polygonize(union_poly))                              

#set figure size and border before plotting
plt.rc('figure', figsize=(6, 6))
plt.rc('axes', edgecolor = '#f3f0d7', linewidth = 10)

#plot polygons, streets, lake, and hwys
ax1 = watershed.plot(color = '#ded3ab')
polygons.plot(color = streets['color'], ax = ax1)
hwy.plot(color = '#f3f0d7', linewidth = 2, ax = ax1)
streets.plot(color = '#f3f0d7', linewidth = 0.75, ax = ax1)
lake.plot(color = '#f3f0d7', edgecolor = '#f3f0d7', linewidth = 2, ax = ax1)

#set scale/limits for how much of the map we see
ax1.set_xlim(-122.418, -122.267)
ax1.set_ylim(47.5759, 47.6801)
plt.subplots_adjust(top = 1, right = 1, bottom = 0, left = 0)

plt.savefig('Seattle', dpi = 300)

#plt.show()
