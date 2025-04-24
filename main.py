#!/usr/bin/env python3
"""
Cyber Intelligence Scraper
--------------------------
A tool to collect cybersecurity and cyber terrorism intelligence from various sources.
"""

import os
import sys
import time
import logging
import argparse
import schedule
from datetime import datetime
from dotenv import load_dotenv

# Import scrapers
from scrapers.us_cert import USCertScraper
from scrapers.mitre import MitreScraper
from scrapers.cisa_dhs import CISADHSScraper
from scrapers.fbi_cyber import FBICyberScraper
from scrapers.nsa_dod import NSADoDScraper
from scrapers.nist_standards import NISTStandardsScraper
from scrapers.research_academic import ResearchAcademicScraper
from scrapers.industry_orgs import IndustryOrgsScraper

# Import utilities
from utils.database import Database
from utils.report import generate_report
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger()

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Cyber Intelligence Scraper')
    parser.add_argument('--sources', nargs='+', help='Specific sources to scrape')
    parser.add_argument('--report', action='store_true', help='Generate report after scraping')
    parser.add_argument('--schedule', type=int, help='Schedule scraping every N hours')
    parser.add_argument('--output', type=str, default='data', help='Output directory')
    return parser.parse_args()

def run_scrapers(args):
    """Run all or specified scrapers."""
    db = Database()
    
    scrapers = {
        'us-cert': USCertScraper(db),
        'mitre': MitreScraper(db),
        'cisa-dhs': CISADHSScraper(db),
        'fbi-cyber': FBICyberScraper(db),
        'nsa-dod': NSADoDScraper(db),
        'nist-standards': NISTStandardsScraper(db),
        'research-academic': ResearchAcademicScraper(db),
        'industry-orgs': IndustryOrgsScraper(db)
    }
    
    # Determine which scrapers to run
    if args.sources:
        selected_scrapers = {k: scrapers[k] for k in args.sources if k in scrapers}
        if not selected_scrapers:
            logger.error(f"No valid sources found among: {args.sources}")
            logger.info(f"Available sources: {list(scrapers.keys())}")
            return
    else:
        selected_scrapers = scrapers
    
    # Run selected scrapers
    for name, scraper in selected_scrapers.items():
        try:
            logger.info(f"Running scraper: {name}")
            scraper.scrape()
        except Exception as e:
            logger.error(f"Error with scraper {name}: {str(e)}")
    
    # Generate report if requested
    if args.report:
        try:
            output_dir = args.output
            os.makedirs(output_dir, exist_ok=True)
            report_path = generate_report(db, output_dir)
            logger.info(f"Report generated: {report_path}")
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")

def scheduled_job(args):
    """Run the scraping job on schedule."""
    logger.info(f"Running scheduled scraping job at {datetime.now()}")
    run_scrapers(args)

def main():
    """Main entry point of the application."""
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    if args.schedule:
        # Schedule the scraping job
        hours = args.schedule
        logger.info(f"Scheduling scraping job every {hours} hours")
        schedule.every(hours).hours.do(scheduled_job, args)
        
        # Run once immediately
        run_scrapers(args)
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        # Run once and exit
        run_scrapers(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled exception: {str(e)}")
        sys.exit(1) 