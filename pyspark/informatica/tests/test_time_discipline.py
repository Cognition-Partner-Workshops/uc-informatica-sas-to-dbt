from pathlib import Path


def test_no_wall_clock_apis_in_package():
    package = Path(__file__).parents[1] / "informatica_pyspark"
    forbidden = ("current_date", "current_timestamp", "datetime.now", "time.time")
    for path in package.rglob("*.py"):
        text = path.read_text()
        assert not any(token in text for token in forbidden), path
