
#################################   Data Analysis at Excella. ############################################

### This script illustrates how to create a map widget from an input file. 

############################################################
####          Install & load the required packages.     ####
############################################################ 

install.packages("tidyverse") # Needed for general data transformations. 
library(tidyverse)

install.packages("leaflet") # Needed to create a map widget. 
library(leaflet)

install.packages("RCurl") # Needed to read data from GitHub repository.
library(RCurl)

############################################################
####           Download the  data set                  ####
############################################################

####### Load the input data from the remote Git repository.

url_data <- getURL("https://raw.githubusercontent.com/excellalabs/data_analytics/master/museums.csv") 
museums <- read.csv(text = url_data) #read data into data frame 

############################################################
####           Process the data.                        ####
############################################################

####### Filter the data to museum in DC only with revenue and geogpraphical data available. 

mus_dc <- museums%>%filter(State..Physical.Location. == 'DC',!(is.na(Longitude)), !is.na(Revenue))

############################################################
####           Creat a map.                            ####
############################################################

####### The leafel package lets you create a map widget using the leaflet() function.

mymap <- leaflet()

####### Let's look at a generic map. 

mymap <- mymap %>%
  addTiles(
    'http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg',
    attribution = 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  ) %>% setView(-97, 40, zoom = 4) # The setView() method focuses the map. 
mymap

####### Add layers to the map by using the layer functions such as addTiles(), addMarkers(). 
####### We are adding layers that are specific to our datset. 

mymap %>% addTiles() %>%addCircleMarkers(data=mus_dc,# The dataset. 
                                         radius = ~ log(Revenue), # Create cricle size according to Revenue. 
                                         label = ~as.character(Museum.Name) # Use this for lables. 
                    )%>%setView(-77.01924, 38.89640, zoom = 13)

#### Hoover over the circles to see the names of the museums. 

###################################################################################

####### End of script. ##########

