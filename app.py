#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 22:21:48 2022
@author: nathanmstrauss
DS2001

This a test file to play around with dash and plotly 
according to their tutorial.
"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

MONTHS = [1,2,3,4,5,6,7,8,9,10,11,12]

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
from shapely.geometry import Point, shape

def read_data(filename):
    col_types = {'YEAR': int,'MONTH': int, 'HOUR': int, 
                 'SHOOTING': int, 'OFFENSE_CODE': int, 
                 'Lat': float, 'Long': float}
    df = pd.read_csv(filename, header=0, converters = col_types, engine="python")
    return df
    
def load_geojson(link):
    with urlopen(link) as response:
        area = json.load(response)
        
    neighborhood_map = {}
    for feature in area['features']:
        feature['ID'] = feature['properties']['PD']
        neighborhood_map[feature['properties']['PLANNING_D']] = feature['ID']
        
    return area, neighborhood_map

def clean_df(df):
    district_names = {'DISTRICT': {'A1': 'Charlestown', 'A15': 'Charlestown', 'A7': 'East Boston', 
                      'B2': 'Roxbury', 'B3': 'Mattapan', 'C6': 'South Boston', 
                      'C11': 'Dorchester', 'D4': 'South End', 'D14': 'Brighton',
                      'E5': 'West Roxbury', 'E13': 'Jamaica Plain', 'E18': 'Hyde Park'}}
    new_df = df.replace(to_replace = district_names)
    if 'URC_PART' in df.columns:
        new_df = new_df.drop(['UCR_PART'], axis = 1)
    if 'OFFENSE_CODE_GROUP' in df.columns:
        new_df = new_df.drop(['OFFENSE_CODE_GROUP'], axis = 1)
    return new_df

def check_place(row, geoJson):
    Boston = geoJson
    point = Point(row['Long'],row['Lat'])
    for feature in Boston['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['ID']
        
    return 'DNE'

def counting_values_df(df):
    #count the number of crimes
    num_crimes = df.value_counts('Neighborhood')

    # generate a new DataFrame based on number of crimes
    values = []
    for district, value in num_crimes.items():
        values.append([district, value]) 
    df_choro = pd.DataFrame(values, columns = ['Neighborhood', 'NUM_REPORTS'])
    # df_choro = clean_df(df_choro)
    
    return df_choro

def generate_choropleth(df_choro, place_Json):
    #generate a choropleth map based on number of crimes
    choropleth_fig = px.choropleth(
        df_choro, #crime database
        locations = 'Neighborhood', #define the limits on the map/geography
        geojson = place_Json, #shape information
        color = 'NUM_REPORTS', #defining the color of the scale through the database
        # hover_name = 'Neighborhood', #the information in the box
        hover_data =['NUM_REPORTS'],
        scope="usa",
        featureidkey = 'ID',
        title = "Crime in Boston", #title of the map
        range_color=[0, 8500]
        # animation_frame = 'YEAR' #creating the application based on the year
    )
    choropleth_fig.update_geos(fitbounds = "locations", visible = False)
    choropleth_fig.update_layout(paper_bgcolor="#236C90", plot_bgcolor="#F4F4F8")
    choropleth_fig.update_layout(margin=dict(t=50, r=50, b=25, l=50))
    choropleth_fig.update_layout(font_color='#FFFFFF')
    choropleth_fig.update_layout(title_pad = dict(b=10, l=160, r=0, t=300))
    choropleth_fig.update_layout(title_font_size=30)
    choropleth_fig.update_layout(autosize=True)
    
    return choropleth_fig
    
def generate_scatterplot(df):
    scatter_fig = px.scatter_mapbox(df, lat="Lat", lon="Long", hover_name = 'INCIDENT_NUMBER', 
                            hover_data = ['Neighborhood', 'MONTH', 'DAY_OF_WEEK', 'HOUR', 'OFFENSE_DESCRIPTION'])

    scatter_fig.update_layout(mapbox_style="open-street-map")
    scatter_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    scatter_fig.update_mapboxes(center={'lat': 42.361145, 'lon': -71.057083})
    
    # heatmap_fig = px.density_heatmap(df, y="Lat", x="Long", hover_name = 'INCIDENT_NUMBER', 
                            # hover_data = ['YEAR', 'MONTH', 'DAY_OF_WEEK', 'HOUR', 'DISTRICT'])
    
    return scatter_fig

# read in the data
crime_df = read_data('BosCrime.csv')
file_path = 'https://bostonopendata-boston.opendata.arcgis.com/datasets/boston::planning-districts.geojson?outSR=%7B%22latestWkid%22%3A2249%2C%22wkid%22%3A102686%7D'
Boston, neighborhoods = load_geojson(file_path)

# get the geoJson map
with open('Planning_Districts.geojson') as response:
    area = json.load(response)
    
crime_df['Neighborhood'] = crime_df.apply(lambda row: check_place(row, geoJson = Boston), axis=1)    
    
df_choro = counting_values_df(crime_df)

# generate graphs
choropleth_fig = generate_choropleth(df_choro, Boston)
scatter_fig = generate_scatterplot(crime_df)



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
            html.A(
                html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                href="https://plotly.com/dash/",
            ),
            html.H4(children="Rate of US Poison-Induced Deaths"),
            html.P(
                id="description",
                children="† Deaths are classified using the International Classification of Diseases, \
                Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying \
                cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 \
                (undetermined intent).",
            ),
        ],
    ),
    html.Div(
        id="selectors",
        children=[
            html.Div([
                html.Br(),
                html.Label('Types of Crime'),
                dcc.Checklist(['Violent', 'Non-violent', 'San Francisco'],
                      ['Violent', 'Non-violent']
                ),
                # dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                #              ['Montréal'], # sets the default selection
                #              multi=True),
                ],               
                style={'Padding': 10, 'width': '49%', 'display': 'flex'}
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
                    style={'Padding': 10, 'width': '49%', 'display': 'flex', 'textAlign':'Right'}
                ),
            ],
        style={'display': 'flex', 'flex-direction': 'row'}
        #style={'width': '49%', 'padding': 100, 'flex': 1}
        
        ),
        ]
    ),
    html.Div(
        id="graph-container",
        children=[
            html.P(id="chart-selector", children="Drag the slider to change the months"),
            html.Div(
                dcc.Slider(
                    id="years-slider",
                    min=min(MONTHS),
                    max=max(MONTHS),
                    value=min(MONTHS),
                    marks={
                        str(month): {
                            "label": str(month),
                            "style": {"color": "#7fafdf"},
                                    }
                        for month in MONTHS
                        },
                ),
                style={'width': '40%'}
            ),
            html.Div(
                dcc.Graph(
                    id='choropleth-crime-graph',
                    figure = choropleth_fig,
                    style={'width': '40%', 'padding': 4, 'display': 'flex'}
                ),
            ),
            html.Div(
                dcc.Graph(
                    id='scatterplot-crime-graph',
                    figure = scatter_fig,
                    style={'width': '40%', 'padding': 4, 'display': 'flex'}
                    )
            )
        ]
    )
    
    # dcc.Graph(
    #     id='scatterplot-crime-graph',
    #     figure=scatter_fig
    # )
])
    
@app.callback(
    Output(component_id='choropleth-crime-graph', component_property='figure'),
    Input(component_id='time_of_day', component_property='value')
)
def update_choropleth(time):
    df = crime_df
    if time == 'Day':
        filtered_df = df[(df.HOUR >= 7) & (df.HOUR < 19)]
    elif time == 'Night':
        filtered_df = df[(df.HOUR < 7) | (df.HOUR >= 19)]
    else:
        filtered_df = df
    
    updated_df = counting_values_df(filtered_df)
    updated_choro_fig = generate_choropleth(updated_df, Boston)
    updated_choro_fig.update_layout(transition_duration=500)
    
    return updated_choro_fig
@app.callback(
    Output(component_id='scatterplot-crime-graph', component_property='figure'),
    Input(component_id='time_of_day', component_property='value')
)
def update_scatterplot(time):
    df = crime_df
    if time == 'Day':
        filtered_df = df[(df.HOUR >= 7) & (df.HOUR < 19)]
    elif time == 'Night':
        filtered_df = df[(df.HOUR < 7) | (df.HOUR >= 19)]
    else:
        filtered_df = df
    
    updated_scatter_fig = generate_scatterplot(filtered_df)
    updated_scatter_fig.update_layout(transition_duration=500)
    
    return updated_scatter_fig

if __name__ == '__main__':
    app.run_server(debug=True)
