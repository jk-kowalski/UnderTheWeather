"""
Scriptname: 02_Bot_Deletion
Author: Merel Timmermans
Coursename: Data Science for Smart Environments
Coursecode: GRS35306
Date: 28-04-2023
Purpose of script: This is a script to get rid of tweets from bots so we mostly have
            spatial data from humans. It can be that there are some bots left in the data because
            it is hard to realy define a bot. 
Output of script: 1) .csv that contains only time and spatial data from humans
"""

### IMPORT THE NECESSARY LIBRARIES ###
import pandas as pd
import geopandas

# Read the .csv file
user_geo_combi = pd.read_csv('data/preprocessed_data/all_user_time_geo_data.csv')

# Make an open list to ascribe bots to
bots = []

# First category:
# P2000 and other services that fall under the 112 help and such
bots = user_geo_combi[ user_geo_combi['name'] == 'p2000amsterdam'].index
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'P2000 Lifeliners'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'Burgernet N-Holland'].index)

# Second category:
# Bots that post when there is a job offer
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == '4-freelancers.nl'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'TMJ-NET Jobs'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'TMJ-NET Retail Jobs'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'TMJ-NET Mgmt. Jobs'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'TMJ-NET HR Jobs'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'TMJ-NET Sales Jobs'].index)

# Third category: 
# Something that is a bot because it tweets from the same location way to quick called 
# This is done with location instead of name because of the layout of the name creating non readable unicode (𝓟𝓻𝓮𝓼𝓼 𝓡𝓮𝓿𝓲𝓮w)
bots = bots.append(user_geo_combi[ user_geo_combi['geometry'] == 'POINT (4.90163963 52.36675189)'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['geometry'] == 'POINT (4.90191913 52.36700757)'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['geometry'] == 'POINT (4.90240926 52.36723194)'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['geometry'] == 'POINT (4.90312633 52.36713)'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['geometry'] == 'POINT (4.90313337 52.36730513)'].index)

# Fourth category:
# Bot with local data if a bridge is open
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'BrugOpen'].index)

# Fifth category:
# Bots with data on a specific distribution market
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'Market Forecast'].index)
bots = bots.append(user_geo_combi[ user_geo_combi['name'] == 'Top Gateways - best payments providers processors'].index)


# Now we use the list with bots to drop all the bots from the dataset
user_geo_combi.drop(bots, inplace = True)

# Drop an unused column from the dataset
sp_df = user_geo_combi.drop(['Unnamed: 0',], axis=1)

# make it a spatial dataframe again
x = sp_df.longitude
y = sp_df.latitude

# Make it a spatial data frame
sp_df = geopandas.GeoDataFrame(sp_df, geometry=geopandas.points_from_xy(x, y))

# Drop some variables to clean memory space
del(x,y,bots)

# Save the output to a .csv file
sp_df.to_csv('output/all_spatial_points_non_bots.csv')

