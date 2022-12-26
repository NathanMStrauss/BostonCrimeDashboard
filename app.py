#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 22:21:48 2022
DS2001 Group Project

This is the app container with the code necessary to create a dashboard that
is hosted locally and is the final product of the group's efforts.
"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# define constants
MONTHS = {1 :"January",2:"February",3:"March",4:"April",5:"May",
          6:"June",7:"July",8:"August",9:"September",10:"October",
          11:"November",12:"December"}
CRIME_DATA_LINK = 'https://data.boston.gov/dataset/crime-incident-reports-august-2015-to-date-source-new-system/resource/313e56df-6d77-49d2-9c49-ee411f10cf58'
GEOJSON_FILENAME = 'Planning_Districts.geojson'

# import everything that's necessary
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from shapely.geometry import Point, shape

def read_data(filename):
    """
    Reads in csv data to a Pandas dataframe. Converts some values to different
    types upon reading.

    Parameters
    ----------
    filename : string
        Name of the file/filepath that the user would like to read in.

    Returns
    -------
    df : Pandas dataframe
        A dataframe containing the values in desired types.

    """
    col_types = {'YEAR': int,'MONTH': int, 'HOUR': int, 
                 'SHOOTING': int, 'OFFENSE_CODE': int, 
                 'Lat': float, 'Long': float}
    df = pd.read_csv(filename, header=0, converters = col_types, engine="python")
    return df

def load_geojson(filename):
    """
    Loads and reads geographical geojson information data.

    Parameters
    ----------
    link : string
        Name of the file/filepath that the user would like to read in..

    Returns
    -------
    area : dictionary 
        The dictionary containing the names, vertices, and other relevant
        information.
    neighborhood_map : dictionary
        Dictionary containing all of the names of the locations and the
        order in which they appear.

    """
    with open(filename,'r') as response:
        area = json.load(response)
        
    neighborhood_map = {}
    for feature in area['features']:
        feature['ID'] = feature['properties']['PD']
        neighborhood_map[feature['properties']['PLANNING_D']] = feature['ID']
        
    return area, neighborhood_map

def check_place(row, geoJson):
    """
    Using the coordinates given by each incident, check which crime occurred
    in which neighborhood of Boston.

    Parameters
    ----------
    row : dataframe
        One instance from a large dataframe.
    geoJson : dictionary
        The dictionary containing the names, geographical vertices, 
        and other relevant information.

    Returns
    -------
    string
        The name of the place that the point has been calculated to be within.

    """
    Boston = geoJson
    point = Point(row['Long'],row['Lat'])
    for feature in Boston['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['ID']
        
    return 'DNE'

def counting_values_df(df):
    """
    Count the number of unique places and the number of crimes that occur 
    in each place given a dataframe.

    Parameters
    ----------
    df : dataframe
        Pandas dataframe containing all of the values that the user 
        would like to tabulate.

    Returns
    -------
    new_df : dataframe
        Pandas dataframe that maps the counts to the values specified..

    """
    #count the number of crimes
    num_crimes = df.value_counts('Neighborhood')

    # generate a new DataFrame based on number of crimes
    values = []
    for district, value in num_crimes.items():
        values.append([district, value]) 
    new_df = pd.DataFrame(values, columns = ['Neighborhood', 'NUM_REPORTS'])
    
    return new_df

def generate_choropleth(df_choro, place_Json):
    """
    Generate a plotly express choropleth graph.

    Parameters
    ----------
    df_choro : Dataframe
        Pandas dataframe that contains the relevant information to plot.
    place_Json : dictionary
        The dictionary containing the names, geographical vertices, 
        and other relevant information.

    Returns
    -------
    choropleth_fig : plotly express figure
        The choropleth figure to be graphed.

    """
    # generate a choropleth map based on number of crimes
    choropleth_fig = px.choropleth(
        df_choro, #crime database
        locations = 'Neighborhood', # define the limits on the map/geography
        geojson = place_Json, # shape information
        color = 'NUM_REPORTS', # defining the color of the scale through the database
        hover_data =['NUM_REPORTS'],
        scope="usa",
        featureidkey = 'ID',
        title = "Crime in Boston", # title of the map
    )
    # make the graph pretty and add some styling to it!
    choropleth_fig.update_geos(fitbounds = "locations", visible = False)
    choropleth_fig.update_layout(paper_bgcolor="#236C90", plot_bgcolor="#F4F4F8")
    choropleth_fig.update_layout(margin=dict(t=0, r=0, b=0, l=20))
    choropleth_fig.update_layout(font_color='#FFFFFF')
    choropleth_fig.update_layout(title_x=0.4)
    choropleth_fig.update_layout(title_y=0.93)
    choropleth_fig.update_layout(title_font_size=24)
    choropleth_fig.update_layout(autosize=True)
    choropleth_fig.update_layout(clickmode='event+select')
    
    return choropleth_fig
    
def generate_scatterplot(df):
    """
    Generate a plotly express scatterplot graph.

    Parameters
    ----------
    df : Dataframe
        Pandas dataframe that contains the relevant information to plot..

    Returns
    -------
    scatter_fig : plotly express figure
        The scatterplot figure to be graphed.

    """
    # make the scatterplot
    scatter_fig = px.scatter_mapbox(df, lat="Lat", lon="Long", hover_name = 'INCIDENT_NUMBER', 
                            hover_data = ['Neighborhood', 'OCCURRED_ON_DATE', 'OFFENSE_DESCRIPTION'])

    # make the scatterplot pretty!
    scatter_fig.update_layout(mapbox_style="open-street-map")
    scatter_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    scatter_fig.update_mapboxes(center={'lat': 42.361145, 'lon': -71.057083})
    
    return scatter_fig

def read_crimetype(filename):
    """
    Reads integer values from a file and add them to a list.

    Parameters
    ----------
    filename : string
        Name of the file the user wants to read.

    Returns
    -------
    all_codes : list
        List of all of the values in the file.

    """
    with open(filename, 'r') as infile:
        codes = infile.readlines()
        all_codes = []
        for code in codes:
            code = code.strip()
            code = int(code)
            all_codes.append(code)
        
    return all_codes

# read in the data
crime_df = read_data('BosCrime.csv')

# read district geography info
Boston, neighborhoods = load_geojson(GEOJSON_FILENAME)

# get the geoJson map
with open('Planning_Districts.geojson') as response:
    area = json.load(response)
    
# filter out the places we are not able to graph
crime_df = crime_df[(crime_df.Lat != 0.0) & (crime_df.Long != 0.0)]

# add the neighborhoods to each row in the dataset
crime_df['Neighborhood'] = crime_df.apply(lambda row: check_place(row, geoJson = Boston), axis=1)    
    

# generate graphs
df_choro = counting_values_df(crime_df)
choropleth_fig = generate_choropleth(df_choro, Boston)
scatter_fig = generate_scatterplot(crime_df)

# read crime types
crime_type = {}
crime_type['ppl'] = read_crimetype('persons.txt')
crime_type['prop'] = read_crimetype('property.txt')
crime_type['soc'] = read_crimetype('society.txt')


app = Dash(__name__,
           meta_tags=[
               {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
           ],
           )
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(children=[
    html.H1(children='Boston Crime Dashboard'),
    
    html.Div(
        id="header",
        children=[
            html.P(
                id="description",
                children=["This the final project for a DS2000 course at \
                Northeastern University investigating crime statistics in \
                Boston Neighborhoods. Though the project is completed, there \
                are still many updates to be made thay come about in the \
                future. The geodata can be found ",
                html.A("here", href='https://data.boston.gov/dataset/planning-districts', target="_blank"),
                ". And the crime data can be found ",
                html.A("here", href=CRIME_DATA_LINK, target="_blank"),
                "."
            ]),
           
            html.P(
                id='description2',
                children = "Day was defined as between the hours of \
                7am and 7pm."
                )
        ],
    ),
    html.Div(
        id="selectors",
        children=[
            html.Div([
                html.Br(),
                html.Label('Crimes against'),
                dcc.Checklist(
                    id = "crimes_against",
                    options = [
                    {'label': 'People', 'value': 'ppl'},
                    {'label': 'Society', 'value': 'soc'},
                    {'label': 'Property', 'value': 'prop'},
                    ],
                    value = ['ppl','soc','prop']
                ),

                ],               
                style={'Padding': 100, 'display': 'inline-block'}
                ),
            html.Div(
                [
                html.Br(),
                html.Label('Time of Day'),
                dcc.RadioItems(
                    id = "time_of_day",
                    options = ['Day', 'Night', 'All'],
                    value = 'All',
                    inline = True,
                ),
            ],
        style={'display': 'inline-block'}
        
        ),
        ],
        style={'display': 'inline-block'}
    ),
    html.Div(
        id="graph-container",
        children=[
            html.P(id="chart-selector", children="Drag the slider to change the months"),
            html.Div(
                dcc.Slider(
                    id="month-slider",
                    min = min(MONTHS.keys()),
                    max = max(MONTHS.keys()),
                    step=None,
                    value=min(MONTHS.keys()),
                    marks={str(month): str(month) for month, name in MONTHS.items()},
                ),
                style={'width': '40%'}
            ),
            html.Div(
                children = [
                    dcc.Graph(
                        id='choropleth-crime-graph',
                        figure = choropleth_fig,
                        style={'padding': 10, 'width': '40%', 'display': 'inline-block'}
                    ),
                    dcc.Graph(
                        id='scatterplot-crime-graph',
                        figure = scatter_fig,
                        style={'padding': 10, 'width': '40%','display': 'inline-block'}
                        )
                ]
            )
        ]
    )

])

# if there are any interactions with the dashboard, make sure it's reflected here!    
@app.callback(
    Output(component_id='choropleth-crime-graph', component_property='figure'),
    Output(component_id='scatterplot-crime-graph', component_property='figure'),
    Input(component_id='time_of_day', component_property='value'),
    Input(component_id='month-slider', component_property='value'),
    Input(component_id='crimes_against', component_property='value'),
)
def update_graphs(time, month, crimes_against):
    """
    Update the graphs that are displayed on the dashboard.

    Parameters
    ----------
    time : string
        The time of day the user is selecting for.
    month : int
        The number of the month the user is selecting for.
    crimes_against : list of strings
        The types of crimes to be considered when filtering the data.

    Returns
    -------
    updated_choro_fig : plotly express figure
        The choropleth figure to be graphed.
    updated_scatter_fig : plotly express figure
        The scatterplot figure to be graphed.

    """
    df = crime_df
    
    # check for time of day
    if time == 'Day':
        filter1_df = df[(df.HOUR >= 7) & (df.HOUR < 19)]
        title = '<br>(in the Day)'
    elif time == 'Night':
        filter1_df = df[(df.HOUR < 7) | (df.HOUR >= 19)]
        title = '<br>(in the Night)'
    else:
        filter1_df = df
        title = ''
    
    # check for month
    filter2_df = filter1_df[filter1_df.MONTH == month]
    
    # check for checkbox selection
    filter3_df = pd.DataFrame()
    if len(crimes_against) == 0:
        filter3_df = filter2_df
    elif len(crimes_against) < 3:
        for val in crimes_against:
            temp_df = filter2_df[filter2_df.OFFENSE_CODE.isin(crime_type[val])]
            filter3_df = pd.concat([filter3_df,temp_df])
    else:
        filter3_df = filter2_df
    
    # update the figures
    updated_df = counting_values_df(filter3_df)
    updated_choro_fig = generate_choropleth(updated_df, Boston)
    updated_choro_fig.update_layout(transition_duration=500)
    updated_choro_fig.update_layout(title_text=f'Crime in Boston in the <br> month of {MONTHS[month]}'+title)
    
    updated_scatter_fig = generate_scatterplot(filter3_df)
    
    return updated_choro_fig, updated_scatter_fig


if __name__ == '__main__':
    app.run_server(debug=True)
