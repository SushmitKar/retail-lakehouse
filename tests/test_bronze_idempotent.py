"""Tests that bronze loads are idempotent: reruns never duplicate or delete data."""
from src.ingestion.load_bronze import LANDING, load_day

DAY1 = LANDING / "transactions_2024-01-01.csv"  # 238 rows
DAY2 = LANDING / "transactions_2024-01-02.csv"  # 137 rows

# @pytest.fixture(scope="module")
# def spark():
#     s = get_spark()
#     s.sparkContext.setLogLevel("ERROR")
#     yield s
#     s.stop()

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


"""Tests for the silver rules: which rows are kept, quarantined, and how they are typed."""
from datetime import date, datetime
from pyspark.sql import Row
from src.transform.silver_transactions import add_reason, to_silver

BASE = {
    "household_key": "1",
    "basket_id": "1",
    "day": "1",
    "product_id": "5",
    "quantity": "1",
    "sales_value": "2.50",
    "store_id": "9",
    "retail_disc": "0",
    "trans_time": "946",
    "week_no": "1",
    "coupon_disc": "0",
    "coupon_match_disc": "0",
    "_file_date": "2024-01-01",
}

def make_df(spark, *changes):
    """Build a bronze style dataframe (all text). Each dict in 'changes' overrides BASE."""
    return spark.createDataFrame([Row(**{**BASE, **c}) for c in changes])

def test_each_rule_gets_its_reason(spark):
    """Every row is kept (None) or quarantined with the right reason."""
    df = make_df(
        spark,
        {"basket_id": "1"},                                      # normal row
        {"basket_id": "2", "quantity": "0", "sales_value": "0"},          # cancelled scan
        {"basket_id": "3", "quantity": "0", "sales_value": "4.99"},
        {"basket_id": "4", "quantity": "abc"},                   # text in a number column
        {"basket_id": "5", "sales_value": "0"},                  # free item, kept
        {"basket_id": "6", "household_key": ""},                 # missing key
    )
    got = {r.basket_id: r.quarantine_reason for r in add_reason(df).collect()}
    assert got == {
        "1": None,
        "2": "zero_qty_and_sales",
        "3": "zero_qty_with_sales",
        "4": "invalid_key_or_type",
        "5": None,
        "6": "invalid_key_or_type",
    }


def test_to_silver_types_and_flags(spark):
    """Kept rows get real types, a real timestamp, and the free-item flag."""
    silver = to_silver(make_df(spark, {"basket_id": "1"}, {"basket_id": "5", "sales_value": "0"}))

    types = dict(silver.dtypes)
    assert types["quantity"] == "bigint"
    assert types["sales_value"] == "double"
    assert types["transaction_date"] == "date"
    assert types["transaction_ts"] == "timestamp"

    rows = {r.basket_id: r for r in silver.collect()}
    assert rows[1].transaction_date == date(2024, 1, 1)
    assert rows[1].transaction_ts == datetime(2024, 1, 1, 9, 46)
    assert rows[1].is_zero_sale is False
    assert rows[5].is_zero_sale is True