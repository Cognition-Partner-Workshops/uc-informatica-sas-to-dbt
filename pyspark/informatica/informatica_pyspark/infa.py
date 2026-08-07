from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


class InformaticaAbort(Exception):
    """Raised when Informatica ABORT() would fail the session."""


def iif(cond, a, b=None):
    return F.when(cond, a).otherwise(F.lit(None) if b is None else b)


def isnull(col):
    return F.col(col).isNull() if isinstance(col, str) else col.isNull()


def not_isnull(col):
    return ~isnull(col)


def rtrim(col):
    return F.rtrim(F.col(col) if isinstance(col, str) else col)


def ltrim(col):
    return F.ltrim(F.col(col) if isinstance(col, str) else col)


def infa_to_date(col, fmt):
    c = F.col(col) if isinstance(col, str) else col
    spark_fmt = fmt.replace("DD", "dd").replace("YYYY", "yyyy")
    # Spark 3.5 has no try_to_date; ANSI=false + CORRECTED makes mismatches NULL.
    return F.to_date(c, spark_fmt)


def md5_concat(*cols):
    return F.md5(F.concat(*[F.col(c) if isinstance(c, str) else c for c in cols]))


def lookup(
    df_lookup,
    keys,
    policy="Use Last Value",
    ordinal_col="__line_ordinal",
    any_value_order=None,
):
    order = [F.col(ordinal_col).desc()]
    if policy == "Use Any Value":
        if not any_value_order:
            raise ValueError("Use Any Value requires explicit any_value_order")
        order = [
            F.col(column).desc() if descending else F.col(column).asc()
            for column, descending in any_value_order
        ]
    window = Window.partitionBy(*[F.col(k) for k in keys]).orderBy(*order)
    return df_lookup.withColumn("__lookup_rank", F.row_number().over(window)).where(
        F.col("__lookup_rank") == 1
    ).drop("__lookup_rank")


def sequence_nextval(df, order_cols, current_value):
    window = Window.orderBy(*[F.col(c) for c in order_cols])
    return df.withColumn(
        "NEXTVAL", F.lit(current_value) + F.row_number().over(window) - F.lit(1)
    )


def abort_if(df: DataFrame, condition, message):
    if df.where(condition).limit(1).count():
        raise InformaticaAbort(message)
    return df
