# data models


from pydantic import BaseModel
from typing import Optional

import re


class Article(BaseModel):
    # attributes
    articleNumber: str 
    articleNumberMinor: Optional[int]
    paragraphNumber: Optional[int]
    lawbook: str
    
    # constructor
    def __init__(self, article_str: str, provider: str):
        """
        Initialize the class with an article string and a provider.

        Parameters:
        article_str (str): A string containing the article.
        provider (str): The provider of the article. Must be either 'human' or 'openai'.

        Raises:
        ValueError: If the provider is not 'human' or 'openai'.
        """
        self.article_ref = article_str.lower()
        self.provider = provider
        self.articleNumber = self.extract_article_num()
        self.lawbook = self.extract_book_name()
        
    # extract article number from the article string
    def extract_article_num(self):
        pattern = r'art\.\s*(\d+[a-z]*)'
        article_match = re.findall(pattern, self.article_ref)
        if article_match:
            return article_match
        else:
            raise ValueError(f'[!] No article extracted from {self.article_ref}')
    
    # extract book name from the article string
    def extract_book_name(self):
        # book name string is in the end of the article string in ground truth articles
        # and in the beginning of the article string in predicted articles
        pos = -1 if self.provider == "human" else 0
        bookname = self.article_ref.split(" ")[pos]
        return bookname


class MetricCalculation:
    def fullArticleMatch(self, other_article: Article) -> bool:
        pass 
    
    def articleNumMinorMatch(self, other_article: Article) -> bool:
        pass 
    
    def articleNumMatch(self, other_article: Article) -> bool:
        pass 
    
    def isIncludedIn(self, other_article: Article) -> bool:
        pass 
    