"""
Scriptname: 01_Read_Json_Create_CSVFiles
Author: Merel Timmermans
Coursename: Data Science for Smart Environments
Coursecode: GRS35306
Date: 28-04-2023
Purpose of script: This is the script that takes the 3 .json files and combines them
    into two datasets.
Output of script: 1) .csv that contains the complete timeframe of when the tweets was taken
                  2) .csv that contains spatial information as a point, usernams and time when the tweet was made
"""

### IMPORT THE NECESSARY LIBRARIES ###
import pandas as pd
import geopandas


### LOAD THE JSON FILES ###
# Load the jsonfiles as a variable
json7 = pd.read_json("data/raw_data/tweets_amsterdam_400k_07-04-2023.json", lines=True)
json13 = pd.read_json("data/raw_data/tweets_amsterdam_400k_13-04-2023.json", lines=True)
json21 = pd.read_json("data/raw_data/tweets_amsterdam_21-04-2023_from12-04_to21-04.json", lines=True)


### GETTING THE RIGHT TIMES ###

# Select the time from the dataset that is later in time, to prevent overlap of data 
# Source: 7

# In this script this step has already been done. 
# But for future refrences the following can be done:
# To get the min and max dates of the dataframe run the following codes in the console: 
# "print(json7.head(1))" and "print(json13.tail(1))" 
# Then copy and paste the min value into the startdate and the max value in enddate 



### SELECTING THE TIMEFRAME TO PREVENT OVERLAP OF DATA ###
# Source: 4
# Set the start and enddate of the timeframe when people tweeted
startdate = "2023-04-06 19:48:32+00:00"
enddate = "2023-04-12 22:54:00+00:00"

# Get the tweets that were tweeted in between those times
json13 = json13.loc[(json13['created_at']> startdate) & (json13['created_at'] <= enddate )]

# Repeat the previous steps if there is a third dataset
startdate = "2023-04-12 22:54:00+00:00" 
enddate = "2023-04-21 10:50:31+00:00"

json21 = json21.loc[(json21['created_at']> startdate) & (json21['created_at'] <= enddate )]

# Delete some variables to clean up working memory
del(startdate, enddate)


### MERGING THE DATAFRAMES ###
# Join the dataframes into one big dataframe
jsonObj = json7.append(json13)
jsonObj = jsonObj.append(json21)

# Delete some variables to clean up working memory
del(json13, json7, json21)


### SELECT ONLY THE NECESSARY COLUMNS FROM THE BIG DATAFRAME ###
# Drop all columns that don't have important information
# Source: 1
# Here we only keep the columns: 'created at', 'geo', 'user'
jsonObj_spat = jsonObj.drop(['id', 'id_str', 'truncated',
       'display_text_range', 'entities', 'metadata', 'source',
       'in_reply_to_status_id', 'in_reply_to_status_id_str',
       'in_reply_to_user_id', 'in_reply_to_user_id_str',
       'in_reply_to_screen_name', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count',
       'favorited', 'retweeted', 'possibly_sensitive', 'lang',
       'extended_entities', 'quoted_status_id', 'quoted_status_id_str',
       'quoted_status', 'place', 'full_text', 'coordinates','withheld_in_countries'], axis=1)

# Delete the huge variable to free memory space
del(jsonObj)


### MAKE THE FIRST CSV WITH ALL THE TIME INFORMATION ###
# Make an empty list
time_data = []

# Ascribe the timedata to the empty list 
time_data = jsonObj_spat['created_at'].to_list()

# Turn this list into a dataframe 
time_df = pd.DataFrame (time_data, columns = ['value'])

# Turn the variables into datetime variables
time_df['value'] = pd.to_datetime(time_df['value'])

# Create new columns to split date and time 
# Source: 6
time_df['date'] = time_df['value'].dt.date
time_df['time'] = time_df['value'].dt.time

# Drop unnecessary columns
time_df = time_df.drop(['value'], axis=1)

# Save it to a .csv
time_df.to_csv('data/timeframe_all_tweetdata.csv')

# Delete some variables to clean up working memory
del(time_data, time_df)


### MAKING THE CSV THAT HAS SPATIAL INFORMATION, USERS AND TIME ###
# Drop every row from the dataframe that has an NA
# For this dataframe that means each row without a geolocation
jsonObj_spat = jsonObj_spat.dropna()


## SPATIAL INFORMATION ###
# Open a list to store the spatial information
sp_data = []

# Ascribe the spatial information to that list
sp_data = jsonObj_spat['geo'].to_list()

# Make a dataframe that splits the list items into the type of geometry and coordinates
# Source: 6
sp_df = pd.DataFrame(sp_data, columns = ['type', 'coordinates']) 

# Get the latitude and longitude from the coordinates column
sp_df[['latitude', 'longitude']] = pd.DataFrame(sp_df['coordinates'].to_list(), index=sp_df.index)

# Drop the column coordinates because you only need the latitude and longitude
sp_df = sp_df.drop('coordinates', axis=1)


# Ascribe the values of the lat and lon to a variable
# Source: 1, 2
x = sp_df.longitude
y = sp_df.latitude

# Turn the dataframe into a spatial data frame using the variables x and y
sp_df = geopandas.GeoDataFrame(sp_df, geometry=geopandas.points_from_xy(x, y))
 
# Clean up the variables to save memory space
del(x,y,sp_data)


## TIME INFORMATION ##
# Create a list and store the date and time to that list
time_data = []
time_data = jsonObj_spat['created_at'].to_list()

# Turn those list into a dataframe
time_df = pd.DataFrame (time_data, columns = ['value'])

# Make the variable a datetime variable
time_df['value'] = pd.to_datetime(time_df['value'])

# Create new columns for date and time 
# Source: 6
time_df['date'] = time_df['value'].dt.date
time_df['time'] = time_df['value'].dt.time

# Clean up the variables to save memory space
del(time_data)


## USER INFORMATION ##
# This is to get rid of bots easily in another script

# Make an empty list to store data and store data into that list
user_data = []
user_data = jsonObj_spat['user'].to_list()

# Get the proper columns and make a dataframe
user_df = pd.DataFrame (user_data, columns = ['name', 'location'])

# Clean up the variables to save memory space
del(user_data)


## JOIN THE DATAFRAMES TOGETHER ##

#join the datasets together
user_geo_time_combi = sp_df.join(time_df)
user_geo_time_combi = user_geo_time_combi.join(user_df)

# Clean up the variables to save memory space
del(time_df,user_df,sp_df)

# Clean up the dataset
user_geo_time_combi = user_geo_time_combi.drop(['value', 'location'], axis=1)

# Save it as a .csv to have the data easily accessible in the future
user_geo_time_combi.to_csv('data/all_user_time_geo_data.csv')
