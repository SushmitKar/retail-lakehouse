"""Tests that bronze loads are idempotent: reruns never duplicate or delete data."""
import pytest

from src.ingestion.load_bronze import load_day


def make_day(folder, file_date, n_rows):
    """Write a small daily CSV named like the real landing files; return its path."""
    path = folder / f"transactions_{file_date}.csv"
    lines = ["household_key,basket_id,day,product_id,quantity,sales_value"]
    lines += [f"1,{i},1,{i},1,2.50" for i in range(n_rows)]
    path.write_text("\n".join(lines))
    return path


@pytest.fixture
def days(tmp_path):
    """Two small daily files: 5 rows on 2024-01-01 and 3 rows on 2024-01-02."""
    return make_day(tmp_path, "2024-01-01", 5), make_day(tmp_path, "2024-01-02", 3)


def count(spark, path, file_date=None):
    """Count rows in a Delta table, optionally for one day only."""
    df = spark.read.format("delta").load(path)
    if file_date:
        df = df.filter(df["_file_date"] == file_date)
    return df.count()


def test_rerun_same_day_no_duplicates(spark, tmp_path, days):
    """Re-running the load for the same day does not create duplicates."""
    day1, _ = days
    bronze = (tmp_path / "bronze").as_posix()

    load_day(spark, day1, bronze)
    first = count(spark, bronze)
    load_day(spark, day1, bronze)

    assert first == 5
    assert count(spark, bronze) == first


def test_rerun_leaves_other_days_untouched(spark, tmp_path, days):
    """Re-running one day does not affect other days in the table."""
    day1, day2 = days
    bronze = (tmp_path / "bronze").as_posix()

    load_day(spark, day1, bronze)
    load_day(spark, day2, bronze)
    load_day(spark, day1, bronze)

    assert count(spark, bronze) == 5 + 3
    assert count(spark, bronze, "2024-01-02") == 3