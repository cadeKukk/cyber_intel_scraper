"""
Report generation utility for Cyber Intelligence Scraper.
"""

import os
import json
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

def generate_report(db, output_dir: str = None) -> str:
    """
    Generate a comprehensive report from the collected data.
    
    Args:
        db: Database instance
        output_dir: Directory to save the report
        
    Returns:
        Path to the generated report file
    """
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    
    os.makedirs(output_dir, exist_ok=True)
    
    report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"cyber_intel_report_{report_time}.html")
    
    try:
        # Get data from database
        vulnerabilities = db.get_vulnerabilities()
        alerts = db.get_alerts()
        threat_actors = db.get_threat_actors()
        incidents = db.get_incidents()
        
        # Convert to pandas dataframes for easier analysis
        vuln_df = pd.DataFrame(vulnerabilities) if vulnerabilities else pd.DataFrame()
        alert_df = pd.DataFrame(alerts) if alerts else pd.DataFrame()
        actor_df = pd.DataFrame(threat_actors) if threat_actors else pd.DataFrame()
        incident_df = pd.DataFrame(incidents) if incidents else pd.DataFrame()
        
        # Generate HTML report
        html_content = generate_html_report(
            vuln_df=vuln_df,
            alert_df=alert_df,
            actor_df=actor_df,
            incident_df=incident_df,
            report_time=report_time
        )
        
        # Write to file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Generated report at {report_path}")
        return report_path
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return ""

def generate_html_report(vuln_df: pd.DataFrame, alert_df: pd.DataFrame, 
                        actor_df: pd.DataFrame, incident_df: pd.DataFrame,
                        report_time: str) -> str:
    """
    Generate an HTML report from dataframes.
    
    Args:
        vuln_df: Vulnerabilities dataframe
        alert_df: Alerts dataframe
        actor_df: Threat actors dataframe
        incident_df: Incidents dataframe
        report_time: Report generation timestamp
        
    Returns:
        HTML content as string
    """
    # Start building HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cyber Intelligence Report - {report_time}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3, h4 {{
                color: #2c3e50;
            }}
            h1 {{
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .summary-box {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 20px;
            }}
            .summary-item {{
                flex: 1;
                min-width: 200px;
                background-color: #fff;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }}
            .summary-item h4 {{
                margin-top: 0;
                color: #3498db;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #3498db;
                color: white;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                font-size: 0.8em;
                color: #7f8c8d;
            }}
            .chart-container {{
                margin: 20px 0;
                height: 300px;
            }}
            .alert {{
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 5px;
            }}
            .alert-critical {{
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }}
            .alert-high {{
                background-color: #fff3cd;
                border: 1px solid #ffeeba;
                color: #856404;
            }}
        </style>
    </head>
    <body>
        <h1>Cyber Intelligence Report</h1>
        <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <div class="section">
            <h2>Summary</h2>
            <div class="summary-box">
                <div class="summary-item">
                    <h4>Vulnerabilities</h4>
                    <p>Total: {len(vuln_df) if not vuln_df.empty else 0}</p>
                </div>
                <div class="summary-item">
                    <h4>Alerts</h4>
                    <p>Total: {len(alert_df) if not alert_df.empty else 0}</p>
                </div>
                <div class="summary-item">
                    <h4>Threat Actors</h4>
                    <p>Total: {len(actor_df) if not actor_df.empty else 0}</p>
                </div>
                <div class="summary-item">
                    <h4>Incidents</h4>
                    <p>Total: {len(incident_df) if not incident_df.empty else 0}</p>
                </div>
            </div>
        </div>
    """
    
    # Add Vulnerabilities section
    if not vuln_df.empty:
        # Sort by date added (most recent first)
        if 'date_added' in vuln_df.columns:
            vuln_df['date_added'] = pd.to_datetime(vuln_df['date_added'], errors='coerce')
            vuln_df = vuln_df.sort_values(by='date_added', ascending=False)
        
        # Limit to most recent 20
        display_vulns = vuln_df.head(20)
        
        html += """
        <div class="section">
            <h2>Recent Vulnerabilities</h2>
            <table>
                <thead>
                    <tr>
                        <th>CVE ID</th>
                        <th>Vendor/Project</th>
                        <th>Product</th>
                        <th>Vulnerability Name</th>
                        <th>Date Added</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for _, row in display_vulns.iterrows():
            date_added = row.get('date_added', '')
            if pd.notna(date_added) and isinstance(date_added, str):
                try:
                    date_added = datetime.fromisoformat(date_added.replace('Z', '+00:00')).strftime('%Y-%m-%d')
                except:
                    pass
            
            html += f"""
                <tr>
                    <td>{row.get('cve_id', '')}</td>
                    <td>{row.get('vendor_project', '')}</td>
                    <td>{row.get('product', '')}</td>
                    <td>{row.get('vulnerability_name', '')}</td>
                    <td>{date_added}</td>
                    <td>{row.get('source', '')}</td>
                </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
        """
    
    # Add Alerts section
    if not alert_df.empty:
        # Sort by published date (most recent first)
        if 'published_date' in alert_df.columns:
            alert_df['published_date'] = pd.to_datetime(alert_df['published_date'], errors='coerce')
            alert_df = alert_df.sort_values(by='published_date', ascending=False)
        
        # Limit to most recent 10
        display_alerts = alert_df.head(10)
        
        html += """
        <div class="section">
            <h2>Recent Alerts</h2>
        """
        
        for _, row in display_alerts.iterrows():
            # Format date
            published_date = row.get('published_date', '')
            if pd.notna(published_date) and isinstance(published_date, str):
                try:
                    published_date = datetime.fromisoformat(published_date.replace('Z', '+00:00')).strftime('%Y-%m-%d')
                except:
                    pass
            
            html += f"""
            <div class="alert alert-high">
                <h3>{row.get('title', 'Untitled Alert')}</h3>
                <p><strong>ID:</strong> {row.get('alert_id', 'N/A')}</p>
                <p><strong>Published:</strong> {published_date}</p>
                <p><strong>Source:</strong> {row.get('source', 'Unknown')}</p>
                <p><strong>Summary:</strong> {row.get('summary', 'No summary available')}</p>
                <p><a href="{row.get('url', '#')}" target="_blank">View full alert</a></p>
            </div>
            """
        
        html += """
        </div>
        """
        
    # Add source attribution section
    html += """
        <div class="section">
            <h2>Data Sources</h2>
            <ul>
                <li>US-CERT - Cybersecurity and Infrastructure Security Agency (CISA)</li>
                <li>MITRE ATT&CK Framework</li>
                <li>ENISA - European Union Agency for Cybersecurity</li>
                <li>NCSC - National Cyber Security Centre (UK)</li>
                <li>ThreatPost</li>
                <li>CISA Known Exploited Vulnerabilities Catalog</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Generated by Cyber Intelligence Scraper</p>
        </div>
    </body>
    </html>
    """
    
    return html 