"""
NSA, US Cyber Command, and other DoD sources scraper for collecting cybersecurity advisories and alerts.
"""

import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class NSADoDScraper(BaseScraper):
    """Scraper for NSA Cybersecurity Directorate, US Cyber Command, and other DoD cyber entities."""
    
    def __init__(self, db):
        """Initialize the NSA/DoD scraper."""
        super().__init__(db)
        self.source_name = "NSA Cybersecurity Directorate"
        self.nsa_base_url = "https://www.nsa.gov"
        self.cybercom_base_url = "https://www.cybercom.mil"
        self.dc3_base_url = "https://www.dc3.mil"
        self.nsa_advisories_url = urljoin(self.nsa_base_url, "/cybersecurity-advisories")
        self.nsa_alerts_url = urljoin(self.nsa_base_url, "/cybersecurity-alerts")
        self.cybercom_news_url = urljoin(self.cybercom_base_url, "/Media/News")
        self.dc3_news_url = urljoin(self.dc3_base_url, "/news")
    
    def scrape(self) -> bool:
        """
        Main scraping method that extracts advisories and alerts from NSA and DoD sources.
        
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # Scrape NSA cybersecurity advisories
        advisories = self.scrape_nsa_advisories()
        if advisories:
            if not self.save_data(advisories, "alert"):
                success = False
        else:
            logger.warning("No advisories found from NSA Cybersecurity Directorate")
            success = False
        
        # Scrape NSA cybersecurity alerts
        alerts = self.scrape_nsa_alerts()
        if alerts:
            if not self.save_data(alerts, "alert"):
                success = False
        else:
            logger.warning("No alerts found from NSA Cybersecurity Directorate")
            success = False
        
        # Scrape US Cyber Command news/alerts
        cybercom_alerts = self.scrape_cybercom_news()
        if cybercom_alerts:
            if not self.save_data(cybercom_alerts, "alert"):
                success = False
        else:
            logger.warning("No alerts found from US Cyber Command")
            success = False
        
        # Scrape DoD Cyber Crime Center (DC3) news/alerts
        dc3_alerts = self.scrape_dc3_news()
        if dc3_alerts:
            if not self.save_data(dc3_alerts, "alert"):
                success = False
        else:
            logger.warning("No alerts found from DC3")
            success = False
            
        return success
    
    def scrape_nsa_advisories(self) -> List[Dict]:
        """
        Scrape advisories from NSA Cybersecurity Directorate.
        
        Returns:
            List of advisory dictionaries
        """
        advisories = []
        
        try:
            response = self.get_page(self.nsa_advisories_url)
            if not response:
                return advisories
                
            soup = self.parse_html(response)
            if not soup:
                return advisories
            
            # Find advisory items (adjust selectors based on actual NSA page structure)
            advisory_items = soup.find_all('div', {'class': 'usa-card'})
            if not advisory_items:
                advisory_items = soup.find_all('div', {'class': 'news-item'})
            
            for item in advisory_items:
                try:
                    # Extract advisory details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.nsa_base_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('time')
                    if not date_text:
                        date_text = item.find('span', {'class': 'date'})
                    
                    published_date = None
                    if date_text:
                        try:
                            published_date = datetime.strptime(date_text.text.strip(), "%B %d, %Y")
                        except ValueError:
                            try:
                                published_date = datetime.strptime(date_text.text.strip(), "%m/%d/%Y")
                            except ValueError:
                                logger.warning(f"Could not parse date: {date_text.text.strip()}")
                    
                    # Extract summary
                    summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Extract advisory ID from title
                    alert_id = ""
                    id_match = re.search(r'(U/OO/\d+/\d+)', title)
                    if id_match:
                        alert_id = id_match.group(1)
                    else:
                        # Generate ID from date if none found
                        alert_id = f"NSA-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    advisory = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    advisories.append(advisory)
                    
                except Exception as e:
                    logger.error(f"Error parsing NSA advisory item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(advisories)} advisories from NSA Cybersecurity Directorate")
            
        except Exception as e:
            logger.error(f"Error scraping NSA advisories: {str(e)}")
        
        return advisories
    
    def scrape_nsa_alerts(self) -> List[Dict]:
        """
        Scrape alerts from NSA Cybersecurity Directorate.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.nsa_alerts_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find alert items (adjust selectors based on actual NSA page structure)
            alert_items = soup.find_all('div', {'class': 'usa-card'})
            if not alert_items:
                alert_items = soup.find_all('div', {'class': 'news-item'})
            
            for item in alert_items:
                try:
                    # Extract alert details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.nsa_base_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('time')
                    if not date_text:
                        date_text = item.find('span', {'class': 'date'})
                    
                    published_date = None
                    if date_text:
                        try:
                            published_date = datetime.strptime(date_text.text.strip(), "%B %d, %Y")
                        except ValueError:
                            try:
                                published_date = datetime.strptime(date_text.text.strip(), "%m/%d/%Y")
                            except ValueError:
                                logger.warning(f"Could not parse date: {date_text.text.strip()}")
                    
                    # Extract summary
                    summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Extract alert ID from title or generate one
                    alert_id = f"NSA-CSA-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing NSA alert item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} alerts from NSA Cybersecurity Directorate")
            
        except Exception as e:
            logger.error(f"Error scraping NSA alerts: {str(e)}")
        
        return alerts
    
    def scrape_cybercom_news(self) -> List[Dict]:
        """
        Scrape news/alerts from US Cyber Command.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.cybercom_news_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find news items (adjust selectors based on actual USCYBERCOM page structure)
            news_items = soup.find_all('div', {'class': 'news-item'})
            if not news_items:
                news_items = soup.find_all('article')
            
            for item in news_items:
                try:
                    # Extract news details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.cybercom_base_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('time')
                    if not date_text:
                        date_text = item.find('span', {'class': 'date'})
                    
                    published_date = None
                    if date_text:
                        try:
                            published_date = datetime.strptime(date_text.text.strip(), "%B %d, %Y")
                        except ValueError:
                            try:
                                published_date = datetime.strptime(date_text.text.strip(), "%m/%d/%Y")
                            except ValueError:
                                logger.warning(f"Could not parse date: {date_text.text.strip()}")
                    
                    # Extract summary
                    summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Generate alert ID
                    alert_id = f"USCYBERCOM-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing USCYBERCOM news item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} news/alerts from US Cyber Command")
            
        except Exception as e:
            logger.error(f"Error scraping USCYBERCOM news: {str(e)}")
        
        return alerts
    
    def scrape_dc3_news(self) -> List[Dict]:
        """
        Scrape news/alerts from DoD Cyber Crime Center (DC3).
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.dc3_news_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find news items (adjust selectors based on actual DC3 page structure)
            news_items = soup.find_all('div', {'class': 'news-item'})
            if not news_items:
                news_items = soup.find_all('article')
            
            for item in news_items:
                try:
                    # Extract news details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.dc3_base_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('time')
                    if not date_text:
                        date_text = item.find('span', {'class': 'date'})
                    
                    published_date = None
                    if date_text:
                        try:
                            published_date = datetime.strptime(date_text.text.strip(), "%B %d, %Y")
                        except ValueError:
                            try:
                                published_date = datetime.strptime(date_text.text.strip(), "%m/%d/%Y")
                            except ValueError:
                                logger.warning(f"Could not parse date: {date_text.text.strip()}")
                    
                    # Extract summary
                    summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Generate alert ID
                    alert_id = f"DC3-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing DC3 news item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} news/alerts from DC3")
            
        except Exception as e:
            logger.error(f"Error scraping DC3 news: {str(e)}")
        
        return alerts 