"""Download Spark Snowflake connector jars outside the repository."""

import argparse
import urllib.request
from pathlib import Path


BASE = "https://maven-central.storage-download.googleapis.com/maven2"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("/tmp/snowflake-spark-jars"))
    parser.add_argument("--connector-version", default="3.2.1-spark_3.5")
    parser.add_argument("--jdbc-version", default="4.0.2")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    artifacts = [
        f"net/snowflake/spark-snowflake_2.12/{args.connector_version}/"
        f"spark-snowflake_2.12-{args.connector_version}.jar",
        f"net/snowflake/snowflake-jdbc/{args.jdbc_version}/"
        f"snowflake-jdbc-{args.jdbc_version}.jar",
    ]
    for relative in artifacts:
        destination = args.output / Path(relative).name
        urllib.request.urlretrieve(f"{BASE}/{relative}", destination)
        print(f"downloaded {destination} ({destination.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
