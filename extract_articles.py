#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from utils import get_openai_response, validate_articles
from compare import get_performance


# command line arguments
try:
    start_row = int(sys.argv[1]) - 1
    end_row = int(sys.argv[2]) - 1
except:
    print(f"\033[31mUSAGE: python {sys.argv[0]} START_ROW END_ROW\nExample: python {sys.argv[0]} 1 3\033[m")
    sys.exit()

# numerical column indexes
col_mapping = {chr(65+i).upper(): i for i in range(1,27)}  

# xlsx files
input_file_path = 'Validation.xlsx'
output_file_path = "Output_Comparison.xlsx"

# Read Articles Extraction sheet
print("[*] Reading Validation.xlsx")
xls = pd.ExcelFile(input_file_path)
overview_df = xls.parse("Overview")
articles_extraction_df = xls.parse("Ground truth")



# extact articles
# for prompt_index, prompt_row in overview_df.iterrows():
for prompt_index in range(start_row, end_row + 1):
    prompt_row = overview_df.iloc[prompt_index]
    
    # read prompts
    prompt_num = prompt_row["Prompt"]
    prompt_name = prompt_row["Prompt Name"]
    full_prompt = prompt_row["Full Prompt"]
    used_model = prompt_row["Used model"]

    # verify values
    if str(prompt_num).lower() == 'nan' or str(prompt_name).lower() == 'nan' or str(full_prompt).lower() == 'nan' or str(used_model).lower() == 'nan': continue
    
    # validate values
    prompt_num = int(prompt_num)   
    prompt_name = prompt_name.strip()
    full_prompt = full_prompt.strip()
    used_model = used_model.strip()

    print(f"\n[prompt:model {prompt_num}] Using: ({prompt_name}, {used_model})")
    
    # read input columns
    situation_column = col_mapping[prompt_row["Col. Situation"]]
    questions_column = col_mapping[prompt_row["Col. Question"]]
    human_articles_column = col_mapping[prompt_row["Col. Relevant Articles"]]
    
    # read output columns
    predicted_article_column = col_mapping[prompt_row["Col. Generated articles"]]
    precision_column = col_mapping[prompt_row["Col. Precision"]]
    recall_column = col_mapping[prompt_row["Col. Recall"]]
    
    # output column names
    predicted_article_column_head = f"{prompt_num}-Articles"
    precision_column_head = f"{prompt_num}-Precision"
    recall_column_head = f"{prompt_num}-Recall"
    
    # create output columns
    if predicted_article_column_head not in articles_extraction_df.columns or precision_column_head not in articles_extraction_df.columns or recall_column_head not in articles_extraction_df.columns:
        articles_extraction_df[predicted_article_column_head] = None
        articles_extraction_df[precision_column_head] = None
        articles_extraction_df[recall_column_head] = None
    
    # inputs to run tests on 
    for inputs_index, inputs_row in articles_extraction_df.iterrows():
        # # read inputs
        # situation = inputs_row[situation_column]
        # question = inputs_row[questions_column]
        # expected_article_refs = inputs_row[human_articles_column]
        
        # read inputs
        situation = articles_extraction_df.iat[inputs_index, situation_column]
        question = articles_extraction_df.iat[inputs_index, questions_column]
        expected_article_refs = articles_extraction_df.iat[inputs_index, human_articles_column]
        
        # validate inputs
        if str(situation).lower() == 'nan': continue
        question = question.strip() if str(question).lower() != 'nan' else ""
        expected_article_refs = set(expected_article_refs.split("\n")) if str(expected_article_refs).lower() != 'nan' else {}

        # predict articles with openai
        response = get_openai_response(
            prompt = full_prompt,
            model = used_model,
            situation = situation,
            question = question,
            index = inputs_index + 1
        )
        predicted_article_refs = validate_articles(response)
        
        precision, recall = get_performance(
            human_articles_set = expected_article_refs,
            predicted_artilces_set = predicted_article_refs
        )
        
        # # write results
        # articles_extraction_df.at[inputs_index, predicted_article_column] = "\n".join(predicted_article_refs)
        # articles_extraction_df.at[inputs_index, precision_column] = precision
        # articles_extraction_df.at[inputs_index, recall_column] = recall

        # write results
        articles_extraction_df.at[inputs_index, predicted_article_column_head] = "\n".join(predicted_article_refs)
        articles_extraction_df.at[inputs_index, precision_column_head] = precision
        articles_extraction_df.at[inputs_index, recall_column_head] = recall

        # save results
        articles_extraction_df.to_excel(output_file_path, sheet_name="Results", index=False)
        print("[+] Response saved")

