#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from utils import rate_performance, get_openai_response, validate_articles, get_performance


# Read Articles Extraction sheet
print("# Reading Validation.xlsx sheet: 'Articles Extraction'")
file_path = 'Validation.xlsx'
xls = pd.ExcelFile(file_path)
articles_extraction_df = xls.parse("Articles Extraction")


# Evaluate performances based on different inputs
def evaluate_performances_for_inputs(start_row: int, end_row: int):
    for index in range(start_row - 1, end_row):
        row = articles_extraction_df.iloc[index]
        
        situation = row["Situation"]
        question = row["Questions"]
        
        expected_article_ref = row["Relevant Articles"]
        
        overview_df = xls.parse("Overview")
        for _, prompt_row in overview_df.iterrows():
            prompt_num = int(prompt_row["Prompt"]),
            prompt_name = prompt_row["Prompt Name"],
            full_prompt = prompt_row["Full Prompt"],
            used_model = prompt_row["Used model"]
            
            print(f"* Using {prompt_num}: {prompt_name}")
            
            response = get_openai_response(
                prompt = full_prompt,
                model = used_model,
                situation = situation,
                question = question
            )
            returned_article_ref = validate_articles(response)
            
            print("Evaluating precision, recall")
            precision, recall = get_performance(
                expected_article_ref = expected_article_ref,
                returned_article_ref = returned_article_ref
            )
            
            articles_extraction_df.at[index, 'Precision'] = precision

        
        # for/
        # returned_articles_ref = get_articles()
        # evaluate the performance
        precision, recall = rate_performance(
            prompt_num = int(row["Prompt"]),
            prompt_name = row["Prompt Name"],
            full_prompt = row["Full Prompt"],
            model = row["Used model"]
        )

        # Update the "Precision" and "Recall" columns with the calculated values
        articles_extraction_df.at[index, 'Precision'] = precision
        articles_extraction_df.at[index, 'Recall'] = recall



