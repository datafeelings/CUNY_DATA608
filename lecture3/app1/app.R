## app.R ##
library(shiny)
library(shinydashboard)
library(dplyr)
library(plotly)

# Read and prep the data

dat = read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv")
dat = dat %>% 
  filter(ICD.Chapter != "Codes for special purposes" & 
           ICD.Chapter != "Diseases of the ear and mastoid process") %>% 
  group_by(Year, ICD.Chapter) %>% 
  mutate(total_pop = sum(Population)) %>% 
  mutate(pop_weight = Population/total_pop) %>% 
  mutate(crude_rate_contrib = Crude.Rate*pop_weight) %>% 
  mutate(nat_avg_crude_rate = sum(crude_rate_contrib),
         nat_crude_rate_sd = sd(Crude.Rate))

states = unique(dat$State)
years = unique(dat$Year)

cause_rank = dat %>% 
  group_by(Year, ICD.Chapter) %>% 
  summarise(tot_deaths = sum(Deaths)) %>% 
  mutate(cause_rank = round(rank(-tot_deaths),0))

causes = data.frame(cause_rank %>% filter(Year == 2010) %>% arrange(cause_rank))$ICD.Chapter



# Code for the server

server <- function(input, output) {
  
  selected_data_cause = reactive({
    dat %>% 
      filter(ICD.Chapter == input$cause_filter1 &
             Year == input$year_filter) %>% 
      arrange(-Crude.Rate)
    
  }) # Subset the data for the selected year and cause
  
  selected_data_state = reactive({
    dat %>% 
      filter(ICD.Chapter == input$cause_filter2 & 
             State %in% input$state_filter) %>% 
      arrange(Year) %>% 
      ungroup()
    
  }) # Subset the data for the selected states and cause
  
  # First tab functions
  
  output$plot1 = renderPlotly({ 
    
    plotly_df = selected_data_cause()
    plotly_df$State = factor(plotly_df$State, levels = unique(plotly_df$State)[order(plotly_df$Crude.Rate)])
    plotly_df$Crude.Rate = as.double(plotly_df$Crude.Rate)
    plot_ly(data = plotly_df, x= ~Crude.Rate, y = ~State,
            type = 'bar') %>% 
      layout(xaxis = list(title = "Deaths per 100k",zeroline=F))
    
  }) # Chart rank per state
  
  output$plot2 = renderPlotly({
    
    plotly_df = selected_data_cause()
    
    plotly_df$hover <- with(plotly_df, paste("State: ", State, '<br>', "Deaths per 100k: ", Crude.Rate, "<br>",
                             "Total Deaths: ", Deaths, "<br>", 
                             "Population: ", round(Population/10^6,1)," Mln."))
    
    # give state boundaries a white border
    l <- list(color = toRGB("white"), width = 2)
    # specify some map projection/options
    g <- list(
      scope = 'usa',
      projection = list(type = 'albers usa'),
      showlakes = TRUE,
      lakecolor = toRGB('white')
    )
    
    p <- plot_geo(plotly_df, locationmode = 'USA-states') %>%
      add_trace(
        z = ~Crude.Rate, text = ~hover, locations = ~State,
        color = ~Crude.Rate, colors = 'Blues',showscale = F
      ) %>%
      layout(
        geo = g
      )
    
  }) # Map rank per state
  
  output$plot4 = renderPlotly({
    
    plotly_df = cause_rank %>% filter(ICD.Chapter == input$cause_filter1) %>% 
      ungroup()
    
    p1 = plot_ly(data = plotly_df, x= ~Year) %>% 
      add_trace(y = ~cause_rank, name = ~ICD.Chapter, 
                type = 'scatter', mode = 'lines+markers',
                line=list(shape="linear"))%>% 
      layout(yaxis = list (title="Rank among mortality causes", autorange="reversed",
                           zeroline=F))
    
  }) # Chart rank of cause over time
  
  # Second tab functions
  
  output$plot3 = renderPlotly({
    
    plotly_df = selected_data_state()
    
    p1 = plot_ly(data = plotly_df, x= ~Year) %>% 
      add_trace(y = ~nat_avg_crude_rate, name = 'National average',
                type = 'scatter',mode = 'lines+markers',
                line=list(shape="spline", color = 'rgb(8,17,17)',width=3)) %>%
      add_trace(y = ~Crude.Rate, name = ~State, split= ~State,
                type = 'scatter', mode = 'lines+markers',
                line=list(shape="spline")) %>% 
      layout(yaxis = list (title="Deaths per 100k", rangemode="tozero",zeroline=F))
    
  }) # Chart state over time vs avg
  
  output$plot5 = renderPlotly({
    
    plotly_df = state_rank %>% filter(ICD.Chapter == input$cause_filter2 &
                                       State %in% input$state_filter )
    
    p = plot_ly(data = plotly_df, x= ~Year) %>% 
      add_trace(y = ~state_rank, name = ~ICD.Chapter, split = ~State,
                type = 'scatter', mode = 'lines+markers',
                line=list(shape="linear",width=3))%>% 
      layout(yaxis = list (title="Rank among states for the selected cause", 
                           autorange="reversed", zeroline=F))
    
  }) # Chart rank of state over time
}

# Code for the ui

ui <- dashboardPage(skin = "black",
  dashboardHeader(title = "CDC Mortality Data Explorer", titleWidth = 300),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Explore causes", tabName = "causes", icon = icon("heartbeat")),
      menuItem("Compare states", tabName = "states", icon = icon("map-marker"))
    )
  ),
  dashboardBody(
    tabItems(
      # First tab content
      tabItem(tabName = "causes",
              fluidRow(
                box(title = h3("Cause distribution across the country"),
                    width = 12,solidHeader = TRUE,collapsible = TRUE,
                    "Use the controls below to filter for cause of mortality and
                    the year the data was collected"
                    ),
                box(title = "Select cause", width = 6,height = 140,
                    selectInput("cause_filter1",label = NULL, 
                                choices = causes, selected = "Neoplasms")
                    ),
                box(title = "Select year", width = 6,height = 140,
                    sliderInput("year_filter", label = NULL,
                                min = 1999, max = 2010, value = 2010)
                ),
                box(title = "Crude Mortality Rate per State", width = 5,
                    plotlyOutput("plot1")
                    ),
                box(title = "Map: Crude Mortality Rate per State", width = 7,
                    plotlyOutput("plot2")
                    ),
                box(title = "Rank of the Mortality Cause over time", width = 12,
                    "This chart shows the position of the selected mortality cause
                    among the 17 causes in the dataset, ranked by the total number of mortalities
                    (rank 1 is highest)",
                    plotlyOutput("plot4")
                    )
               )
                
              ),
      
      # Add comments:
      # reporting the death rate per 100,000 persons
      # Source: https://wonder.cdc.gov/
      
      # Second tab content
      tabItem(tabName = "states",
              fluidRow(
                box(title = h3("State performance vs. the national average"),
                    width = 12,solidHeader = TRUE,collapsible = TRUE,
                    "Use the controls below to filter for the state and cause of mortality in 
                    order to compare with the weighted average national mortality"
                ),
                box(title = "Select cause", width = 6,height = 140,
                    selectInput("cause_filter2",label = NULL, 
                                choices = causes, selected = "Neoplasms")
                ),
                box(title = "Select state", height = 140,
                    "You can select multiple states",
                    selectInput("state_filter", label = NULL,choices = states,
                                selected = "NY", multiple = TRUE)
                    ),
                box(title = "Annual crude mortality rate", width = 12,
                    plotlyOutput("plot3")
                    ),
                box(title = "National rank of the state for the mortality cause", width = 12,
                    "This chart shows the position of the selected states among all 
                    the states, ranked by the crude mortality rate from the selected cause
                    (rank 1 is highest)",
                    plotlyOutput("plot5"))
              )
      )
    )
  )
)


shinyApp(ui, server)
