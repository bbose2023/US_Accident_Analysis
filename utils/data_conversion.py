
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import plotly as plotly
import json

mongo = MongoClient(port=27017)
db = mongo.us_accidents_db
accident = db.us_accident
person = db.us_person

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
        "YEAR": { "$eq": int(year) }
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
    list_of_dicts = df_state.to_dict(orient='records')
    return flatten_list_of_dicts(list_of_dicts)

#Returns Year, State, Fatals
def accidentsTotalByStateAndYear(year, state):
    
    pipeline_state = [
        {
        "$match": {
        "YEAR": { "$eq": int(year)},
        "STATENAME": { "$eq": state },
        }
    },
        {"$group": {"_id":{"Year":"$YEAR","State":"$STATENAME"}, "Fatals": {"$sum": 1}}},
        {"$sort": {"Fatals": -1}}  # Sort by fatalities descending
    ]
    fatalities_by_state = list(accident.aggregate(pipeline_state))
    df_state = pd.DataFrame(flatten_list_of_dicts(fatalities_by_state)).rename(columns={'State': '_id'})
    df_state['percent'] = round((df_state['Fatals'] / df_state['Fatals'].sum()) * 100, 2)
    list_of_dicts = df_state.to_dict(orient='records')
    return list_of_dicts

#Returns Year, State, Fatals
def accidentsTotalByStateYear(year):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(f'Year received in the request {year}')
    
    pipeline_state = [
    {
        "$match": {
        "YEAR": { "$eq": int(year) }
        }
    },
        {"$group": {"_id":{"Year":"$YEAR","State":"$STATENAME"}, "Fatals": {"$sum": 1}}},
        {"$sort": {"Fatals": -1}}  # Sort by fatalities descending
    ]
    fatalities_by_state = list(accident.aggregate(pipeline_state))
    print(flatten_list_of_dicts(fatalities_by_state))
    df_state = pd.DataFrame(flatten_list_of_dicts(fatalities_by_state)).rename(columns={'State': '_id'})
    df_state['percent'] = round((df_state['Fatals'] / df_state['Fatals'].sum()) * 100, 2)
    list_of_dicts = df_state.to_dict(orient='records')
    return list_of_dicts

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
    return flatten_list_of_dicts(df_state)

#Get all accident entries for the given year and state
def getAccidentsMarkers(year, state):
    # print(year)
    # print(state)
    fields_to_select = {
        'YEAR': 1, 
        'STATENAME':1, 
        'FATALS': 1, 
        'LATITUDE':1, 
        'LONGITUD':1,
        'HARM_EVNAME':1,
        'VE_TOTAL':1,
        'MONTH' :1,
        'MONTHNAME':1,
        'DAY':1,
        'DAY_WEEK':1,
        'DAY_WEEKNAME':1,
        'COUNTYNAME':1,
        'CITYNAME':1,
        'HOUR':1,
        'HOURNAME':1,
        '_id': 0
        } 
    
    if year and state:
        filter_condition = {"YEAR": int(year), "STATENAME": state}        
    elif year:
        filter_condition = {"YEAR": int(year)}  
    else:
        return [{'error': 'Year parameter is required'}]
    
        
    query_result = list(accident.find(filter_condition,fields_to_select))
    print(flatten_list_of_dicts(query_result))
    return query_result
    

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
                "YEAR": { "$eq": int(year) },
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
                        "YEAR": { "$eq": int(year) }
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

    print(f'Weather Data {year} {state} {flatten_list_of_dicts(result)}')
    
    return flatten_list_of_dicts(result)



# Get the accident count per year or for selected state per year 
# Year, Week, Hour,  Fatals
# Year, Week , Fatals
# Week, Fatals

def getWeekFactors(year, state):
    
    #Calculate fatalities by Week days
    if year and state:
        pipeline_week = [
        {
            "$match": {
                "YEAR": { "$eq": int(year)},
                "STATENAME": { "$eq": state },
                "HOUR": {"$lte": 23}
                }
        },
        {   "$group": {
                "_id":{
                      "Year":"$YEAR","State":"$STATENAME",
                      "WeekID":"$DAY_WEEK",
                      "Week":"$DAY_WEEKNAME",
                      "HourID":"$HOUR",
                      "Hour":"$HOURNAME"
                }, 
                "Fatals": {"$sum": 1}}
        },
        {
            "$sort": {"_id.Year":-1,"Fatals": -1}
        }
    ]
    elif year:
        pipeline_week = [
        { 
            "$match": {
                "YEAR": { "$eq": int(year) },
                "HOUR": {"$lte": 23}
                }
        },
        {   "$group": {
                "_id":{
                       "Year":"$YEAR",
                       "WeekID":"$DAY_WEEK",
                       "Week":"$DAY_WEEKNAME",
                       "HourID":"$HOUR",
                       "Hour":"$HOURNAME"
                }, 
                "Fatals": {"$sum": 1}}
        },
        {
            "$sort": {"_id.Year":-1,"Fatals": -1}
        }
    ]
    else:
        # Total Fatalities for weekdays in 4 years 
        pipeline_week = [
        {   
            "$match": {
                "HOUR": {"$lte": 23}
                }
        },
        {
            "$group": {
                "_id":{
                        "WeekID":"$DAY_WEEK",
                        "Week":"$DAY_WEEKNAME",
                        "HourID":"$HOUR",
                        "Hour":"$HOURNAME"
                }, 
                "Fatals": {"$sum": 1}}
        },
        {
            "$sort": {"Fatals": -1}
        }
    ]
       
    result = list(accident.aggregate(pipeline_week))

    print(f'********************************Week Data {year} {state} {flatten_list_of_dicts(result)}*************************************')
    
    return flatten_list_of_dicts(result)


#Get the accident count per year or for selected state per year 
# Year, State, sex, Fatals
# Year, sex, Fatals
# sex, Fatals
#Get the sex count per year or for selected state per year 
def getSexFilter(year,state):
    #Calculate fatalities by sex 
    print('here',241,year, 'state',state)
    
    if year and state:
        intYear=int(year)
        vyear=[intYear]
        sex_pipeline = [
            {
                "$match": {
                    '$and': [
                        #{"PER_TYP": 1},  # Filter for PER_TYP = 1
                        {"SEXNAME": {'$in': ['Male', 'Female']}},
                        {"STATENAME": {'$in': [state]}},
                        {"YEAR": {'$in': vyear}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$SEXNAME" , "COUNT": {"$sum": 1}  # Count occurrences
                }
            },
            {
                "$sort": {
                    "_id.SEXNAME": 1  # Sort by sex ascending
                }
            }
        ]
    elif year:
        intYear=int(year)
        vyear=[intYear]
        sex_pipeline = [
            {
                "$match": {
                    '$and': [
                        #{"PER_TYP": 1},  # Filter for PER_TYP = 1
                        {"SEXNAME": {'$in': ['Male', 'Female']}},
                        #{"STATENAME": {'$in': state}},
                        {"YEAR": {'$in': vyear}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$SEXNAME" , "COUNT": {"$sum": 1}  # Count occurrences
                }
            },
            {
                "$sort": {
                    "_id.SEXNAME": 1  # Sort by sex ascending
                }
            }
        ]
    else:
        sex_pipeline = [
        {
            "$match": {
                '$and': [
                    #{"PER_TYP": 1},  # Uncomment if you need to filter by PER_TYP = 1
                    {"SEXNAME": {'$in': ['Male', 'Female']}},  # Filter for Male or Female
                    {"INJ_SEV": 4}  # Filter by injury severity level 4
                ]
            }
        },
        {
            "$group": {
                "_id": "$SEXNAME",  # Group by the sex name
                "COUNT": {"$sum": 1}  # Count occurrences of each sex
            }
        },
        {
            "$sort": {
                "_id.SEXNAME": 1  # Sort alphabetically by the SEXNAME field
            }
        }
    ]


    # Execute the aggregation
    sex_plot = list(person.aggregate(sex_pipeline))
    print(sex_pipeline)
    return sex_plot


#Get the accident count per year or for selected state per year 
# Year, State, age, Fatals
# Year,  age, Fatals
# age, Fatals    

#Get the age count per year or for selected state per year 
def categorize_age(age):
    if 0 <= age < 5:
        return '0 to 05 Years'
    elif 5 <= age < 9:
        return '05 to 09 Years'
    elif 10 <= age < 14:
        return '10 to 14 Years'
    elif 15 <= age < 20:
        return '15 to 20 Years'
    elif 21 <= age < 24:
        return '21 to 24 Years'
    elif 25 <= age < 34:
        return '25 to 34 Years'
    elif 35 <= age < 44:
        return '35 to 44 Years'
    elif 45 <= age < 54:
        return '45 to 54 Years'   
    elif 55 <= age < 64:
        return '55 to 64 Years'
    elif 65 <= age < 74:
        return '65 to 74 Years'     
    else:
        return '75+ Age'
    
def getageFilter(year,state):
    #Calculate fatalities by age    
    if year and state:
        intYear=int(year)
        vyear=[intYear]
        age_pipeline = [
        {
            "$match": {
                '$and': [
                    #{"PER_TYP": 1},  # Filter for PER_TYP = 1
                    #{'AGE': {'$gte': 15, '$lte': 100}},  # Filter for age between 15 and 100
                    {"STATENAME": {'$in': [state]}},
                    {"YEAR": {'$in': vyear}},
                    {"INJ_SEV":4}
                ]
            }
        },
        {
            "$group": {
                "_id": "$AGE",  # Group by age
                "COUNT": {"$sum": 1}  # Count occurrences
            }
        },
        {
            "$sort": {
                "_id": 1  # Sort by age ascending
            }
        }
    ]
    elif year:
        age_pipeline = [
            {
                "$match": {
                    '$and': [
                        #{"PER_TYP": 1},  # Filter for PER_TYP = 1
                        #{'AGE': {'$gte': 15, '$lte': 100}},  # Filter for age between 15 and 100
                        #{"STATENAME": {'$in': state}},
                        {"YEAR": {'$in': vyear}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$AGE",  # Group by age
                    "COUNT": {"$sum": 1}  # Count occurrences
                }
            },
            {
                "$sort": {
                    "_id": 1  # Sort by age ascending
                }
            }
        ]
    else:
        age_pipeline = [
            {
                "$match": {
                    '$and': [
                        #{"PER_TYP": 1},  # Filter for PER_TYP = 1
                        #{'AGE': {'$gte': 15, '$lte': 100}},  # Filter for age between 15 and 100
                        #{"STATENAME": {'$in': state}},
                        #{"YEAR": {'$in': year}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$AGE",  # Group by age
                    "COUNT": {"$sum": 1}  # Count occurrences
                }
            },
            {
                "$sort": {
                    "_id": 1  # Sort by age ascending
                }
            }
        ]


    # Execute the aggregation
    df_age_plot = pd.DataFrame(list(person.aggregate(age_pipeline))).rename(columns={'_id': 'AGE'})
    df_age_plot['AGE_GROUP'] = df_age_plot['AGE'].apply(categorize_age)
    
    df_age_agg_plot = df_age_plot.groupby('AGE_GROUP', as_index=False)['COUNT'].sum()
    
    #df_age_agg_plot.head(20)
    # Convert df_age_agg_plot DataFrame to a list of dictionaries
    age_agg_list = df_age_agg_plot.to_dict(orient='records')
    
    # Display the list of dictionaries
    return age_agg_list

#Get the accident count per year or for selected state per year 
# Year, State, person type, Fatals
# Year,person type, Fatals
# person type, Fatals   

def getpersontypeFilter(year,state):
    #Calculate fatalities by person type
    
    if year and state:
        intYear=int(year)
        vyear=[intYear]
        person_type_pipeline = [
            {
                "$match": {
                    '$and': [
                        {"PER_TYP": {"$in": [1, 2, 5]}}, 
                    
                        {"STATENAME": {'$in': [state]}},
                        {"YEAR": {'$in': vyear}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$PER_TYPNAME", 
                    "COUNT": {"$sum": 1}  # Count occurrences
                }
            },
            {
                "$sort": {
                    "_id": 1  
                }
            }
        ]
    elif year:
        print('i am here',268)
        person_type_pipeline = [
            {
                "$match": {
                    '$and': [
                        {"PER_TYP": {"$in": [1, 2, 5]}}, 
                    
                        #{"STATENAME": {'$in': state}},
                        {"YEAR": {'$in':vyear}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$PER_TYPNAME", 
                    "COUNT": {"$sum": 1}  # Count occurrences
                }
            },
            {
                "$sort": {
                    "_id": 1  
                }
            }
        ]
    else:
        person_type_pipeline = [
                {
                    "$match": {
                        '$and': [
                            {"PER_TYP": {"$in": [1, 2, 5]}}, 
                        
                            #{"STATENAME": {'$in': state}},
                            #{"YEAR": {'$in': year}},
                            {"INJ_SEV":4}
                        ]
                    }
                },
                {
                    "$group": {
                        "_id": "$PER_TYPNAME", 
                        "COUNT": {"$sum": 1}  # Count occurrences
                    }
                },
                {
                    "$sort": {
                        "_id": 1  
                    }
                }
            ]

    # Execute the aggregation
    persontype_plot = list(person.aggregate(person_type_pipeline))
     # Process data for the chart
    return flatten_list_of_dicts(persontype_plot)

#Get the accident count per year or for selected state per year 
# Year, State, driver drunk type, Fatals
# Year,driver drunk type, Fatals
# driver drunk type, Fatals 


def getdrdrunktypeFilter(year,state):
    #Calculate fatalities by person type
    
    if year and state:
        intYear=int(year)
        vyear=[intYear]
        dr_drunk_type_pipeline = [
            {
                "$match": {
                    '$and': [
                        {"DRINKING": {"$in": [0, 1, 8, 9]}}, 
                        {"PER_TYP": 1},
                        {"STATENAME": {'$in': [state]}},
                        {"YEAR": {'$in': vyear}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$DRINKINGNAME", 
                    "COUNT": {"$sum": 1}  # Count occurrences
                }
            },
            {
                "$sort": {
                    "_id": 1  
                    
                }
            }
        ]
    elif year:
        dr_drunk_type_pipeline = [
                {
                    "$match": {
                        '$and': [
                            {"DRINKING": {"$in": [0, 1, 8, 9]}}, 
                            {"PER_TYP": 1},
                            #{"STATENAME": {'$in': state}},
                            {"YEAR": {'$in': vyear}},
                            {"INJ_SEV":4}
                        ]
                    }
                },
                {
                    "$group": {
                        "_id": "$DRINKINGNAME", 
                        "COUNT": {"$sum": 1}  # Count occurrences
                    }
                },
                {
                    "$sort": {
                        "_id": 1  
                        
                    }
                }
            ]
    else:
        dr_drunk_type_pipeline = [
                {
                    "$match": {
                        '$and': [
                            {"DRINKING": {"$in": [0, 1, 8, 9]}}, 
                            {"PER_TYP": 1},
                            #{"STATENAME": {'$in': state}},
                            #{"YEAR": {'$in': year}},
                            {"INJ_SEV":4}
                        ]
                    }
                },
                {
                    "$group": {
                        "_id": "$DRINKINGNAME", 
                        "COUNT": {"$sum": 1}  # Count occurrences
                    }
                },
                {
                    "$sort": {
                        "_id": 1  
                        
                    }
                }
            ]

    # Execute the aggregation
    dr_drunk_type_plot = list(person.aggregate(dr_drunk_type_pipeline))
    # Process data for the chart
    return flatten_list_of_dicts(dr_drunk_type_plot)

def getTotalFatality(year,state):
    #Calculate fatalities by person type
    if year and state:
        intYear=int(year)
        vyear=[intYear]
        total_pipeline = [
            {
                "$match": {
                    '$and': [
                        {"STATENAME": {'$in': [state]}},
                        {"YEAR": {'$in': vyear}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$sort": {
                    "_id": 1  
                    
                }
            }
        ]
    elif year:
        print('i am here',268)
        total_pipeline = [
                {
                    "$match": {
                        '$and': [
                            #{"STATENAME": {'$in': state}},
                            {"YEAR": {'$in': vyear}},
                            {"INJ_SEV":4}
                        ]
                    }
                },
                {
                    "$sort": {
                        "_id": 1  
                        
                    }
                }
            ]
    else:
        total_pipeline = [
                {
                    "$match": {
                        '$and': [
                            #{"STATENAME": {'$in': state}},
                            #{"YEAR": {'$in': year}},
                            {"INJ_SEV":4}
                        ]
                    }
                },
                {
                    "$sort": {
                        "_id": 1  
                        
                    }
                }
            ]

    # Execute the aggregation
    total_count = list(person.aggregate(total_pipeline))
    # Process data for the chart
    return [len(total_count)]

#Get the accident count per year or for selected state per year 
# Year, State, driver drug type, Fatals
# Year,driver drug type, Fatals
# driver drug type, Fatals 


def getdrdrugtypeFilter(year,state):
    #Calculate fatalities by drug type
    
    if year and state:
        intYear=int(year)
        vyear=[intYear]
        dr_drugs_pipeline = [
                {
                    "$match": {
                        '$and': [
                            {"DRUGS": {"$in": [0, 1, 8, 9]}}, 
                            {"PER_TYP": 1},
                            {"STATENAME": {'$in': [state]}},
                            {"YEAR": {'$in': vyear}},
                            {"INJ_SEV":4}
                        ]
                    }
                },
                {
                    "$group": {
                        "_id": "$DRUGSNAME", 
                        "COUNT": {"$sum": 1}  # Count occurrences
                    }
                },
                {
                    "$sort": {
                        "_id": 1  
                        
                    }
                }
            ]
    elif year:
        dr_drugs_pipeline = [
                {
                    "$match": {
                        '$and': [
                            {"DRUGS": {"$in": [0, 1, 8, 9]}}, 
                            {"PER_TYP": 1},
                            #{"STATENAME": {'$in': [state]}},
                            {"YEAR": {'$in': vyear}},
                            {"INJ_SEV":4}
                        ]
                    }
                },
                {
                   "$group": {
                        "_id": "$DRUGSNAME", 
                        "COUNT": {"$sum": 1}  # Count occurrences
                    }
                },
                {
                    "$sort": {
                        "_id": 1  
                        
                    }
                }
            ]
    else:
        dr_drugs_pipeline = [
                {
                    "$match": {
                        '$and': [
                            {"DRUGS": {"$in": [0, 1, 8, 9]}}, 
                            {"PER_TYP": 1},
                            #{"STATENAME": {'$in': [state]}},
                            #{"YEAR": {'$in': vyear}},
                            {"INJ_SEV":4}
                        ]
                    }
                },
                {
                    "$group": {
                        "_id": "$DRUGSNAME", 
                        "COUNT": {"$sum": 1}  # Count occurrences
                    }
                },
                {
                    "$sort": {
                        "_id": 1  
                        
                    }
                }
            ]

    # Execute the aggregation
    dr_drug_type_plot = list(person.aggregate(dr_drugs_pipeline))
    # Process data for the chart
    return flatten_list_of_dicts(dr_drug_type_plot)

#Get the accident count per year or for selected state per year 
# Year, State, race type, Fatals
# Year,race type, Fatals


def getracetypeFilter(year,state):
    #Calculate fatalities by person type
    
    if year and state:
        intYear=int(year)
        vyear=[intYear]
        race_type_pipeline = [
            {
                "$match": {
                    '$and': [
                        {"RACE": {"$in": [1,2,18,99]}}, 
                        {"STATENAME": {'$in': [state]}},
                        {"YEAR": {'$in': vyear}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$RACENAME", 
                    "COUNT": {"$sum": 1}  # Count occurrences
                }
            },
            {
                "$sort": {
                    "_id": 1  
                }
            }
        ]
    elif year:
        race_type_pipeline = [
            {
                "$match": {
                    '$and': [
                        {"RACE": {"$in": [1,2,18,99]}}, 
                        {"YEAR": {'$in':vyear}},
                        {"INJ_SEV":4}
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$RACENAME", 
                    "COUNT": {"$sum": 1}  # Count occurrences
                }
            },
            {
                "$sort": {
                    "_id": 1  
                }
            }
        ]
    else:
        race_type_pipeline = [
                {
                    "$match": {
                        '$and': [
                            {"RACE": {"$in": [1,2,18,99]}}, 
                            {"INJ_SEV":4}
                        ]
                    }
                },
                {
                    "$group": {
                        "_id": "$RACENAME", 
                        "COUNT": {"$sum": 1}  # Count occurrences
                    }
                },
                {
                    "$sort": {
                        "_id": 1  
                    }
                }
            ]

    # Execute the aggregation
    racetype_plot = list(person.aggregate(race_type_pipeline))
     # Process data for the chart
    return flatten_list_of_dicts(racetype_plot)


#Get the accident count per year or for selected state per year 
# Year,State,Month,Fatals
# Year,Month, Fatals
# Week, Fatals

def getMonthFactors(year, state):
    
    #Calculate fatalities by Week days
    if year and state:
        pipeline_month = [
        {
            "$match": {
                "YEAR": { "$eq": year },
                "STATENAME": { "$eq": state },
                }
        },
        {   "$group": {
                "_id":{
                      "Year":"$YEAR","State":"$STATENAME",
                      "MonthID":"$MONTH",
                      "Month":"$MONTHNAME"
                      
                }, 
                "Fatals": {"$sum": 1}}
        },
        {
            "$sort": {"_id.Year":-1,"Fatals": -1}
        }
    ]
    elif year:
        pipeline_month = [
        { 
            "$match": {
                "YEAR": { "$eq": year },
                }
        },
        {   "$group": {
                "_id":{
                       "Year":"$YEAR",
                       "MonthID":"$MONTH",
                       "Month":"$MONTHNAME"
                }, 
                "Fatals": {"$sum": 1}}
        },
        {
            "$sort": {"_id.Year":-1,"Fatals": -1}
        }
    ]
    else:
        # Total Fatalities for weekdays in 4 years 
        pipeline_month = [
        {
            "$group": {
                "_id":{
                      "MonthID":"$MONTH",
                      "Month":"$MONTHNAME"
                }, 
                "Fatals": {"$sum": 1}}
        },
        {
            "$sort": {"Fatals": -1}
        }
    ]
       
    result = list(accident.aggregate(pipeline_month))
    
    return flatten_list_of_dicts(result)

