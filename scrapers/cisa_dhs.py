"""
CISA and DHS scraper for collecting cybersecurity advisories, vulnerabilities, and alerts.
"""

import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class CISADHSScraper(BaseScraper):
    """Scraper for CISA (Cybersecurity and Infrastructure Security Agency) and DHS."""
    
    def __init__(self, db):
        """Initialize the CISA/DHS scraper."""
        super().__init__(db)
        self.source_name = "CISA & DHS"
        self.base_url = "https://www.cisa.gov"
        self.advisories_url = urljoin(self.base_url, "/known-exploited-vulnerabilities-catalog")
        self.alerts_url = urljoin(self.base_url, "/uscert/ncas/alerts")
        self.bulletins_url = urljoin(self.base_url, "/uscert/ncas/bulletins")
    
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
            logger.warning("No vulnerabilities found from CISA/DHS")
            success = False
        
        # Scrape alerts
        alerts = self.scrape_alerts()
        if alerts:
            if not self.save_data(alerts, "alert"):
                success = False
        else:
            logger.warning("No alerts found from CISA/DHS")
            success = False
        
        # Scrape bulletins
        bulletins = self.scrape_bulletins()
        if bulletins:
            if not self.save_data(bulletins, "alert"):
                success = False
        else:
            logger.warning("No bulletins found from CISA/DHS")
            success = False
            
        return success
    
    def scrape_vulnerabilities(self) -> List[Dict]:
        """
        Scrape vulnerabilities from the Known Exploited Vulnerabilities Catalog.
        
        Returns:
            List of vulnerability dictionaries
        """
        vulnerabilities = []
        
        try:
            response = self.get_page(self.advisories_url)
            if not response:
                return vulnerabilities
                
            soup = self.parse_html(response)
            if not soup:
                return vulnerabilities
            
            # Find the vulnerability table
            vuln_table = soup.find('table', {'class': 'usa-table'})
            if not vuln_table:
                logger.warning("Vulnerability table not found on CISA/DHS page")
                return vulnerabilities
            
            # Process each row in the table
            rows = vuln_table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cells = row.find_all('td')
                if len(cells) >= 6:
                    try:
                        cve_id = cells[0].text.strip()
                        vendor_project = cells[1].text.strip()
                        product = cells[2].text.strip()
                        vulnerability_name = cells[3].text.strip()
                        
                        # Parse date
                        date_added_text = cells[4].text.strip()
                        date_added = None
                        try:
                            date_added = datetime.strptime(date_added_text, "%m/%d/%Y")
                        except ValueError:
                            logger.warning(f"Could not parse date: {date_added_text}")
                        
                        due_date_text = cells[5].text.strip()
                        due_date = None
                        try:
                            due_date = datetime.strptime(due_date_text, "%m/%d/%Y")
                        except ValueError:
                            logger.warning(f"Could not parse date: {due_date_text}")
                        
                        vulnerability = {
                            "cve_id": cve_id,
                            "vendor_project": vendor_project,
                            "product": product,
                            "vulnerability_name": vulnerability_name,
                            "date_added": date_added,
                            "due_date": due_date,
                            "source_url": self.advisories_url,
                        }
                        
                        vulnerabilities.append(vulnerability)
                    except Exception as e:
                        logger.error(f"Error parsing vulnerability row: {str(e)}")
                        continue
            
            logger.info(f"Scraped {len(vulnerabilities)} vulnerabilities from CISA/DHS")
            
        except Exception as e:
            logger.error(f"Error scraping CISA/DHS vulnerabilities: {str(e)}")
        
        return vulnerabilities
    
    def scrape_alerts(self) -> List[Dict]:
        """
        Scrape alerts from CISA/DHS.
        
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
            
            logger.info(f"Scraped {len(alerts)} alerts from CISA/DHS")
            
        except Exception as e:
            logger.error(f"Error scraping CISA/DHS alerts: {str(e)}")
        
        return alerts
    
    def scrape_bulletins(self) -> List[Dict]:
        """
        Scrape bulletins from CISA/DHS.
        
        Returns:
            List of bulletin dictionaries (formatted as alerts)
        """
        bulletins = []
        
        try:
            response = self.get_page(self.bulletins_url)
            if not response:
                return bulletins
                
            soup = self.parse_html(response)
            if not soup:
                return bulletins
            
            # Find bulletin items (similar structure to alerts)
            bulletin_items = soup.find_all('div', {'class': 'item-list'})
            
            for item in bulletin_items:
                try:
                    # Extract bulletin details
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
                    
                    # Extract bulletin ID from title
                    alert_id = ""
                    id_match = re.search(r'(SB\d+-\d+)', title)
                    if id_match:
                        alert_id = id_match.group(1)
                    
                    bulletin = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    bulletins.append(bulletin)
                    
                except Exception as e:
                    logger.error(f"Error parsing bulletin item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(bulletins)} bulletins from CISA/DHS")
            
        except Exception as e:
            logger.error(f"Error scraping CISA/DHS bulletins: {str(e)}")
        
        return bulletins 