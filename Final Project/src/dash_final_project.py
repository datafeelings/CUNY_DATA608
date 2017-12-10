# -*- coding: utf-8 -*-

# Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html

from plotly.graph_objs import *
import pandas as pd
pd.options.mode.chained_assignment = None


## ------------- ## App data ## ------------- ##

## First chart

markdown_text_1 = """
### Deaths over time
  
The deaths from drug abuse related causes have been growing strongly over the past 16 years. 
"""

deaths_year = pd.read_csv("processed_data/deaths_year.csv")

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

markdown_text_2 = """
### Comparison to leading non-injury causes of death
  
While the incidence for four out of five top non-injury causes of death declined between 1999 and 2015, 
the death rate for drug overdose related causes increased almost 3 times!
"""

deaths_year_comp = pd.read_csv("processed_data/deaths_year_comp.csv")

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

fig_2 = dict(data=data, layout=layout)

## Third chart

markdown_text_3 = """
### Comparison of death rates per state
  
Looking at the data on state level highlights the differences accross the country: 
there is a troubling cluster of high death rates around West Virginia, another one in
New England, and New Mexico and Utah are worse than the rest of the states in the west of the country.
"""

state_deaths = pd.read_csv("processed_data/state_deaths.csv")

#  Make choropleth map

df = state_deaths.loc[state_deaths["Year"]==2015]

scl = [
    [6.0, 'rgb(254,229,217)'],
    [13.0, 'rgb(252,174,145)'],
    [16.0, 'rgb(251,106,74)'],
    [21.0, 'rgb(222,45,38)'],
    [45.0, 'rgb(165,15,21)']
                 ]

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
                color = 'rgb(255,255,255)',
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

## Fourth chart: Explore state over time

markdown_text_4 = """
### Explore data per state
  
Here you can explore the rise of the drug abuse related mortality per state and identify the demographic
groups that were affected most by the epidemic.
"""

states = state_deaths["State"].unique()
states_inputset = [dict(label= item, value= item) for item in states]

## Fifth chart: Explore state demographics

deaths_dem = pd.read_csv("processed_data/deaths_dem.csv")

## Sixth chart: Explore state demographics

urb_deaths = pd.read_csv("processed_data/urb_deaths.csv")


## ------------- ## App style ## ------------- ##

app = dash.Dash()

colors = {
    "background": "#ffffff",
    "text": "black"
}


## ------------- ## App rendering ## ------------- ##


app.layout = html.Div([

    # First chart: Deaths over time 
    dcc.Markdown(children=markdown_text_1),
    
    dcc.Graph(
        id="deaths_year",
        figure=fig_1
    ),
    
    # Second chart: Causes growth comparison
    dcc.Markdown(children=markdown_text_2),
    dcc.Graph(
        id="deaths_comp",
        figure=fig_2
    ),
    
    # Third chart: Rates per state
    dcc.Markdown(children=markdown_text_3),
    dcc.Graph(
        id="state_deaths_map",
        figure=fig_3
    ),
    
    # Fourth chart: Rate over time in a state
    dcc.Markdown(children=markdown_text_4),
    html.Label('Select a state'),
    dcc.Dropdown(
        id="state_dropdown",
        options=states_inputset,
        value='West Virginia'),
    dcc.Graph(id="state_deaths_year"),
    
    # Fifth chart: State rate by demographic 
    dcc.Graph(id="deaths_dem_comp"),
    
    # Sixth chart: State rate by demographic 
    dcc.Graph(id="urb_deaths")
       
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
    title = selected_state + ": Deaths per 100k population from drug overdose related causes: 1999 - 2015"
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

    layout = dict(title = title,xaxis = dict(title=xaxis_title),yaxis = dict(title=yaxis_title))
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
    title=selected_state + ": Drug overdose mortality rate change in 2015 vs. 1999"
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
        yaxis=dict(title=yaxis_title),
        showlegend = True,
        barmode='group'
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
    title = selected_state + " : Deaths per 100k population from drug overdose related causes: 1999 - 2015"
    xaxis_title=""
    yaxis_title="Deaths per 100k population"

    # Add reliability indicator
    df["marker"] = "circle"
    df.loc[df["aar_unreliable"]==1,"marker"] = "x"

    # Add colorscale
    scl = {6:['rgb(200,249,197)',"NonCore (non-metro)"]
           ,5:['rgb(190,235,197)',"Micropolitan (non-metro)"]
           ,4:['rgb(168,221,181)',"Small Metro"]
           ,3:['rgb(123,204,196)',"Medium Metro"]
           ,2:['rgb(67,162,202)',"Large Fringe Metro"]
           ,1:['rgb(28,104,172)',"Large Central Metro"]}

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