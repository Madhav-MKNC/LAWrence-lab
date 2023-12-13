# LAWrence-lab
Comparing the performance of several models with several prompts based on their responses.

Steps to run the system on local:

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

Run:

```
python main.py START_ROW END_ROW
```

Example Usage:

```
python main.py 1 3
```