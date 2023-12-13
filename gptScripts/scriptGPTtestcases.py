import os 


# from data_models import *
import json
from openai import OpenAI, OpenAIError

import pandas as pd
import openai

# Set your OpenAI API key
openai_client = OpenAI(api_key='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')
GPT_MODEL = "gpt-4-1106-preview"


def replace_multiple_first_occurrence(original_string, replacements):
    for old, new in replacements.items():
        # print(f"#####old: {old}, new: {new}")
        original_string = original_string.replace(old, new)
    return original_string

# Function to call OpenAI API

def get_openai_response(prompt, situation, question):
    print(f"####input: {situation},  \n questions: {question}")
    
    substituted_prompt = replace_multiple_first_occurrence(prompt, {"{language}": "German", "{situation}": situation, "{question}": question})
    
    
    # print(f'subtituted prompt: \n{substituted_prompt}')
    
    messages = [
        {
            'role': 'system',
            'content': substituted_prompt
        }
    ]

    try:
        response = openai_client.chat.completions.create(
            messages=messages,
            model = GPT_MODEL,
            response_format = {"type": "json_object"},
            max_tokens=4096,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
    except OpenAIError as e:
        print('\033[31m*** get_openai_response():', str(e), "\033[m")
        
        
    # response = openai.ChatCompletion.create(
    #     model="gpt-4-1106-preview",  # Replace with your desired model
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    return response.choices[0].message.content

def processCsv(): 
    # Read the CSV file
    # df = pd.read_csv('testcases.csv')
    df = pd.read_excel('testcases.xlsx')
    
    with open('prompts/articles.txt', 'r') as file:
        old_prompt = file.read().strip()

    with open('prompts/testing_articles.txt', 'r') as file:
        few_shot_prompt = file.read().strip()
    
    # Iterate over the rows and get responses
    for index, row in df.iterrows():
        response_old_prompt = get_openai_response(old_prompt, row['situation'], row['question'])
        response_few_shot_prompt = get_openai_response(few_shot_prompt, row['situation'], row['question'])
        print(f"\033[93m response_old_prompt: "+ response_old_prompt+"\033[m")
        print(f"\033[93m response_few_shot_prompt: "+ response_few_shot_prompt+"\033[m")
        df.at[index, 'old_prompt_response'] = response_old_prompt
        df.at[index, 'few_shot_prompt_response'] = response_few_shot_prompt
        df.to_excel('output.xlsx', index=False)
        

    # Save the updated dataframe to a new CSV file
    # df.to_csv('updated_file.csv', index=False)


processCsv() 
