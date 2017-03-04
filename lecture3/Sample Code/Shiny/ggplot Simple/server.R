library(ggplot2)
library(dplyr)

setwd('/Users/Charley/Downloads/cuny/CUNY_DATA608/lecture3/Sample Code')
df <- read.csv('hpi.csv')
df$DATE <- as.POSIXct(strptime(df$DATE, format = '%m/%d/%y'))

function(input, output, session) {
  
  output$plot1 <- renderPlot({
    
    dfSlice <- df %>%
      filter(Seasonality == input$seas, Metro == input$metro)
    
    ggplot(dfSlice, aes(x = DATE, y = HPI, color = Tier)) +
      geom_line()
  })
  
  output$stats <- renderPrint({
    dfSlice <- df %>%
      filter(Seasonality == input$seas, Metro == input$metro, Tier == input$tier)
    
    summary(dfSlice$HPI)
  })
  
}