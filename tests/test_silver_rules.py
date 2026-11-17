"""Tests for the silver rules: which rows are kept, quarantined, and how they are typed."""
from datetime import date, datetime
from pyspark.sql import Row
from src.transform.silver_transactions import add_reason, to_silver
from src.transform.silver_reference import CONFIG, add_reason as ref_reason, to_silver as ref_silver

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
        {"basket_id": "1"},
        {"basket_id": "2", "quantity": "0", "sales_value": "0"},
        {"basket_id": "3", "quantity": "0", "sales_value": "4.99"},
        {"basket_id": "4", "quantity": "abc"},
        {"basket_id": "5", "sales_value": "0"},
        {"basket_id": "6", "household_key": ""},
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

def test_coupon_copies_keep_one(spark):
    """Identical coupon rows: one is kept, the extra goes to quarantine as duplicate_key."""
    df = spark.createDataFrame(
        [("1", "10", "5"), ("1", "10", "5"), ("2", "10", "5")],
        ["coupon_upc", "product_id", "campaign"]
    )
    reasons = [r.quarantine_reason for r in ref_reason(df, CONFIG["coupon"]).collect()]
    assert reasons.count(None) == 2
    assert reasons.count("duplicate_key") == 1

def test_product_blanks_and_bad_number(spark):
    """Blank text becomes Unknown or NULL, and a non-number id is quarantined."""
    cols = ["product_id", "manufacturer", "department", "brand", "commodity_desc", "sub_commodity_desc", "curr_size_of_product"]
    df = spark.createDataFrame(
        [("1", "7", "", "National", "", "", ""), ("abc", "7", "GROCERY", "Private", "X", "Y", "12 OZ")],
        cols,
    )
    flagged = ref_reason(df, CONFIG["product"])
    assert {r.product_id: r.quarantine_reason for r in flagged.collect()} == {"1": None, "abc": "invalid_type"}
    row = ref_silver(flagged.filter("quarantine_reason IS NULL"), CONFIG["product"]).collect()[0]
    assert row.department == "Unknown"
    assert row.curr_size_of_product is None
    assert row.product_id == 1