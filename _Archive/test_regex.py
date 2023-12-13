import re

article_refs = [i.lower() for i in [
    "Art. 108 Ziff. 3 OR",
    "OR ART. 27 Abs. 2bis",
]]

# Define a regex pattern to match book name, article number, and paragraph number
pattern = r'(?:[A-Z]+\.)?\s*((?:\d+\w*)|(?:[A-Z]+\s*\d+\w*))(?:\s*(?:Abs\.|Ziff\.)\s*(\d+\w*))?\s*([A-Z]+)?'


# Function to extract book name, article number, and paragraph number from a string
def extract_book_and_article(string):
    match = re.search(pattern, string)
    if match:
        return match.group(0), match.group(1), match.group(2), match.group(3)
    else:
        return None, None, None

# Extract book name, article number, and paragraph number from each input string
for article_ref in article_refs:
    print(article_ref, "#", extract_book_and_article(article_ref))
