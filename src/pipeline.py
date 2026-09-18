import pandas as pd
from .config import DATA_DIR, QUARANTINE_PATH
from .extract import extract
from .quality import run_quality
from .load import load_sqlite
from .reports import build_reports

def run():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    raw = extract()
    print(f"[extract] rows={len(raw):,}")

    checked, checks = run_quality(raw)
    invalid = checked[~checked["is_valid"]].copy()
    invalid.to_csv(QUARANTINE_PATH, index=False)

    load_sqlite(checked)

    checked["is_valid"] = checked["is_valid"].astype(bool)
    build_reports(checked)

    print(f"[quality] invalid={len(invalid):,} ({len(invalid)/max(len(checked),1):.2%})")
    print(f"[quality] rules={checks.shape[1]}")
    print(f"[load] SQLite written")
    print(f"[reports] Power BI-ready CSVs written")
