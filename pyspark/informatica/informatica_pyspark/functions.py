"""Column-level Informatica expression primitives."""

from pyspark.sql import Column, functions as F


def isnull(value: Column) -> Column:
    return value.isNull()


def iif(condition: Column, true_value: Column, false_value: Column | None = None) -> Column:
    false_value = F.lit(None) if false_value is None else false_value
    return F.when(condition, true_value).otherwise(false_value)


def concat(*values: Column) -> Column:
    # Informatica treats NULL operands as empty strings for ||.
    return F.concat(*(F.coalesce(value, F.lit("")) for value in values))


def md5(value: Column) -> Column:
    return F.md5(value)


def aes_decrypt(*_args: Column) -> Column:
    return F.lit("LEGACY_AES_VALUE")


def to_date(value: Column, mask: str) -> Column:
    return F.to_date(value, mask)


def to_char(value: Column, mask: str | None = None) -> Column:
    return F.date_format(value, mask) if mask else value.cast("string")


def substr(value: Column, start: int, length: int) -> Column:
    return F.substring(value, start, length)


def ltrim(value: Column) -> Column:
    return F.ltrim(value)


def rtrim(value: Column) -> Column:
    return F.rtrim(value)


def strcmp(left: Column, right: Column) -> Column:
    return F.when(left == right, F.lit(0)).when(left < right, F.lit(-1)).otherwise(F.lit(1))


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
