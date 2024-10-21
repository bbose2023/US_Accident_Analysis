from importlib.metadata import distribution
from re import L
from flask import Flask, jsonify, render_template, request, url_for, redirect
import requests
from numpy import var
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import plotly as plotly
import json
from utils import *
import os
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    fatalities_by_state = accidentsTotalByStateAllYear()
    df_state = pd.DataFrame(fatalities_by_state).rename(columns={'_id': 'state'})
    
    states = gpd.read_file(gplt.datasets.get_path('contiguous_usa'))
    print(states.columns)
    print(type(states))    

    # Merge your data with geometries
    df_states = states.merge(df_state, on="state")

    # Plot the choropleth map
    ax = gplt.choropleth(
    df_states,
    hue='Fatals',
    cmap='Reds',
    linewidth=0.5,
    edgecolor='black',
    legend=True,
    projection=gcrs.AlbersEqualArea()
    )

    # Set title and show the plot
    plt.title('Total Fatal Crashes State Wide 2019 - 2022')

    plt.savefig("static\images\TotalStatesCrashes.jpeg")
    return render_template('home.html') 

@app.route('/summary')
def summary():
    return render_template('summary.html') 

@app.route('/state-cases')
def state_cases():
    return render_template('state-cases.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/person')
def person():
    return render_template('person.html')

@app.route('/about')
def about():
    return render_template('about.html')


#################################################
# Fatals By Year
# '/api/state-cases/all' - Get Fatals for all years (2019 - 2022)
# '/api/state-cases/all/&year=2019' - Get Fatals for provided year
#################################################
# Fatals for States
#################################################
# '/api/state-cases/all/&factor=state' - Get Fatals for provided year and State
# '/api/state-cases/all/&factor=state&year=2019' - Get Fatals for provided year and State
# '/api/state-cases/all/&factor=state&year=2019&state=Alabama' - Get Fatals for provided year and State
#################################################
# Fatals by weather
#################################################
# '/api/state-cases/all/&factor=weather' - Get Fatals for provided year and State
# '/api/state-cases/all/&factor=weather&year=2019' - Get Fatals for provided year and State
# '/api/state-cases/all/&factor=weather&year=2019&state=Alabama' - Get Fatals for provided year and State
#################################################
# Fatals Data for Map
#################################################
# '/api/state-cases/all/&factor=markers&year=2019' - Get Fatals for provided year and State
# '/api/state-cases/all/&factor=markers&year=2019&state=Alabama' - Get Fatals for provided year and State
#################################################
# Fatals by Week
#################################################
# '/api/state-cases/all/&factor=week' - Get Fatals for provided year and State
# '/api/state-cases/all/&factor=week&year=2019' - Get Fatals for provided year and State
# '/api/state-cases/all/&factor=week&year=2019&state=Alabama' - Get Fatals for provided year and State

@app.route('/api/state-cases/all', methods=['GET'])
def accidentsData():
    year = request.args.get('year')
    state_name = request.args.get('state')
    factor = request.args.get('factor')
    print(type(year))
    if not factor:
        if not year:
            # No year or factor
            return jsonify(accidentsTotalByAllYear())
        else:
            # Logic to fetch accidents for all states for the given year
            return jsonify(accidentsTotalByYear(year))
    if factor == 'state':
        if year and state_name: 
            return jsonify(accidentsTotalByStateYear(year))
        elif year:
            return jsonify(accidentsTotalByStateYear(year))
        elif state_name:
            # Logic to fetch accidents for a specific state for the given year
            return jsonify({'message': f'Year parameter not provided for {state_name}'})
        else:
            return jsonify(accidentsTotalByStateAllYear())
    elif factor == 'weather':
        return jsonify(getWeatherFactors(year,state_name))
    elif factor == 'week':
        return jsonify(getWeekFactors(year, state_name))
    elif factor == 'month':
        return jsonify(getMonthFactors(year, state_name))
    elif factor == 'markers':
        print(year)
        print(state_name)
        return jsonify(getAccidentsMarkers(year, state_name))
    
    elif factor == 'pop':
        return jsonify(getStatePopulationFromCSV())
    
if __name__ == "__main__":
    app.run(debug=True)

