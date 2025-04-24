"""
Research and Academic sources scraper for collecting cybersecurity research and publications.
"""

import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class ResearchAcademicScraper(BaseScraper):
    """Scraper for academic and research cybersecurity sources."""
    
    def __init__(self, db):
        """Initialize the research and academic scraper."""
        super().__init__(db)
        self.source_name = "Academic & Research"
        self.sei_base_url = "https://www.sei.cmu.edu"
        self.cerias_base_url = "https://www.cerias.purdue.edu"
        self.stanford_base_url = "https://cyber.stanford.edu"
        self.sei_insights_url = urljoin(self.sei_base_url, "/insights/publications")
        self.cerias_tech_url = urljoin(self.cerias_base_url, "/tech-reports")
        self.stanford_pubs_url = urljoin(self.stanford_base_url, "/publications")
        self.darpa_base_url = "https://www.darpa.mil"
        self.darpa_i2o_url = urljoin(self.darpa_base_url, "/news-events/research-projects/I2O")
    
    def scrape(self) -> bool:
        """
        Main scraping method that extracts research publications from academic sources.
        
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # Scrape SEI publications
        sei_pubs = self.scrape_sei_publications()
        if sei_pubs:
            if not self.save_data(sei_pubs, "alert"):
                success = False
        else:
            logger.warning("No publications found from SEI")
            success = False
        
        # Scrape CERIAS tech reports
        cerias_reports = self.scrape_cerias_reports()
        if cerias_reports:
            if not self.save_data(cerias_reports, "alert"):
                success = False
        else:
            logger.warning("No tech reports found from CERIAS")
            success = False
        
        # Scrape Stanford Cyber Initiative publications
        stanford_pubs = self.scrape_stanford_publications()
        if stanford_pubs:
            if not self.save_data(stanford_pubs, "alert"):
                success = False
        else:
            logger.warning("No publications found from Stanford Cyber Initiative")
            success = False
        
        # Scrape DARPA I2O news/research
        darpa_news = self.scrape_darpa_i2o()
        if darpa_news:
            if not self.save_data(darpa_news, "alert"):
                success = False
        else:
            logger.warning("No news/research found from DARPA I2O")
            success = False
            
        return success
    
    def scrape_sei_publications(self) -> List[Dict]:
        """
        Scrape publications from Software Engineering Institute.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.sei_insights_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find publication items (adjust selectors based on actual SEI page structure)
            pub_items = soup.find_all('div', {'class': 'publication-item'})
            if not pub_items:
                pub_items = soup.find_all('article')
            
            for item in pub_items:
                try:
                    # Extract publication details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.sei_base_url, title_link.get('href', ''))
                    
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
                    summary = item.find('p', {'class': 'abstract'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Check if it's cybersecurity related
                    if not self._is_cybersecurity_related(title, summary_text):
                        continue
                    
                    # Generate alert ID from date
                    alert_id = f"SEI-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing SEI publication item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} publications from SEI")
            
        except Exception as e:
            logger.error(f"Error scraping SEI publications: {str(e)}")
        
        return alerts
    
    def scrape_cerias_reports(self) -> List[Dict]:
        """
        Scrape tech reports from CERIAS.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.cerias_tech_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find report items (adjust selectors based on actual CERIAS page structure)
            report_items = soup.find_all('div', {'class': 'tech-report'})
            if not report_items:
                report_items = soup.find_all('article')
            
            for item in report_items:
                try:
                    # Extract report details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.cerias_base_url, title_link.get('href', ''))
                    
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
                    summary = item.find('p', {'class': 'abstract'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Check if it's cybersecurity related
                    if not self._is_cybersecurity_related(title, summary_text):
                        continue
                    
                    # Extract report ID from title or generate one
                    alert_id = ""
                    id_match = re.search(r'(\d{4}-\d+)', title)
                    if id_match:
                        alert_id = f"CERIAS-{id_match.group(1)}"
                    else:
                        alert_id = f"CERIAS-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing CERIAS report item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} tech reports from CERIAS")
            
        except Exception as e:
            logger.error(f"Error scraping CERIAS tech reports: {str(e)}")
        
        return alerts
    
    def scrape_stanford_publications(self) -> List[Dict]:
        """
        Scrape publications from Stanford Cyber Initiative.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.stanford_pubs_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find publication items (adjust selectors based on actual Stanford page structure)
            pub_items = soup.find_all('div', {'class': 'publication'})
            if not pub_items:
                pub_items = soup.find_all('article')
            
            for item in pub_items:
                try:
                    # Extract publication details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    title = header.text.strip()
                    url = urljoin(self.stanford_base_url, title_link.get('href', '')) if title_link else self.stanford_pubs_url
                    
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
                    summary = item.find('p', {'class': 'abstract'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Check if it's cybersecurity related
                    if not self._is_cybersecurity_related(title, summary_text):
                        continue
                    
                    # Generate alert ID from date
                    alert_id = f"SCI-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing Stanford publication item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} publications from Stanford Cyber Initiative")
            
        except Exception as e:
            logger.error(f"Error scraping Stanford publications: {str(e)}")
        
        return alerts
    
    def scrape_darpa_i2o(self) -> List[Dict]:
        """
        Scrape news/research from DARPA I2O.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.darpa_i2o_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find news items (adjust selectors based on actual DARPA page structure)
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
                    url = urljoin(self.darpa_base_url, title_link.get('href', ''))
                    
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
                    
                    # Check if it's cybersecurity related
                    if not self._is_cybersecurity_related(title, summary_text):
                        continue
                    
                    # Generate alert ID from date
                    alert_id = f"DARPA-I2O-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing DARPA I2O news item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} news/research items from DARPA I2O")
            
        except Exception as e:
            logger.error(f"Error scraping DARPA I2O news: {str(e)}")
        
        return alerts
    
    def _is_cybersecurity_related(self, title: str, summary: str) -> bool:
        """
        Check if a publication is cybersecurity related based on keywords.
        
        Args:
            title: Publication title
            summary: Publication summary/abstract
            
        Returns:
            True if cybersecurity related, False otherwise
        """
        # Combine title and summary text for checking
        text = f"{title} {summary}".lower()
        
        # List of cybersecurity-related keywords
        keywords = [
            'cyber', 'security', 'vulnerability', 'hack', 'threat', 'attack', 'exploit',
            'malware', 'ransomware', 'phishing', 'breach', 'intrusion', 'encryption',
            'authentication', 'authorization', 'identity', 'privacy', 'data protection',
            'penetration test', 'zero day', 'patch', 'backdoor', 'botnet', 'ddos',
            'firewall', 'ids', 'ips', 'siem', 'defense', 'risk', 'compliance'
        ]
        
        # Check if any keyword is present
        for keyword in keywords:
            if keyword in text:
                return True
                
        return False 