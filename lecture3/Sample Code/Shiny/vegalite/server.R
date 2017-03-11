library(ggplot2)
library(dplyr)
library(vegalite)
library(shiny)

function(input, output, session) {
  
  selectedData <- reactive({
    dfSlice <- df %>%
      filter(Seasonality == input$seas, Metro == input$metro)
  })
  
  output$plot1 <- renderVegalite({
    
    vegalite() %>%
      cell_size(500, 300) %>%
      add_data(selectedData()) %>%
      encode_x(field = 'DATE', type='temporal') %>%
      encode_y(field = 'HPI', type = 'quantitative') %>%
      encode_color(field = 'Tier', type='nominal') %>%
      mark_line()
  })
  
  output$stats <- renderPrint({
    dfSliceTier <- selectedData() %>%
      filter(Tier == input$tier)
    
    summary(dfSliceTier$HPI)
  })
  
}