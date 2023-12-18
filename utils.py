#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()

import json
from openai import OpenAI, OpenAIError


# OpenAI client
openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


# Function to call OpenAI API
def get_openai_response(
    prompt: str,
    model: str,
    situation: str,
    question: str,
    language: str = "German",
    index = "#"
) -> str:
    print(f"\n[input row {index}] INPUT:\n* SITUATION: {str(situation)[0:50]}...\n* QUESTION: {str(question)[0:50]}...")

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
            seed = 0,
        )
        return response.choices[0].message.content

    except OpenAIError as e:
        print('\033[31m*** get_openai_response():', str(e), "\033[m")
        return "{'articles': []}"


# Validate gpt response
def validate_articles(output: str) -> set:
    """
    Expects the output:str returned from openai API call in the following structure:-
    {
        "some key": [
            {"article_ref": "CO ART. 337"},
            {"article_ref": "OR ART. 12a Abs. 2"}
        ]
    }
    """
    articles = set()
    try:
        output = json.loads(output)
        output = list(output.values())[0]
        # print(f"\033[93m* Articles retured from GPT: {output}\033[m")
        for i in output:
            articles.add(i["article_ref"])
        print('[+] Validated articles returned from GPT.')
    except Exception as e:
        print('\033[31m*** validate_articles():', str(e), "\033[m")
    return articles

