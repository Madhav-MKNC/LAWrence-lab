"""
Testing with _Archive/test_regex.py
"""

import re


# extract article_num string from the article_ref string
def extract_article(article_string: str) -> list:
    """
    Extracts the article number and minor.
    """
    article_string = article_string.lower()
    article_match = re.findall(r'art\.\s*(\d+[a-z]*)', article_string)
    if article_match:
        return article_match
    else:
        print(f'\033[31m[!] extract_article(): No article extracted from {article_string}\033[m')
        return []


# extract bookname string from the article_ref string
def extract_book_from_human(article_string: str) -> str:
    """
    Extracts the name of the law book.
    Assumptions: The book name is expected to be at the start or end of the string only.
    Approach: If the string starts with 'art.', then the book name must be at the end; otherwise, the book name will be at the beginning.
    Final Conclusion: Bookname will always be at the end.
    """
    article_string = article_string.lower()
    return str(article_string.split(" ")[-1])


# extract bookname string from the article_ref string
def extract_book_from_openai(article_string: str):
    """
    Extracts the lawbook name.
    Assumption: bookname would be at the beginning
    """
    # book_name = re.sub(r'art\.\s*(\d+[a-z]*)|([a-z]+\.\s*\d+[a-z]*)', '', article_string.lower()).strip().lower()
    book_name = article_string.lower().strip().split(" ")[0]
    return book_name


# check if predicted_article string is subset of human_article
def is_subset_article(human_article, predicted_article):
    """
    Checks if the predicted article is the same as or a subset of the human-labeled article.
    For example, '34' is a subset of '34a', and '34' matches '34'.
    Approach:   If predicted_article is subset of human_article then after removing predicted_article string
                from human_article string there is be only alpha (a,b,c..) or '' left.
    """
    # return predicted_article.startswith(human_article)
    x = human_article.replace(predicted_article, '')
    return x.isalpha() or x == ""


# get precision, recall
def get_performance(
    human_articles_set: set,
    predicted_artilces_set: set
) -> (float, float, float):
    """
    Evaluate the precision and recall of prompt/model based on the output recieved.
    """
    if not human_articles_set or not predicted_artilces_set:
        precision, recall, coverage = 0, 0, 0
        print("\033[32m[=]", precision, recall, "\033[m")
        return precision, recall, coverage

    # extract human articles and booknames
    human_articles = set()
    for ref in human_articles_set:
        for art in extract_article(ref):
            x = (extract_book_from_human(ref), art)
            human_articles.add(x)
    
    # extract predicted articles and booknames
    predicted_articles = set()
    for ref in predicted_artilces_set:
        for art in extract_article(ref):
            x = (extract_book_from_openai(ref), art)
            predicted_articles.add(x)

    # true positives set
    true_positives = set()
    for pbookname, particle in predicted_articles:
        for hbookname, harticle in human_articles:
            if pbookname == hbookname and is_subset_article(harticle, particle):
                true_positives.add((hbookname, harticle))

    # logging
    print(f"\033[30m*** Human     : {human_articles}\033[m")
    print(f"\033[30m*** Generated : {predicted_articles}\033[m")
    print(f"\033[30m*** true_positives : {true_positives}\033[m")
    
    if not len(predicted_articles) or not len(human_articles):
        precision, recall, coverage = 0, 0, 0
        print("\033[32m[=]", precision, recall, "\033[m")
        return precision, recall, coverage

    precision = len(true_positives) / len(predicted_articles)
    recall = len(true_positives) / len(human_articles)
    coverage = 0
    
    print("\033[32m[=]", precision, recall, "\033[m")
    return precision, recall, coverage
