"""
Testing with _Archive/test_regex.py
"""

import re


# def extract_with_openai(article_string: str):
#     """
#     Extracts {bookName: articleNum(minor)} with OpenAI API.
#     NOTE: this utility is on hold currently 
#     """
#     prompt = "Your task is to extract lawbook name and article num from the following string" ... ya ... "following set"


def extract_article(article_string: str):
    """
    Extracts the article number and minor.
    """
    article_match = re.search(r'art\.\s*(\d+[a-z]*)', article_string.lower())
    if article_match:
        return article_match.group(1).lower()
    else:
        print(f'\033[31m*** extract_article(): No article extracted from {article_string.lower()}\033[m')
        exit()


def extract_book(article_string: str):
    """
    Extracts the lawbook name.
    """
    book_name = re.sub(r'art\.\s*(\d+[a-z]*)|([a-z]+\.\s*\d+[a-z]*)', '', article_string.lower()).strip().lower()
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
        precision, recall = 0, 0
        print("\033[32m[=]", precision, recall, "\033[m")
        return precision, recall
    
    # # printing for comparing visually
    # print(f"\033[34m*** Human     : {human_articles_set}\033[m")
    # print(f"\033[36m*** Generated : {predicted_artilces_set}\033[m")

    # human articles 
    human_articles = []
    for ref in human_articles_set:
        x = (extract_book(ref), extract_article(ref))
        if x not in human_articles:
            human_articles.append(x)
    
    # predicted articles
    predicted_articles = []
    for ref in predicted_artilces_set:
        x = (extract_book(ref), extract_article(ref))
        if x not in predicted_articles:
            predicted_articles.append(x)
    
    # human_articles = [(extract_book(ref), extract_article(ref)) for ref in human_articles_set]
    # predicted_articles = [(extract_book(ref), extract_article(ref)) for ref in predicted_artilces_set]
    
    # printing for comparing visually
    print(f"\033[30m*** Human     : {human_articles}\033[m")
    print(f"\033[30m*** Generated : {predicted_articles}\033[m")
    
    true_positives = {
        (pbookname, particle)
        for (pbookname, particle) in predicted_articles
        for (hbookname, harticle) in human_articles
        if pbookname == hbookname and is_subset_article(harticle, particle)
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
    
    print("\033[32m[=]", precision, recall, "\033[m")
    return precision, recall
