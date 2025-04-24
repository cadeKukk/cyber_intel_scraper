"""
Industry Organizations and Information Sharing Centers scraper for collecting cybersecurity intelligence.
"""

import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class IndustryOrgsScraper(BaseScraper):
    """Scraper for industry organizations, ISACs, and cybersecurity coalitions."""
    
    def __init__(self, db):
        """Initialize the industry organizations scraper."""
        super().__init__(db)
        self.source_name = "Industry Organizations"
        self.sans_base_url = "https://isc.sans.edu"
        self.cta_base_url = "https://cyberthreatalliance.org"
        self.cis_base_url = "https://www.cisecurity.org"
        self.fs_isac_base_url = "https://www.fsisac.com"
        self.ms_isac_base_url = "https://www.cisecurity.org/ms-isac"
        self.sans_diary_url = urljoin(self.sans_base_url, "/diary")
        self.cta_blog_url = urljoin(self.cta_base_url, "/blog")
        self.cis_advisories_url = urljoin(self.cis_base_url, "/advisories")
        self.fs_isac_news_url = urljoin(self.fs_isac_base_url, "/newsroom")
        self.ms_isac_advisories_url = urljoin(self.ms_isac_base_url, "/advisories")
        self.first_base_url = "https://www.first.org"
        self.first_news_url = urljoin(self.first_base_url, "/news")
        self.cert_base_url = "https://www.kb.cert.org"
        self.cert_vuln_url = urljoin(self.cert_base_url, "/vuls")
    
    def scrape(self) -> bool:
        """
        Main scraping method that extracts intelligence from industry organizations.
        
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # Scrape SANS Internet Storm Center diaries
        sans_diaries = self.scrape_sans_diaries()
        if sans_diaries:
            if not self.save_data(sans_diaries, "alert"):
                success = False
        else:
            logger.warning("No diaries found from SANS ISC")
            success = False
        
        # Scrape Cyber Threat Alliance blog
        cta_blogs = self.scrape_cta_blog()
        if cta_blogs:
            if not self.save_data(cta_blogs, "alert"):
                success = False
        else:
            logger.warning("No blogs found from Cyber Threat Alliance")
            success = False
        
        # Scrape CIS advisories
        cis_advisories = self.scrape_cis_advisories()
        if cis_advisories:
            if not self.save_data(cis_advisories, "alert"):
                success = False
        else:
            logger.warning("No advisories found from CIS")
            success = False
        
        # Scrape FS-ISAC news
        fs_isac_news = self.scrape_fs_isac_news()
        if fs_isac_news:
            if not self.save_data(fs_isac_news, "alert"):
                success = False
        else:
            logger.warning("No news found from FS-ISAC")
            success = False
        
        # Scrape MS-ISAC advisories
        ms_isac_advisories = self.scrape_ms_isac_advisories()
        if ms_isac_advisories:
            if not self.save_data(ms_isac_advisories, "alert"):
                success = False
        else:
            logger.warning("No advisories found from MS-ISAC")
            success = False
        
        # Scrape FIRST news
        first_news = self.scrape_first_news()
        if first_news:
            if not self.save_data(first_news, "alert"):
                success = False
        else:
            logger.warning("No news found from FIRST")
            success = False
        
        # Scrape CERT/CC vulnerabilities
        cert_vulns = self.scrape_cert_vulnerabilities()
        if cert_vulns:
            if not self.save_data(cert_vulns, "vulnerability"):
                success = False
        else:
            logger.warning("No vulnerabilities found from CERT/CC")
            success = False
            
        return success
    
    def scrape_sans_diaries(self) -> List[Dict]:
        """
        Scrape diaries from SANS Internet Storm Center.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.sans_diary_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find diary items (adjust selectors based on actual SANS ISC page structure)
            diary_items = soup.find_all('div', {'class': 'diary-item'})
            if not diary_items:
                diary_items = soup.find_all('div', {'class': 'content'})
            
            for item in diary_items:
                try:
                    # Extract diary details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.sans_base_url, title_link.get('href', ''))
                    
                    # Extract date
                    date_text = item.find('div', {'class': 'diary-date'})
                    if not date_text:
                        date_text = item.find('time')
                    
                    published_date = None
                    if date_text:
                        try:
                            published_date = datetime.strptime(date_text.text.strip(), "%Y-%m-%d")
                        except ValueError:
                            try:
                                published_date = datetime.strptime(date_text.text.strip(), "%B %d, %Y")
                            except ValueError:
                                logger.warning(f"Could not parse date: {date_text.text.strip()}")
                    
                    # Extract summary
                    summary = item.find('div', {'class': 'diary-body'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Generate alert ID from date
                    alert_id = f"SANS-ISC-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing SANS ISC diary item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} diaries from SANS ISC")
            
        except Exception as e:
            logger.error(f"Error scraping SANS ISC diaries: {str(e)}")
        
        return alerts
    
    def scrape_cta_blog(self) -> List[Dict]:
        """
        Scrape blog posts from Cyber Threat Alliance.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.cta_blog_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find blog items (adjust selectors based on actual CTA page structure)
            blog_items = soup.find_all('article')
            if not blog_items:
                blog_items = soup.find_all('div', {'class': 'post'})
            
            for item in blog_items:
                try:
                    # Extract blog details
                    header = item.find(['h2', 'h3', 'h4'])
                    if not header:
                        continue
                        
                    title_link = header.find('a')
                    if not title_link:
                        continue
                        
                    title = title_link.text.strip()
                    url = urljoin(self.cta_base_url, title_link.get('href', ''))
                    
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
                    summary = item.find('div', {'class': 'excerpt'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Generate alert ID from date
                    alert_id = f"CTA-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing CTA blog item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} blog posts from Cyber Threat Alliance")
            
        except Exception as e:
            logger.error(f"Error scraping CTA blog: {str(e)}")
        
        return alerts
    
    def scrape_cis_advisories(self) -> List[Dict]:
        """
        Scrape advisories from Center for Internet Security.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.cis_advisories_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find advisory items (adjust selectors based on actual CIS page structure)
            advisory_items = soup.find_all('div', {'class': 'advisory-item'})
            if not advisory_items:
                advisory_items = soup.find_all('article')
            
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
                    url = urljoin(self.cis_base_url, title_link.get('href', ''))
                    
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
                    summary = item.find('div', {'class': 'summary'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Extract advisory ID from title or generate one
                    alert_id = ""
                    id_match = re.search(r'(CIS-\d+-\d+)', title)
                    if id_match:
                        alert_id = id_match.group(1)
                    else:
                        alert_id = f"CIS-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing CIS advisory item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} advisories from CIS")
            
        except Exception as e:
            logger.error(f"Error scraping CIS advisories: {str(e)}")
        
        return alerts
    
    def scrape_fs_isac_news(self) -> List[Dict]:
        """
        Scrape news from Financial Services ISAC.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.fs_isac_news_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find news items (adjust selectors based on actual FS-ISAC page structure)
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
                    url = urljoin(self.fs_isac_base_url, title_link.get('href', ''))
                    
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
                    summary = item.find('div', {'class': 'summary'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Generate alert ID from date
                    alert_id = f"FS-ISAC-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing FS-ISAC news item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} news items from FS-ISAC")
            
        except Exception as e:
            logger.error(f"Error scraping FS-ISAC news: {str(e)}")
        
        return alerts
    
    def scrape_ms_isac_advisories(self) -> List[Dict]:
        """
        Scrape advisories from Multi-State ISAC.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.ms_isac_advisories_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find advisory items (adjust selectors based on actual MS-ISAC page structure)
            advisory_items = soup.find_all('div', {'class': 'advisory-item'})
            if not advisory_items:
                advisory_items = soup.find_all('article')
            
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
                    url = urljoin(self.ms_isac_base_url, title_link.get('href', ''))
                    
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
                    summary = item.find('div', {'class': 'summary'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Extract advisory ID from title or generate one
                    alert_id = ""
                    id_match = re.search(r'(MS-ISAC-\d+-\d+)', title)
                    if id_match:
                        alert_id = id_match.group(1)
                    else:
                        alert_id = f"MS-ISAC-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing MS-ISAC advisory item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} advisories from MS-ISAC")
            
        except Exception as e:
            logger.error(f"Error scraping MS-ISAC advisories: {str(e)}")
        
        return alerts
    
    def scrape_first_news(self) -> List[Dict]:
        """
        Scrape news from FIRST.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            response = self.get_page(self.first_news_url)
            if not response:
                return alerts
                
            soup = self.parse_html(response)
            if not soup:
                return alerts
            
            # Find news items (adjust selectors based on actual FIRST page structure)
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
                    url = urljoin(self.first_base_url, title_link.get('href', ''))
                    
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
                    summary = item.find('div', {'class': 'summary'})
                    if not summary:
                        summary = item.find('p')
                    summary_text = summary.text.strip() if summary else ""
                    
                    # Generate alert ID from date
                    alert_id = f"FIRST-{published_date.strftime('%Y%m%d')}" if published_date else ""
                    
                    alert = {
                        "alert_id": alert_id,
                        "title": title,
                        "url": url,
                        "published_date": published_date,
                        "summary": summary_text,
                    }
                    
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.error(f"Error parsing FIRST news item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(alerts)} news items from FIRST")
            
        except Exception as e:
            logger.error(f"Error scraping FIRST news: {str(e)}")
        
        return alerts
    
    def scrape_cert_vulnerabilities(self) -> List[Dict]:
        """
        Scrape vulnerabilities from CERT/CC.
        
        Returns:
            List of vulnerability dictionaries
        """
        vulnerabilities = []
        
        try:
            response = self.get_page(self.cert_vuln_url)
            if not response:
                return vulnerabilities
                
            soup = self.parse_html(response)
            if not soup:
                return vulnerabilities
            
            # Find vulnerability items (adjust selectors based on actual CERT/CC page structure)
            vuln_items = soup.find_all('div', {'class': 'vuln-item'})
            if not vuln_items:
                vuln_items = soup.find_all('tr')
            
            for item in vuln_items:
                try:
                    # Extract vulnerability details
                    vuln_id_elem = item.find('a', {'class': 'vuln-id'})
                    if not vuln_id_elem:
                        continue
                    
                    vuln_id = vuln_id_elem.text.strip()
                    url = urljoin(self.cert_base_url, vuln_id_elem.get('href', ''))
                    
                    # Extract title
                    title_elem = item.find('td', {'class': 'vuln-title'})
                    if not title_elem:
                        continue
                    
                    title = title_elem.text.strip()
                    
                    # Extract date
                    date_elem = item.find('td', {'class': 'vuln-date'})
                    published_date = None
                    if date_elem:
                        try:
                            published_date = datetime.strptime(date_elem.text.strip(), "%Y-%m-%d")
                        except ValueError:
                            logger.warning(f"Could not parse date: {date_elem.text.strip()}")
                    
                    # Map CERT/CC ID to CVE if available
                    cve_id = ""
                    cve_match = re.search(r'(CVE-\d+-\d+)', title)
                    if cve_match:
                        cve_id = cve_match.group(1)
                    
                    vulnerability = {
                        "cve_id": cve_id,
                        "vendor_project": "Multiple",
                        "product": "Multiple",
                        "vulnerability_name": title,
                        "date_added": published_date,
                        "due_date": None,
                        "source_url": url,
                    }
                    
                    vulnerabilities.append(vulnerability)
                    
                except Exception as e:
                    logger.error(f"Error parsing CERT/CC vulnerability item: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(vulnerabilities)} vulnerabilities from CERT/CC")
            
        except Exception as e:
            logger.error(f"Error scraping CERT/CC vulnerabilities: {str(e)}")
        
        return vulnerabilities 