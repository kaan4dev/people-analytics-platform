import os
import pandas as pd
from sqlalchemy import create_engine, text

def db_url() -> str:
    host = os.getenv("DB_HOST", "postgres")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "people")
    user = os.getenv("DB_USER", "people")
    pw = os.getenv("DB_PASSWORD", "people")
    return f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{name}"

def main():
    engine = create_engine(db_url(), pool_pre_ping = True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT employee_id, date, status FROM raw.attendance"))
        df = pd.DataFrame(result.fetchall(), columns = result.keys())

    issues = []
    if df.empty:
        issues.append("raw.attendance is empty!")

    for col in ["employee_id", "date", "status"]:
        if col not in df.columns:
            issues.append(f"missing column values: {col}")
        elif df[col].isna().any():
            issues.append(f"nulls in column: {col}")

    allowed = {"present", "absent", "remote", "leave"}
    if not df.empty:
        bad = df[~df["status"].str.lower().isin(allowed)].shape[0]
        if bad:
            issues.append(f"invalid status values: {bad} rows (allowed={sorted(allowed)})")
        
    if issues:
        raise SystemExit("DQ failed: " + "|".join(issues))
    
    print("DQ passed.")

if __name__ == "__main__":
    main()
