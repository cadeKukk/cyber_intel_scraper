"""
US-CERT scraper for collecting cybersecurity advisories and vulnerabilities.
"""

import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class USCertScraper(BaseScraper):
    """Scraper for US-CERT (Cybersecurity and Infrastructure Security Agency)."""
    
    def __init__(self, db):
        """Initialize the US-CERT scraper."""
        super().__init__(db)
        self.source_name = "US-CERT"
        self.base_url = "https://www.cisa.gov"
        self.advisories_url = urljoin(self.base_url, "/known-exploited-vulnerabilities-catalog")
        self.alerts_url = urljoin(self.base_url, "/uscert/ncas/alerts")
    
    def scrape(self) -> bool:
        """
        Main scraping method that extracts both vulnerabilities and alerts.
        
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # Scrape vulnerabilities
        vulns = self.scrape_vulnerabilities()
        if vulns:
            if not self.save_data(vulns, "vulnerability"):
                success = False
        else:
            logger.warning("No vulnerabilities found from US-CERT")
            success = False
        
        # Scrape alerts
        alerts = self.scrape_alerts()
        if alerts:
            if not self.save_data(alerts, "alert"):
                success = False
        else:
            logger.warning("No alerts found from US-CERT")
            success = False
            
        return success
    
    def scrape_vulnerabilities(self) -> List[Dict]:
        """
        Get the Known Exploited Vulnerabilities Catalog (from CISA's JSON feed).

        Returns:
            List of vulnerability dictionaries
        """
        return self.fetch_kev_catalog()

    def scrape_alerts(self) -> List[Dict]:
        """
        Scrape alerts from US-CERT.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.alerts_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find alert items
            alert_items = soup.find_all('div', {'class': 'item-list'})
            
            for item in alert_items:
                try:
                    # Extract alert details
                    header = item.find('h2')
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.base_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('span', {'class': 'date-display-single'})
                    published_date = None
                    if date_text:
                        try:
                            published_date = datetime.strptime(date_text.text.strip(), "%B %d, %Y")
                        except ValueError:
                            logger.warning(f"Could not parse date: {date_text.text.strip()}")
                    
                    # Extract summary
                    summary = item.find('div', {'class': 'field-content'})
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Extract alert ID from title
                    alert_id = ""
                    id_match = re.search(r'(TA\d+-\d+)', title)
                    if id_match:
                        alert_id = id_match.group(1)
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing alert item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} alerts from US-CERT")
            
        except Exception as e:
            logger.error(f"Error scraping US-CERT alerts: {str(e)}")
        
        return alerts 