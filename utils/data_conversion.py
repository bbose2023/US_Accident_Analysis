from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import plotly as plotly
import json

mongo = MongoClient(port=27017)
db = mongo.us_accidents_db
accident = db.us_accident

# Example MongoDB output
# fatalities_by_state = [
#     {'_id': {'State': 'Alabama', 'StateID': 1, 'Year': 2022}, 'total_fatalities': 913} ]
# flattened_data = flatten_list_of_dicts(fatalities_by_state)
# Output - {'State': 'Alabama', 'StateID': 1, 'Year': 2022, 'total_fatalities': 913}

def flatten_dict(d):
    items = []
    for k, v in d.items():
        new_key = k
        if isinstance(v, dict):
            items.extend(flatten_dict(v).items())
        else:
            items.append((new_key, v))
    return dict(items)

def flatten_list_of_dicts(list_of_dicts):
    flattened_list = [flatten_dict(d) for d in list_of_dicts]
    return flattened_list

#################################################
# Mongo DB Setup
#################################################

# Retrieve Jasonified data that holds state name and its population
def getStatePopulationFromCSV():
    print("Starting to read the File")
    # Read the CSV file into a DataFrame
    df = pd.read_csv("Resources/us_census_2020.csv")
    result = df.to_dict(orient='records')  # Convert DataFrame to list of dicts
    
    # Transform the list of dicts to the required structure
    new_data = []
    for item in result:
        for k, v in item.items():
            new_data.append({"StateName":k,"Population":v})
    
    return new_data


# Total Accident Count For All Year
def accidentsTotalByAllYear():
    pipeline_all_year = [
    {"$group": {"_id": "$YEAR", "Fatals": {"$sum": 1}}},
    {"$sort": {"_id": -1}}  # Sort by year descending
    ]
    fatalities_all_year = list(accident.aggregate(pipeline_all_year))
    # Process data for the chart
   
    return flatten_list_of_dicts(fatalities_all_year)

# Total Accident Count for input Year
def accidentsTotalByYear(year):
    
    pipeline_by_year = [
    {
        "$match": {
        "YEAR": { "$eq": year }
        }
    },
    {"$group": {"_id": "$YEAR", "Fatals": {"$sum": 1}}},
    {"$sort": {"_id": -1}}
    ]
    fatalities_by_year = list(accident.aggregate(pipeline_by_year))
    
    # Process data for the chart
    return flatten_list_of_dicts(fatalities_by_year)

# Cummulative count for crashes from 2019-2022 for each state
#Returns _id, Fatals, percent
def accidentsTotalByStateAllYear():
    
    pipeline_state = [
        {"$group": {"_id": "$STATENAME", "Fatals": {"$sum": 1}}},
        {"$sort": {"Fatals": -1}}  # Sort by fatalities descending
    ]
    fatalities_by_state = list(accident.aggregate(pipeline_state))
    df_state = pd.DataFrame(fatalities_by_state)
    df_state['percent'] = round((df_state['Fatals'] / df_state['Fatals'].sum()) * 100, 2)
    result = df_state.to_dict(orient='records')  # Convert DataFrame to list of dicts
    
    return result

#Returns Year, State, Fatals
def accidentsTotalByStateAndYear(year, state):
    
    pipeline_state = [
        {
        "$match": {
        "YEAR": { "$eq": year },
        "STATE": { "$eq": state },
        }
    },
        {"$group": {"_id":{"Year":"$YEAR","State":"$STATENAME"}, "Fatals": {"$sum": 1}}},
        {"$sort": {"Fatals": -1}}  # Sort by fatalities descending
    ]
    fatalities_by_state = list(accident.aggregate(pipeline_state))
    df_state = pd.DataFrame(fatalities_by_state).rename(columns={'_id': 'StateName'})
    df_state['percent'] = round((df_state['Fatals'] / df_state['Fatals'].sum()) * 100, 2)
    result = df_state.to_dict(orient='records')  # Convert DataFrame to list of dicts
    
    return result

#Returns Year, State, Fatals
def accidentsTotalByStateYear(year):
    
    pipeline_state = [
    {
        "$match": {
        "YEAR": { "$eq": year }
        }
    },
        {"$group": {"_id":{"Year":"$YEAR","State":"$STATENAME"}, "Fatals": {"$sum": 1}}},
        {"$sort": {"Fatals": -1}}  # Sort by fatalities descending
    ]
    fatalities_by_state = list(accident.aggregate(pipeline_state))
    df_state = pd.DataFrame(fatalities_by_state).rename(columns={'_id': 'StateName'})
    df_state['percent'] = round((df_state['Fatals'] / df_state['Fatals'].sum()) * 100, 2)
    result = df_state.to_dict(orient='records')  # Convert DataFrame to list of dicts
    
    return result

# Cummulative count for crashes from 2019-2022 for each state along with its population
#Returns StateName, Fatals, percent, Population
def accidentsTotalAndPopByStateAllYear():
    
    pipeline_state = [
        {"$group": {"_id": "$STATENAME", "Fatals": {"$sum": 1}}},
        {"$sort": {"Fatals": -1}}  # Sort by fatalities descending
    ]
    fatalities_by_state = list(accident.aggregate(pipeline_state))
    df_state = pd.DataFrame(fatalities_by_state).rename(columns={'_id': 'StateName'})
    df_state['percent'] = round((df_state['Fatals'] / df_state['Fatals'].sum()) * 100, 2)

    # Add the population for 2022 for each state
    df_pop = pd.read_csv("Resources/us_census_2020.csv")
    result = df_pop.to_dict(orient='records')  # Convert DataFrame to list of dicts
    
    # Transform the list of dicts to the required structure
    new_data = []
    for item in result:
        for k, v in item.items():
            new_data.append({"StateName": k, "Population": v})    
    df_pop_final = pd.DataFrame(new_data)
    
    # Merge the DataFrames
    df_state = df_state.merge(df_pop_final, on="StateName")
    result = df_state.to_dict(orient='records')  # Convert DataFrame to list of dicts
   
    return result

#Get all accident entries for the given year and state
def getAccidentsMarkers(year, state):
    
    fields_to_select = {
        'YEAR': 1, 
        'STATENAME':1, 
        'FATALS': 1, 
        'LATITUDE':1, 
        'LONGITUD':1,
        '_id': 0} 
    if year and state:
        filter_condition = {"YEAR": year, "STATENAME": state}        
    elif year:
        filter_condition = {"YEAR": year}  
    else:
        return [{'error': 'Year parameter is required'}]
        
    query_result = accident.find(filter_condition,fields_to_select)
    
    return flatten_list_of_dicts(query_result)
    

#Get the accident count per year or for selected state per year 
# Year, State, Weather, Fatals
# Year,  Weather, Fatals
# Weather, Fatals
def getWeatherFactors(year, state):
    
    #Calculate fatalities by Weather
    if year and state:
        pipeline_weather = [
            {
                "$match": {
                "YEAR": { "$eq": year },
                "STATENAME": { "$eq": state },
                }
            },
            {
                "$group": {
                "_id":{"Year":"$YEAR","State":"$STATENAME","Weather":"$WEATHERNAME"}, 
                "Fatals": {"$sum": 1}}
            },
            {"$sort": {"_id.Year":-1,"Fatals": -1}}
        ]
    elif year:
        pipeline_weather = [
            {
                    "$match": {
                        "YEAR": { "$eq": year }
                    }
            },
            {
                "$group": {
                "_id":{"Year":"$YEAR","Weather":"$WEATHERNAME"}, 
                "Fatals": {"$sum": 1}}
            },
            {"$sort": {"_id.Year":-1,"Fatals": -1}}
        ]
    else:
        # Weather Types total in 4 years 
        pipeline_weather = [
            {
                "$group": {
                "_id":{"Weather":"$WEATHERNAME"}, 
                "Fatals": {"$sum": 1}}
            },
            {"$sort": {"Fatals": -1}}
        ]
       
    result = list(accident.aggregate(pipeline_weather))
    
    return flatten_list_of_dicts(result)