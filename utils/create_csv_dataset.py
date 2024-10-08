import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import chardet as chardet


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