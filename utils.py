#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI, OpenAIError


# Set your OpenAI API key
openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# model = "gpt-4-1106-preview"




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
        return "{}"

