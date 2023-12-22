#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import create_backup, extract_articles
from datetime import datetime
import sys
import pandas as pd


# command line arguments
try:
    start_row = int(sys.argv[1]) - 1
    end_row = int(sys.argv[2]) - 1
except:
    print(f"\033[31mUSAGE: python {sys.argv[0]} START_ROW END_ROW\nExample: python {sys.argv[0]} 1 3\033[m")
    sys.exit()


# input xlsx file
file_path = 'Ground Truth.xlsx'
create_backup(source_file_path=file_path)

# output xlsx
current_timestamp = datetime.now()
formatted_date = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
output_file_path =  f"Outputs/row{start_row+1}to_row{end_row+1}_{formatted_date}.xlsx"


# Read overview sheet
print("[*] Reading Ground Truth.xlsx file")
xls = pd.ExcelFile(file_path)
overview_df = xls.parse("Overview")
articles_extraction_df = xls.parse("Ground truth")
original_df = articles_extraction_df.copy()


# extracting articles and evualutating performance
print("\n####################################################")
print("## Extracting articles and Evaluating performance ##")
print("####################################################")

for prompt_index in range(start_row, end_row + 1):
    print(f"\n[*] Reading row no. {prompt_index + 1}")
    
    # read for a valid [prompt:model] row
    try:
        prompt_row = overview_df.iloc[prompt_index]
        prompt_num = int(prompt_row["Prompt"])
        prompt_name = prompt_row["Prompt Name"].strip()
        full_prompt = prompt_row["Full Prompt"].strip()
        used_model = prompt_row["Used model"].strip()
    except:
        print(f"\033[31m[{prompt_index+1}] Invalid row.\033[m")
        continue

    # Evaluating performance and updating articles_extraction_df
    extract_articles(
        ground_truth_df = articles_extraction_df,
        prompt_index = prompt_index,
        prompt_num = prompt_num,
        prompt_name = prompt_name,
        full_prompt = full_prompt,
        used_model = used_model,
        output_file_path = output_file_path,
    )


# Calculating average performance
print("\n#####################################")
print("## Calculating average performance ##")
print("#####################################")

for index in range(start_row, end_row + 1):
    print(f"\n[*] Reading row no. {index + 1}")
    
    # read for a valid [prompt:model] row
    try:
        row = overview_df.iloc[index]
        prompt_num = int(row["Prompt"])
        prompt_name = row["Prompt Name"].strip()
        full_prompt = row["Full Prompt"].strip()
        used_model = row["Used model"].strip()
    except:
        print(f"\033[31m[{index+1}] Invalid row.\033[m")
        continue
    
    # fetching performance
    try:
        precision_column = articles_extraction_df[f"{prompt_num}-Precision"]
        recall_column = articles_extraction_df[f"{prompt_num}-Recall"]
    except Exception as e:
        print(f"\033[31m[{index+1}]This [prompt:model] has not been evaluated yet.", str(e), "\033[m")
        continue

    # calculating average values
    sum_p, total_p = 0, 0
    sum_r, total_r = 0, 0
    for p, r  in zip(precision_column, recall_column):
        if str(p).lower() != 'nan':
            sum_p += float(p)
            total_p += 1
        if str(r).lower() != 'nan':
            sum_r += float(r)
            total_r += 1 
    
    # results
    avg_precision, avg_recall = sum_p / total_p, sum_r / total_r

    # # Update the "Precision" and "Recall" columns with the calculated values
    # overview_df.at[index, 'Precision'] = avg_precision
    # overview_df.at[index, 'Recall'] = avg_recall
    
    # # Saving output
    # print("[*] Saving Ouput")
    # with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    #     overview_df.to_excel(writer, sheet_name='Overview', index=False)
    #     original_df.to_excel(writer, sheet_name='Ground truth', index=False)
    # print("[+] Response saved")

    # display results
    print(f"\033[96m[{index+1}] Prompt Num  : {prompt_num}")
    print(f"\033[96m[{index+1}] Prompt Name : {prompt_name}")
    print(f"\033[96m[{index+1}] Used Model  : {used_model}")
    print(f"\033[96m[{index+1}] Prompt      : {full_prompt[0:50]}...")
    print(f"\033[92m[=] Average Precision : {avg_precision}")
    print(f"\033[92m[=] Average Recall    : {avg_recall}\033[m")
    