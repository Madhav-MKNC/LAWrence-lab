#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()

import json
from typing import List
from openai import OpenAI, OpenAIError


# OpenAI client
openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


# get precision and recall
def rate_performance(
    prompt_num: int,
    prompt_name: str,
    full_prompt: str,
    model: str
):
    
    
    precision = 0.3
    recall = 0.4
    # process
    return precision, recall



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


# get precision, recall
def get_performance(
    expected_article_ref: str,
    returned_article_ref: str
) -> (float, float):
    # process
    return 0.2, 0.3


# average of results 
def get_average_performance(
    prompt_num: int
) -> (float, float):
    # process
    return 0.22, 0.33
