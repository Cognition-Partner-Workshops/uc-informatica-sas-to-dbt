from datetime import date

import pytest
from pyspark.sql import functions as F

from informatica_pyspark.infa import (
    InformaticaAbort,
    abort_if,
    iif,
    infa_to_date,
    lookup,
    sequence_nextval,
)


def test_infa_helpers(spark):
    df = spark.createDataFrame([("31/01/2024", "bad")], ["good", "bad"])
    assert df.select(infa_to_date("good", "DD/MM/YYYY")).first()[0] == date(2024, 1, 31)
    assert df.select(infa_to_date("bad", "DD/MM/YYYY")).first()[0] is None
    assert df.select(iif(F.lit(True), F.lit("yes"))).first()[0] == "yes"


def test_lookup_policies(spark):
    df = spark.createDataFrame([(1, 2, 1), (1, 9, 2)], ["id", "Key", "__line_ordinal"])
    assert lookup(df, ["id"], "Use Last Value").first()["Key"] == 9
    assert lookup(df, ["id"], "Use Any Value").first()["Key"] == 9


def test_sequence_and_abort(spark):
    df = spark.createDataFrame([(2,), (1,)], ["id"])
    assert [r.NEXTVAL for r in sequence_nextval(df, ["id"], 57).orderBy("id").collect()] == [57, 58]
    with pytest.raises(InformaticaAbort):
        abort_if(df, F.col("id") == 1, "bad")
