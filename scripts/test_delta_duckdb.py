"""Check that DuckDB can read a silver Delta table."""
import duckdb

con = duckdb.connect()
con.sql("INSTALL delta")
con.sql("LOAD delta")
print(con.sql("SELECT COUNT(*) FROM delta_scan('data/lake/silver/product')").fetchall())