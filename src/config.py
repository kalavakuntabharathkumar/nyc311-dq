from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
DB_PATH = DATA_DIR / "nyc311.db"
QUARANTINE_PATH = DATA_DIR / "quarantine.csv"

SODA_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
API_LIMIT = int(os.getenv("NYC311_LIMIT", "5000"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
