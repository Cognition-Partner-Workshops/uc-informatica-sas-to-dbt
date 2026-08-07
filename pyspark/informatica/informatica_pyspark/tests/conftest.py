import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    session = SparkSession.builder.master("local[2]").appName("tests").getOrCreate()
    session.conf.set("spark.sql.ansi.enabled", "false")
    yield session
    session.stop()
