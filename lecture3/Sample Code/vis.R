library(googleVis)
library(reshape2)
library(ggplot2)
library(vegalite)
library(quantmod)
library(dplyr)

# GoogleVis syntax

setwd('/Users/Charley/Downloads/cuny/CUNY_DATA608/lecture3/Sample Code')
df <- read.csv('hpi.csv')
df$DATE <- as.POSIXct(strptime(df$DATE, format = '%m/%d/%y'))

data <- df %>%
  filter(Seasonality == 'SA', Metro == 'Atlanta') %>%
  select(DATE, Tier, HPI) %>%
  dcast(DATE ~ Tier, value.var = 'HPI')

line <- gvisLineChart(data, xvar = 'DATE', yvar = c('High', 'Middle', 'Low'))

plot(line)

# GoogleVis with Options

df <- data.frame(country=c("US", "GB", "BR"), val1=c(1,3,4), val2=c(23,12,32))

options = list(
  title = 'Hello World',
  titleTextStyle = 
    '{color: "red", fontName: "Courier", fontSize: 16',
  backgroundColor = '#D3D3D3',
  vAxis = '{gridlines:{color:"red", count:3}}',
  hAxis="{title:'Country', titleTextStyle:{color:'blue'}}",
  series="[{color:'green', targetAxisIndex: 0},
      {color: 'orange',targetAxisIndex:1}]",
  vAxes="[{title:'val1'}, {title:'val2'}]",
  legend="bottom",
  curveType="function",
  width=500,
  height=300
)

line <- gvisLineChart(df, xvar = 'country', yvar = c('val1', 'val2'),
                      options = options)

plot(line)

# googleVis is famous for motioncharts
# AKA Hans Rosling style charts

p <- gvisMotionChart(Fruits, idvar='Fruit', timevar='Year')
plot(p)

# Vega

# Javascript Visualizations with a visualization grammer

setwd('/Users/Charley/Downloads/cuny/CUNY_DATA608/lecture3/Sample Code')
df <- read.csv('hpi.csv')
df$DATE <- as.POSIXct(strptime(df$DATE, format = '%m/%d/%y'))

data <- df %>%
  filter(Seasonality == 'SA', Metro == 'Atlanta') %>%
  select(DATE, Tier, HPI)

vegalite() %>%
  cell_size(500, 300) %>%
  add_data(data) %>%
  encode_x(field = 'DATE', type='temporal') %>%
  encode_y(field = 'HPI', type = 'quantitative') %>%
  encode_color(field = 'Tier', type='nominal') %>%
  mark_line()

# Aggregations``

data <- read.csv('https://vega.github.io/vega-lite/data/seattle-temps.csv')

vegalite() %>%
  cell_size(500, 300) %>%
  add_data('https://vega.github.io/vega-lite/data/seattle-temps.csv') %>%
  encode_x(field = 'date', type='temporal') %>%
  timeunit_x("month") %>%
  encode_y(field = 'temp', type='quantitative', aggregate = 'mean') %>%
  mark_bar()


 
  
encode_x()
vegalite() %>%
  cell_size(500, 300) %>%
  add_data("https://vega.github.io/vega-editor/app/data/unemployment-across-industries.json") %>%
  encode_x("date", "temporal") %>%
  encode_y("count", "quantitative", aggregate="sum") %>%
  encode_color("series", "nominal") %>%
  scale_color_nominal(range="category20b") %>%
  timeunit_x("yearmonth") %>%
  scale_x_time(nice="month") %>%
  axis_x(axisWidth=0, format="%Y", labelAngle=0) %>%
  mark_area(interpolate="basis", stack="center")

data <- fromJSON(txt = 'https://vega.github.io/vega-editor/app/data/unemployment-across-industries.json')

data2 <- data %>%
  group_by(series, date) %>%
  summarise(count = sum(count)) %>%
  dcast(date ~ series, value.var = 'count')


data3 <- data2 %>% select(-date)

applyFunc <- function(x){
  return(cumsum(x) - (sum(x)/2))
}
data3 <- cbind(zero = 0, data3)

data4 <- data.frame(t(apply(data3, 1, applyFunc)))
colnames(data2) <- c('date', tail(colnames(data4),-1))

colnames(data2) <- c('date', paste(tail(colnames(data2), -1), '.Hover', sep=''))
data5 <- cbind(data2, data4)

c <- '~zero'
p <- plot_ly(data5) %>%
  add_trace(y = formula(c), x = ~date, type='scatter', mode = 'lines',
            fill = 'tonexty', hoverinfo = 'none', showlegend = F)

ind <- 'Agriculture'




for(ind in tail(colnames(data4), -1)){
  var <- paste('~', ind, sep='')
  varHov <- paste('~', ind, '.Hover', sep='')
  p <- p %>%
    add_trace(x = ~date, y = formula(var), text = formula(varHov), type='scatter',
              mode = 'lines', fill = 'tonexty', name = ind, hoverinfo = 'text')
  
  print(var)
  print(varHov)
}


for(ind in c(1,2,3)){
  var <- paste()
  p <- p %>% add_trace()
}



data4 <- cbind(data2$date, data4)

data5 <- melt(data4)

plot_ly(data4, id.vars = 'date')

data2 <- dcast(data2, date ~ series)

plot_ly(data, x = ~date, y = ~count, color = ~series, type='scatter', mode = 'lines')

library(jsonlite)



data <- data.frame(a = c(1,2,3), b = c(2,4,6))

setwd('/Users/Charley/Downloads/cuny/CUNY_DATA608/lecture3/Sample Code')

df <- read.csv('hpi.csv')
df$DATE <- as.POSIXct(strptime(df$DATE, format = '%m/%d/%y'))

data <- df %>%
  filter(Seasonality == 'SA', Metro == 'Atlanta') %>%
  select(DATE, Tier, HPI)

plot_ly(data, x = ~DATE, y = ~HPI, color = ~Tier, type='scatter', mode='lines')
