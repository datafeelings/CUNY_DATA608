library(ggplot2)
library(dplyr)

df <- read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/Sample%20Code/hpi.csv')
df$DATE <- as.POSIXct(strptime(df$DATE, format = '%m/%d/%y'))

function(input, output, session) {
  
  selectedData <- reactive({
    dfSlice <- df %>%
      filter(Seasonality == input$seas, Metro == input$metro)
  })
  
  output$plot1 <- renderPlotly({
    
    dfSlice <- df %>%
      filter(Seasonality == input$seas, Metro == input$metro)
    
    plot_ly(selectedData(), x = ~DATE, y = ~HPI, color = ~Tier, type='scatter',
           mode = 'lines')
  })
  
  output$stats <- renderPrint({
    dfSliceTier <- selectedData() %>%
      filter(Tier == input$tier)
    
    summary(dfSliceTier$HPI)
  })
  
}