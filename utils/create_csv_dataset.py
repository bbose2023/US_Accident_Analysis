import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import chardet as chardet
import dask.dataframe as dd


def createCSV(original_csv_file_name, lst_label_name, new_csv_file_name):
    orig_csv_file_path = Path(f"Resources/{original_csv_file_name}.csv")
    # Define the file path
    with open(orig_csv_file_path, 'rb') as f:
        result = chardet.detect(f.read())
        detected_encoding = result['encoding']
   
    lbl_names_file_path = Path(f"Resources/{lst_label_name}.csv")
   
    # Read the CSV file into a DataFrame
    df_original_csv = pd.read_csv(orig_csv_file_path, encoding=detected_encoding)
    df_labels_csv = pd.read_csv(lbl_names_file_path)
    df_new_csv_file = pd.DataFrame([])
    # # loop through label_names and get each label
    for col in df_labels_csv.columns:
        df_new_csv_file[col] = df_original_csv[col]

    print(df_new_csv_file.info())

    #Save the new cleaned data file
    cleaned_csv_path = Path(f"Resources/{new_csv_file_name}.csv")
    df_new_csv_file.to_csv(cleaned_csv_path, index=False)

# base_path = Path("Resources")
# createCSVUsingDask(f"{base_path}/accident_2022.csv.gz",f"{base_path}/accident_2022_label.csv","us_accident_2022")

def createCSVUsingDask(orig_csv_file_path, lbl_names_file_path, new_csv_file_name):
    
    print("Starting to read the File")
    
    # Read the CSV file into a DataFrame
    df_original_csv = dd.read_csv(orig_csv_file_path)
    print(f"################Original File################# {df_original_csv}")
    
    df_labels_csv = pd.read_csv(lbl_names_file_path)
    print(f"################Labels to save###################### {df_labels_csv}")
    print(df_original_csv.columns)
    # Create a list of columns to keep
    columns_to_keep = df_labels_csv.columns
    # [col for col in df_original_csv.columns if col not in df_labels_csv.columns]
    print(columns_to_keep.tolist())
    # Select only the desired columns
    # dask.config.set({"dataframe.convert-string": False})
    df = df_original_csv.drop(columns=columns_to_keep.tolist(),axis=1)
    # df = df_original_csv[columns_to_keep]
    print(df)
    #########################Saving of the CSV file doesn't work#############################
    # Save the transformed DataFrame to a new CSV scroll    
    # cleaned_csv_path = Path(f"Resources/{new_csv_file_name}.csv")
    # df.to_csv(cleaned_csv_path, index=False)