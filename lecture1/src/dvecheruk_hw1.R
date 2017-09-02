######
# CUNY MSDA Fall 2017 Semester
# DATA 608 
# Homework 1
# By Dmitriy Vecheruk
######

library("readr")
library("dplyr")
library("tidyr")
library("ggplot2")

# Read data
inp = read_csv("lecture1/Data/inc5000_data.csv")

# Inspect data
summary(inp)

# Create a graph that shows the distribution of companies in the dataset by State 
# (ie how many are in each state). There are a lot of States, so consider which 
# axis you should use assuming I am using a ‘portrait’ oriented screen (ie taller 
# than wide). 

company_by_state = inp %>% 
  group_by(State) %>% 
  # select(Name) %>% 
  summarise(company_count = n_distinct(Name)) %>% 
  arrange(-company_count)

figure_1 = ggplot(company_by_state,aes(x=reorder(State, company_count),
                                       y=company_count,
                                       label = company_count)) + 
  geom_col() + 
  coord_flip()+
  geom_text(size = 2.5,hjust = 0, nudge_y = 2) +
  labs(title = "Number of fastest growing companies per state",
       subtitle = "Among Inc. magazine's 5,000 fastest growing companies",
       y = "Company count", x = "State") +
  theme(
    panel.grid.major.y = element_blank(),panel.grid.minor.y = element_blank())

ggsave("lecture1/figure1.png",figure_1)

# Let’s dig in on the State with the 3rd  most companies in the data set. 
# Create a plot of average employment by industry for companies in this state 
# (only use cases with full data (user R’s complete.cases() function). Your graph 
# should show how variable the ranges are, and exclude outliers.

print (company_by_state %>% slice(3))

# The 3rd state in the rank is New York.
# Construct a dataframe for NY excluding the values in the top and bottom 5% per 
# industry in order to take care of outliers.
# Before calculating the outliers, the industries with less than 10 observations 
# each are put in a common bucket "Other"

ny_employment_filtered = inp %>% select(Industry,Employees, State) %>% 
  filter(complete.cases(.) & State == "NY") %>% 
  group_by(Industry) %>% 
  mutate(company_count = n()) %>% 
  mutate(industry_group = ifelse(company_count<10,"Other",Industry)) %>%
  ungroup() %>% 
  
  group_by(industry_group) %>% 
  mutate(upper_fence = quantile(Employees,0.75) + 1.5*IQR(Employees)) %>% 
  mutate(outlier = ifelse(test=(Employees > upper_fence ),
                          yes = 1, no = 0)) %>% 
  filter(outlier == 0) %>% 
  summarise(se = sd(Employees)/sqrt(n()), mean_emp = mean(Employees))

figure_2 =
  ggplot(ny_employment_filtered,aes(x = reorder(industry_group,mean_emp),
                                  y = mean_emp, label = round(mean_emp))) +
  geom_col() + 
  geom_errorbar(aes(ymin = mean_emp-se , ymax=mean_emp+se,width = .2))+
  geom_text(size = 3,nudge_x = 0.3,nudge_y = 7) +
  coord_flip()+
  labs(title = "Average number of employees per company and industry in the New York state",
       subtitle = "Among Inc. magazine's 5,000 fastest growing companies (outliers excluded)",
       y = "Employee number", x = "") +
  theme(panel.grid.major.y = element_blank(),panel.grid.minor.y = element_blank(),
        panel.grid.major.x = element_blank(),panel.grid.minor.x = element_blank()) 
  
ggsave("lecture1/figure2.png",figure_2)


# Now imagine you work for an investor and want to see which industries generate 
# the most revenue per employee. Create a chart makes this information clear.

rev_per_emp = inp %>% 
  mutate(rev_per_emp = Revenue / Employees) %>% 
  filter(complete.cases(rev_per_emp) & Employees > 1) %>% # filter to exclude 1-person businesses
  mutate(state = ifelse(State == "NY","New_York","Rest_of_USA")) %>% 
  group_by(Industry,state) %>% 
  summarise(med_rev = median(rev_per_emp)) %>% 
  spread(key = state,value = med_rev ) %>% 
  ungroup() %>% 
  mutate(industry_rank = dense_rank(Rest_of_USA)) # Calculate difference for nice order in the chart

library("scales")

figure_3 = ggplot(rev_per_emp,aes(x=reorder(Industry,industry_rank))) +
  geom_pointrange(aes(y = New_York,ymin = 0, ymax = New_York,color="New York")) +
  geom_pointrange(aes(y = Rest_of_USA,ymin = 0, ymax = Rest_of_USA, color = "Rest of USA")) +
  scale_y_continuous(labels = dollar) +
  coord_flip() +
  labs(title = "Median revenue per employee and industry in New York and rest of the US",
       subtitle = "Among Inc. magazine's 5,000 fastest growing companies", 
       y = "Median revenue per employee", x = "") +
  theme(panel.grid.minor.y = element_blank(),panel.grid.minor.x = element_blank(),
        legend.title = element_blank()) 

ggsave("lecture1/figure3.png",figure_3)

# Reference:
# http://ggplot2.tidyverse.org/reference/index.html#section-coordinate-systems
# https://www.rstudio.com/wp-content/uploads/2015/02/data-wrangling-cheatsheet.pdf
# https://stackoverflow.com/questions/3744178/ggplot2-sorting-a-plot
# https://stackoverflow.com/questions/22353633/filter-for-complete-cases-in-data-frame-using-dplyr-case-wise-deletion
# http://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm 
# https://www.rstudio.com/wp-content/uploads/2015/03/ggplot2-cheatsheet.pdf 