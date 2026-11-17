from src.transform.silver_reference import CONFIG, add_reason as ref_reason, to_silver as ref_silver

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