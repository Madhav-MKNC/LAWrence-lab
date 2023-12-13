#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from utils import rate_performance


# command line arguments
args = sys.argv
USAGE = f"USAGE: python {args[0]} START_ROW END_ROW\nExample: python {args[0]} 1 3"

if len(args) != 3:
    print(USAGE)
    sys.exit()

if not args[1].isnumeric() or not args[2].isnumeric():
    print(USAGE)
    sys.exit()


# Read overview sheet
print("# Reading Validation.xlsx")
file_path = 'Validation.xlsx'
xls = pd.ExcelFile(file_path)
overview_df = xls.parse("Overview")


# Processing the prompts within the specified range
def evaluate_performances(start_row: int, end_row: int):
    for index in range(start_row - 1, end_row):
        row = overview_df.iloc[index]

        # evaluate the performance
        precision, recall = rate_performance(
            prompt_num = int(row["Prompt"]),
            prompt_name = row["Prompt Name"],
            full_prompt = row["Full Prompt"],
            model = row["Used model"]
        )

        # Update the "Precision" and "Recall" columns with the calculated values
        overview_df.at[index, 'Precision'] = precision
        overview_df.at[index, 'Recall'] = recall


if __name__ == "__main__":
    print("# Evaluating performances")
    evaluate_performances(
        start_row = args[1],
        end_row = args[2]
    )
