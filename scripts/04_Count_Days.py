"""
Scriptname: 03_Count_Days
Author: Merel Timmermans
Coursename: Data Science for Smart Environments
Coursecode: GRS35306
Date: 28-04-2023
Purpose of script: This is a script that creates a dataset to count the amount of tweets that are made
                for the whole timeframe, for the spatial tweets and the spatial human tweets.
Output of script: 1) .csv that contains the amount of tweets made and percentages
"""

### IMPORT THE NECESSARY LIBRARIES ###
import pandas as pd

### GET THE DAYS AND AMOUNT OF ALL THE TWEETS ###
# Load in the .csv with the dates and times of all the tweets
all_time = pd.read_csv('data/preprocessed_data/timeframe_all_tweetdata.csv')

# Count all the rows that are for uniqe dates and sort them
# Source: 8
all_time_count = pd.Series(all_time['date']).value_counts().sort_index()

# Turn the series into a dataframe
all_time_count = pd.DataFrame(all_time_count)

# Rename the columns
all_time_count['count_of_tweets'] = all_time_count['date'] 

# Drop unnecessary column
all_time_count = all_time_count.drop(['date'], axis=1)

# Delete variable to clean up memory
del(all_time)

### GET THE DAYS AND NUMBER OF TWEETS THAT ARE SPATIAL ###
# Load the corresonding .csv file
all_spatial = pd.read_csv('data/preprocessed_data/all_user_time_geo_data.csv') 

# Count how much tweets were done on unique dates and sort them
# Source: 8
all_spatial_count = pd.Series(all_spatial['date']).value_counts().sort_index()

# Turn the series into a dataframe
all_spatial_count = pd.DataFrame(all_spatial_count)

# Rename the column
all_spatial_count['count_of_spatial_tweets'] = all_spatial_count['date'] 

# Drop unnecessary column
all_spatial_count = all_spatial_count.drop(['date'], axis=1)

# Delete variable to clean up memory
del(all_spatial)


### GET THE DAYS AND NUMBER OF ALL THE SPATIAL TWEETS THAT AREN'T BOTS ###
# Load the correct .csv file
users_df = pd.read_csv('output/all_spatial_points_non_bots.csv')

# While running the script there was an error because there was a date missing
# So now a part to fill in an extra date

# Create a new dictionary with the date and amount of tweets
# Source: 9
new_date = {'2023-03-28': 0 } 

# Turn this dictionary into a series
new_date = pd.Series(data = new_date, index=['2023-03-28'])

# Count the unique vaulues of the dates
users_df = pd.Series(users_df['date']).value_counts()

# Add the own created date series to the count series
# Source: 10
users_df = users_df.add(new_date, fill_value=0) 

# Sort the values
users_df = users_df.sort_index()

# Turn the Series back into a dataframe
users_df = pd.DataFrame(users_df)

# Change the name of the column
users_df['nr_of_spatial_nonbots'] = users_df[0] 

# Drop the column
users_df = users_df.drop([0], axis=1)

# Delete variable to clean up memory
del(new_date)

### MAKE A DATAFRAME WITH ALL INFORMATION ###
# Join the two dataframes
# Source: 11
total_tweets = all_time_count.join(all_spatial_count)
total_tweets = total_tweets.join(users_df)


### DO SOME CALCULATIONS ###
# Caluclate the percentages of how much of the tweets are actually spatial and spatial_non_bots
# Source: 12, 13
total_tweets['percentage_spatial'] = ((total_tweets['count_of_spatial_tweets']/total_tweets['count_of_tweets'])*100).round(decimals = 2) 
total_tweets['percentage_nonbots_spatial'] = ((total_tweets['nr_of_spatial_nonbots']/total_tweets['count_of_tweets'])*100).round(decimals = 2)

### SAVE IT ###
total_tweets.to_csv('output/total_tweets_stats.csv')
