"""
NIST and standards-related sources scraper for collecting cybersecurity frameworks, guidelines, and standards.
"""

import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class NISTStandardsScraper(BaseScraper):
    """Scraper for NIST Cybersecurity Framework, NCCoE, and related standards sources."""
    
    def __init__(self, db):
        """Initialize the NIST and standards scraper."""
        super().__init__(db)
        self.source_name = "NIST Cybersecurity Framework"
        self.nist_base_url = "https://www.nist.gov"
        self.nccoe_base_url = "https://www.nccoe.nist.gov"
        self.csf_url = urljoin(self.nist_base_url, "/cyberframework")
        self.nvd_url = "https://nvd.nist.gov"
        self.nvd_alerts_url = urljoin(self.nvd_url, "/general")
        self.nccoe_pubs_url = urljoin(self.nccoe_base_url, "/publications")
        self.sp800_url = urljoin(self.nist_base_url, "/itl/publications/nist-special-publications")
    
    def scrape(self) -> bool:
        """
        Main scraping method that extracts standards, publications, and alerts from NIST sources.
        
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # Scrape NIST CSF news/updates
        csf_alerts = self.scrape_csf_updates()
        if csf_alerts:
            if not self.save_data(csf_alerts, "alert"):
                success = False
        else:
            logger.warning("No updates found from NIST Cybersecurity Framework")
            success = False
        
        # Scrape NVD alerts
        nvd_alerts = self.scrape_nvd_alerts()
        if nvd_alerts:
            if not self.save_data(nvd_alerts, "alert"):
                success = False
        else:
            logger.warning("No alerts found from NVD")
            success = False
        
        # Scrape NCCoE publications
        nccoe_pubs = self.scrape_nccoe_publications()
        if nccoe_pubs:
            if not self.save_data(nccoe_pubs, "alert"):
                success = False
        else:
            logger.warning("No publications found from NCCoE")
            success = False
        
        # Scrape SP 800-series publications
        sp800_pubs = self.scrape_sp800_publications()
        if sp800_pubs:
            if not self.save_data(sp800_pubs, "alert"):
                success = False
        else:
            logger.warning("No SP 800-series publications found")
            success = False
            
        return success
    
    def scrape_csf_updates(self) -> List[Dict]:
        """
        Scrape updates from NIST Cybersecurity Framework.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.csf_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find news/update items (adjust selectors based on actual NIST page structure)
            update_items = soup.find_all('div', {'class': 'news-item'})
            if not update_items:
                update_items = soup.find_all('article')
            
            for item in update_items:
                try:
                    # Extract update details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        title = header.text.strip()
                        url = self.csf_url
                    else:
                        title = title_link.text.strip()
                        url = urljoin(self.nist_base_url, title_link.get('href', ''))
                    
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
                    
                    # Generate alert ID from date
                    alert_id = f"NIST-CSF-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing NIST CSF update item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} updates from NIST Cybersecurity Framework")
            
        except Exception as e:
            logger.error(f"Error scraping NIST CSF updates: {str(e)}")
        
        return alerts
    
    def scrape_nvd_alerts(self) -> List[Dict]:
        """
        Scrape alerts from National Vulnerability Database.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.nvd_alerts_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find alert items (adjust selectors based on actual NVD page structure)
            alert_items = soup.find_all('div', {'class': 'announcement'})
            if not alert_items:
                alert_items = soup.find_all('div', {'class': 'item'})
            
            for item in alert_items:
                try:
                    # Extract alert details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title = header.text.strip()
                    
                    # Extract link if exists
                    link = item.find('a')
                    url = urljoin(self.nvd_url, link.get('href', '')) if link else self.nvd_url
                    
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
                    
                    # Generate alert ID from date
                    alert_id = f"NVD-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing NVD alert item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} alerts from NVD")
            
        except Exception as e:
            logger.error(f"Error scraping NVD alerts: {str(e)}")
        
        return alerts
    
    def scrape_nccoe_publications(self) -> List[Dict]:
        """
        Scrape publications from National Cybersecurity Center of Excellence.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.nccoe_pubs_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find publication items (adjust selectors based on actual NCCoE page structure)
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
                    url = urljoin(self.nccoe_base_url, title_link.get('href', ''))
                    
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
                    
                    # Extract publication ID from title or generate one
                    alert_id = ""
                    id_match = re.search(r'(SP\s+\d+-\d+)', title)
                    if id_match:
                        alert_id = id_match.group(1).replace(" ", "")
                    else:
                        alert_id = f"NCCoE-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing NCCoE publication item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} publications from NCCoE")
            
        except Exception as e:
            logger.error(f"Error scraping NCCoE publications: {str(e)}")
        
        return alerts
    
    def scrape_sp800_publications(self) -> List[Dict]:
        """
        Scrape SP 800-series publications from NIST.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.sp800_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find publication items (adjust selectors based on actual NIST page structure)
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
                    url = urljoin(self.nist_base_url, title_link.get('href', ''))
                    
                    # Only process SP 800-series publications
                    if not re.search(r'(SP\s+800-\d+)', title, re.IGNORECASE):
                        continue
                    
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
                    
                    # Extract publication ID from title
                    alert_id = ""
                    id_match = re.search(r'(SP\s+800-\d+)', title, re.IGNORECASE)
                    if id_match:
                        alert_id = id_match.group(1).replace(" ", "")
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing SP 800-series publication item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} SP 800-series publications")
            
        except Exception as e:
            logger.error(f"Error scraping SP 800-series publications: {str(e)}")
        
        return alerts 