from __future__ import annotations

from typing import Iterable

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


LEGACY_AES_VALUE = "LEGACY_AES_VALUE"


class InformaticaAbort(RuntimeError):
    """Raised when an Informatica ABORT guard matches any input row."""


def _column(value):
    if hasattr(value, "_jc"):
        return value
    if isinstance(value, str):
        return F.col(value)
    return F.lit(value)


def inf_rtrim(value):
    return F.rtrim(_column(value))


def inf_ltrim(value):
    return F.ltrim(_column(value))


def inf_isnull(value):
    return _column(value).isNull()


def inf_iif(condition, true_value, false_value=None):
    return F.when(condition, _column(true_value)).otherwise(_column(false_value))


def inf_md5(*values):
    return F.md5(
        F.concat(*[F.coalesce(_column(value), F.lit("")) for value in values])
    )


def inf_concat(*values):
    return F.concat(*[F.coalesce(_column(value), F.lit("")) for value in values])


def inf_to_date_ddmmyyyy(value):
    return F.to_date(_column(value), "dd/MM/yyyy")


def inf_aes_decrypt_unrecoverable(*_args):
    return F.lit(LEGACY_AES_VALUE)


def inf_abort(message: str) -> None:
    raise InformaticaAbort(message)


def assert_no_abort(
    df: DataFrame, predicate_col, message: str
) -> None:
    if df.where(predicate_col).limit(1).count():
        raise InformaticaAbort(message)


def _collapse_lookup(
    lookup_df: DataFrame, keys: Iterable[str], order_columns
) -> DataFrame:
    keys = list(keys)
    window = Window.partitionBy(*keys).orderBy(*order_columns)
    return (
        lookup_df.withColumn("__lookup_rank", F.row_number().over(window))
        .where(F.col("__lookup_rank") == 1)
        .drop("__lookup_rank")
    )


def lookup_use_last_value(
    lookup_df: DataFrame, keys: Iterable[str], order_col: str
) -> DataFrame:
    return _collapse_lookup(
        lookup_df, keys, [F.col(order_col).desc()]
    )


def lookup_use_any_value(
    lookup_df: DataFrame, keys: Iterable[str], order_col: str
) -> DataFrame:
    tie_column = "Key" if "Key" in lookup_df.columns else list(keys)[0]
    return _collapse_lookup(
        lookup_df,
        keys,
        [F.col(tie_column).desc_nulls_last(), F.col(order_col).desc()],
    )
