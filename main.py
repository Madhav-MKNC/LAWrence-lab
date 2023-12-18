#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pandas as pd

# command line arguments
try:
    start_row = int(sys.argv[1]) - 1
    end_row = int(sys.argv[2]) - 1
except:
    print(f"\033[31mUSAGE: python {sys.argv[0]} START_ROW END_ROW\nExample: python {sys.argv[0]} 1 3\033[m")
    sys.exit()

# xlsx files
file_path = 'Validation.xlsx'

# Read overview sheet
print("[*] Reading Validation.xlsx sheet")
xls = pd.ExcelFile(file_path)
overview_df = xls.parse("Overview")
articles_extraction_df = xls.parse("Ground truth")

# Calculating average performance
# for index, row in overview_df.iterrows():
for index in range(start_row, end_row + 1):
    print(f"\n[*] Reading row no. {index + 1}")
    
    # read [prompt:model]
    try:
        row = overview_df.iloc[index]
        prompt_num = int(row["Prompt"])
    except:
        print("\033[31m[!] [prompt:model] row empty.\033[m")
        continue
    
    # fetching performance from Output_Comparison.xlsx
    print(f"[*] [prompt:model] {prompt_num}")
    try:
        precision_column = articles_extraction_df[f"{prompt_num}-Precision"]
        recall_column = articles_extraction_df[f"{prompt_num}-Recall"]
    except Exception as e:
        print("\033[31m[-]This [prompt:model] has not been evaluated yet.", str(e), "\033[m")
        continue
    
    # mean precision
    sum_p = 0
    total_p = 0
    for p in precision_column:
        if str(p).lower() != 'nan':
            sum_p += float(p)
            total_p += 1
    
    # mean recall
    sum_r = 0
    total_r = 0
    for n in recall_column:
        if str(n).lower() != 'nan':
            sum_r += float(n)
            total_r += 1
    
    avg_precision, avg_recall = sum_p/total_p, sum_r/total_r

    # Update the "Precision" and "Recall" columns with the calculated values
    overview_df.at[index, 'Precision'] = avg_precision
    overview_df.at[index, 'Recall'] = avg_recall

    # Saving output
    print("[*] Saving Ouput")
    with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        overview_df.to_excel(writer, sheet_name='Overview', index=False)
        articles_extraction_df.to_excel(writer, sheet_name='Ground truth', index=False)
    print("[+] Response saved")

