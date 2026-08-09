from pyspark.sql import functions as F

from informatica_pyspark.config import RunConfig
from informatica_pyspark.context import MappingContext
from informatica_pyspark.lineage import Lineage
from informatica_pyspark.mappings import m_demo_mapping3


def test_mapping3_casts_filters_and_routes(spark):
    source = spark.read.option("header", "true").csv(
        "legacy/informatica/data/demo_source2.csv"
    )
    result = m_demo_mapping3.run(
        MappingContext(spark, RunConfig(), {"demo_source2": source})
    )
    assert result.targets["demo_target2"].count() == 3
    assert result.targets["demo_target21"].count() == 3
    assert result.targets["demo_target2"].where("Soc_Number is not null").count() == 0
    assert result.targets["demo_target21"].where("Member_Suffix != ''").count() == 0
    assert result.targets["demo_target2"].where("Member_Identifier = 30005").count() == 0
    assert result.targets["demo_target21"].where(
        "Relationship_to_Subscriber_Code_Label = 'SELF'"
    ).count() == 1
    assert result.targets["demo_target2"].columns == result.targets["demo_target21"].columns
    assert str(result.targets["demo_target2"].schema["Member_Identifier"].dataType) == "DoubleType()"
    assert str(result.targets["demo_target2"].schema["Date_of_Birth"].dataType) == "DateType()"


def test_mapping3_uses_guarded_label_and_leaves_default_unconnected():
    graph = Lineage()
    chain = graph.chain(
        "m_demo_mapping3", "demo_target2",
        "Relationship_to_Subscriber_Code_Label",
    )
    assert chain[-1][:2] == (
        "EXPTRANS", "o_Relationship_to_Subscriber_Code_Label"
    )
    assert "EXPTRANS.Relationship_to_Subscriber_Code_Label" in graph.dead_ports(
        "m_demo_mapping3"
    )
    assert all("DEFAULT1" not in port for port in graph.dead_ports("m_demo_mapping3"))


def test_mapping3_abort_predicate_is_post_sql_override(spark):
    source = spark.read.option("header", "true").csv(
        "legacy/informatica/data/demo_source2.csv"
    ).where("Member_ID = '30001'").withColumn(
        "Relationship_to_Subscriber_Code_Label", F.lit(None).cast("string")
    )
    result = m_demo_mapping3.run(
        MappingContext(spark, RunConfig(), {"demo_source2": source})
    )
    assert result.abort_checks[0].predicate_df.count() == 1
