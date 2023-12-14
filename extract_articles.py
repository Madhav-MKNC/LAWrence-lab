#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from utils import get_openai_response, validate_articles
from compare import get_performance


# command line arguments
start_row = 1
end_row = 30
# try:
#     start_row = int(sys.argv[1])
#     end_row = int(sys.argv[2])
# except:
#     print(f"USAGE: python {sys.argv[0]} START_ROW END_ROW\nExample: python {sys.argv[0]} 1 3")
#     sys.exit()

# xlsx files
input_file_path = 'Validation.xlsx'
output_file_path = "Output_Comparison.xlsx"

# Read Articles Extraction sheet
print("[*] Reading Validation.xlsx")
xls = pd.ExcelFile(input_file_path)
overview_df = xls.parse("Overview")
articles_extraction_df = xls.parse("Articles Extraction")


# extact articles
for _, prompt_row in overview_df.iterrows():
    prompt_num = prompt_row["Prompt"]
    prompt_name = prompt_row["Prompt Name"]
    full_prompt = prompt_row["Full Prompt"]
    used_model = prompt_row["Used model"]

    if str(prompt_num).lower() == 'nan' or str(prompt_name).lower() == 'nan' or str(full_prompt).lower() == 'nan' or str(used_model).lower() == 'nan': continue
    
    prompt_num = int(prompt_num)    
    print(f"\n[prompt:model {prompt_num}] Using: {prompt_name}")
    
    # Add rows
    articles_column = f"{prompt_num}-Articles"
    precision_column = f"{prompt_num}-Precision"
    recall_column = f"{prompt_num}-Recall"
    
    articles_extraction_df[articles_column] = None
    articles_extraction_df[precision_column] = None
    articles_extraction_df[recall_column] = None
    
    # inputs to run tests on 
    for index in range(start_row - 1, end_row):
        inputs_row = articles_extraction_df.iloc[index]
        
        situation = inputs_row["Situation"]
        question = inputs_row["Questions"]
        expected_article_refs = inputs_row["Relevant Articles"]
        
        if str(situation).lower() == 'nan': continue
        if str(question).lower() == 'nan': question = ""
        expected_article_refs = set(expected_article_refs.split("\n")) if str(expected_article_refs).lower() != 'nan' else {}
        
        # print("########################################")
        # print(type(expected_article_ref), expected_article_ref, str(expected_article_ref))
        # print("########################################")
        
        response = get_openai_response(
            prompt = full_prompt,
            model = used_model,
            situation = situation,
            question = question,
            index = index + 1
        )
        predicted_article_refs = validate_articles(response)
        
        precision, recall = get_performance(
            human_articles_set = expected_article_refs,
            predicted_artilces_set = predicted_article_refs
        )
        
        # write results
        articles_extraction_df.at[index, articles_column] = "\n".join(predicted_article_refs)
        articles_extraction_df.at[index, precision_column] = precision
        articles_extraction_df.at[index, recall_column] = recall
        
        # save results
        articles_extraction_df.to_excel(output_file_path, sheet_name="Results", index=False)
        print("[+] Response saved")

