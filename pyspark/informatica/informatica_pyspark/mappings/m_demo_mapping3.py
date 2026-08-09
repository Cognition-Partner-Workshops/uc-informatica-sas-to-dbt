"""PySpark implementation of the recovered m_demo_mapping3 mapping."""

from pyspark.sql import functions as F

from ..context import AbortCheck, MappingContext, MappingResult
from ..functions import abort, iif, isnull, not_

MAPPING_NAME = "m_demo_mapping3"
SOURCES = ("demo_source2",)
TARGET_INSTANCES = ("demo_target2", "demo_target21")
_ABORT_MESSAGE = "Relationship_to_Subscriber_Code_Labe valuel is null"


def _cast_source(frame):
    for name in (
        "Member_ID", "Member_Record_Number", "Social_Security_Number",
        "Member_Type_Code", "Relationship_to_Subscriber_Code",
    ):
        frame = frame.withColumn(name, F.col(name).cast("double"))
    for name in ("Birth_Date", "Original_Effective_Date"):
        frame = frame.withColumn(name, F.col(name).cast("date"))
    return frame


def run(ctx: MappingContext) -> MappingResult:
    source = _cast_source(ctx.sources["demo_source2"])
    source = source.where(not_(isnull(source.Member_Type_Code)))
    label = iif(
        isnull(source.Relationship_to_Subscriber_Code_Label),
        abort(F.lit(True), _ABORT_MESSAGE),
        source.Relationship_to_Subscriber_Code_Label,
    )
    transformed = source.withColumn("o_Relationship_to_Subscriber_Code_Label", label)
    abort_rows = transformed.where(
        isnull(transformed.Relationship_to_Subscriber_Code_Label)
    )

    def projected(frame):
        return frame.select(
            F.col("Title").alias("Title"),
            F.col("Gender_Code").alias("Gender"),
            F.col("First_Name").alias("First_Name"),
            F.col("Middle_Name").alias("Middle_Name"),
            F.col("Last_Name").alias("Last_Name"),
            F.col("Member_ID").alias("Member_Identifier"),
            F.col("Member_Suffix").alias("Member_Suffix"),
            F.col("Birth_Date").alias("Date_of_Birth"),
            F.col("Member_Record_Number").alias("Member_Number"),
            F.col("Social_Security_Number").alias("Soc_Number"),
            F.col("Member_Type_Code").alias("Type_Code"),
            F.col("Relationship_to_Subscriber_Code").alias(
                "Relationship_to_Subscriber_Code"
            ),
            F.col("o_Relationship_to_Subscriber_Code_Label").alias(
                "Relationship_to_Subscriber_Code_Label"
            ),
            F.col("Original_Effective_Date").alias("Effective_Date"),
        )

    no_ssn = transformed.where(isnull(transformed.Social_Security_Number))
    has_ssn = transformed.where(not_(isnull(transformed.Social_Security_Number)))
    return MappingResult(
        targets={"demo_target2": projected(no_ssn), "demo_target21": projected(has_ssn)},
        abort_checks=[AbortCheck(abort_rows, _ABORT_MESSAGE)],
        sort_keys={
            "demo_target2": ("Member_Identifier",),
            "demo_target21": ("Member_Identifier",),
        },
    )
