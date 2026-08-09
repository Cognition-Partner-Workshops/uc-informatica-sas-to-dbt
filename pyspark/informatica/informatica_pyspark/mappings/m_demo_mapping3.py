"""PySpark implementation of the recovered m_demo_mapping3 mapping."""

from pyspark.sql import functions as F

from ..context import MappingContext, MappingResult
from ..context import AbortCheck
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
    source = source.where(source.Member_Type_Code.isNotNull())
    label = iif(
        isnull(source.Relationship_to_Subscriber_Code_Label),
        abort(F.lit(True), _ABORT_MESSAGE),
        source.Relationship_to_Subscriber_Code_Label,
    )
    transformed = source.withColumn("o_Relationship_to_Subscriber_Code_Label", label)
    abort_rows = transformed.where(
        isnull(transformed.Relationship_to_Subscriber_Code_Label)
    )

    bindings = {
        "Title": "Title",
        "Gender": "Gender_Code",
        "First_Name": "First_Name",
        "Middle_Name": "Middle_Name",
        "Last_Name": "Last_Name",
        "Member_Identifier": "Member_ID",
        "Member_Suffix": "Member_Suffix",
        "Date_of_Birth": "Birth_Date",
        "Member_Number": "Member_Record_Number",
        "Soc_Number": "Social_Security_Number",
        "Type_Code": "Member_Type_Code",
        "Relationship_to_Subscriber_Code": "Relationship_to_Subscriber_Code",
        "Relationship_to_Subscriber_Code_Label": "o_Relationship_to_Subscriber_Code_Label",
        "Effective_Date": "Original_Effective_Date",
    }

    def projected(frame):
        return frame.select(
            *[F.col(source_name).alias(target_name)
              for target_name, source_name in bindings.items()]
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
