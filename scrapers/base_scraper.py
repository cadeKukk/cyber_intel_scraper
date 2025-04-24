"""
Base Scraper module that defines the common interface for all scrapers.
"""

import time
import random
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# Get logger
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all scrapers."""
    
    def __init__(self, db, user_agent: str = None):
        """
        Initialize the base scraper.
        
        Args:
            db: Database connection instance
            user_agent: Custom user agent string (optional)
        """
        self.db = db
        self.session = requests.Session()
        
        # Use a realistic user agent if none provided
        if not user_agent:
            self.user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        else:
            self.user_agent = user_agent
            
        self.session.headers.update({"User-Agent": self.user_agent})
        
        # Set default attributes
        self.source_name = self.__class__.__name__
        self.base_url = ""
        self.last_scrape_time = None
    
    def get_page(self, url: str, params: Dict = None, retries: int = 3, 
                 backoff_factor: float = 0.5) -> Optional[requests.Response]:
        """
        Get a web page with retry logic.
        
        Args:
            url: URL to fetch
            params: Request parameters
            retries: Number of retries on failure
            backoff_factor: Exponential backoff factor
            
        Returns:
            Response object if successful, None otherwise
        """
        attempt = 0
        while attempt < retries:
            try:
                # Add small random delay to be respectful to servers
                if attempt > 0:
                    delay = backoff_factor * (2 ** attempt) + random.uniform(0.1, 0.5)
                    time.sleep(delay)
                
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response
            
            except RequestException as e:
                attempt += 1
                logger.warning(f"Request to {url} failed (attempt {attempt}/{retries}): {str(e)}")
                
                if attempt >= retries:
                    logger.error(f"Max retries exceeded for {url}")
                    return None
        
        return None
    
    def parse_html(self, response: requests.Response) -> Optional[BeautifulSoup]:
        """
        Parse HTML from response.
        
        Args:
            response: Response object from requests
            
        Returns:
            BeautifulSoup object if successful, None otherwise
        """
        if not response or not response.content:
            return None
        
        try:
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Failed to parse HTML: {str(e)}")
            return None
    
    def save_data(self, data: Union[Dict, List], content_type: str) -> bool:
        """
        Save scraped data to the database.
        
        Args:
            data: The data to save (dictionary or list of dictionaries)
            content_type: Type of content being saved
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if isinstance(data, list):
                for item in data:
                    item['source'] = self.source_name
                    item['scrape_date'] = datetime.now()
            elif isinstance(data, dict):
                data['source'] = self.source_name
                data['scrape_date'] = datetime.now()
            
            self.db.save(data, content_type)
            count = len(data) if isinstance(data, list) else 1
            logger.info(f"Saved {count} {content_type} items from {self.source_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save data from {self.source_name}: {str(e)}")
            return False
    
    @abstractmethod
    def scrape(self) -> bool:
        """
        Main method to scrape the source.
        This must be implemented by each subclass.
        
        Returns:
            True if scraping succeeded, False otherwise
        """
        pass 