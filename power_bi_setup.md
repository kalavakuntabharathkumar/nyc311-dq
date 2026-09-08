# Power BI setup

Use **Get Data → Text/CSV** and import:
- `reports/daily_quality_scores.csv`
- `reports/complaint_trends.csv`
- `reports/closure_time_patterns.csv`

Suggested 3 pages:

1. **Complaint Trends**
   - Line chart: complaint count by day
   - Bar chart: complaint type
   - Slicers: date, complaint type

2. **Closure Time**
   - Average/median resolution hours
   - Complaint type comparison
   - Daily resolution trend

3. **Data Quality**
   - Quality score KPI
   - Invalid-record count
   - Invalid-record percentage
   - Daily quality score trend
