# -*- coding: utf-8 -*-

import pandas as pd


# xlsx files
input_file_path = 'Validation.xlsx'
output_file_path = 'Output_Validation.xlsx'

# Read overview sheet
print("# Reading Validation.xlsx sheet: 'Overview'")
file_path = 'Validation.xlsx'
xls = pd.ExcelFile(input_file_path)
df = xls.parse("Ground truth")

print(df)

# new_column1 = [1, 2, 3]  # Replace with your data
# new_column2 = ['A', 'B', 'C']  # Replace with your data

# df = df.assign(NewColumn1=new_column1, NewColumn2=new_column2)
# df.to_excel(output_file_path, index=False)

# print("Excel file updated successfully.")


# print(df.iloc[0:2])
# print(df.iloc[0:5]["Used model"])

# print(list(map(int, df["Test"])))
