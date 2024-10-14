from flask import Flask, jsonify, render_template, request, url_for, redirect
from pymongo import MongoClient
import pandas as pd

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

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
#     return render_template('index.html')

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



if __name__ == "__main__":
    app.run(debug=True)