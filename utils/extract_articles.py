#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import time
import pandas as pd

from utils.tools import get_openai_response, validate_articles
from utils.compare import get_performance


# create backup for Validation.xlsx
def create_backup(source_file_path):
    if not os.path.exists("_bak"): os.makedirs("_bak")
    destination_file_path = f"_bak/{time.time()}{source_file_path}"
    shutil.copyfile(source_file_path, destination_file_path)


# save output files
def save_output(df, output_file_path):
    if not os.path.exists("Outputs"): 
        os.makedirs("Outputs")
    df.to_excel(output_file_path, sheet_name="Results", index=False)


# extact articles
def extract_articles(
    prompt_index,
    overview_df,
    ground_truth_df,
    output_file_path
):
    prompt_row = overview_df.iloc[prompt_index]
    
    # read prompts
    prompt_num = prompt_row["Prompt"]
    prompt_name = prompt_row["Prompt Name"]
    full_prompt = prompt_row["Full Prompt"]
    used_model = prompt_row["Used model"]

    # verify values
    if str(prompt_num).lower() == 'nan' or str(prompt_name).lower() == 'nan' or str(full_prompt).lower() == 'nan' or str(used_model).lower() == 'nan':
        return
    
    # validate values
    prompt_num = int(prompt_num)   
    prompt_name = prompt_name.strip()
    full_prompt = full_prompt.strip()
    used_model = used_model.strip()

    print(f"\n[prompt:model {prompt_num}] Using: ({prompt_name}, {used_model})")
    
    # input columns names
    situation_column_head = "Situation"
    questions_column_head = "Questions"
    human_articles_column_head = "Relevant Articles"

    # output column names
    predicted_article_column_head = f"{prompt_num}-Articles"
    precision_column_head = f"{prompt_num}-Precision"
    recall_column_head = f"{prompt_num}-Recall"
    
    # create output columns
    if predicted_article_column_head not in ground_truth_df.columns or precision_column_head not in ground_truth_df.columns or recall_column_head not in ground_truth_df.columns:
        ground_truth_df[predicted_article_column_head] = None
        ground_truth_df[precision_column_head] = None
        ground_truth_df[recall_column_head] = None
    
    # inputs to run tests on 
    for inputs_index, inputs_row in ground_truth_df.iterrows():
        # read inputs
        situation = ground_truth_df.at[inputs_index, situation_column_head]
        question = ground_truth_df.at[inputs_index, questions_column_head]
        expected_article_refs = ground_truth_df.at[inputs_index, human_articles_column_head]
        
        # validate inputs
        if str(situation).lower() == 'nan': continue
        question = question.strip() if str(question).lower() != 'nan' else ""
        human_articles_set = set()
        if str(expected_article_refs).lower() != "nan":
            for i in expected_article_refs.strip().split("\n"):
                human_articles_set.add(i.strip())

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
            human_articles_set = human_articles_set,
            predicted_artilces_set = predicted_article_refs
        )

        # write results
        ground_truth_df.at[inputs_index, predicted_article_column_head] = "\n".join(predicted_article_refs)
        ground_truth_df.at[inputs_index, precision_column_head] = precision
        ground_truth_df.at[inputs_index, recall_column_head] = recall

        # save results
        print("[*] Saving response...")
        save_output(
            df = ground_truth_df,
            output_file_path = output_file_path
        )
        print("[+] Response saved")

