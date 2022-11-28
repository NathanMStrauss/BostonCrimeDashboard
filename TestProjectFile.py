#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 22:46:48 2022
@author: nathanmstrauss
DS2000/DS2001
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from urllib.request import urlopen
import json
from shapely.geometry import Point, shape

PLACES = ['East Boston', 'Charlestown', 'South Boston', 'Central', 
          'Back Bay/Beacon Hill', 'South End', 'Fenway/Kenmore', 
          'Allston/Brighton', 'Jamaica Plain', 'Roxbury', 'North Dorchester', 
          'South Dorchester', 'Mattapan', 'Roslindale', 'West Roxbury', 
          'Hyde Park', 'Harbor Islands']

DISTRICT_NAMES = {'DISTRICT': {'A1': 'Charlestown', 'A15': 'Charlestown', 'A7': 'East Boston', 
                  'B2': 'Roxbury', 'B3': 'Mattapan', 'C6': 'South Boston', 
                  'C11': 'Dorchester', 'D4': 'South End', 'D14': 'Brighton',
                  'E5': 'West Roxbury', 'E13': 'Jamaica Plain', 'E18': 'Hyde Park'}}

def read_data(filename):
    col_types = {'YEAR': int,'MONTH': int, 'HOUR': int, 
                 'SHOOTING': int, 'OFFENSE_CODE': int, 
                 'Lat': float, 'Long': float}
    
    df = pd.read_csv(filename, header=0, converters = col_types, engine="python")
    
    # print(df.iloc[0:100]['OCCURRED_ON_DATE'])
    # print()
    # print(df.iloc[508])
    # print(df.iloc[1102])
    return df

def clean_df(df):
    new_df = df.replace(to_replace = DISTRICT_NAMES) 
    
    if 'URC_PART' in df.columns:
        new_df = new_df.drop(['UCR_PART'], axis = 1)
    if 'OFFENSE_CODE_GROUP' in df.columns:
        new_df = new_df.drop(['OFFENSE_CODE_GROUP'], axis = 1)
        
    new_df[['OCCURRENCE_DATE','OCCURRENCE_TIME']] = df.OCCURRED_ON_DATE.str.split(expand=True)
    return new_df

def map_of_crimes(df):
    plt.figure(dpi=200)
    lats_exist = df[df["Lat"] != 0]
    coords_exist = lats_exist[lats_exist["Long"] != 0]
    coords_exist.plot.scatter(x = "Long", y = "Lat", alpha = 0.3)
    
    plt.title('Crime in Boston by Location')
    plt.xlim([-71.4, -70.9])
    plt.ylim([42.2, 42.5])
    plt.plot(-71.089007, 42.339475, 'rx')
    plt.annotate('Northeastern', (-71.089007, 42.339475), textcoords = 'offset points', xytext = (5,-5))
    plt.plot(-71.062415, 42.356259, 'rx')
    plt.annotate('Park Street', (-71.062415, 42.356259), textcoords = 'offset points', xytext = (5,-5))
    plt.plot(-71.117092, 42.374196, 'rx')
    plt.annotate('Harvard', (-71.117092, 42.374196), textcoords = 'offset points', xytext = (5,-5))
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    plt.show()
    
def bar_by_district(df):
    uniques = set(df["DISTRICT"])

    plt.figure(figsize=[9,7], dpi=200)
    for district in uniques:
        height = 0
        height = len(df[df["DISTRICT"] == district])
        # print(f'{district:12} ', '\theight: ', height)
        plt.bar(district, height)
        
    plt.title('Crime by district')
    plt.xlabel('District')    
    plt.ylabel('Frequency')    
    plt.show()

def load_geojson(link):
    with urlopen(link) as response:
        area = json.load(response)
        
    neighborhood_map = {}
    for feature in area['features']:
        feature['ID'] = feature['properties']['PD']
        neighborhood_map[feature['properties']['PLANNING_D']] = feature['ID']
        
    return area, neighborhood_map

def time_df(df,time_of_day):
    
    if time_of_day == 'night':
        df = df[(df.HOUR < 7) | (df.HOUR >= 18)]
    elif time_of_day == 'day':
        df = df[(df.HOUR >= 7) & (df.HOUR < 18)]
        
    return df


def check_place(row, geoJson):
    Boston = geoJson
    point = Point(row['Long'],row['Lat'])
    for feature in Boston['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['ID']
        
    return 'DNE'

    
def main():
    df = read_data('BosCrime.csv')
    df = clean_df(df)
    
    Boston, neighborhoods = load_geojson('https://bostonopendata-boston.opendata.arcgis.com/datasets/boston::planning-districts.geojson?outSR=%7B%22latestWkid%22%3A2249%2C%22wkid%22%3A102686%7D')
    # df = df[(df.Lat != 0.0) & (df.Long != 0.0)]
    
    print()
    day_df = time_df(df, time_of_day = 'night')
    # print(day_df)
    
    df['Neighborhood'] = df.apply(lambda row: check_place(row, geoJson = Boston), axis=1)
    print(df.columns)

    
            
    # map_of_crimes(df)
    # bar_by_district(df)
    
    
main()