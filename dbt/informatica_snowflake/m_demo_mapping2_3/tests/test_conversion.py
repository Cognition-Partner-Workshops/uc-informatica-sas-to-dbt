"""Exercise conversion SQL independently against normal, empty and bad inputs."""
import importlib.util
from pathlib import Path

import duckdb
import pytest
from jinja2 import Environment

PROJECT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("m23_loader", PROJECT / "load_inputs.py")
loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loader)


def materialize(con, name):
    path = PROJECT / "models" / (name + ".sql")
    if not path.exists():
        path = PROJECT / "models/intermediate" / (name + ".sql")
    sql = Environment().from_string(path.read_text()).render(
        source=lambda group, table: f"infa_src_infa_m23.{table}",
        ref=lambda model: model,
    )
    con.execute(f'create or replace table "{name}" as {sql}')


@pytest.fixture
def connection(tmp_path):
    path = tmp_path / "case.duckdb"
    loader.load(path)
    with duckdb.connect(str(path)) as con:
        yield con


def test_normal(connection):
    con = connection
    for model in ("m2_lookup", "m3_expression", "DEMO_TARGET1_INS",
                  "DEMO_TARGET1_UPD", "DEMO_TARGET2", "DEMO_TARGET21"):
        materialize(con, model)
    for model, count in (("DEMO_TARGET1_INS", 4), ("DEMO_TARGET1_UPD", 3),
                         ("DEMO_TARGET2", 3), ("DEMO_TARGET21", 3)):
        assert con.execute(f"select count(*) from {model}").fetchone()[0] == count
    assert con.execute('select min("Key"), max("Key") from DEMO_TARGET1_INS').fetchone() == (57, 60)
    assert con.execute(
        'select "Key" from DEMO_TARGET1_UPD where ID=\'REC00002\''
    ).fetchone() == (99,)


def test_empty(connection):
    con = connection
    for table in ("demo_source1", "demo_source2"):
        con.execute(f"delete from infa_src_infa_m23.{table}")
    for model in ("m2_lookup", "m3_expression", "DEMO_TARGET1_INS",
                  "DEMO_TARGET1_UPD", "DEMO_TARGET2", "DEMO_TARGET21"):
        materialize(con, model)
        assert con.execute(f"select count(*) from {model}").fetchone()[0] == 0


def test_abort_and_filtered_null(connection):
    con = connection
    con.execute("update infa_src_infa_m23.demo_source2 "
                "set Relationship_to_Subscriber_Code_Label = null")
    with pytest.raises(duckdb.InvalidInputException, match="ABORT"):
        materialize(con, "m3_expression")
    con.execute("update infa_src_infa_m23.demo_source2 set Member_Type_Code = null")
    materialize(con, "m3_expression")
    assert con.execute("select count(*) from m3_expression").fetchone()[0] == 0
