"""
MITRE ATT&CK scraper for collecting threat actor information.
"""

import logging
import re
import json
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class MitreScraper(BaseScraper):
    """Scraper for MITRE ATT&CK Framework."""
    
    def __init__(self, db):
        """Initialize the MITRE scraper."""
        super().__init__(db)
        self.source_name = "MITRE ATT&CK"
        self.base_url = "https://attack.mitre.org"
        self.groups_url = urljoin(self.base_url, "/groups/")
        self.json_url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    
    def scrape(self) -> bool:
        """
        Main scraping method that extracts threat actor groups.
        
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # Try to get structured data from MITRE's JSON
        threat_actors = self.scrape_threat_actors_json()
        
        # If JSON method fails, fallback to web scraping
        if not threat_actors:
            threat_actors = self.scrape_threat_actors_web()
        
        if threat_actors:
            if not self.save_data(threat_actors, "threat_actor"):
                success = False
        else:
            logger.warning("No threat actors found from MITRE ATT&CK")
            success = False
            
        return success
    
    def scrape_threat_actors_json(self) -> List[Dict]:
        """
        Scrape threat actors from MITRE's JSON data.
        
        Returns:
            List of threat actor dictionaries
        """
        threat_actors = []
        
        try:
            response = self.get_page(self.json_url)
            if not response:
                return threat_actors
                
            # Parse JSON data
            attack_data = response.json()
            
            # Extract only the group (threat actor) objects
            group_objects = [obj for obj in attack_data.get('objects', []) 
                            if obj.get('type') == 'intrusion-set']
            
            for group in group_objects:
                try:
                    # Extract basic information
                    group_id = group.get('id', '')
                    name = group.get('name', '')
                    description = group.get('description', '')
                    
                    # Extract aliases
                    aliases = []
                    if 'aliases' in group:
                        aliases = group['aliases']
                    
                    # Extract country
                    country = None
                    if 'country' in group:
                        country = group['country']
                    
                    # Extract first/last seen
                    first_seen = None
                    last_seen = None
                    if 'first_seen' in group:
                        try:
                            first_seen = datetime.strptime(group['first_seen'], "%Y-%m-%dT%H:%M:%SZ")
                        except ValueError:
                            pass
                    if 'last_seen' in group:
                        try:
                            last_seen = datetime.strptime(group['last_seen'], "%Y-%m-%dT%H:%M:%SZ")
                        except ValueError:
                            pass
                    
                    # Extract motivation
                    motivation = ""
                    if 'primary_motivation' in group:
                        motivation = group['primary_motivation']
                    
                    # Extract capabilities from external references
                    capabilities = []
                    for ref in group.get('external_references', []):
                        if ref.get('source_name') == 'mitre-attack' and 'url' in ref:
                            url = ref['url']
                            # Add MITRE ATT&CK ID as capability
                            tech_id = ref.get('external_id', '')
                            if tech_id:
                                capabilities.append(tech_id)
                    
                    # Build threat actor object
                    threat_actor = {
                        'name': name,
                        'aliases': aliases,
                        'description': description,
                        'country': country,
                        'motivation': motivation,
                        'first_seen': first_seen,
                        'last_seen': last_seen,
                        'capabilities': capabilities,
                        'source': self.source_name,
                        'source_url': urljoin(self.base_url, f"/groups/{group_id}")
                    }
                    
                    threat_actors.append(threat_actor)
                    
                except Exception as e:
                    logger.error(f"Error parsing MITRE threat actor JSON: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(threat_actors)} threat actors from MITRE ATT&CK JSON")
            
        except Exception as e:
            logger.error(f"Error scraping MITRE threat actors from JSON: {str(e)}")
        
        return threat_actors
    
    def scrape_threat_actors_web(self) -> List[Dict]:
        """
        Fallback method to scrape threat actors from the MITRE ATT&CK website.
        
        Returns:
            List of threat actor dictionaries
        """
        threat_actors = []
        
        try:
            response = self.get_page(self.groups_url)
            if not response:
                return threat_actors
                
            soup = self.parse_html(response)
            if not soup:
                return threat_actors
            
            # Find all group cards on the page
            group_cards = soup.find_all('div', {'class': 'card'})
            
            for card in group_cards:
                try:
                    # Extract group name and link
                    header = card.find('h4', {'class': 'card-title'})
                    if not header:
                        continue
                    
                    name_link = header.find('a')
                    if not name_link:
                        continue
                    
                    name = name_link.text.strip()
                    group_url = urljoin(self.base_url, name_link.get('href', ''))
                    
                    # Extract group ID from URL
                    group_id = group_url.split('/')[-1]
                    
                    # Extract description
                    desc = card.find('div', {'class': 'card-text'})
                    description = desc.text.strip() if desc else ""
                    
                    # Extract associated countries and other metadata
                    aliases = []
                    country = None
                    
                    metadata_items = card.find_all('div', {'class': 'col-md-6'})
                    for item in metadata_items:
                        item_text = item.text.strip()
                        if "Associated Groups:" in item_text:
                            aliases_text = item_text.replace("Associated Groups:", "").strip()
                            aliases = [alias.strip() for alias in aliases_text.split(',') if alias.strip()]
                        elif "Country:" in item_text:
                            country = item_text.replace("Country:", "").strip()
                    
                    # Build threat actor object
                    threat_actor = {
                        'name': name,
                        'aliases': aliases,
                        'description': description,
                        'country': country,
                        'source': self.source_name,
                        'source_url': group_url
                    }
                    
                    # For more detailed info, we would need to visit each group's page
                    # but we'll keep it simple for the fallback method
                    
                    threat_actors.append(threat_actor)
                    
                except Exception as e:
                    logger.error(f"Error parsing MITRE threat actor card: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(threat_actors)} threat actors from MITRE ATT&CK website")
            
        except Exception as e:
            logger.error(f"Error scraping MITRE threat actors from website: {str(e)}")
        
        return threat_actors 