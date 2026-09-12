"""Render the existing report template with fictional data. No scraping or database."""
import importlib.util
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("report", ROOT / "utils/report.py")
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)
vulnerabilities = pd.DataFrame([{
    "cve_id": "DEMO-001", "vendor_project": "Example vendor", "product": "Demo service",
    "vulnerability_name": "Fictional access-control issue", "date_added": "2026-09-12",
    "source": "Synthetic demo fixture",
}])
alerts = pd.DataFrame([{
    "alert_id": "DEMO-ALERT-001", "title": "Example maintenance notice",
    "published_date": "2026-09-12", "source": "Synthetic demo fixture",
    "summary": "Fictional content for checking the report layout. This is not a security advisory.",
    "url": "https://example.com",
}])
html = report.generate_html_report(vulnerabilities, alerts, pd.DataFrame(), pd.DataFrame(), "Demo fixture")
html = html.replace('<body>', '<body><p style="padding:16px;background:#fff3cd"><strong>Offline demo.</strong> All records below are fictional. The source list belongs to the report template and does not attribute these records.</p>')
destination = Path(__file__).with_name("sample-report.html")
destination.write_text("\n".join(line.rstrip() for line in html.splitlines()).strip() + "\n")
print(destination)
