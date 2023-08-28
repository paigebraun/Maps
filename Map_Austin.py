import geopandas as gpd
import numpy as np
import random
import matplotlib.pyplot as plt
import shapely.ops
from shapely.ops import polygonize
import os

#get current working directory
current_directory = os.getcwd()

#define relative path to shapefile data
relative_path_street = 'kx-travis-county-2layers-SHP/city-of-austin-texas-street-centerline/city-of-austin-texas-street-centerline.shp'
relative_path_lake = 'kx-travis-county-2layers-SHP/city-of-austin-texas-lakes/city-of-austin-texas-lakes.shp'

#join current directory with relative path to create absolute path for shapefile data
absolute_path_street = os.path.join(current_directory, relative_path_street)
absolute_path_lake = os.path.join(current_directory, relative_path_lake)

#load in shapefile data
streets = gpd.read_file(absolute_path_street)
lake = gpd.read_file(absolute_path_lake)

#custom colors
colors = ['#404c3a', '#ddd3ab', '#cb8729', '#877d5d', '#85ab87', '#43b192', '#65533a', '#c4a065','#f68e18']

#create color column for each street and assign each street a random color based on our custom color list
for i in range(len(streets)):
    streets.loc[streets.index[i], "color"] = random.choice(colors) 

#create polygons from the street linestrings
union_poly = shapely.ops.unary_union(streets.geometry)
polygons = gpd.GeoSeries(polygonize(union_poly))

#get list of hwys and roads that we want to be plotted with bigger linewidth to stand out
hwy_id = []
for j in range(len(streets)):
    if streets['street_typ'][j] == 'HWY' or streets['street_typ'][j] == 'SVRD' or streets['street_typ'][j] == 'EXPY':
        hwy_id.append(j)

hwy_geom = []
for k in range(len(hwy_id)):
    hwy_geom.append(streets.at[hwy_id[k], "geometry"])
hwy = gpd.GeoSeries(hwy_geom)

#set figure size and border before plotting
plt.rc('figure', figsize=(6, 6))
plt.rc('axes', edgecolor = '#f3f0d7', linewidth = 10)

#plot polygons, streets, lake, and hwys
ax1 = polygons.plot(color = streets['color'])
streets.plot(color = '#f3f0d7', linewidth = 0.75, ax = ax1)
lake.plot(color = '#f3f0d7', edgecolor = '#f3f0d7', linewidth = 2, ax = ax1)
hwy.plot(color = '#f3f0d7', linewidth = 2.5, ax = ax1)

#set scale/limits for how much of the map we see
ax1.set_xlim(-97.789, -97.679)
ax1.set_ylim(30.229, 30.339)
plt.subplots_adjust(top = 1, right = 1, bottom = 0, left = 0)

plt.savefig('Austin', dpi = 300)
