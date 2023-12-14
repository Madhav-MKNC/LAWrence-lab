"""
Testing with _Archive/test_regex.py
"""

import re


# def extract_with_openai(article_string: str):
#     """
#     Extracts {bookName: articleNum(minor)} with OpenAI API.
#     """
#     prompt = "Your task is to extract lawbook name and article num from the following string" ... ya ... "following set"


def extract_article(article_string: str):
    """
    Extracts the article number and minor.
    """
    article_match = re.search(r'art\.\s*(\d+[a-z]*)', article_string.lower())
    if article_match:
        return article_match.group(1)
    else:
        print(f'\033[31m*** extract_article(): No article extracted from {article_string.lower()}\033[m')


def extract_book(article_string: str):
    """
    Extracts the lawbook name.
    """
    book_name = re.sub(r'art\.\s*(\d+[a-z]*)|([a-z]+\.\s*\d+[a-z]*)', '', article_string.lower()).strip()
    return book_name


def is_subset_article(human_article, predicted_article):
    """
    Checks if the predicted article is the same as or a subset of the human-labeled article.
    For example, '34' is a subset of '34a', and '34' matches '34'.
    """
    return predicted_article.startswith(human_article)


# get precision, recall
def get_performance(
    human_articles_set: set,
    predicted_artilces_set: set
) -> (float, float):
    if not human_articles_set or not predicted_artilces_set:
        return 0, 0 
    
    human_articles = {
        extract_book(ref): extract_article(ref) for ref in human_articles_set
    }
    predicted_articles = {
        extract_book(ref): extract_article(ref) for ref in predicted_artilces_set
    }
    true_positives = {
        pred
        for pred in predicted_articles
        for hum in human_articles
        if pred == hum and is_subset_article(human_articles[hum], predicted_articles[pred])
    }
  
    # human_articles = {extract_article(s) for s in human_articles_set}
    # predicted_articles = {extract_article(s) for s in predicted_artilces_set}
    # human_articles.discard(None)
    # predicted_articles.discard(None)
    # if not human_articles or not predicted_articles:
    #     return 0, 0
    # true_positives = {pred for pred in predicted_articles for hum in human_articles if is_subset_article(hum, pred)}
    # false_positives = predicted_articles.difference(true_positives)
    # false_negatives = {hum for hum in human_articles if not any(is_subset_article(hum, pred) for pred in predicted_articles)}

    precision = len(true_positives) / len(predicted_articles)
    recall = len(true_positives) / len(human_articles)
    
    print("\033[31m[=]", precision, recall, "\033[m")
    return precision, recall
