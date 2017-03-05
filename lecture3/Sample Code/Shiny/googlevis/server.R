library(ggplot2)
library(dplyr)
library(googleVis)
library(reshape2)

df <- read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/Sample%20Code/hpi.csv')
df$DATE <- as.POSIXct(strptime(df$DATE, format = '%m/%d/%y'))

function(input, output, session) {
  
  selectedData <- reactive({
    dfSlice <- df %>%
      filter(Seasonality == input$seas, Metro == input$metro)
  })
  
  output$plot1 <- renderGvis({
    
    dataSlice <- dcast(selectedData(), DATE ~ Tier, value.var = 'HPI')
    
    gvisLineChart(dataSlice, xvar = 'DATE', yvar = c('High', 'Middle', 'Low'))
  
  })
  
  output$stats <- renderPrint({
    dfSliceTier <- selectedData() %>%
      filter(Tier == input$tier)
    
    summary(dfSliceTier$HPI)
  })
  
}