#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime

from utils.openai import get_openai_response, validate_articles
from utils.compare import get_performance


# create output file
def get_output_file_path(start_row, end_row):
    current_timestamp = datetime.now()
    formatted_date = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"Outputs/row{start_row+1}to_row{end_row+1}_{formatted_date}.xlsx"    
    return file_path


# save output files
def save_output(df, output_file_path):
    if not os.path.exists("Outputs"): 
        os.makedirs("Outputs")
    df.to_excel(output_file_path, sheet_name="Results", index=False)


# extact articles
def extract_articles(
    ground_truth_df,
    prompt_index,
    prompt_num,
    prompt_name,
    full_prompt,
    used_model,
    output_file_path
):
    print(f"\n[{prompt_num}] Using: ({prompt_name}, {used_model})")
    
    # input columns names
    situation_column_head = "Situation"
    questions_column_head = "Questions"
    human_articles_column_head = "Relevant Articles"

    # output column names
    predicted_article_column_head = f"{prompt_num}-Articles"
    precision_column_head = f"{prompt_num}-Precision"
    recall_column_head = f"{prompt_num}-Recall"
    
    # create output columns if not already exists
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
        
        # logging  
        print(f"\n[{prompt_index+1}.{inputs_index+1}] INPUT:\n*** SITUATION: {str(situation)[0:50]}...\n*** QUESTION: {str(question)[0:50]}...")

        # predict articles with openai
        response = get_openai_response(
            prompt = full_prompt,
            model = used_model,
            situation = situation,
            question = question
        )
        
        # validate openai response
        predicted_article_refs = validate_articles(response)
        
        # evaluate performance
        precision, recall, coverage = get_performance(
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

