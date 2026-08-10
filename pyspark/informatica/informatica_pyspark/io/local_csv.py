from pathlib import Path

from pyspark.sql import DataFrame, SparkSession, functions as F

from .base import ORDINAL_COL, SourceReader, TargetWriter


class LocalCsvReader(SourceReader):
    def __init__(self, spark: SparkSession, source_dir: str, source_variant: str = "normal"):
        self.spark = spark
        self.source_dir = Path(source_dir)
        self.source_variant = source_variant

    def read(self, logical_name: str) -> DataFrame:
        path = self.source_dir / f"{logical_name}.csv"
        if logical_name == "demo_source2" and self.source_variant == "abort":
            path = self.source_dir / "abort" / "demo_source2.csv"
        raw = self.spark.read.option("header", "true").option("inferSchema", "false").csv(str(path))
        schema = raw.schema
        rows = raw.rdd.zipWithIndex().map(lambda pair: tuple(pair[0]) + (pair[1],))
        return self.spark.createDataFrame(rows, schema=schema.add(ORDINAL_COL, "long", False))


class LocalCsvWriter(TargetWriter):
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)

    def prepare(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        for path in self.target_dir.glob("*.csv"):
            path.unlink()

    def write(self, target_instance: str, df: DataFrame) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        path = self.target_dir / f"{target_instance}.csv"
        temp = self.target_dir / f".{target_instance}.tmp"
        output = df.drop(ORDINAL_COL) if ORDINAL_COL in df.columns else df
        (
            output
            .coalesce(1)
            .write.mode("overwrite")
            .option("header", "true")
            .option("dateFormat", "yyyy-MM-dd")
            .option("timestampFormat", "yyyy-MM-dd HH:mm:ss")
            .csv(str(temp))
        )
        part = next(temp.glob("part-*.csv"))
        part.replace(path)
        for child in temp.iterdir():
            child.unlink()
        temp.rmdir()
