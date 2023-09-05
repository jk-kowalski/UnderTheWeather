#Author: Kees

install.packages("readxl")
library(readxl)

#read in excel knmi data
Precipitation <- read_excel("neerslaggeg_AMSTERDAM_441.xlsx", sheet = "neerslaggeg_AMSTERDAM_441")

#Remove NA columns
Precipitation <- data.frame(Precipitation[c('STN', 'YYYYMMDD', "RD")])

#Change YYYYMMDD column to YYYY-MM-DD
names(Precipitation)[names(Precipitation) == 'YYYYMMDD'] <- 'date'
Precipitation$date <- as.Date(as.character(Precipitation$date), format = '%Y%m%d')

#Define rainy function
GetRainy <- function(startdate, enddate, rain_threshold){ #dates in Y-m-d, threshold in 0.1mm/day
  subset <- Precipitation[Precipitation$date >= as.Date(startdate) & Precipitation$date <= as.Date(enddate), ] #Make a subset of timeframe
  return(subset[subset$RD >= rain_threshold, ]$date) #return timeframes of rainy days
  }

#Define dry function
GetDry <- function(startdate, enddate, rain_threshold){ #dates in Y-m-d, threshold in 0.1 mm/day
  subset <- Precipitation[Precipitation$date >= as.Date(startdate) & Precipitation$date <= as.Date(enddate), ] #Make a subset of timeframe
  return(subset[subset$RD < rain_threshold, ]$date) #return timeframes of dry days
}


#Read tweet data
Tweets <- read_excel("Tweets_BS_amsterdam.csv.xlsx", sheet = "Tweets_BS_amsterdam")
#Remove unnecessary rows and columns
Tweets <- Tweets[complete.cases(Tweets$tweet_date), ]
Tweets <- Tweets[, -c(8:19)]

#Transfer serial date of excel format into date (yyyy-mm-dd)
Tweets$tweet_date <- as.Date(as.numeric(Tweets$tweet_date), origin = "1899-12-30")
#Remove NA and outlier dates
Tweets <- Tweets[complete.cases(Tweets$tweet_date), ] #Remove NA's based on date
Tweets <- Tweets[complete.cases(Tweets$latitude) & complete.cases(Tweets$longitude), ] #Remove NA's based on location
Tweets <- Tweets[-(which.min(Tweets$tweet_date)), ] #Remove tweet supposedly from 1905

#Check whether date was rainy or dry and add to column (takes some time)
for (i in seq_along(Tweets$tweet_date)){ 
  if (Tweets$tweet_date[i] %in% GetRainy((min(Tweets$tweet_date)), (max(Tweets$tweet_date)), 2)){
    Tweets$weather[i] <- 'Rainy'
  } else if (Tweets$tweet_date[i] %in% GetDry((min(Tweets$tweet_date)), (max(Tweets$tweet_date)), 2)){
    Tweets$weather[i] <- 'Dry'
  }
}

#Add season column to Tweet dataset based on month (takes some time)
for (i in seq_along(Tweets$tweet_date)){ 
  if (format(as.Date(Tweets$tweet_date[i]), "%m") %in% c('12', '01', '02')) {
    Tweets$season[i] <- 'Winter'
  } else if (format(as.Date(Tweets$tweet_date[i]), "%m") %in% c('03', '04', '05')){
    Tweets$season[i] <- 'Spring'
  } else if (format(as.Date(Tweets$tweet_date[i]), "%m") %in% c('06', '07', '08')){
    Tweets$season[i] <- 'Summer'
  } else if (format(as.Date(Tweets$tweet_date[i]), "%m") %in% c('09', '10', '11')){
      Tweets$season[i] <- 'Autumn'
  }}

#Add points to map per season:
Seasonal_diff <- function(season, weather_condition){
  Season_weather <- Tweets[Tweets$season == season & Tweets$weather == weather_condition, ]
  title = paste0('Spatial distribution of Tweets in ', season, ' with ', weather_condition, ' weather')
  if (season != 'Spring'){
    return(plot(Season_weather$longitude, Season_weather$latitude, xlab = 'longitude', ylab = 'latitude', main = title))}
  else if (season == 'Spring'){
    Season_weather <- Season_weather[-order(Season_weather$longitude)[1:2],] #remove 2 outliers in spring
    return(plot(Season_weather$longitude, Season_weather$latitude, xlab = 'longitude', ylab = 'latitude', main = title))}
}

par(mfrow = c(1,2))
Seasonal_diff('Summer', 'Dry')
Seasonal_diff('Summer', 'Rainy')


# Load rgdal package
library(rgdal)
library(sf)
library(terra)

pand <- readOGR('bgt_pand.gml', layer = 'wkbPolygon')
