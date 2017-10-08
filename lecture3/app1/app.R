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
causes = unique(dat$ICD.Chapter)
years = unique(dat$Year)


a = dat %>% filter(ICD.Chapter=="Certain infectious and parasitic diseases",
                   Year == 2010) %>% 
  arrange(-Crude.Rate)

a$State <- factor(a$State, levels = unique(a$State)[order(a$Crude.Rate)])



# Code for the server

server <- function(input, output) {
  
  selected_data = reactive({
    dat %>% 
      filter(ICD.Chapter == input$cause_filter,
             Year == input$year_filter) %>% 
      arrange(-Crude.Rate)
    
  })
  
  output$plot1 <- renderPlotly({
    
    plotly_df = selected_data()
    plotly_df$State = factor(plotly_df$State, levels = unique(plotly_df$State)[order(plotly_df$Crude.Rate)])
    plotly_df$Crude.Rate = as.double(plotly_df$Crude.Rate)
    plot_ly(data = plotly_df, x= ~Crude.Rate, y = ~State,
            type = 'bar') %>% 
      layout(xaxis = list(title = "Deaths per 100k",zeroline=F))
    
  })
  
  output$plot2 <- renderPlotly({
    
    plotly_df = selected_data()
    
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
    
  })
}

# Code for the ui

ui <- dashboardPage(
  dashboardHeader(title = "Mortality Data Explorer"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Cause Explorer", tabName = "causes", icon = icon("heartbeat")),
      selectInput("cause_filter",label = "Select Cause", choices = causes, selected = "Neoplasms"),
      selectInput("year_filter", label = "Select year" ,choices = years,selected = 2010),
      menuItem("State Explorer", tabName = "states", icon = icon("map-marker"))
    )
  ),
  dashboardBody(
    tabItems(
      # First tab content
      tabItem(tabName = "causes",
              fluidRow(
                box(title = h2("Cause distribution across the country"),
                    status="primary", width = 12),
                box(title = "Crude Mortality Rate per State", width = 5,
                    status = "primary",
                  plotlyOutput("plot1")
                  ),
                box(title = "Map: Crude Mortality Rate per State", width = 7,
                    status = "primary",
                    plotlyOutput("plot2")
                )
              )
      ),
      
      # Add comments:
      # reporting the death rate per 100,000 persons
      # Source: https://wonder.cdc.gov/
      
      # Second tab content
      tabItem(tabName = "states",
              fluidRow(
                box(title = h2("State performance vs. the national average"),
                    status="primary", width = 12)
              )
      )
    )
  )
)


shinyApp(ui, server)
