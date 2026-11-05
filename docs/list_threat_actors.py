"""Print the first few threat actors stored by `python main.py --sources mitre`.

Run from the repository root after a scrape. It only reads data/cyber_intel.db.
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
logging.disable(logging.INFO)

from utils.database import Database  # noqa: E402

db = Database()
print(len(db.get_threat_actors()), "threat actors")
for actor in db.get_threat_actors(limit=5):
    group_id = actor["capabilities"][0] if actor["capabilities"] else ""
    aliases = ", ".join(actor["aliases"][1:3])
    print(f"{actor['name']:<11} {group_id:<6} {aliases}")
