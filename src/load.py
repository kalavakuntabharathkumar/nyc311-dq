import sqlite3
from .config import DB_PATH, CHUNK_SIZE

def load_sqlite(df):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    try:
        df.to_sql("service_requests", con, if_exists="replace", index=False, chunksize=CHUNK_SIZE)
        con.execute("CREATE INDEX IF NOT EXISTS idx_created ON service_requests(created_dt)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_complaint ON service_requests(complaint_type)")
        con.commit()
    finally:
        con.close()
