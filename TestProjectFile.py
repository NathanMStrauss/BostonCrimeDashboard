#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 22:46:48 2022
@author: nathanmstrauss
DS2000/DS2001
"""

import pandas as pd
import matplotlib.pyplot as plt

def read_data(filename):
    col_types = {'YEAR': int,'MONTH': int, 'HOUR': int, 
                 'SHOOTING': int, 'OFFENSE_CODE': int, 
                 'Lat': float, 'Long': float}
    
    df = pd.read_csv(filename, header=0, converters = col_types, engine="python")
    
    # print(df.iloc[0])
    # print()
    # print(df.iloc[508])
    # print(df.iloc[1102])
    return df


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

    
def main():
    df = read_data('BosCrime.csv')
    map_of_crimes(df)
    bar_by_district(df)
    
    
main()