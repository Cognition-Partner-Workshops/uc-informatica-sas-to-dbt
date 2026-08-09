from pyspark.sql import functions as F

from informatica_pyspark.functions import (
    aes_decrypt, concat, decode, iif, to_date,
)


def test_expression_primitives(spark):
    row = spark.range(1).select(
        concat(F.lit("A"), F.lit(None)).alias("concat"),
        to_date(F.lit("2024-01-31"), "dd/MM/yyyy").alias("bad_date"),
        iif(F.lit(False), F.lit("yes")).alias("false_iif"),
        aes_decrypt(F.lit("cipher"), F.lit("key"), F.lit(256)).alias("aes"),
        decode(F.lit("B"), F.lit("A"), F.lit(1), F.lit("B"), F.lit(2), F.lit(0)).alias("decode"),
    ).first()
    assert row.concat == "A"
    assert row.bad_date is None
    assert row.false_iif is None
    assert row.aes == "LEGACY_AES_VALUE"
    assert row.decode == 2
