# LAWrence-lab
Comparing the performance of several models with several prompts based on their responses.

# Setup

```
touch .env
```

Add the following creds inside .env file.

```
OPENAI_API_KEY=
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

For mean performances: (output will be saved as Output_Performance.xlsx)

<code>python evaluate.py START_ROW END_ROW</code>

Example Usage:

```
python evaluate.py 1 3
```