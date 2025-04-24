"""
Database utility for storing and retrieving cyber intelligence data.
"""

import os
import json
import logging
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Union, Optional

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

logger = logging.getLogger(__name__)

Base = declarative_base()

class Vulnerability(Base):
    """Vulnerability data model."""
    
    __tablename__ = 'vulnerabilities'
    
    id = Column(Integer, primary_key=True)
    cve_id = Column(String(20), index=True)
    vendor_project = Column(String(100))
    product = Column(String(100))
    vulnerability_name = Column(String(200))
    date_added = Column(DateTime)
    due_date = Column(DateTime, nullable=True)
    source = Column(String(50))
    source_url = Column(String(500))
    scrape_date = Column(DateTime, default=datetime.now)
    details = Column(Text, nullable=True)
    
    def to_dict(self) -> Dict:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'cve_id': self.cve_id,
            'vendor_project': self.vendor_project,
            'product': self.product,
            'vulnerability_name': self.vulnerability_name,
            'date_added': self.date_added.isoformat() if self.date_added else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'source': self.source,
            'source_url': self.source_url,
            'scrape_date': self.scrape_date.isoformat() if self.scrape_date else None,
            'details': self.details
        }


class Alert(Base):
    """Alert data model."""
    
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    alert_id = Column(String(20), index=True)
    title = Column(String(200))
    url = Column(String(500))
    published_date = Column(DateTime, nullable=True)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    source = Column(String(50))
    scrape_date = Column(DateTime, default=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'alert_id': self.alert_id,
            'title': self.title,
            'url': self.url,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'summary': self.summary,
            'content': self.content,
            'source': self.source,
            'scrape_date': self.scrape_date.isoformat() if self.scrape_date else None
        }


class ThreatActor(Base):
    """Threat Actor data model."""
    
    __tablename__ = 'threat_actors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    aliases = Column(Text, nullable=True)  # Stored as JSON list
    description = Column(Text)
    country = Column(String(50), nullable=True)
    motivation = Column(String(100), nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    capabilities = Column(Text, nullable=True)  # Stored as JSON list
    source = Column(String(50))
    source_url = Column(String(500))
    scrape_date = Column(DateTime, default=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'aliases': json.loads(self.aliases) if self.aliases else [],
            'description': self.description,
            'country': self.country,
            'motivation': self.motivation,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'capabilities': json.loads(self.capabilities) if self.capabilities else [],
            'source': self.source,
            'source_url': self.source_url,
            'scrape_date': self.scrape_date.isoformat() if self.scrape_date else None
        }


class Incident(Base):
    """Cybersecurity Incident data model."""
    
    __tablename__ = 'incidents'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(Text)
    incident_date = Column(DateTime, nullable=True)
    target_sectors = Column(Text, nullable=True)  # Stored as JSON list
    target_countries = Column(Text, nullable=True)  # Stored as JSON list
    attack_vector = Column(String(100), nullable=True)
    impact = Column(Text, nullable=True)
    source = Column(String(50))
    source_url = Column(String(500))
    scrape_date = Column(DateTime, default=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'incident_date': self.incident_date.isoformat() if self.incident_date else None,
            'target_sectors': json.loads(self.target_sectors) if self.target_sectors else [],
            'target_countries': json.loads(self.target_countries) if self.target_countries else [],
            'attack_vector': self.attack_vector,
            'impact': self.impact,
            'source': self.source,
            'source_url': self.source_url,
            'scrape_date': self.scrape_date.isoformat() if self.scrape_date else None
        }


class Database:
    """Database handler for the cyber intelligence scraper."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        if not db_path:
            # Use default path in data directory
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, 'cyber_intel.db')
            
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.Session = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        
        logger.info(f"Database initialized at {db_path}")
    
    def save(self, data: Union[Dict, List], content_type: str) -> bool:
        """
        Save data to the database.
        
        Args:
            data: Dictionary or list of dictionaries to save
            content_type: Type of content ('vulnerability', 'alert', 'threat_actor', 'incident')
            
        Returns:
            True if successful, False otherwise
        """
        # Convert single dict to list for uniform processing
        if isinstance(data, dict):
            data = [data]
        
        session = self.Session()
        try:
            # Map content types to models
            model_map = {
                'vulnerability': Vulnerability,
                'alert': Alert,
                'threat_actor': ThreatActor,
                'incident': Incident
            }
            
            if content_type not in model_map:
                raise ValueError(f"Unknown content type: {content_type}")
            
            model_class = model_map[content_type]
            
            # Process each item
            for item in data:
                # Special processing for JSON fields
                if content_type == 'threat_actor' and 'aliases' in item and isinstance(item['aliases'], list):
                    item['aliases'] = json.dumps(item['aliases'])
                if content_type == 'threat_actor' and 'capabilities' in item and isinstance(item['capabilities'], list):
                    item['capabilities'] = json.dumps(item['capabilities'])
                if content_type == 'incident' and 'target_sectors' in item and isinstance(item['target_sectors'], list):
                    item['target_sectors'] = json.dumps(item['target_sectors'])
                if content_type == 'incident' and 'target_countries' in item and isinstance(item['target_countries'], list):
                    item['target_countries'] = json.dumps(item['target_countries'])
                
                # Create model instance
                model_instance = model_class(**item)
                session.add(model_instance)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving to database: {str(e)}")
            return False
            
        finally:
            session.close()
    
    def get_vulnerabilities(self, limit: int = None, offset: int = 0, 
                          cve_id: str = None, source: str = None) -> List[Dict]:
        """
        Retrieve vulnerabilities from the database.
        
        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            cve_id: Filter by CVE ID
            source: Filter by source
            
        Returns:
            List of vulnerability dictionaries
        """
        session = self.Session()
        try:
            query = session.query(Vulnerability)
            
            if cve_id:
                query = query.filter(Vulnerability.cve_id == cve_id)
            if source:
                query = query.filter(Vulnerability.source == source)
            
            query = query.order_by(Vulnerability.date_added.desc())
            
            if limit:
                query = query.limit(limit).offset(offset)
                
            return [vuln.to_dict() for vuln in query.all()]
            
        except Exception as e:
            logger.error(f"Error retrieving vulnerabilities: {str(e)}")
            return []
            
        finally:
            session.close()
    
    def get_alerts(self, limit: int = None, offset: int = 0, 
                 source: str = None) -> List[Dict]:
        """
        Retrieve alerts from the database.
        
        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            source: Filter by source
            
        Returns:
            List of alert dictionaries
        """
        session = self.Session()
        try:
            query = session.query(Alert)
            
            if source:
                query = query.filter(Alert.source == source)
            
            query = query.order_by(Alert.published_date.desc())
            
            if limit:
                query = query.limit(limit).offset(offset)
                
            return [alert.to_dict() for alert in query.all()]
            
        except Exception as e:
            logger.error(f"Error retrieving alerts: {str(e)}")
            return []
            
        finally:
            session.close()
    
    def get_threat_actors(self, limit: int = None, offset: int = 0, 
                        country: str = None) -> List[Dict]:
        """
        Retrieve threat actors from the database.
        
        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            country: Filter by country
            
        Returns:
            List of threat actor dictionaries
        """
        session = self.Session()
        try:
            query = session.query(ThreatActor)
            
            if country:
                query = query.filter(ThreatActor.country == country)
            
            query = query.order_by(ThreatActor.name)
            
            if limit:
                query = query.limit(limit).offset(offset)
                
            return [actor.to_dict() for actor in query.all()]
            
        except Exception as e:
            logger.error(f"Error retrieving threat actors: {str(e)}")
            return []
            
        finally:
            session.close()
    
    def get_incidents(self, limit: int = None, offset: int = 0) -> List[Dict]:
        """
        Retrieve incidents from the database.
        
        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            
        Returns:
            List of incident dictionaries
        """
        session = self.Session()
        try:
            query = session.query(Incident).order_by(Incident.incident_date.desc())
            
            if limit:
                query = query.limit(limit).offset(offset)
                
            return [incident.to_dict() for incident in query.all()]
            
        except Exception as e:
            logger.error(f"Error retrieving incidents: {str(e)}")
            return []
            
        finally:
            session.close()
    
    def export_to_json(self, output_dir: str = None) -> Dict[str, str]:
        """
        Export all data to JSON files.
        
        Args:
            output_dir: Directory to save the JSON files
            
        Returns:
            Dictionary with paths to the exported files
        """
        if not output_dir:
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        
        os.makedirs(output_dir, exist_ok=True)
        
        result = {}
        
        try:
            # Export vulnerabilities
            vulns = self.get_vulnerabilities()
            vuln_path = os.path.join(output_dir, 'vulnerabilities.json')
            with open(vuln_path, 'w') as f:
                json.dump(vulns, f, indent=2)
            result['vulnerabilities'] = vuln_path
            
            # Export alerts
            alerts = self.get_alerts()
            alerts_path = os.path.join(output_dir, 'alerts.json')
            with open(alerts_path, 'w') as f:
                json.dump(alerts, f, indent=2)
            result['alerts'] = alerts_path
            
            # Export threat actors
            actors = self.get_threat_actors()
            actors_path = os.path.join(output_dir, 'threat_actors.json')
            with open(actors_path, 'w') as f:
                json.dump(actors, f, indent=2)
            result['threat_actors'] = actors_path
            
            # Export incidents
            incidents = self.get_incidents()
            incidents_path = os.path.join(output_dir, 'incidents.json')
            with open(incidents_path, 'w') as f:
                json.dump(incidents, f, indent=2)
            result['incidents'] = incidents_path
            
            logger.info(f"Exported data to JSON files in {output_dir}")
            
        except Exception as e:
            logger.error(f"Error exporting data to JSON: {str(e)}")
        
        return result 