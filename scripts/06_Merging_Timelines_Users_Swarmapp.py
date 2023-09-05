# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 15:29:11 2023

@author: kubak
"""
import pandas as pd
import glob, os
import geopandas

# Selecting the directory which contains all timelines in seperate .json files
json_dir = 'data/raw_data/swarm'

# Importing all individual .json files from the directory
json_pattern = os.path.join(json_dir, '*.json') # source: 14 
file_list = glob.glob(json_pattern)

# Merging the imported .json files
dfs = []
for file in file_list:
	df_temp = pd.read_json(file,  lines=True)
	df_temp['source'] = file.rsplit("/", 1)[-1]
	dfs.append(df_temp)
df = pd.concat(dfs)

df.columns
   
# Drop all columns that don't have important information/ Keep the columns 'created at', 'geo', 'user'
jsonObj_spat = df.drop(['id', 'id_str', 'truncated',
       'display_text_range', 'entities', 'source',
       'in_reply_to_status_id', 'in_reply_to_status_id_str',
       'in_reply_to_user_id', 'in_reply_to_user_id_str',
       'in_reply_to_screen_name', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count',
       'favorited', 'retweeted', 'retweeted_status', 'possibly_sensitive', 'lang',
       'extended_entities', 'quoted_status_id', 'quoted_status_id_str',
       'quoted_status', 'place', 'full_text', 'coordinates','withheld_in_countries','quoted_status_permalink',
       'withheld_scope', 'withheld_copyright'], axis=1) 

# Drop every row that has a NA (which in this case are all the rows without a geolocation)
jsonObj_spat = jsonObj_spat.dropna()

## GET THE SPATIAL INFORMATION
# Open a list to store the spatial information
sp_data = []

# Ascribe the spatial information to that list
sp_data = jsonObj_spat['geo'].to_list()

# Make a dataframe that splits the list items into the type of geometry and coordinates
sp_df = pd.DataFrame(sp_data, columns = ['type', 'coordinates']) # source = chatGPT # source 6

# Get the lat and lon from the coordinates
sp_df[['latitude', 'longitude']] = pd.DataFrame(sp_df['coordinates'].to_list(), index=sp_df.index)

# Drop the column coordinates because you only need the lat and lon
sp_df = sp_df.drop('coordinates', axis=1)

# Ascribe the values of the lat and lon to a variable
x = sp_df.longitude
y = sp_df.latitude

# Make it a spatial data frame using the variables x and y
sp_df = geopandas.GeoDataFrame(sp_df, geometry=geopandas.points_from_xy(x, y))

# Clean up the variables
del(x,y,sp_data)


## TIME INFORMATION
# Create a list and store the date and time to that list
time_data = []
time_data = jsonObj_spat['created_at'].to_list()

# turn those list into a dataframe and combine both
time_df = pd.DataFrame (time_data, columns = ['value'])
time_df['value'] = pd.to_datetime(time_df['value'])

# create new columns for date and time # source ChatGPT
time_df['date'] = time_df['value'].dt.date
time_df['time'] = time_df['value'].dt.time

del(time_data)


## USER INFORMATION
# get a list with the users that have tweeted the spatial information to get rid of bots
user_data = []
user_data = jsonObj_spat['user'].to_list()
user_df = pd.DataFrame (user_data, columns = ['name', 'location'])

del(user_data)

#join the datasets together and select only the BrugOpen dataset
user_geo_time_combi = sp_df.join(time_df)
user_geo_time_combi = user_geo_time_combi.join(user_df)

#del(time_df,user_df,sp_df)
del(time_df, sp_df)
# clean up the dataset
user_geo_time_combi = user_geo_time_combi.drop(['value', 'location'], axis=1)

# save it as a csv to have the data easily accessible in the future
user_geo_time_combi.to_csv('C:/GRS35306/merel_scripts/output/tweets_swarm_coordinates_all.csv')
