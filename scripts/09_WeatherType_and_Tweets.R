#Author: Kees

install.packages("readxl")
library(readxl)

#read in excel knmi data
knmi <- read_excel("knmi.xlsx", sheet = "etmgeg_240", col_types = 'numeric')

#Only keep precipitation (RH in 0.1mm), Sunshine (SP in % from possible sunshine), Average temperature (TG in 0.1 degrees Celsius) columns
knmi <- data.frame(knmi[c('YYYYMMDD', 'RH', 'SP', 'TG')])

#Remove rows with NA values
knmi <- knmi[complete.cases(knmi$RH) & complete.cases(knmi$SP) & complete.cases(knmi$TG), ]

#Change YYYYMMDD column to YYYY-MM-DD
names(knmi)[names(knmi) == 'YYYYMMDD'] <- 'date'
knmi$date <- as.Date(as.character(knmi$date), format = '%Y%m%d')

#Change columns to right units
knmi$TG <- knmi$TG / 10
knmi$RH <- knmi$RH / 10

#Weather types are as follows:
#1. Dry-Sunny-Hot
# Precipitation < 0.2 mm, Sunshine > 50%, Temperature > 10 degrees Celsius
#2. Dry-Sunny-Cold
# Precipitation < 0.2 mm, Sunshine > 50%, Temperature < 10 degrees Celsius
#3. Dry-Cloudy-Hot
# Precipitation < 0.2 mm, Sunshine < 50%, Temperature > 10 degrees Celsius
#4. Dry-Cloudy-Cold
# Precipitation < 0.2 mm, Sunshine < 50%, Temperature < 10 degrees Celsius
#5. Rainy-Sunny-Hot
# Precipitation > 0.2 mm, Sunshine > 50%, Temperature > 10 degrees Celsius
#6. Rainy-Sunny-Cold
# Precipitation > 0.2 mm, Sunshine > 50%, Temperature < 10 degrees Celsius
#7. Rainy-Cloudy-Hot
# Precipitation > 0.2 mm, Sunshine > 50%, Temperature > 10 degrees Celsius
#8. Rainy-Cloudy-Cold
# Precipitation > 0.2 mm, Sunshine < 50%, Temperature < 10 degrees Celsius


#Define function that returns weather type based on weather data
GetWeatherType <- function(precipitation, sunshine, temperature) {
  if (precipitation < 0.2) {
    if (sunshine > 50) {
      if (temperature > 10) {
        return("Dry-Sunny-Hot")
      } else {
        return("Dry-Sunny-Cold")
      }
    } else {
      if (temperature > 10) {
        return("Dry-Cloudy-Hot")
      } else {
        return("Dry-Cloudy-Cold")
      }
    }
  } else {
    if (sunshine > 50) {
      if (temperature > 10) {
        return("Rainy-Sunny-Hot")
      } else {
        return("Rainy-Sunny-Cold")
      }
    } else {
      if (temperature > 10) {
        return("Rainy-Cloudy-Hot")
      } else {
        return("Rainy-Cloudy-Cold")
      }
    }
  }
}

#Add weather type to knmi dataset
for (i in 1:nrow(knmi)){
 knmi$weather_type[i] <- GetWeatherType(knmi$RH[i], knmi$SP[i], knmi$TG[i])}


#Define function that gives dates per weather type
GetDates <- function(startdate, enddate, WeatherType){ #dates in Y-m-d
  timeframe <- knmi[knmi$date >= as.Date(startdate) & knmi$date <= as.Date(enddate), ] #Make a subset of timeframe
  return(timeframe[timeframe$weather_type == WeatherType, ]$date) #return timeframes of dry days
}

GetWeatherCondition <- function(date) {
  date <- as.Date(date)
  subset <- knmi[knmi$date == date, ]
  return(subset$weather_type)}

#Example: get dates in 2014 where it was dry, sunny and cold
GetDates('2014-01-01', '2014-12-31', 'Dry-Sunny-Cold')

#Example: get weather type of 1 januari 2014
GetWeatherCondition('2014-01-01')

#Read twitter data
tweets <- read_excel("timeframe_all_tweetdata.xlsx")
#Adjust format of time column
tweets$time <- format(as.POSIXct(tweets$time, format="%Y-%m-%d %H:%M:%S"), format="%H:%M:%S")
#Keep date and time column only
tweets <- tweets[, c('date', 'time')]
#Change tweet date from POSIXct to Date type
tweets$date <- as.Date(tweets$date)

#Merge knmi data with tweet data
tweets_weather <- merge(tweets, knmi, by = 'date')

#Create empty dataframe
tweet_frequency <- data.frame(matrix(ncol = 2, nrow = 8))
row.names(tweet_frequency) <- unique(knmi$weather_type)
colnames(tweet_frequency) <- c('Amount of tweets', 'Tweets per day')

#Add amount of tweets per weather type in the tweet_frequency dataframe
for (i in 1:8){
tweet_frequency$`Amount of tweets`[i]<- sum(tweets_weather$weather_type == unique(knmi$weather_type)[i])
}

#Add amount of tweets and tweets per day in the tweet_frequency dataframe
count <- aggregate(tweets_weather$date, by = list(tweets_weather$weather_type), FUN = function(x) length(unique(x)))
tweet_frequency <- merge(tweet_frequency, count, by.x = 'row.names', by.y = 'Group.1', all.x=TRUE)
#Change column names
row.names(tweet_frequency) <- tweet_frequency$Row.names
colnames(tweet_frequency)[colnames(tweet_frequency) == 'x'] <- 'Days'
#Delete unnecessary columns
tweet_frequency$Row.names <- NULL
#Calculate tweets per day
tweet_frequency <- tweet_frequency[c(1, 3, 2)]
tweet_frequency$`Tweets per day` <- tweet_frequency$`Amount of tweets`/ tweet_frequency$Days
tweet_frequency[is.na(tweet_frequency)] <- 0



#Create weather type graph by date
tweets_weather$time <- NULL
weather_graph <- unique(tweets_weather)
#export to excel
library(openxlsx)
write.xlsx(weather_graph, "Weather_data.xlsx", sheetName = "28-03-2023 - 12-04-2023")




