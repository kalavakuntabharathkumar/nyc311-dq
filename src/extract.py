import random
from datetime import datetime, timedelta
import pandas as pd
import requests
from .config import SODA_URL, API_LIMIT, CHUNK_SIZE

def fetch_socrata():
    rows = []
    offset = 0
    columns = [
        "unique_key","created_date","closed_date","complaint_type","descriptor",
        "borough","incident_zip","latitude","longitude","incident_address"
    ]
    while offset < API_LIMIT:
        limit = min(CHUNK_SIZE, API_LIMIT - offset)
        params = {
            "$limit": limit, "$offset": offset,
            "$select": ",".join(columns),
            "$order": "created_date DESC"
        }
        r = requests.get(SODA_URL, params=params, timeout=30)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        rows.extend(batch)
        offset += len(batch)
        if len(batch) < limit:
            break
    return pd.DataFrame(rows)

def synthetic_data(n=5000):
    random.seed(42)
    types = [
        ("Noise - Residential", "Loud Music/Party"),
        ("HEAT/HOT WATER", "HEAT"),
        ("Blocked Driveway", "No Access"),
        ("Street Light Condition", "Street Light Out"),
        ("Water System", "Leak"),
    ]
    boroughs = ["BRONX","BROOKLYN","MANHATTAN","QUEENS","STATEN ISLAND"]
    base = datetime(2025, 1, 1)
    data = []
    for i in range(n):
        created = base + timedelta(days=random.randint(0, 365), minutes=random.randint(0, 1439))
        closed = created + timedelta(hours=random.randint(1, 96))
        ct, desc = random.choice(types)
        row = {
            "unique_key": str(100000000 + i),
            "created_date": created.isoformat(sep=" "),
            "closed_date": closed.isoformat(sep=" "),
            "complaint_type": ct,
            "descriptor": desc,
            "borough": random.choice(boroughs),
            "incident_zip": str(random.randint(10001, 11697)),
            "latitude": round(random.uniform(40.50, 40.92), 6),
            "longitude": round(random.uniform(-74.25, -73.70), 6),
            "incident_address": f"{random.randint(1,9999)} MAIN ST",
        }
        # Inject a small, deterministic set of quality failures.
        if i % 97 == 0:
            row["created_date"] = "not-a-date"
        if i % 131 == 0:
            row["latitude"] = 99
        if i % 173 == 0:
            row["closed_date"] = None
        data.append(row)
    return pd.DataFrame(data)

def extract():
    try:
        df = fetch_socrata()
        if df.empty:
            raise RuntimeError("Socrata returned no rows")
        return df
    except Exception as exc:
        print(f"[extract] API unavailable ({exc}); using reproducible synthetic fallback.")
        return synthetic_data(max(1000, min(API_LIMIT, 5000)))
