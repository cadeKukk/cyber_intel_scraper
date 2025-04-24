"""
FBI Cyber Division and related sources scraper for collecting cybersecurity alerts and incidents.
"""

import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class FBICyberScraper(BaseScraper):
    """Scraper for FBI Cyber Division, Internet Crime Complaint Center, and related sources."""
    
    def __init__(self, db):
        """Initialize the FBI Cyber scraper."""
        super().__init__(db)
        self.source_name = "FBI Cyber Division"
        self.base_url = "https://www.fbi.gov"
        self.ic3_url = "https://www.ic3.gov"
        self.cyber_alerts_url = urljoin(self.base_url, "/investigate/cyber/alerts-and-updates")
        self.cyber_news_url = urljoin(self.base_url, "/investigate/cyber/news")
        self.ic3_alerts_url = urljoin(self.ic3_url, "/Media/Default/PDF/IC3Alerts")
        self.pin_url = urljoin(self.base_url, "/pin")
        self.flash_url = urljoin(self.base_url, "/flash")
    
    def scrape(self) -> bool:
        """
        Main scraping method that extracts alerts and incidents from FBI and IC3.
        
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # Scrape FBI Cyber alerts
        alerts = self.scrape_fbi_alerts()
        if alerts:
            if not self.save_data(alerts, "alert"):
                success = False
        else:
            logger.warning("No alerts found from FBI Cyber Division")
            success = False
        
        # Scrape FBI PINs (Private Industry Notifications)
        pins = self.scrape_pins()
        if pins:
            if not self.save_data(pins, "alert"):
                success = False
        else:
            logger.warning("No PINs found from FBI Cyber Division")
            success = False
        
        # Scrape FBI FLASH notices
        flashes = self.scrape_flashes()
        if flashes:
            if not self.save_data(flashes, "alert"):
                success = False
        else:
            logger.warning("No FLASH notices found from FBI Cyber Division")
            success = False
        
        # Scrape IC3 alerts
        ic3_alerts = self.scrape_ic3_alerts()
        if ic3_alerts:
            if not self.save_data(ic3_alerts, "alert"):
                success = False
        else:
            logger.warning("No alerts found from IC3")
            success = False
            
        return success
    
    def scrape_fbi_alerts(self) -> List[Dict]:
        """
        Scrape alerts from FBI Cyber Division pages.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.cyber_alerts_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find alert items (adjust selectors based on actual FBI page structure)
            alert_items = soup.find_all('div', {'class': 'fbi-card'})
            
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
                    url = urljoin(self.base_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('time')
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
                    summary = item.find('p', {'class': 'summary'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Generate alert ID from date and title
                    alert_id = f"FBI-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing FBI alert item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} alerts from FBI Cyber Division")
            
        except Exception as e:
            logger.error(f"Error scraping FBI Cyber alerts: {str(e)}")
        
        return alerts
    
    def scrape_pins(self) -> List[Dict]:
        """
        Scrape Private Industry Notifications (PINs) from FBI.
        
        Returns:
            List of alert dictionaries
        """
        pins = []
        
        try:
            response = self.get_page(self.pin_url)
            if not response:
                return pins
                
            soup = self.parse_html(response)
            if not soup:
                return pins
            
            # Find PIN items (adjust selectors based on actual FBI page structure)
            pin_items = soup.find_all('div', {'class': 'fbi-card'})
            
            for item in pin_items:
                try:
                    # Extract PIN details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.base_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('time')
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
                    
                    # Extract PIN ID from title
                    alert_id = ""
                    id_match = re.search(r'(PIN\s+\d+-\d+)', title, re.IGNORECASE)
                    if id_match:
                        alert_id = id_match.group(1).replace(" ", "")
                    
                    pin = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    pins.append(pin)
                    
                except Exception as e:
                    logger.error(f"Error parsing FBI PIN item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(pins)} PINs from FBI Cyber Division")
            
        except Exception as e:
            logger.error(f"Error scraping FBI PINs: {str(e)}")
        
        return pins
    
    def scrape_flashes(self) -> List[Dict]:
        """
        Scrape FLASH notices from FBI.
        
        Returns:
            List of alert dictionaries
        """
        flashes = []
        
        try:
            response = self.get_page(self.flash_url)
            if not response:
                return flashes
                
            soup = self.parse_html(response)
            if not soup:
                return flashes
            
            # Find FLASH items (adjust selectors based on actual FBI page structure)
            flash_items = soup.find_all('div', {'class': 'fbi-card'})
            
            for item in flash_items:
                try:
                    # Extract FLASH details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.base_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('time')
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
                    
                    # Extract FLASH ID from title
                    alert_id = ""
                    id_match = re.search(r'(FLASH\s+\d+-\d+)', title, re.IGNORECASE)
                    if id_match:
                        alert_id = id_match.group(1).replace(" ", "")
                    
                    flash = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    flashes.append(flash)
                    
                except Exception as e:
                    logger.error(f"Error parsing FBI FLASH item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(flashes)} FLASH notices from FBI Cyber Division")
            
        except Exception as e:
            logger.error(f"Error scraping FBI FLASH notices: {str(e)}")
        
        return flashes
    
    def scrape_ic3_alerts(self) -> List[Dict]:
        """
        Scrape alerts from Internet Crime Complaint Center (IC3).
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.ic3_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find IC3 alerts (adjust selectors based on actual IC3 page structure)
            alert_items = soup.find_all('div', {'class': 'ic3-alert'})
            
            for item in alert_items:
                try:
                    # Extract alert details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    title = header.text.strip()
                    url = ""
                    
                    if title_link:
                        url = urljoin(self.ic3_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('div', {'class': 'date'})
                    if not date_text:
                        date_text = item.find('time')
                    
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
                    
                    # Generate alert ID from date and title
                    alert_id = f"IC3-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing IC3 alert item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} alerts from IC3")
            
        except Exception as e:
            logger.error(f"Error scraping IC3 alerts: {str(e)}")
        
        return alerts 