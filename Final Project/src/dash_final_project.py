# -*- coding: utf-8 -*-

# Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html

from plotly.graph_objs import *
import pandas as pd
pd.options.mode.chained_assignment = None


## ------------- ## App data ## ------------- ##

## Intro
markdown_text_0 = """
### Introduction
The terms *opioid epidemic* and *overdose epidemic* have recently become a much-discussed topic in the US media,
as evidenced by the multiple recent news headlines and the following Google Trends chart:  

![opioid epidemic](https://lh3.googleusercontent.com/mXZ8BM94A-OkOcpuLuelnr0rMYpZ3lf8jCom3gA5XqUV8JLmhCd8hourRrGN3Au1KL8W8H0W7v2jG7Gp9khn=w1294-h960-rw)
  
This project investigates the national and state-level data from the CDC on deaths related to drug overdose 
in order to provide a more detailed view on the scale, social and geographical impact of the problem.
"""

## First chart

markdown_text_1 = """
### Deaths over time
  
The deaths from drug abuse related causes have been growing strongly over the past 16 years. 
"""

deaths_year = pd.read_csv("https://raw.githubusercontent.com/datafeelings/CUNY_DATA608/master/Final%20Project/processed_data/deaths_year.csv")

df = deaths_year[deaths_year["Cause"]=="Drug overdose related causes"]
x = "Year"
y = "Deaths"
category = "Cause"

groups = df[category].unique()
data = []

for item in groups: 
    data.append(
        Scatter(
            x = df[df["Cause"]==item][x],
            y = df[df["Cause"]==item][y],
            name = item,
            mode = 'lines+markers',
            line = dict(
                    width = 2,
                    color = 'rgb(0, 0, 0)',
                    shape='spline'
                )
            )
        )


layout = dict(
    title = 'Deaths from drug abuse related causes: 1999 - 2015'
)

fig_1 = dict(data=data, layout=layout)

## Second chart

markdown_text_2a = """
### Comparison to leading non-injury causes of death
  
However, an epidemic condition is different from a simple increase in mortalities. According to the CDC:  
> **Epidemic** refers to an increase, often sudden, in the number of cases of a disease above 
> what is normally expected in that population in that area. 
  
While the incidence for four out of five top non-injury causes of death declined between 1999 and 2015, 
the death rate for drug overdose related causes increased almost 3 times! This observation alone is sufficient
to call out an epidemic of overdose-related mortalities.

"""

deaths_year_comp = pd.read_csv("https://raw.githubusercontent.com/datafeelings/CUNY_DATA608/master/Final%20Project/processed_data/deaths_year_comp.csv")

df = deaths_year_comp[deaths_year_comp["Year"]==2015.0].sort_values("Growth since 1999")
x = "Growth since 1999"
y = "Cause"
category = "Cause"

scl = {
    'Drug overdose related causes': 'rgb(222,45,38)',
    'Alzheimers disease': 'rgb(251,106,74)',
    'Cerebrovascular diseases, including stroke': 'rgb(153,216,201)',
    'Chronic lower respiratory diseases': 'rgb(153,216,201)',
    'Diseases of Heart': 'rgb(153,216,201)',
    'Malignant neoplasms (Cancers)': 'rgb(153,216,201)'
                 }

groups = df[category].unique()
data = []

for item in groups: 
    data.append(
        Bar(
            x = df[df[category]==item][x],
            y = df[df[category]==item][y],
            name = item,
            text = df[df[category]==item][x].round(0).astype("str")+"%",
            textposition = 'auto',
            orientation = 'h',
            marker=dict(color = scl[item])
            )
        )


layout = dict(
    title = 'Mortality rate change from selected causes: 2015 vs. 1999',
    showlegend = False,
    margin=Margin(
        l=260
    ),
)

fig_2a = dict(data=data, layout=layout)

## Third chart (fig_2b)

markdown_text_2b = """
### The drugs behind the epidemic
  
Looking at the more recent data released by the CDC, the role of synthetic opioids becomes apparent: 
in the last three years they have overtaken heroin as the leading cause of overdose deaths.
"""

def plotly_figure_line(df,x,y,group=None,group_colors=None,mode="lines+markers",
                       title="",xaxis_title="",yaxis_title=""):
    
    if group is not None:
        pass
    else:
        df["trace_id"] = "1" # set up a dummy variable to iterate over
        group = "trace_id" 
        
    if group_colors is not None:
        pass
    else:
        group_colors = {"1":"rgb(0,0,0)"}

    groups = df[group].unique()
    
    data = []
    
    for item in groups: 
        data.append(
            Scatter(
                x = df[df[group]==item][x],
                y = df[df[group]==item][y],
                name = item,
                mode = mode,
                line = dict(
                        width = 2,
                        color = group_colors[item],
                        shape='spline'
                    )
                )
            )

    return data

deaths_drugs = pd.read_csv("https://raw.githubusercontent.com/datafeelings/CUNY_DATA608/master/Final%20Project/processed_data/deaths_drugs.csv")

# Setup continuous x axis
deaths_drugs["year_month"] = deaths_drugs["Year"].astype("str")+" "+deaths_drugs["Month"].astype("str")

df = deaths_drugs[(deaths_drugs["State Name"]=="United States") & 
                  (deaths_drugs["Month"].isin(["January","July"]))]

# Setup the colorscale
levels = deaths_drugs.Indicator.unique()
colors = ['rgb(178,24,43)','rgb(239,138,98)','rgb(223,189,179)','rgb(150,150,150)','rgb(93,93,93)','rgb(77,77,177)']
scl = dict([item for item in zip(levels,reversed(colors))])


data = plotly_figure_line(df=df,x="year_month",y="Data Value",group="Indicator",
                          group_colors = scl,mode="lines+markers")

title = "12 Month-ending provisional counts of drug overdose deaths by drug"
xaxis_title = ""
yaxis_title = "Provisional count of deaths"


layout = dict(title = title,
              xaxis = dict(title=xaxis_title),
              yaxis = dict(title=yaxis_title))

fig_2b = dict(data=data, layout=layout)

## Fourth chart (fig_3)

markdown_text_3 = """
### Comparison of death rates per state
  
Looking at the data on state level highlights the differences accross the country: 
there is a troubling cluster of high death rates around West Virginia, another one in
New England, and New Mexico and Utah are worse than the rest of the states in the west of the country.
"""

state_deaths = pd.read_csv("https://raw.githubusercontent.com/datafeelings/CUNY_DATA608/master/Final%20Project/processed_data/state_deaths.csv")

#  Make choropleth map

df = state_deaths.loc[state_deaths["Year"]==2015]

# Set up the colorscale

colors = colors = ['rgb(254,240,217)','rgb(253,204,138)','rgb(252,91,89)','rgb(255,38,11)']
levels = [0.0,0.25,0.5,1.0]
scl = [list(item) for item in zip(levels,colors)]

df['text'] = df['State']+ '<br>' +\
    'Deaths per 100k population: '+df['Age Adjusted Rate'].astype(str)

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = df['code'],
        z = df['Age Adjusted Rate'],
        locationmode = 'USA-states',
        text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(50,50,50)',
                width = 1
            ) ),
        colorbar = dict(
            title = "Deaths per 100k population")
        ) ]

layout = dict(
        title = '2015: Death rates due to drug overdose',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig_3 = dict( data=data, layout=layout )

## Chart 5: Explore state over time

markdown_text_4 = """
### Explore the data per state
  
Here you can explore the rise of the drug abuse related mortality per state and identify the demographic
groups that were affected most by the epidemic.
"""

states = state_deaths["State"].unique()
states_inputset = [dict(label= item, value= item) for item in states]

## Chart 6: Explore state demographics

deaths_dem = pd.read_csv("https://raw.githubusercontent.com/datafeelings/CUNY_DATA608/master/Final%20Project/processed_data/deaths_dem.csv")

## Markdown comments for the state

markdown_text_5 = """
The dynamics of the overdose epidemic vary greatly from one state to the other: some states have
an increase across all demographics and urbanization types like Ohio, whereas in other states death 
rates diverge for some age groups (e.g. in Texas) or urbanization types (e.g. in Colorado).  
Death rates in the most of the states marked with a deeper red color in the overview map above 
have surpassed the national median death rate in early 2000s, and have stayed at a higher level since.
However, an additional alarming trend is visible in the eastern cluster of the most affected states: 
all of them show a noticeable jump in the mortality starting from 2013. 
It is especially visible in New Hampshire, where the death rate doubled from 2013 to 2016.
  
Note that some of the less populous states do not have sufficient data to provide the splits by 
demographic or urbanization, and all observations that are based on unreliably small sample sizes 
(less than 20 persons) are marked in the charts with a * or an 
an ![x](https://github.com/datafeelings/CUNY_DATA608/blob/master/Final%20Project/processed_data/x.png?raw=true "x").
"""

## Chart 7: Explore state demographics

urb_deaths = pd.read_csv("https://raw.githubusercontent.com/datafeelings/CUNY_DATA608/master/Final%20Project/processed_data/urb_deaths.csv")

# Technical notes and reference

markdown_text_6 = """
### Technical notes
  
The data presented in these charts was queried using a GUI tools [CDC WONDER](http://wonder.cdc.gov/cmf-icd10.html) and [NVSS Vital Statistics Rapid Release](https://www.cdc.gov/nchs/nvss/vsrr/drug-overdose-data.htm). 
Drug overdose related deaths are those classified as fitting at least one the following underlying cause-of-death codes from the Tenth Revision of ICD (ICD–10): X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), 
and Y10–Y14 (undetermined). Drug overdose deaths involving selected drug categories are identified by specific multiple cause-of-death codes. 

Further documentation is available [here](https://wonder.cdc.gov/wonder/help/cmf.html).

Excluding the chart with the split by demograpics, the data shows an age-adjusted death rate. The age-adjusted rate is used for the following methodological reason cited on the [CDC website](https://wonder.cdc.gov/wonder/help/cmf.html):
>The rates of almost all causes of death vary by age. Age adjustment is a technique for "removing" the effects of age from crude rates, so as to allow meaningful comparisons across populations with different underlying age structures. For example, comparing the crude rate of heart disease in Florida to that of California is misleading, because the relatively older population in Florida will lead to a higher crude death rate, even if the age-specific rates of heart disease in Florida and California are the same. For such a comparison, age-adjusted rates are preferable. Age-adjusted rates should be viewed as relative indexes rather than as direct or actual measures of mortality risk.
  
This project was developed in Jupyter Notebook and ported to Plotly Dash.   
All the data preprocessing steps are available in this [notebook](https://github.com/datafeelings/CUNY_DATA608/blob/master/Final%20Project/Dmitriy_Vecheruk_data608_final_project.ipynb).
  
  
### Reference

1) Centers for Disease Control and Prevention, National Center for Health Statistics. Compressed Mortality File 1999-2015 on CDC WONDER Online Database, released December 2016. Data are from the Compressed Mortality File 1999-2015 Series 20 No. 2U, 2016, as compiled from data provided by the 57 vital statistics jurisdictions through the Vital Statistics Cooperative Program. Accessed at http://wonder.cdc.gov/cmf-icd10.html on Dec 3, 2017 9:27:17 AM
  
2) Ahmad FB, Rossen LM, Spencer MR, Warner M, Sutton P. Provisional drug overdose death counts. National Center for Health Statistics. 2017. Accessed at https://www.cdc.gov/nchs/nvss/vsrr/drug-overdose-data.htm on Dec 10, 2017 9:00:00 AM
 
3) US state codes: https://www.50states.com/abbreviations.htm  
4) Pandas documentation: https://pandas.pydata.org/pandas-docs/stable/  
5) Google Trends on "Opioid Epidemic": https://trends.google.com/trends/explore?geo=US&q=opioid%20epidemic  
6) CDC definition of an epidemic: https://www.cdc.gov/ophss/csels/dsepd/ss1978/lesson1/section11.html  
"""


## ------------- ## App style ## ------------- ##

app = dash.Dash()

colors = {
    "background": "#ffffff",
    "text": "black"
}


## ------------- ## App rendering ## ------------- ##


app.layout = html.Div([

    # Title and intro
    html.H2('Drug overdose epidemic in the United States:'),
    html.H3('An overview of the dynamics between 1999 and 2015'),
    html.P('CUNY MSDA DATA 608 Final Project by Dmitriy Vecheruk'),
    dcc.Markdown(children=markdown_text_0),
    
    # First chart: Deaths over time 
    dcc.Markdown(children=markdown_text_1),
    
    dcc.Graph(
        id="deaths_year",
        figure=fig_1
    ),
    
    # Second chart: Causes growth comparison
    dcc.Markdown(children=markdown_text_2a),
    dcc.Graph(
        id="deaths_comp",
        figure=fig_2a
    ),
    
    # Third chart: Drugs comparison
    dcc.Markdown(children=markdown_text_2b),
    dcc.Graph(
        id="deaths_drugs",
        figure=fig_2b
    ),
    
    # Fourth chart: Rates per state
    dcc.Markdown(children=markdown_text_3),
    dcc.Graph(
        id="state_deaths_map",
        figure=fig_3
    ),
    
    # State selector
    dcc.Markdown(children=markdown_text_4),
    html.Label('Select a state',className='row'),
    
    # chart 5: Rate over time in a state
    dcc.Dropdown(
        id="state_dropdown",
        options=states_inputset,
        value='Ohio',
        className='four columns'),
    
    html.Div([],className='row'),
    
    dcc.Graph(id="state_deaths_year",
              className='container',style={"float":"left","width":"50%"}),
    
    # chart 6: State rate by demographic 
    dcc.Graph(id="deaths_dem_comp",className='container',style={"float":"right","width":"50%"}),
    
    # Markdown comments
    html.Div([
        dcc.Markdown(children=markdown_text_5)
    ], className='container',style={"float":"left","width":"50%"}),
    
    # chart 7: State rate by urbanization 
    dcc.Graph(id="urb_deaths",className='container',style={"float":"right","width":"50%"}),
    
    # Technical notes and reference 
    html.Div([
        dcc.Markdown(children=markdown_text_6)
    ], className='row',style={"float":"left","width":"100%"}),
    
       
], style={"backgroundColor": colors["background"]})


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

### Update growth over time per state chart

@app.callback(
    dash.dependencies.Output('state_deaths_year', 'figure'),
    [dash.dependencies.Input('state_dropdown', 'value')])

def update_figure_1(selected_state):

    df = state_deaths[state_deaths["State"] == selected_state]
    x = "Year"
    y = "Age Adjusted Rate"
    title = "Annual mortality rate related to drug overdose"
    xaxis_title=""
    yaxis_title="Deaths per 100k population"

    # Add reliability indicator
    df["marker"] = "circle"
    df.loc[df["aar_unreliable"]==1,"marker"] = "x"

    data = []

    data.append(
                Scatter(
                    x = df[x],
                    y = df[y],
                    name = selected_state,
                    mode = "lines+markers",
                    line = dict(
                            width = 3,
                            color = "rgb(0,0,0)",
                            shape='spline'
                        ),
                    marker = dict(symbol=df["marker"],size=8)
                    )
                )

    # Add a trace with the national median rate
    state_deaths_median = state_deaths.groupby(["Year"])["Age Adjusted Rate"].median().reset_index()

    trace_median = Scatter(
                    x = state_deaths_median[x],
                    y = state_deaths_median[y],
                    name = "National Median",
                    mode = "lines",
                    line = dict(
                            width = 2,
                            color = "rgb(50,50,50)",
                            dash = 'dot',
                            shape='spline'
                        )
                    )

    data.append(trace_median)

    layout = dict(title = title,xaxis = dict(title=xaxis_title),yaxis = dict(title=yaxis_title),
                 legend=dict(xanchor='left',x=0.05))
    return dict(data=data, layout=layout)

### Update state age-gender change chart

@app.callback(
    dash.dependencies.Output('deaths_dem_comp', 'figure'),
    [dash.dependencies.Input('state_dropdown', 'value')])

def update_figure_2(selected_state):
    
    deaths_dem_comp = deaths_dem.loc[(deaths_dem["State"] == selected_state) 
                                     & (deaths_dem["Year"].isin([1999.0,2015.0]))]
    deaths_dem_comp = deaths_dem_comp.sort_values(["Gender","Age Group","Year"])
    deaths_dem_comp["Growth since 1999"] = deaths_dem_comp.groupby(["Gender","Age Group"])["Crude Rate"].pct_change()*100
    deaths_dem_comp["Growth since 1999"] = deaths_dem_comp["Growth since 1999"].round(0).fillna(0).astype("int")
    # Add rate reliability indicator if either 1999 or 2015 rates are unreliable
    deaths_dem_comp["base_rate_unrel"] = deaths_dem_comp.groupby(["Gender","Age Group"])["rate_unreliable"].shift()
    deaths_dem_comp["base_rate_unrel"] = deaths_dem_comp["base_rate_unrel"].fillna(0)
    deaths_dem_comp["rate_unreliable"] = deaths_dem_comp["rate_unreliable"]+deaths_dem_comp["base_rate_unrel"]
    
    df = deaths_dem_comp[deaths_dem_comp["Year"]==2015.0].sort_values("Age Group")
    y = "Growth since 1999"
    x = "Age Group"
    title="Drug overdose mortality rate change vs. 1999 by demographic"
    xaxis_title="Age Group"
    yaxis_title="Rate change vs. 1999"

    genders = list(df.Gender.unique())
    df["warning"] = ""
    df.loc[df.rate_unreliable==1.0,"warning"] = "*"


    scl = {"Male":'rgb(241,163,64)', "Female":'rgb(153,142,195)'}

    data = []

    for gender in genders:
        data.append(
            Bar(
                x = df[(df["Gender"]==gender)][x],
                y = df[(df["Gender"]==gender)][y],
                name = gender,
                text = df[(df["Gender"]==gender)][y].round(1).astype("str")+"%"+df[(df["Gender"]==gender)]["warning"],
                textposition = 'outside',
                marker=dict(color = scl[gender])
            )
        )

    layout = dict(
        title = title, xaxis=dict(title=xaxis_title),
        yaxis=dict(title=yaxis_title,visible=False),
        showlegend = True,
        barmode='group',
        legend=dict(xanchor='left',x=0.05)
    )
    
    return dict(data=data, layout=layout)

### Update state urbanization change chart

@app.callback(
    dash.dependencies.Output('urb_deaths', 'figure'),
    [dash.dependencies.Input('state_dropdown', 'value')])

def update_figure_3(selected_state):
    
    df = urb_deaths[(urb_deaths["State"] == selected_state) &
                    (urb_deaths["Year"].isin([1999,2015]))]\
    .sort_values(["Year","2013 Urbanization Code"])

    x = "Year"
    y = "Age Adjusted Rate"
    group = "2013 Urbanization Code"
    title = "Drug overdose mortality rate in 1999 and 2015 by community type"
    xaxis_title=""
    yaxis_title="Deaths per 100k population"

    # Add reliability indicator
    df["marker"] = "circle"
    df.loc[df["aar_unreliable"]==1,"marker"] = "x"

    # Add colorscale

    ids = [1,2,3,4,5,6]
    colors = ['rgb(140,81,10)','rgb(216,179,101)','rgb(146,132,95)','rgb(159,204,199)','rgb(90,180,172)','rgb(1,102,94)']
    levels = ["Large Central Metro","Large Fringe Metro","Medium Metro"
              ,"Small Metro","Micropolitan (non-metro)","NonCore (non-metro)"]
    col_levels = [item for item in zip(colors[::-1],levels)]
    scl = dict(zip(ids,col_levels))

    groups = sorted(list(df[group].unique()))
    data = []

    for item in groups:

        data.append(
                Scatter(
                    x = df[df[group]==item][x],
                    y = df[df[group]==item][y],
                    name = scl[item][1],
                    mode = "lines+markers",
                    line = dict(
                            width = 2,
                            color = scl[item][0],
                            shape='spline'
                        ),
                    marker = dict(symbol=df["marker"],size=8)
                    )
                )

    layout = dict(title = title
                  ,xaxis = dict(title=xaxis_title,type="category")
                  ,yaxis = dict(title=yaxis_title)
                  ,legend = dict(traceorder="normal"))  
    
    return dict(data=data, layout=layout)

if __name__ == "__main__":
    app.run_server(debug=True)