from datetime import date
from pathlib import Path

from pyspark.sql.types import (
    DateType,
    DoubleType,
    LongType,
    StringType,
    TimestampType,
)

from informatica_pyspark.config import RunConfig
from informatica_pyspark.context import MappingContext
from informatica_pyspark.io.local_csv import LocalCsvReader
from informatica_pyspark.mappings import MAPPINGS


DATA = Path(__file__).resolve().parents[3] / "legacy/informatica/data"


# RECOVERED from the XML Source Qualifier port datatypes. The target3
# PRODUCT_ID exception is deliberate: XML says number, but the SQ port carries
# the string value PRD0001 and the conversion must preserve its emitted bytes.
EXPECTED_TYPES = {
    "m_demo_mapping1": {
        "demo_target3": {
            "PRODUCT_ID": StringType(), "PRODUCT_NM": StringType(),
            "PRODUCT_NO": StringType(), "COLOR": StringType(),
            "STD_COST": StringType(), "LIST_PRICE": StringType(),
            "SELL_ST_DT": DateType(), "SELL_ED_DT": DateType(),
        },
        "demo_target5": {
            "ACCT_ID": LongType(), "FIRST_NM": StringType(),
            "LAST_NM": StringType(), "BAL_AMT": DoubleType(),
            "CRDT_SCORE": LongType(),
        },
        "demo_target6": {
            "ACCT_ID": LongType(), "ACCT_TYP": StringType(),
            "ACCT_DESC": StringType(), "CR8_DT": DateType(),
            "CRDT_LN": StringType(), "CLSR_DT": DateType(),
            "ACCT_STAT_CD": StringType(), "TX_ID": LongType(),
            "ACCT_KEY": LongType(), "TX_DTTM": TimestampType(),
            "TX_AMT": DoubleType(), "TX_TYPE_CD": StringType(),
        },
    },
    "m_demo_mapping2": {
        "demo_target1_INS": {
            "Key": LongType(), "LEAD_CO_MNE": StringType(),
            "BRANCH_CO_MNE": StringType(), "MIS_DATE": StringType(),
            "ID": StringType(), "DESCRIPTION": StringType(),
            "SHORT_NAME": StringType(), "CREATED_BY": StringType(),
            "CREATED_TIME": DateType(),
        },
        "demo_target1_UPD": {
            "Key": DoubleType(), "LEAD_CO_MNE": StringType(),
            "BRANCH_CO_MNE": StringType(), "MIS_DATE": StringType(),
            "ID": StringType(), "DESCRIPTION": StringType(),
            "SHORT_NAME": StringType(), "UPDATED_BY": StringType(),
            "UPDATED_TIME": DateType(),
        },
    },
    "m_demo_mapping3": {
        "demo_target2": {
            "Title": StringType(), "Gender": StringType(),
            "First_Name": StringType(), "Middle_Name": StringType(),
            "Last_Name": StringType(), "Member_Identifier": DoubleType(),
            "Member_Suffix": StringType(), "Date_of_Birth": DateType(),
            "Member_Number": DoubleType(), "Soc_Number": DoubleType(),
            "Type_Code": DoubleType(), "Relationship_to_Subscriber_Code": DoubleType(),
            "Relationship_to_Subscriber_Code_Label": StringType(),
            "Effective_Date": DateType(),
        },
        "demo_target21": {
            "Title": StringType(), "Gender": StringType(),
            "First_Name": StringType(), "Middle_Name": StringType(),
            "Last_Name": StringType(), "Member_Identifier": DoubleType(),
            "Member_Suffix": StringType(), "Date_of_Birth": DateType(),
            "Member_Number": DoubleType(), "Soc_Number": DoubleType(),
            "Type_Code": DoubleType(), "Relationship_to_Subscriber_Code": DoubleType(),
            "Relationship_to_Subscriber_Code_Label": StringType(),
            "Effective_Date": DateType(),
        },
    },
}


def _sources(spark, names):
    reader = LocalCsvReader(spark, str(DATA))
    return {name: reader.read(name) for name in names}


def test_mapping_output_types_follow_source_qualifier_contract(spark):
    for mapping_name, expected_targets in EXPECTED_TYPES.items():
        spec = MAPPINGS[mapping_name]
        result = spec.run(
            MappingContext(
                spark=spark,
                config=RunConfig(business_date=date(2024, 1, 31)),
                sources=_sources(spark, spec.sources),
            )
        )
        for target_name, expected in expected_targets.items():
            actual = {
                field.name: field.dataType
                for field in result.targets[target_name].schema.fields
            }
            assert actual == expected, (mapping_name, target_name, actual)
