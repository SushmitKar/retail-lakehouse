import duckdb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT/"data"/"raw"

print("Raw folder:", RAW)
print("CSV files:", len(list(RAW.glob("*.csv"))))

con = duckdb.connect()

for f in sorted(RAW.glob("*.csv")):
    src = f"read_csv_auto('{f.as_posix()}')"
    n = con.sql(f"SELECT COUNT(*) FROM {src}").fetchall()[0][0]
    print(f"\n{f.name}: {n:,} rows")
    con.sql(f"DESCRIBE SELECT * FROM {src}").show()