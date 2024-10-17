import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import chardet as chardet
import dask.dataframe as dd
import os

def file_exists(filename):
    return os.path.exists(filename)

def add_year_to_csv(file_path, year):
    if file_exists(file_path):  
        print("Starting to read the File")
        # Read the CSV file
        df = pd.read_csv(file_path, encoding='ISO-8859-1', low_memory=False)
        # Add 'year' column with the specified value
        df['YEAR'] = year
        # Save the updated DataFrame to a new CSV file
        #new_file_path = file_path.replace('.csv', f'_with_year_{year}.csv')
        df.to_csv(file_path, index = False, mode='w')
        print(f"CSV file updated successfully. New file saved as {file_path}")
    else:
        print(f"{file_path} does not exist.")   

def mergeCSV(orig_csv_file_path, new_csv_file_name, mode):
    # Code that helped to find the encoding error
    # with open(orig_csv_file_path, 'rb') as f:
    #     content = f.read()
    #     print(content[260920:260925])
    if file_exists(orig_csv_file_path):  
        print("Starting to read the File")
        # Read the CSV file into a DataFrame
        df_original_csv = pd.read_csv(orig_csv_file_path, low_memory=False, encoding='latin-1')
        cleaned_csv_path = Path(f"Resources/{new_csv_file_name}.csv")
        if mode == 'a':
            df_original_csv.to_csv(cleaned_csv_path, index=False, mode=mode, header=False) 
        else:
            df_original_csv.to_csv(cleaned_csv_path, index=False, mode=mode)
    else:
        print(f"{orig_csv_file_path} does not exist.")


# The two lines below shows how to call it.
# base_path = Path("Resources")
# createCSV(f"{base_path}/accident_2022.csv.gz",f"{base_path}/accident_2022_label.csv","us_accident_2022","a")
# Mode - a (append in existing file) or w(Overwrite the file)
def createCSV(orig_csv_file_path, lbl_names_file_path, new_csv_file_name, mode):

    if file_exists(orig_csv_file_path):    
        # Code that helped to find the encoding error
        # with open(orig_csv_file_path, 'rb') as f:
        #     content = f.read()
        #     print(content[260920:260925]) 
        print("Starting to read the File")
        df_labels_csv = pd.read_csv(lbl_names_file_path)
        columns_to_keep = df_labels_csv.columns
        print(f"################Labels to Save###################### {columns_to_keep}")
        # Read the CSV file into a DataFrame
        df_original_csv = pd.read_csv(orig_csv_file_path, usecols=df_labels_csv.columns, encoding='latin-1')
        print(f"################Updated CSV File################# {df_original_csv}") 
        #Save the new cleaned data file
        df_original_csv = df_original_csv[df_labels_csv.columns]
        cleaned_csv_path = Path(f"Resources/{new_csv_file_name}.csv")
        if mode == 'a':
            df_original_csv.to_csv(cleaned_csv_path, index=False, mode=mode, header=False) 
        else:
            df_original_csv.to_csv(cleaned_csv_path, index=False, mode=mode)    
    else:
        print(f"{orig_csv_file_path} does not exist.")

# The two lines below shows how to call it.
# base_path = Path("Resources")
# createCSVUsingDask(f"{base_path}/accident_2022.csv.gz",f"{base_path}/accident_2022_label.csv","us_accident_2022")
# TODO - It's not able to overwrite the file, if its present.
# Mode - at (append in existing file) or wt(Overwrite the file)
def createCSVUsingDask(orig_csv_file_path, lbl_names_file_path, new_csv_file_name, mode):
    
    if file_exists(orig_csv_file_path):
        df_labels_csv = pd.read_csv(lbl_names_file_path)
        # Create a list of columns to keep
        columns_to_keep = df_labels_csv.columns
        print(f"################Labels to Save###################### {columns_to_keep}")
        
        # Read the CSV file into a DataFrame with the selected columns
        df_original_csv = dd.read_csv(orig_csv_file_path, usecols=columns_to_keep, encoding='latin-1',dtype={'MINUTENAME': 'object'})
        print(f"################Updated CSV File################# {df_original_csv.columns}")        
    
        # Save the transformed DataFrame to a new CSV scroll    
        cleaned_csv_path = Path(f"Resources/{new_csv_file_name}.csv")
        if mode == 'a':
            df_original_csv.to_csv(cleaned_csv_path, index=False, single_file=True, mode=mode, header=False)
        else:
            df_original_csv.to_csv(cleaned_csv_path, index=False, single_file=True, mode=mode)
    else:
        print(f"{orig_csv_file_path} does not exist.")