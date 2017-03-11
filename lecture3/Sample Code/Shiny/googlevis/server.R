library(ggplot2)
library(dplyr)
library(googleVis)
library(reshape2)

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