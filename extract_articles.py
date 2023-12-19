#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import time
import pandas as pd
from utils import get_openai_response, validate_articles
from compare import get_performance


# create backup for Validation.xlsx
def create_backup(file_path):
    source_file_path = file_path
    if not os.path.exists("bak"): os.makedirs("bak")
    destination_file_path = f"bak/{time.time()}{source_file_path}"
    shutil.copyfile(source_file_path, destination_file_path)


# extact articles
def extract_articles(
    prompt_index,
    overview_df,
    articles_extraction_df,
    file_path
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
    if predicted_article_column_head not in articles_extraction_df.columns or precision_column_head not in articles_extraction_df.columns or recall_column_head not in articles_extraction_df.columns:
        articles_extraction_df[predicted_article_column_head] = None
        articles_extraction_df[precision_column_head] = None
        articles_extraction_df[recall_column_head] = None
    
    # inputs to run tests on 
    for inputs_index, inputs_row in articles_extraction_df.iterrows():
        # read inputs
        situation = articles_extraction_df.at[inputs_index, situation_column_head]
        question = articles_extraction_df.at[inputs_index, questions_column_head]
        expected_article_refs = articles_extraction_df.at[inputs_index, human_articles_column_head]
        
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
        articles_extraction_df.at[inputs_index, predicted_article_column_head] = "\n".join(predicted_article_refs)
        articles_extraction_df.at[inputs_index, precision_column_head] = precision
        articles_extraction_df.at[inputs_index, recall_column_head] = recall

        # save results
        print("[*] Saving response...")
        with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            overview_df.to_excel(writer, sheet_name='Overview', index=False)
            articles_extraction_df.to_excel(writer, sheet_name='Ground truth', index=False)
        print("[+] Response saved")

