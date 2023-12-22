# data models


from pydantic import BaseModel
from typing import Optional, List, Set, Dict

import re


class Article(BaseModel):
    """
    Base class for Articles.
    """
    articleNumber: str 
    articleNumberMinor: Optional[int]
    paragraphNumber: Optional[int]
    lawbook: str

    def __init__(self, article_str: str, source: str) -> None:
        """
        Initialize the class with an article string and a source.

        Parameters:
        article_str (str): A string containing the article.
        source (str): The source of the article. Must be either 'human' or 'openai'.

        Raises:
        ValueError: If the source is not 'human' or 'openai'.
        """
        
        self.article_ref = article_str.lower()
        self.source = source
        self.articleNumber = self.__extract_article_num()
        self.lawbook = self.__extract_book_name()
        self.article_tuple = (self.lawbook, self.articleNumber)
        
    def __extract_article_num(self) -> str:
        """
        Extract article number from the article string.
        """
        
        pattern = r'art\.\s*(\d+[a-z]*)'
        article_match = re.findall(pattern, self.article_ref)
        if article_match:
            return article_match
        else:
            raise ValueError(f'[!] No article extracted from {self.article_ref}')
    
    def __extract_book_name(self) -> str:
        """
        Extract book name from the article string.
        """
        
        # book name string is in the end of the article string in ground truth articles
        # and in the beginning of the article string in predicted articles
        pos = -1 if self.source == "human" else 0
        bookname = self.article_ref.split(" ")[pos]
        return bookname


class MetricCalculation:
    """
    Class for handling performance evaluating operations.
    """
    
    def __init__(self, human_article: Article, predicted_article: Article) -> None:
        
        self.human_article = human_article
        self.predicted_article = predicted_article
    
    def fullArticleMatch(self) -> bool:
        """
        Compares the full article i.e. (bookname, articlenum) tuple
        """
        
        return True
    
    def is_subset_article(human_article: Article, predicted_article: Article) -> bool:
        """
        Checks if the predicted article is the same as or a subset of the human-labeled article.
        For example, '34' is a subset of '34a', and '34' matches '34'.
        Approach:   If predicted_article is subset of human_article then after removing predicted_article string
                    from human_article string there is be only alpha (a,b,c..) or '' left.
        """
        
        return True
    
    def calculate_precision(self) -> float:
        """
        Calculate the precision of prompt/model based on the output recieved.
        """
        
        self.precision = 0
        return self.precision
    
    def calculate_recall(self) -> float:
        """
        Calculate the recall of prompt/model based on the output recieved.
        """
        
        self.recall = 0 
        return self.recall
    
    def calculate_coverage(self) -> float:
        """
        Calculate the coverage of prompt/model based on the output recieved.
        """
        
        self.coverage = 0
        return self.coverage


class OpenAI:
    """
    Class for handling OpenAI calls.
    """
    response_format: Optional[Dict[str, str]]
    temperature: Optional[int]
    top_p: Optional[int]
    frequency_penalty: Optional[int]
    presence_penalty: Optional[int]
    seed: Optional[int]
    
    def get_response(
        self,
        prompt_content: str,
        model: str,
        role: str = 'system',
    ) -> str:
        """
        OpenAI chat completion API.
        """
        
        messages = [{'role': role, 'content': prompt_content}]
        response = ...
        return response

    def get_article(
        self,
        prompt: str,
        model: str,
        situation: str,
        question: str,
        language: str = "German",
    ) -> Set[str]:
        """
        Retrieve Articles.
        """
        
        prompt_content = prompt.format(
            situation = situation,
            question = question,
            language = language
        )
        output = self.get_response(
            prompt_content = prompt_content,
            model = model
        )
        articles = self.validate_articles(output)
        return articles

    def validate_articles(self, output_str) -> Set[str]:
        """
        Validate the Retrieved Articles.

        Expects the output:str returned from openai API call in the following structure:-
            {
                "some key": [
                    {"article_ref": "CO ART. 337"},
                    {"article_ref": "OR ART. 12a Abs. 2"}
                ]
            }
        Returns:-
            {
                "CO ART. 337",
                "OR ART. 12a Abs. 2"
            }
        """
        
        return {"OR Art. 99m"}


class HandleCSVData:
    """
    Class for processing the CSV data.
    """
    