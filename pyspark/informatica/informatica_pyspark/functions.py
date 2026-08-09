"""Column-level Informatica expression primitives."""

import re
from datetime import date, datetime, time
from py4j.protocol import Py4JError, Py4JJavaError
from pyspark.sql import Column, DataFrame, Window, functions as F

from .io.base import ORDINAL_COL

INFORMATICA_DEFAULT_DATE_MASK = "MM/DD/YYYY HH24:MI:SS"
_MASK_TOKENS = {
    "HH24": "HH", "HH12": "hh", "MONTH": "MMMM", "MON": "MMM",
    "YYYY": "yyyy", "YY": "yy", "MI": "mm", "US": "SSSSSS",
    "DD": "dd", "MM": "MM", "SS": "ss",
}


def informatica_mask(mask: str) -> str:
    pattern = "|".join(sorted(_MASK_TOKENS, key=len, reverse=True))
    return re.sub(pattern, lambda match: _MASK_TOKENS[match.group(0)], mask.upper())


def isnull(value: Column) -> Column:
    return value.isNull()


def iif(condition: Column, true_value: Column, false_value: Column | None = None) -> Column:
    if false_value is None:
        try:
            # Spark otherwise resolves the untyped NULL branch as NullType.
            data_type = true_value._jc.expr().dataType().catalogString()
            false_value = F.lit(None).cast(data_type)
        except (AttributeError, Py4JError, Py4JJavaError):
            false_value = F.lit(None)
    return F.when(condition, true_value).otherwise(false_value)


def not_(value: Column) -> Column:
    return ~value


def concat(*values: Column) -> Column:
    # Informatica treats NULL operands as empty strings for ||.
    return F.concat(*(F.coalesce(value, F.lit("")) for value in values))


def md5(value: Column) -> Column:
    return F.md5(value)


def aes_decrypt(*_args: Column) -> Column:
    return F.lit("LEGACY_AES_VALUE")


def to_date(value: Column, mask: str) -> Column:
    return F.to_date(value, informatica_mask(mask))


def to_char(value: Column, mask: str | None = None) -> Column:
    return F.date_format(value, informatica_mask(mask or INFORMATICA_DEFAULT_DATE_MASK))


def substr(value: Column, start: int, length: int | None = None) -> Column:
    return F.substring(value, start, length if length is not None else 2147483647)


def ltrim(value: Column) -> Column:
    return F.ltrim(value)


def rtrim(value: Column) -> Column:
    return F.rtrim(value)


def last_value(frame: DataFrame, key_columns: str | tuple[str, ...]) -> DataFrame:
    """Keep the last physical source row for each lookup key.

    Informatica Use Last Value and the migration's Use Any Value decision both
    use the contract-sanctioned physical source ordinal as their tie-break.
    """
    keys = (key_columns,) if isinstance(key_columns, str) else key_columns
    rank = Window.partitionBy(*(F.col(key) for key in keys)).orderBy(
        F.col(ORDINAL_COL).desc()
    )
    return (
        frame.withColumn("WRK_LOOKUP_RANK", F.row_number().over(rank))
        .where(F.col("WRK_LOOKUP_RANK") == 1)
        .drop("WRK_LOOKUP_RANK")
    )


def strcmp(left: Column, right: Column) -> Column:
    return (
        F.when(left.isNull() | right.isNull(), F.lit(None))
        .when(left == right, F.lit(0))
        .when(left < right, F.lit(-1))
        .otherwise(F.lit(1))
    )


def decode(value: Column, *pairs: Column) -> Column:
    if len(pairs) < 2:
        return F.lit(None)
    default = pairs[-1] if len(pairs) % 2 == 1 else F.lit(None)
    pairs = pairs[:-1] if len(pairs) % 2 == 1 else pairs
    result = default
    for i in range(len(pairs) - 2, -1, -2):
        result = F.when(value == pairs[i], pairs[i + 1]).otherwise(result)
    return result


def error(_message: str) -> Column:
    # ERROR is a row-reject/default-value primitive in this migration.
    return F.lit(None)


def abort(value: Column, message: str) -> Column:
    return F.when(value, F.lit(message)).otherwise(F.lit(None))


def sysdate(business_date: date) -> Column:
    return F.lit(business_date)


def systimestamp(business_date: date) -> Column:
    return F.lit(datetime.combine(business_date, time.min))
