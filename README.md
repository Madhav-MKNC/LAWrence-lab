# LAWrence-lab
Comparing the performance of several models with several prompts based on their responses.

# Setup

```
touch .env
```

Add the following creds inside .env file inside the the uc-02 folder and save it.

```
OPENAI_API_KEY=
ENDPOINT=
COSMOS_DB_KEY=
DATABASE_NAME=
CONTAINER_NAME=
```

Install dependencies:

```
pip install -r requirements.txt
```

# Important NOTE

Every prompt should mention only this response format explicitly

```
{
    "articles": [
        {"article_ref": "CO ART. 337"},
        {"article_ref": "OR ART. 12a Abs. 2"}
    ]
}
```

# Run

For Extracting and comparing articles: (output will be saved as Output_Comparison.xlsx)

<code>python extract_articles.py START_ROW END_ROW</code>

Example Usage:

```
python extract_articles.py 1 3
```

For mean performances: (output will be saved as Output_Performance.xlsx)

```
python main.py
```
