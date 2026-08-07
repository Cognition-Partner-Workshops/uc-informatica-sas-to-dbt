"""Mapping 3 contract: return exact target-instance schemas; abort before writing any target."""

from pyspark.sql import functions as F

from ..config import RunContext
from ..infa import abort_if, iif, isnull, not_isnull

TARGETS = ["demo_target2", "demo_target21"]
ABORT_MESSAGE = "Relationship_to_Subscriber_Code_Labe valuel is null"

SOURCE_PORTS = [
    "Title",
    "First_Name",
    "Middle_Name",
    "Last_Name",
    "Member_ID",
    "Member_Suffix",
    "Birth_Date",
    "Gender_Code",
    "Member_Record_Number",
    "Social_Security_Number",
    "Member_Type_Code",
    "Original_Effective_Date",
    "Relationship_to_Subscriber_Code",
    "Relationship_to_Subscriber_Code_Label",
]

TARGET_COLUMNS = [
    ("Title", "Title"),
    ("Gender", "Gender_Code"),
    ("First_Name", "First_Name"),
    ("Middle_Name", "Middle_Name"),
    ("Last_Name", "Last_Name"),
    ("Member_Identifier", "Member_ID"),
    ("Member_Suffix", "Member_Suffix"),
    ("Date_of_Birth", "Birth_Date"),
    ("Member_Number", "Member_Record_Number"),
    ("Soc_Number", "Social_Security_Number"),
    ("Type_Code", "Member_Type_Code"),
    ("Relationship_to_Subscriber_Code", "Relationship_to_Subscriber_Code"),
    ("Relationship_to_Subscriber_Code_Label", "o_Relationship_to_Subscriber_Code_Label"),
    ("Effective_Date", "Original_Effective_Date"),
]


def run(ctx: RunContext) -> dict:
    source = ctx.io.read("demo_source2").select(*SOURCE_PORTS)
    filtered = source.where(not_isnull("Member_Type_Code"))
    filtered = abort_if(
        filtered,
        isnull("Relationship_to_Subscriber_Code_Label"),
        ABORT_MESSAGE,
    )
    expression = filtered.withColumn(
        "o_Relationship_to_Subscriber_Code_Label",
        iif(
            isnull("Relationship_to_Subscriber_Code_Label"),
            F.lit(None),
            F.col("Relationship_to_Subscriber_Code_Label"),
        ),
    )
    target = expression.select(
        *[F.col(source_name).alias(target_name) for target_name, source_name in TARGET_COLUMNS]
    )
    return {
        "demo_target2": target.where(isnull("Social_Security_Number")),
        "demo_target21": target.where(not_isnull("Social_Security_Number")),
    }
