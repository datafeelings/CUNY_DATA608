library(ggplot2)
library(dplyr)
library(plotly)

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