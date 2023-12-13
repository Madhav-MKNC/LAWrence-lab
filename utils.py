#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import json
from typing import List
from openai import OpenAI, OpenAIError


# OpenAI client
openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


# Function to call OpenAI API
def get_openai_response(
    prompt: str,
    model: str,
    situation: str,
    question: str,
    language: str = "German"
) -> str:
    print(f"# INPUT:\n* SITUATION: {situation}\n* QUESTION: {question}")

    messages = [
        {
            'role': 'system',
            'content': prompt.format(situation=situation, question=question, language=language)
        }
    ]

    try:
        response = openai_client.chat.completions.create(
            messages = messages,
            model = model,
            response_format = {"type": "json_object"},
            max_tokens = 4096,
            temperature = 0,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0,
            seed=0,
        )
        return response.choices[0].message.content

    except OpenAIError as e:
        print('\033[31m*** get_openai_response():', str(e), "\033[m")
        return "{'articles': []}"


# Validate gpt response
def validate_articles(output: str) -> List[str]:
    """
    Expects the output:str returned from openai API call in the following structure:-
    {
        "some key": [
            {"article_ref": "CO ART. 337"},
            {"article_ref": "OR ART. 12a Abs. 2"}
        ]
    }
    """
    articles = []
    try:
        output = json.loads(output)
        output = list(output.values())[0]
        print("\033[93m[+] Articles retured from GPT:")
        print(str(output) + "\033[m")
        for i in output:
            articles.append(i["article_ref"])
        print('[+] Validated articles returned from GPT.')
    except Exception as e:
        print('\033[31m*** validate_articles():', str(e), "\033[m")
    return articles


# average of results 
def get_average_performance(
    prompt_num: int
) -> (float, float):
    # Read Output_Comparison
    print("[*] Reading Output_Comparison.xlsx")
    file_path = 'Output_Comparison.xlsx'
    xls = pd.ExcelFile(file_path)
    articles_extraction_df = xls.parse("Results")

    precision_column =  list(map(float, articles_extraction_df[f"{prompt_num}-Precision"]))
    recall_column =  list(map(float, articles_extraction_df[f"{prompt_num}-Recall"]))

    avg_precision = sum(precision_column) / len(precision_column)
    avg_recall = sum(recall_column) / len(recall_column)
    
    return avg_precision, avg_recall

