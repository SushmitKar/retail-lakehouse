import duckdb
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "transaction_data.csv"
LANDING = ROOT / "data" / "landing" / "transactions"
LANDING.mkdir(parents=True, exist_ok=True)

START_DATE = date(2024,1,1)

con = duckdb.connect()
con.sql(f"CREATE TABLE transactions AS SELECT * FROM read_csv_auto('{RAW.as_posix()}')")    ## Converts a Windows path to forward slashes.

days = [r[0] for r in con.sql(f"SELECT DISTINCT DAY FROM transactions ORDER BY DAY").fetchall()]

for d in days:
    file_date = START_DATE + timedelta(days=d - 1)
    out = LANDING / f"transactions_{file_date.isoformat()}.csv"
    con.sql(
        f"COPY (SELECT * FROM transactions WHERE DAY = {d}) TO '{out.as_posix()}' (HEADER, DELIMITER ',')"
    )

files = list(LANDING.glob("transactions_*.csv"))
total = sum(
    con.sql(f"SELECT COUNT(*) FROM read_csv_auto('{f.as_posix()}')").fetchall()[0][0]
    for f in files
)
print(f"Files written: {len(files)}")
print(f"Rows across files: {total:,} (expected 2,595,732)")