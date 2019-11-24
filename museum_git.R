###### Load libraries ###### 

install.packages("tidyverse")
library(tidyverse)

install.packages("leaflet")

library(leaflet)

####### loading the data

museums <- read_csv("C:\\Users\\Valentina\\Documents\\Excella\\excella_labs\\museums.csv")

############# 

# filter to DC only and museums with revenue and geogpraphical data

mus_dc <- museums%>%filter(`State (Physical Location)` == 'DC',!(is.na(Longitude)), !is.na(Revenue))

#### build a  

mymap <- leaflet()

#####  Create a map widget by calling leaflet().

mymap <- mymap %>%
  addTiles(
    'http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg',
    attribution = 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  ) %>% setView(-97, 40, zoom = 4)
mymap
#### hoover over the circles to see the names of the museums. 

### increase the circle size according to revenue 
mymap %>% addTiles() %>%addCircleMarkers(data=mus_dc,
  radius = ~ log(Revenue),
  label = ~as.character(`Museum Name`)
  )%>%setView(-77.01924, 38.89640, zoom = 13)

###################################################################################



