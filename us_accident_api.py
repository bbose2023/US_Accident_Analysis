from importlib.metadata import distribution
from re import L
from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_cors import CORS
from numpy import var
from pymongo import MongoClient
import pandas as pd

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)
#################################################
# Mongo DB Setup
#################################################

local_mongo_uri = f"mongodb://localhost:27017/"

mongo = MongoClient(port=27017)

db = mongo.us_accidents_db

accident = db.us_accident

#################################################
# Flask Routes
#################################################

# @app.route('/', methods=('GET', 'POST'))
# def index():
#return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

def accidentsByYear():
    pipeline_year = [
    {"$group": {"_id": "$YEAR", "total_fatalities": {"$sum": 1}}},
    {"$sort": {"_id": -1}}  # Sort by year descending
    ]
    fatalities_by_year = list(accident.aggregate(pipeline_year))
    # Process data for the chart
    data_dict = {item['_id']: item['total_fatalities'] for item in fatalities_by_year}
    return data_dict

# Get the Total Falalities By Year (2019 - 2022)
@app.route('/accidentsByYearData')   
def accidentsByYearData():
    return jsonify(accidentsByYear())

def getAccidentData(YEAR=None, STATE=None):
    # Define the fields you want to select
    fields_to_select = {'YEAR': 1, 'STATE':1, 'VE_TOTAL':1,'STATENAME':1, 'FATALS': 1, 'MONTHNAME':1,'DAY':1,'DAY_WEEKNAME':1, 'COUNTYNAME':1,'CITYNAME':1,'LATITUDE':1, 'LONGITUD':1,'_id': 0}       
    filter_condition = {}
    if YEAR:
        filter_condition['YEAR'] = int(YEAR)  # Ensure YEAR is treated as an integer
    if STATE:
        filter_condition['STATE'] = int(STATE)  # Query STATE as an integer
     # Perform the query using find() with projection
    query_result = list(accident.find(filter_condition,fields_to_select))
    
    return query_result

@app.route('/map/<int:YEAR>/<int:STATE>')
def map_page(YEAR, STATE):
    # Render the index.html template and pass the year and state values
    return render_template('map.html', YEAR=YEAR, STATE=STATE)

@app.route('/data')
def data():
    # Get YEAR and STATE from request arguments
    YEAR = request.args.get('YEAR')
    STATE = request.args.get('STATE')
    # Call the function to get data for 2022 and a specific state
    accident_data = getAccidentData(YEAR=YEAR, STATE=STATE)

    return jsonify(accident_data)

if __name__ == "__main__":
    app.run(debug=True)

