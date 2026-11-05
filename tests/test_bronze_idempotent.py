"""Tests that bronze loads are idempotent: reruns never duplicate or delete data."""
import pytest
import sys
from pathlib import Path

# ROOT = Path(__file__).resolve().parents[1]
# sys.path.insert(0, str(ROOT / "src" / "ingestion"))

# from load_bronze import LANDING, get_spark, load_day
from src.ingestion.load_bronze import LANDING, load_day, get_spark


DAY1 = LANDING / "transactions_2024-01-01.csv"  # 238 rows
DAY2 = LANDING / "transactions_2024-01-02.csv"  # 137 rows

@pytest.fixture(scope="module")
def spark():
    s = get_spark()
    s.sparkContext.setLogLevel("ERROR")
    yield s
    s.stop()

def count(spark, path, file_date=None):
    df = spark.read.format('delta').load(path)
    if file_date:
        df = df.filter(df["_file_date"] == file_date)
    return df.count()

def test_rerun_same_day_no_duplicates(spark, tmp_path):
    """
    Test that re-running the load for the same day does not create duplicates in the bronze table.
    """
    bronze = (tmp_path / "bronze").as_posix()

    load_day(spark, DAY1, bronze)
    first = count(spark, bronze)

    load_day(spark, DAY1, bronze)
    second = count(spark, bronze)

    assert first == 238
    assert second == first

def test_rerun_leaves_other_days_untouched(spark, tmp_path):
    """
    Test that re-running the load for one day does not affect other days in the bronze table.
    """
    bronze = (tmp_path / "bronze").as_posix()

    load_day(spark, DAY1, bronze)
    load_day(spark, DAY2, bronze)
    load_day(spark, DAY1, bronze)   ## Rerun day 1.

    assert count(spark, bronze) == 238 + 137
    assert count(spark, bronze, "2024-01-02") == 137