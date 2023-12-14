#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from utils import get_average_performance


# xlsx files
input_file_path = 'Validation.xlsx'
comparison_results_path = 'Output_Comparison.xlsx'
output_file_path = 'Output_Performance.xlsx'

# Read overview sheet
print("[*] Reading Validation.xlsx sheet: 'Overview'")
xls = pd.ExcelFile(input_file_path)
overview_df = xls.parse("Overview")

# Read comparison results 
print("[*] Reading Output_Comparison.xlsx")
xls = pd.ExcelFile(comparison_results_path)
comparison_df = xls.parse("Results")

# Calculating average performance
for index, row in overview_df.iterrows():
    avg_precision, avg_recall = get_average_performance(
        prompt_num = int(row["Prompt"]),
        results_df = comparison_df
    )

    # Update the "Precision" and "Recall" columns with the calculated values
    overview_df.at[index, 'Precision'] = avg_precision
    overview_df.at[index, 'Recall'] = avg_recall

    # Saving output
    print(f"[*] Saving Ouput for Prompt num: {int(row["Prompt"])}")
    overview_df.to_excel(output_file_path, sheet_name="Results", index=False)
    print("[+] Saved.")

