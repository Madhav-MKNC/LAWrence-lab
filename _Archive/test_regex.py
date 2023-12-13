import re


def extract_article(article_string):
    """
    Extracts the article number and minor.
    """
    match = re.search(r'Art\.\s*(\d+[a-z]?)', article_string)
    return match.group(1).lower() if match else None


def extract_book(article_string):
    """
    Extracts the lawbook name.
    """
    match = re.search(r'Art\.\s*(\d+[a-z]?)', article_string)
    return match.group(1).lower() if match else None


def is_subset_article(human_article, predicted_article):
    """
    Checks if the predicted article is the same as or a subset of the human-labeled article.
    For example, '34' is a subset of '34a', and '34' matches '34'.
    """
    return predicted_article.startswith(human_article)

def calculate(human_labeled_set, predicted_set):
    human_articles = {extract_article(s) for s in human_labeled_set}
    predicted_articles = {extract_article(s) for s in predicted_set}

    human_articles.discard(None)
    predicted_articles.discard(None)

    if not human_articles or not predicted_articles:
        return 0, 0

    true_positives = {pred for pred in predicted_articles for hum in human_articles if is_subset_article(hum, pred)}
    false_positives = predicted_articles.difference(true_positives)
    false_negatives = {hum for hum in human_articles if not any(is_subset_article(hum, pred) for pred in predicted_articles)}

    precision = len(true_positives) / len(predicted_articles)
    recall = len(true_positives) / len(human_articles)

    return precision, recall



article_refs = [i.lower() for i in [
    "Art. 108 Ziff. 3 OR",
    "OR ART. 27 Abs. 2bis",
]]


# Extract book name, article number, and paragraph number from each input string
for article_ref in article_refs:
    print(article_ref, "#", extract_article(article_ref))
