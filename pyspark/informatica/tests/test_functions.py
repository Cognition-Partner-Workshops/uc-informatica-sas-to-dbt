from datetime import date

from pyspark.sql import functions as F

from informatica_pyspark.config import RunConfig
from informatica_pyspark.functions import (
    abort, aes_decrypt, concat, decode, error, iif, isnull, ltrim, md5, not_,
    rtrim, strcmp, substr, sysdate, systimestamp, to_char, to_date,
)


def value(spark, expression):
    return spark.range(1).select(expression.alias("value")).first().value


def test_iif_two_and_three_argument_null_semantics(spark):
    assert value(spark, iif(F.lit(True), F.lit(4))) == 4
    assert value(spark, iif(F.lit(False), F.lit(4))) is None
    assert value(spark, iif(F.lit(False), F.lit(4), F.lit(9))) == 9
    assert value(spark, iif(F.lit(None).cast("boolean"), F.lit(4), F.lit(9))) == 9


def test_isnull_and_not(spark):
    assert value(spark, isnull(F.lit(None))) is True
    assert value(spark, isnull(F.lit("x"))) is False
    assert value(spark, not_(F.lit(True))) is False
    assert value(spark, not_(F.lit(None).cast("boolean"))) is None


def test_md5_null_behavior(spark):
    assert value(spark, md5(F.lit("abc"))) == "900150983cd24fb0d6963f7d28e17f72"
    assert value(spark, md5(F.lit(None))) is None


def test_aes_decrypt_is_legacy_constant_even_for_null(spark):
    assert value(spark, aes_decrypt(F.lit(None), F.lit(None), F.lit(None))) == "LEGACY_AES_VALUE"


def test_to_date_informatica_masks_and_nulls(spark):
    assert value(spark, to_date(F.lit("31/01/2024"), "DD/MM/YYYY")) == date(2024, 1, 31)
    # Verbatim XML expression mask from line 662: default TO_CHAR is 01/31/2024 00:00:00.
    rendered = to_char(F.lit(date(2024, 1, 31)))
    assert value(spark, to_date(rendered, "DD/MM/YYYY")) is None
    assert value(spark, to_date(F.lit(None), "DD/MM/YYYY")) is None


def test_to_char_default_and_explicit_masks(spark):
    source = F.lit(date(2024, 1, 31))
    assert value(spark, to_char(source)) == "01/31/2024 00:00:00"
    assert value(spark, to_char(source, "DD-MM-YYYY")) == "31-01-2024"
    assert value(spark, to_char(F.lit(None), "DD-MM-YYYY")) is None


def test_sysdate_and_systimestamp_use_config_business_date(spark):
    config = RunConfig(business_date=date(2024, 1, 31))
    assert value(spark, sysdate(config.business_date)) == date(2024, 1, 31)
    assert value(spark, systimestamp(config.business_date)).isoformat() == "2024-01-31T00:00:00"


def test_substr_length_optional_and_negative_start(spark):
    assert value(spark, substr(F.lit("abcdef"), 2, 3)) == "bcd"
    assert value(spark, substr(F.lit("abcdef"), 2)) == "bcdef"
    assert value(spark, substr(F.lit("abcdef"), -2, 2)) == "ef"
    assert value(spark, substr(F.lit(None), 2, 2)) is None


def test_trim_functions_preserve_null(spark):
    assert value(spark, ltrim(F.lit("  abc"))) == "abc"
    assert value(spark, rtrim(F.lit("abc  "))) == "abc"
    assert value(spark, ltrim(F.lit(None))) is None
    assert value(spark, rtrim(F.lit(None))) is None


def test_strcmp_order_and_null(spark):
    assert value(spark, strcmp(F.lit("a"), F.lit("a"))) == 0
    assert value(spark, strcmp(F.lit("a"), F.lit("b"))) == -1
    assert value(spark, strcmp(F.lit("b"), F.lit("a"))) == 1
    assert value(spark, strcmp(F.lit(None), F.lit("a"))) is None


def test_decode_all_default_modes(spark):
    assert value(spark, decode(F.lit("B"), F.lit("A"), F.lit(1), F.lit("B"), F.lit(2), F.lit(0))) == 2
    assert value(spark, decode(F.lit("C"), F.lit("A"), F.lit(1), F.lit(0))) == 0
    assert value(spark, decode(F.lit("C"), F.lit("A"), F.lit(1))) is None


def test_concat_null_is_empty_string(spark):
    assert value(spark, concat(F.lit("A"), F.lit(None))) == "A"
    assert value(spark, concat(F.lit(None), F.lit(None))) == ""


def test_error_is_null_and_abort_is_message_or_null(spark):
    assert value(spark, error("transformation error")) is None
    assert value(spark, abort(F.lit(True), "abort message")) == "abort message"
    assert value(spark, abort(F.lit(False), "abort message")) is None
