from flask import Flask, jsonify, render_template, request, url_for, redirect
import requests
import pandas as pd
import plotly.express as px
import plotly as plotly
import json
from utils import *
import os

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
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
@app.route('/api/state-cases/all', methods=['GET'])
def accidentsData():
    year = request.args.get('year')
    state_name = request.args.get('state')
    factor = request.args.get('factor')
    if not factor:
        if not year:
            # No year or factor
            return jsonify(accidentsTotalByAllYear())
        else:
            # Logic to fetch accidents for all states for the given year
            return jsonify(accidentsTotalByYear(year))

    if factor == 'state':
        if year and state_name:
            return jsonify(accidentsTotalByStateAndYear(year, state_name))
        elif year:
            return jsonify(accidentsTotalByStateYear(year))
        elif state_name:
            # Logic to fetch accidents for a specific state for the given year
            return jsonify({'message': f'Year parameter not provided for {state_name}'})
        else:
            return jsonify(accidentsTotalByStateAllYear())
    elif factor == 'weather':
        return jsonify(getWeatherFactorsForStates(year,state_name))
    elif factor == 'markers':
        return jsonify(getAccidentsByYearOrStateData(year, state_name))
    elif factor == 'pop':
        return jsonify(getStatePopulationFromCSV())

if __name__ == '__main__':

    app.run(debug=True)