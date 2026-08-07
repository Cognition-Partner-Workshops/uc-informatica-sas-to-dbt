from datetime import date

from pyspark.sql import functions as F

from informatica_pyspark.config import RunConfig, RunContext
from informatica_pyspark.io import attach_line_ordinal
from informatica_pyspark.mappings import m_demo_mapping2


class MemoryIO:
    def __init__(self, values):
        self.values = values

    def read(self, name):
        value = self.values[name]
        if name == "demo_source1" and "__line_ordinal" not in value.columns:
            return attach_line_ordinal(value)
        return value


def test_mapping2_router_lookup_sequence_and_unconnected_columns(spark):
    source = spark.createDataFrame(
        [
            ("L", "B", "2024-01-31", "REC00001", "new one", "ONE"),
            ("L", "B", "2024-01-31", "REC00002", "new two", "TWO"),
            ("L", "B", "2024-01-31", "REC00003", "new three", "THREE"),
            ("L", "B", "2024-01-31", "REC00004", "new four", "FOUR"),
        ],
        ["LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME"],
    )
    target = spark.createDataFrame(
        [
            (1.0, "L", "B", "2024-01-01", "REC00001", "old", "ONE"),
            (2.0, "L", "B", "2024-01-01", "REC00002", "old", "TWO"),
            (99.0, "L", "B", "2024-01-02", "REC00002", "newest", "TWO"),
        ],
        ["Key", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME"],
    )
    target = target.withColumn("__line_ordinal", F.when(F.col("Key") == 99.0, 2).otherwise(F.col("Key").cast("long")))
    ctx = RunContext(
        cfg=RunConfig(business_date=date(2024, 1, 31)),
        spark=spark,
        io=MemoryIO({"demo_source1": source, "demo_target1": target}),
    )

    result = m_demo_mapping2.run(ctx)
    ins = result["demo_target1_INS"].orderBy("ID").collect()
    upd = result["demo_target1_UPD"].orderBy("ID").collect()
    assert [r.ID for r in ins] == ["REC00003", "REC00004"]
    assert [r.Key for r in ins] == [57.0, 58.0]
    assert [r.ID for r in upd] == ["REC00001", "REC00002"]
    assert [r.Key for r in upd] == [1.0, 99.0]
    assert [r.DESCRIPTION for r in upd] == ["new one", "new two"]
    assert all(r.CREATED_BY is None for r in upd)
    assert all(r.UPDATED_BY == "IDWUSER" for r in upd)
    assert "__line_ordinal" not in result["demo_target1_INS"].columns
    assert "__line_ordinal" not in result["demo_target1_UPD"].columns


def test_attach_line_ordinal_is_zero_based(spark):
    df = spark.createDataFrame([("a",), ("b",)], ["value"])
    assert [
        row["__line_ordinal"]
        for row in attach_line_ordinal(df).orderBy("__line_ordinal").collect()
    ] == [0, 1]
