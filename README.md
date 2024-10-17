

US_Accident_Analysis
The US-Accidents dataset is a comprehensive collection of traffic accident data from across all states in the United States. This dataset aggregates information sourced from nhtsa.gov. The National Highway Traffic Safety Administration (NHTSA) is a federal agency within the U.S. Department of Transportation, dedicated to ensuring the safety of motor vehicles and their occupants. NHTSA collects and analyzes data related to motor vehicle crashes, aiding in the identification of safety issues and the development of countermeasures.
One key system employed by NHTSA is the Fatality Analysis Reporting System (FARS), which provides data on fatal injuries resulting from motor vehicle traffic crashes in the U.S. Users can run custom queries using the FARS Query System or download comprehensive datasets from their FTP site, covering data from 1975 to 2022.



Project Overview: 
Our project aims to uncover patterns in traffic accidents across the United States by analyzing fatalities over different years. The primary objective is to develop a dashboard that visualizes road accident fatalities in relation to various parameters such as:
* Demographics: Including factors like sex and age of those involved.
* Vehicle Characteristics: Differentiating between various types of vehicles involved in accidents.
* Environmental Conditions: Assessing the impact of weather on accident occurrences.
* Driver Condition: Including intoxication status to evaluate its correlation with fatal outcomes.
Additionally, the dashboard will provide insights into the fatalities categorized by roles, such as drivers, passengers, and collateral victims. To enhance user experience, the dashboard will also feature an interactive map using Leaflet, showcasing the geographical distribution of accidents.
 Data:
The dataset is organized into folders, each containing CSV files that capture various attributes related to traffic accidents. Inside each year’s folder (covering the years 2019 to 2022), the files include:
* Demographic Information: Details on the sex and age of individuals involved in accidents.
* Vehicle Types: Categorization of the different types of vehicles involved in crashes.
* Accident Conditions: Information related to environmental factors like weather conditions and road type at the time of the accident.
* Casualty Details: Statistics on fatalities involving drivers, passengers, and bystanders.
This structured format allows for an in-depth analysis of trends and patterns in traffic accidents over the years. The data is sourced from the NHTSA Fatality Analysis Reporting System (FARS), and we are focusing on data from 2019 to 2022.

ETL:
The data has been queried, cleaned, transformed, and loaded into MongoDB using Python libraries such as Pandas and PyMongo. This systematic approach ensures that the dataset is reliable and well-organized, facilitating comprehensive analysis of traffic accident patterns.



 Data Modeling:
To model the US Accidents dataset, we used a basic data modeling technique called Entity-Relationship Diagrams (ERD). By using this technique six employee database entities or tables are identified, these entities are us_accident, us_vechicle, us_person, us_drug, us_race, us_vision. The attribute or the data type of the entities also presented. At last, the ER diagram was drawn to visualize the relationships between entities/objects (primary key or foreign keys in a database). For a detailed description of the data model and to view the ER diagram, click the following link: QuickDBD-Accident_ERD.png.

Flask REST API Implementation:
A Python Flask REST API has been developed to manage HTTP requests, render templates, and provide JSON serialized data for chart manipulation within the dashboard. This API serves as a bridge between the frontend and backend, allowing for seamless interaction with the data stored in MongoDB.
Dashboard Features:
* Demographic Insights: Analyze fatality rates across age, sex, and race groups.
* Vehicle Involvement: Breakdown of accidents by vehicle type.
* Environmental Impact: Visualize how weather and road conditions correlate with accident rates.
* Driver Condition: Insights into the influence of intoxication on accident outcomes.
* Role-based Fatalities: Statistics on fatalities involving drivers, passengers, and pedestrians.
* Geospatial Mapping: The Leaflet-based map shows the accident locations geographically, allowing users to filter by year or state.









