"""Shared pytest fixtures."""
import pytest

from src.ingestion.load_bronze import get_spark

@pytest.fixture(scope="session")
def spark():
    """Start a SparkSession for the whole test session then stop it."""
    s = get_spark()
    s.sparkContext.setLogLevel("ERROR")
    yield s
    s.stop()