"""
Scriptname: 04_Plot_Densitymap
Author: Merel Timmermans
Coursename: Data Science for Smart Environments
Coursecode: GRS35306
Date: 28-04-2023
Purpose of script: This is a script that creates folium.html maps of the density of spatial tweets
Output of script: 1) folium.html map of all the spatial tweets as a heatmap
                  2) folium.html map of all the spatial tweets from humans as a heatmap
                  3) folium.html map of all the spatial tweets from users of the SwarmApp
"""

### IMPORT THE NECESSARY LIBRARIES ###
import pandas as pd
import folium
import geopandas as gpd
from folium import plugins


############################# PLOT ALL THE SPATIAL TWEET POINTS #############################
# Read the datafile and load it as a dataframe
sp_df = pd.read_csv('data/preprocessed_data/all_user_time_geo_data.csv')

# Make it a spatial dataframe
# Source: 1, 2

# Get the longitude and latitude values
x = sp_df.longitude
y = sp_df.latitude

# Turn the dataframe into a spatial dataframe
sp_df = gpd.GeoDataFrame(sp_df, geometry=gpd.points_from_xy(x, y))

# Delete some variables to clean up memory
del(x,y)

# Initialize the map
usersmap = folium.Map([52.3826, 4.91378], zoom_start=13, tiles="OpenStreetMap")

# Re-project the dataset to the correct crs
sp_df = sp_df.set_crs("EPSG:4289")

# Make a dataset for the density_data
# Source: 3
density_data = [[point.xy[1][0], point.xy[0][0]] for point in sp_df.geometry]

# Add the tweet locations
# Source: 5
plugins.HeatMap(density_data, name="tweet_density", max_zoom=18, radius=12, blur=5).add_to(usersmap)

# Save the map to the output, go to the output map if you want to open the map
usersmap.save('output/all_spatial_density_map.html')



##################### PLOT THE POINTS FOR ALL THE TWEETS THAT ARE NOT MADE BY A BOT #####################
# Read the file
sp_df = pd.read_csv('output/all_spatial_points_non_bots.csv')

# Make it a spatial dataframe
# Source: 1, 2

# Get the longitude and latitude values
x = sp_df.longitude
y = sp_df.latitude

# Turn the dataframe into a spatial dataframe
sp_df = gpd.GeoDataFrame(sp_df, geometry=gpd.points_from_xy(x, y))

# Delete some variables to clean up memory
del(x,y)

# Initialize the map
usersmap = folium.Map([52.3826, 4.91378], zoom_start=13, tiles="OpenStreetMap")

# Re-project the dataset to the correct crs
sp_df = sp_df.set_crs("EPSG:4289")

# Make a dataset for the density_data
# Source: 3
density_data = [[point.xy[1][0], point.xy[0][0]] for point in sp_df.geometry]

# Add the tweet locations
# Source: 5
plugins.HeatMap(density_data, name="tweet_density", max_zoom=18, radius=12, blur=5).add_to(usersmap)


# Save the map to the output, go to the output map if you want to open the map
usersmap.save('output/non_bots_density_map.html')


##################################### PLOT ALL THE SWARM USERS #####################################
sp_df = pd.read_csv('data/preprocessed_data/swarm_timelines_users.csv')

# Make it a spatial dataframe
# Source: 1, 2

# Get the longitude and latitude values
x = sp_df.longitude
y = sp_df.latitude

# Turn the dataframe into a spatial dataframe
sp_df = gpd.GeoDataFrame(sp_df, geometry=gpd.points_from_xy(x, y))

# Delete some variables to clean up memory
del(x,y)

# Initialize the map
usersmap = folium.Map([52.3826, 4.91378], zoom_start=13, tiles="OpenStreetMap")

# Re-project the dataset to the correct crs
sp_df = sp_df.set_crs("EPSG:4289")

# Make a dataset for the density_data
# Source: 3
density_data = [[point.xy[1][0], point.xy[0][0]] for point in sp_df.geometry]

# Add the tweet locations
# Source: 5
plugins.HeatMap(density_data, name="tweet_density", max_zoom=18, radius=6, blur=1).add_to(usersmap)

# Save the map to the output, go to the output map if you want to open the map)
usersmap.save('output/swarm_users_density_map.html')