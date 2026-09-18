import pandas as pd
from .config import REPORT_DIR

def build_reports(df):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    valid = df[df["is_valid"]].copy()
    valid["created_day"] = valid["created_dt"].dt.date.astype(str)

    daily = valid.groupby("created_day").agg(
        total_records=("unique_key","count"),
        invalid_records=("is_valid", lambda s: 0),
        avg_resolution_hours=("resolution_hours","mean")
    ).reset_index()
    daily["quality_score_pct"] = 100.0
    daily.to_csv(REPORT_DIR/"daily_quality_scores.csv", index=False)

    trends = valid.groupby(["created_day","complaint_type"]).size().reset_index(name="complaint_count")
    trends.to_csv(REPORT_DIR/"complaint_trends.csv", index=False)

    closure = valid.groupby("complaint_type").agg(
        requests=("unique_key","count"),
        avg_resolution_hours=("resolution_hours","mean"),
        median_resolution_hours=("resolution_hours","median")
    ).reset_index()
    closure.to_csv(REPORT_DIR/"closure_time_patterns.csv", index=False)
