# Cyber Intelligence Scraper

A comprehensive Python application for gathering cybersecurity and cyber terrorism intelligence from various international and US sources. This tool collects data on vulnerabilities, security alerts, threat actors, and cybersecurity incidents from authoritative sources and stores them in a structured format for analysis.

## Features

- **Multi-Source Intelligence**: Collects data from US and international cybersecurity organizations
- **Comprehensive Data Collection**: Gathers information on vulnerabilities, security alerts, threat actors, and incidents
- **Scheduled Scraping**: Set up automatic scraping at specified intervals
- **Data Storage**: Stores all collected intel in an SQLite database for easy querying
- **Report Generation**: Creates HTML reports summarizing the collected intelligence
- **Export Capabilities**: Export data to JSON for integration with other tools
- **Respectful Scraping**: Implements rate limiting and appropriate user agents

## Sources

The tool currently scrapes the following sources:

- [US-CERT](https://www.cisa.gov/) - Cybersecurity and Infrastructure Security Agency
- [MITRE ATT&CK](https://attack.mitre.org/) - MITRE's Adversarial Tactics, Techniques, and Common Knowledge database
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [ENISA](https://www.enisa.europa.eu/) - European Union Agency for Cybersecurity
- [NCSC](https://www.ncsc.gov.uk/) - National Cyber Security Centre (UK)
- [ThreatPost](https://threatpost.com/) - Cybersecurity news and analysis site

## Installation

### Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/CadeKukk/cyber_intel_scraper.git
   cd cyber_intel_scraper
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the scraper with default settings:

```
python main.py
```

This will collect data from all sources and store it in the SQLite database in the `data` directory.

### Command Line Options

- `--sources`: Specify which sources to scrape (space-separated)
  ```
  python main.py --sources us-cert mitre
  ```

- `--report`: Generate an HTML report after scraping
  ```
  python main.py --report
  ```

- `--schedule`: Run the scraper at regular intervals (hours)
  ```
  python main.py --schedule 12  # Run every 12 hours
  ```

- `--output`: Specify output directory for reports and data
  ```
  python main.py --output /path/to/output
  ```

### Examples

1. Scrape only vulnerabilities from US-CERT and CISA, and generate a report:
   ```
   python main.py --sources us-cert cisa --report
   ```

2. Run a scheduled scrape every 24 hours with all sources:
   ```
   python main.py --schedule 24 --report
   ```

## Data Structure

The application stores the following types of data:

### Vulnerabilities

- CVE ID
- Vendor/Project name
- Product
- Vulnerability name
- Date added
- Due date (if available)
- Source
- Source URL

### Alerts

- Alert ID
- Title
- URL
- Published date
- Summary
- Content (if available)
- Source

### Threat Actors

- Name
- Aliases
- Description
- Country of origin (if known)
- Motivation
- First seen date
- Last seen date
- Capabilities
- Source
- Source URL

### Incidents

- Title
- Description
- Incident date
- Target sectors
- Target countries
- Attack vector
- Impact
- Source
- Source URL

## Accessing the Data

### Using the Database

The application uses SQLite to store data, which can be accessed using standard SQL queries or using the Database class provided in the application:

```python
from utils.database import Database

# Initialize database
db = Database()

# Get recent vulnerabilities
vulnerabilities = db.get_vulnerabilities(limit=10)

# Get alerts from a specific source
alerts = db.get_alerts(source="US-CERT")

# Get threat actors by country
threat_actors = db.get_threat_actors(country="Russia")

# Get all incidents
incidents = db.get_incidents()
```

### Exporting Data

You can export all data to JSON format using the Database class:

```python
from utils.database import Database

# Initialize database
db = Database()

# Export all data to JSON files
export_paths = db.export_to_json(output_dir="exports")

# Access exported files
vulnerabilities_file = export_paths['vulnerabilities']
```

## Extending the Tool

### Adding New Sources

To add a new source:

1. Create a new scraper class in the `scrapers` directory, inheriting from the `BaseScraper` class
2. Implement the `scrape()` method and any other helper methods
3. Add the new scraper to the dictionary in the `run_scrapers()` function in `main.py`

Example of a minimal scraper:

```python
from scrapers.base_scraper import BaseScraper

class NewSourceScraper(BaseScraper):
    def __init__(self, db):
        super().__init__(db)
        self.source_name = "New Source"
        self.base_url = "https://example.com"
    
    def scrape(self):
        # Implement scraping logic
        data = []  # Collect data
        return self.save_data(data, "vulnerability")  # Save data
```

## Best Practices and Ethics

When using this tool, please adhere to the following guidelines:

1. **Respect robots.txt**: Ensure the sites you're scraping allow automated access
2. **Rate limiting**: Do not overwhelm servers with requests
3. **Attribution**: Always provide proper attribution when using the collected data
4. **Legal compliance**: Ensure your use of the tool complies with relevant laws and regulations
5. **Responsible disclosure**: If you discover security issues, follow responsible disclosure protocols

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for legitimate cybersecurity research and information gathering. Users are responsible for ensuring their use of this tool complies with applicable laws and regulations. The authors are not responsible for any misuse of this software.

---

Created with ❤️ for the cybersecurity community 