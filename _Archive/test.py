# -*- coding: utf-8 -*-

# import pandas as pd


# # xlsx files
# input_file_path = 'Validation.xlsx'
# output_file_path = 'Output_Validation.xlsx'

# # Read overview sheet
# print("# Reading Validation.xlsx sheet: 'Overview'")
# file_path = 'Validation.xlsx'
# xls = pd.ExcelFile(input_file_path)
# df = xls.parse("Ground truth")

# print(df)

# new_column1 = [1, 2, 3]  # Replace with your data
# new_column2 = ['A', 'B', 'C']  # Replace with your data

# df = df.assign(NewColumn1=new_column1, NewColumn2=new_column2)
# df.to_excel(output_file_path, index=False)

# print("Excel file updated successfully.")


# print(df.iloc[0:2])
# print(df.iloc[0:5]["Used model"])

# print(list(map(int, df["Test"])))

import pandas as pd

# Define your process_it function here
def process_it(df):
    # Modify the DataFrame as needed
    # This is a placeholder function
    return df

# Path to your Excel file
file_path = 'your_file.xlsx'

# Read the specific sheets from the Excel file
df_overview = pd.read_excel(file_path, sheet_name='Overview')
df_ground_truth = pd.read_excel(file_path, sheet_name='Ground truth')

# Process the dataframes
df_overview_processed = process_it(df_overview)
df_ground_truth_processed = process_it(df_ground_truth)

# Write the updated data back to the Excel file
with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    df_overview_processed.to_excel(writer, sheet_name='Overview', index=False)
    df_ground_truth_processed.to_excel(writer, sheet_name='Ground truth', index=False)
