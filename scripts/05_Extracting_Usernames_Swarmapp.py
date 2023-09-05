# -*- coding: utf-8 -*-
"""
Getting usernames from JSON of SwarmApp users

Created on Tue Apr 18 15:46:58 2023

@author: Merel, Kuba
"""

# import the libraries
import pandas as pd

## LOAD THE JSON FILE(S) OF SWARMAPP USERS
# Load SwarmApp jsonfile as a variable
jsonObj= pd.read_json("data/raw_data/tweets_swarm.json", lines=True)

# Drop all columns that don't have important information/ Keep the columns 'created at', 'geo', 'user'
jsonObj_spat = jsonObj.drop(['id', 'id_str', 'truncated',
       'display_text_range', 'entities', 'metadata', 'source',
       'in_reply_to_status_id', 'in_reply_to_status_id_str',
       'in_reply_to_user_id', 'in_reply_to_user_id_str',
       'in_reply_to_screen_name', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count',
       'favorited', 'retweeted', 'possibly_sensitive', 'lang',
       'extended_entities', 'place', 'full_text', 'coordinates', 'retweeted_status'], axis=1)

# Delete the huge variable to free memory space
del(jsonObj)

# Drop every row that has a NA (which in this case are all the rows without a geolocation)
jsonObj_spat = jsonObj_spat.dropna()

## GET THE SPATIAL INFORMATION
# Open a list to store the spatial information
sp_data = []

# Asscribe the spatial information to that list
sp_data = jsonObj_spat['user'].to_list()

# Make a dataframe that splits the list items into the type of geometry and coordinates
# Source: 6
sp_df = pd.DataFrame(sp_data, columns = ['id', 'screen_name'])

# Export the list of usernames of SwarmApp users to .csv
sp_df.to_csv('output/tweets_swarm_usernames.csv')


