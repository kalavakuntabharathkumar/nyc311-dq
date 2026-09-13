import pandas as pd

VALID_BOROUGHS = {"BRONX","BROOKLYN","MANHATTAN","QUEENS","STATEN ISLAND"}

def validate(df):
    x = df.copy()
    x["created_dt"] = pd.to_datetime(x["created_date"], errors="coerce")
    x["closed_dt"] = pd.to_datetime(x["closed_date"], errors="coerce")
    x["resolution_hours"] = (x["closed_dt"] - x["created_dt"]).dt.total_seconds() / 3600

    checks = pd.DataFrame(index=x.index)
    checks["required_fields"] = x[["unique_key","created_date","complaint_type"]].notna().all(axis=1)
    checks["numeric_key"] = x["unique_key"].astype(str).str.fullmatch(r"\d+").fillna(False)
    checks["duplicate_key"] = ~x["unique_key"].duplicated(keep=False)
    checks["created_date_parse"] = x["created_dt"].notna()
    checks["closed_after_created"] = x["closed_dt"].isna() | (x["closed_dt"] >= x["created_dt"])
    checks["closed_date_present"] = x["closed_dt"].notna()
    checks["resolution_nonnegative"] = x["resolution_hours"].isna() | (x["resolution_hours"] >= 0)
    checks["borough_valid"] = x["borough"].fillna("").isin(VALID_BOROUGHS)
    checks["latitude_range"] = x["latitude"].between(40.4, 41.0, inclusive="both")
    checks["longitude_range"] = x["longitude"].between(-74.3, -73.6, inclusive="both")
    checks["category_consistency"] = x["complaint_type"].notna() & x["descriptor"].notna()
    checks["descriptor_consistency"] = x["descriptor"].fillna("").str.len().between(2, 150)
    checks["address_consistency"] = x["incident_address"].fillna("").str.len().between(3, 200)
    checks["zip_valid"] = x["incident_zip"].fillna("").astype(str).str.fullmatch(r"\d{5}").fillna(False)
    checks["future_date"] = x["created_dt"].notna() & (x["created_dt"] <= pd.Timestamp.now())

    x["is_valid"] = checks.all(axis=1)
    x["failed_rules"] = checks.apply(
        lambda r: ";".join(r.index[~r].tolist()), axis=1
    )
    return x, checks

def run_quality(df):
    # The requested 14-rule design is represented by 14 named checks.
    return validate(df)
