# Under the Weather
Repository for the project of group Social Media 2 for course GRS-35306 Data Science for Smart Environments.

---

### Items in this repository:
This repository contains scripts and datafiles to recreate the research and show the results of the analysis of the Twitter data. This data was harvested between the 28th of March and the 21st of April. 
Here is a short summary of the items.

#### Scripts 
In the directory "scripts", the following scripts can be found:

- **01_twarc_commands.txt**: The twarc command lines to run in the console to retireve data from Twitter.

- **02_Read_Json_Create_CSVFiles.py**: This is the script that takes three .json files with data gathered from Twitter and combines them into two datasets.

- **03_Bot_Deletion.py**: This is a script to get rid of tweets from bots so we mostly have spatial data from humans. It can be that there are some bots left in the data because it is hard to realy define a bot. 

- **04_Count_Days.py**: This is a script that creates a dataset to count the amount of tweets that are made for the whole timeframe, for the spatial tweets and the spatial human tweets.

- **05_Extracting_Usernames_Swarmapp.py**: This is a script that extracts twitterdata from a .json file with twitterdata from users of the Swarm app in the Netherlands.

- **06_Merging_Timelines_Users_Swarmapp.py**: This is a script that takes multiple .json from Swarm app users and combines it into one big dataset.

- **07_Plot_Densitymap.py**: This is a script that creates folium.html maps of the density of spatial tweets from three diffrent datasets.

- **08_GetRainyGetDry_functions.R**: This is the script that determined the different weatherconditions and formed the basis for the other R script.

- **09_WeatherType_and_Tweets.R**: This is the script that creates the data on the weather types.


#### Other files

- **README.txt**: The .txt file containing the information you are now reading

- **chatgpt_history_reading_tweetdata.txt**: A .txt file that contains the chat history of the authors and ChatGPT that was used to write some parts of the scripts.

- **preprocessed_data.zip**: A .zip file that contains preprocessed data. This preprocessed data is included because the scripts for reading .jsons take a long time and this saves time and memory space.

#### What you also maybe need:
This is a WeTransfer link to download the raw data. It is a .zip file that is 710 MB so it cannot be uploaded directly to GitHub. The link was made on April 27th and it expires on May 4th 2023! To request a new link, please write to kuba.kowalski@wur.nl

https://we.tl/t-j86yRM38pt
---

### How to run to reproduce data:

**Data check**
First, make sure you have a data and output map in the same directory where you will be running the scripts in.
Make sure the following files are in the right directory when running the scripts:

    __Raw data needed to run scripts 2, 5, 6, 8 and 9__
    
    1. tweets_amsterdam_400k_07-04-2023.json
    2. tweets_amsterdam_400k_13-04-2023.json
    3. tweets_amsterdam_21-04-2023_from12-04_to21-04.json
    4. tweets_swarm.json
    5. neerslaggeg_AMSTERDAM_441.xlsx
    6. Tweets_BS_amsterdam.csv.xlsx
    7. knmi.xlsx
    8. swarm filemap
    
The preprocessed data is needed in script 3, 4, 7 and 9.
Also check if the directories in the scripts are correct before running each file.
   
**Libraries check**    
Secondly, check if the following libraries are installed in the environment in which you run the Python scripts:
    1. Twarc1
    2. pandas
    3. geopandas
    4. glob
    5. os
    6. folium
 
If they are not installed, install them.  

**Running the scripts**      
Next, run the scripts in the order. The scripts have the numbers of the order in front of them so hopefully it shouldn't be that complicated.

1. **01_twarc_commands.txt**: Open the console and run each line in it that does not have a _#_ in front of it.
After running these command lines in the console you should get the following output:
    > - tweets_amsterdam_21-04-2023.json

2. **02_Read_Json_Create_CSVFiles.py**: 
It is important to note that this script takes a long time to run because it has to load all the .json data. (It can take around 25 minutes.)
To make sure that your program does not crash during running this script, close unnecessary programs on your computer that are running in the background. 
After running this file you should have the following data:
    > - timeframe_all_tweetdata.csv
    > - all_user_time_geo_data.csv
 
3. **03_Bot_Deletion.py**: 
Look at this script first and see if you might need to add some more users which are bots or not. After this check-up you can run the script.
It should give you the following output data:
    > - all_spatial_points_non_bots.csv

4. **04_Count_Days.py**: 
Before you run this script with other data than used for this project, check the bot dates to see if there are more days missing and adapt the script around line 65.
If all goes well with this script, it should produce the following output:
    > - total_tweets_stats.csv

5. **05_Extracting_Usernames_Swarmapp.py**: 
This is a script that extracts twitterdata from a .json file with twitterdata from users of the Swarm app. It is used to get the names of Swarm users that have been in Amsterdam to get their timeline data. 
After running the script, you get the following as output:
    > - tweets_swarm_usernames.csv

6. **06_Merging_Timelines_Users_Swarmapp.py**:
This is a script to combine multiple .jsons of Swarm app users that have been in Amsterdam into one dataset that contains a datetime stamp, geometry and some user information. 
After the script is run, it produces the following output:
    > - tweets_swarm_coordinates_all.csv

7. **07_Plot_Densitymap.py**:
Check if all the data from the previous scripts and the swarm users are there before running the script. 
You can change the parameters of max_zoom, radius and blur when producing the heatmap.
The script should produce the following output:
    > - non_bots_density_map.html
    > - all_spatial_density_map.html
    > - swarm_users_density_map.htm

8. **08_GetRainyGetDry_functions.R**: 
This script writen in R is the setup for the next R script. It contains functions that determine wether a day is wet or dry. This script produces no output.

9. **09_WeatherType_and_Tweets.R**:
This is a script that combines the weatherdata with the twitter data to make one dataset that contains which weather it was on which day and the amount of tweets made that day.
The output of this script is the following:
    > - Weather_data.xlsx
      
--- 

### Discussion and difficulties
Some of the issues we ran into were the reading of the .json files. Another issue was the size of the .json files. Opening them once they were a dataframe gave an issue that it was too big and no action could be taken to ameliorate this.
This project also has some difficulties. Working with Twitter data for example is in the gray area of research ethics. We use data that was not intended for this purpose and the research subjects did not give informed consent for their data to be used. Most importantly, Twitter usernames were used to harvest data specifically of the Swarm app users. Consequently, this study infringes directly upon their privacy. 
When pre-processing the data by removing bots, we discovered that some bots could simply not be removed without overwhelming risk of removing actual human users. Based on visual inspection of the results, we suspect that a non-insignificant number of bots remained even after pre-processing. 
Another difficulty in this project was the limit of time and the level in skills in programming. If there was more time, some maps would be made more aesthethically pleasing and saved in an easily shareable format instead of an html map. This problem was now solved by importing the data as a .csv file with coordinate fields in ArcGIS pro.
The last difficulty is in the use of Anaconda and the problems it would sometimes give with installing packages.
Finally, working with WFS data that would not work due to various technical issues which range from outdated links to inefficient scripts.

### Conclusion
Ultimately, the project proved to be extremely rewarding and informative despite its many challenges. We used a plethora of tools which are standard in our studies, but are rarely used in combination. The use of the API while frustrating showed us both the pitfalls and the enourmous promise of social media data in research. The project will most certainly inform all of our future endeavours in this domain of research as we will try to avoid the mistakes that we made here. Still, nearly all of these mistakes were a vital part of the learning process and they could not have been avoided without severely limiting the ambitious goals of our reserach. 
   
---    
#### Sources used in these scripts:

These are sources corresponding to the sourcenumbers spread accross the four python files that create and read data

Creating a spatial dataset 
1) Droping data from a pandas.dataframe:
    > https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
    
2) Turning a pandas.dataframe into a geopandas dataframe: 
    > https://geopandas.org/en/stable/gallery/create_geopandas_from_pandas.html

3) Plotting heatmaps with folium: 
    > https://geopandas.org/en/stable/gallery/plotting_with_folium.html 

4) Getting the timerange from the data:
    > https://thispointer.com/pandas-select-rows-within-a-date-range/

5) Adding the locations of tweet to a folium map:
    > https://python-visualization.github.io/folium/plugins.html 

6) Various questions about reading a .json file in Python and creating date time variables:
    > Chat GPT. History of the conversation that was used can be found in the file: chatgpt_history_reading_tweetdata.txt

7) How to get the tail and head of a dataframe:
   > https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.tail.html
   
8) How to get the uniqe values of dates and sort them in the right order:
    > https://medium.com/nerd-for-tech/how-to-plot-timeseries-data-in-python-and-plotly-1382d205cc2

9) How to create a pandas.series:
    > https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html
    
10) How to add a pandas.series to another pandas.series: 
    > https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.add.html 
    
11) How to join two pandas.dataframes on the same indexnumber:
    > https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html 
    
12) How to do calculations with columns to create output in a new column:
    > https://www.statology.org/pandas-combine-two-columns/ # doing calculation with columns

13) How to round off numbers of a cell in a pandas.dataframe:
    > https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.round.html

14) How to import all .json files from the directory and merge them
    > https://softhints.com/merge-multiple-json-files-pandas-dataframe/
    
    
---
#### Authors
   > Kees Dings, Mehala Koneru, Kuba Kowalski, Kross Lin, Emily van Lookeren Campagne, Merel Timmermans
    
   > This project was done for the course 'GRS35309 Data Science for Smart Environments' at the Wageningen University
    
   > April 2023
