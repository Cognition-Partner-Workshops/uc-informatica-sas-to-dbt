"""Characterize mapping SQL against frozen inputs and edge cases offline."""

import re
from pathlib import Path

import duckdb
import pandas as pd
import pytest

from informatica_baseline import load
from parity_nfr import compare

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "dbt/informatica_snowflake"


def sql(path):
    value = path.read_text()
    value = re.sub(r"\{\{\s*config\(.*?\)\s*\}\}", "", value)
    value = re.sub(r"\{\{\s*ref\('([^']+)'\)\s*\}\}", r"\1", value)
    return value.replace("timestamp_ntz", "timestamp")


@pytest.fixture
def connection(monkeypatch):
    monkeypatch.chdir(ROOT)
    with duckdb.connect() as con:
        load(con)
        # Snowflake landing exposes the ordering column as SEED_ROW.
        con.execute("alter table demo_target1_pre_raw rename __seed_row to seed_row")
        for name, source in [
            ("demo_source1", "demo_source1"),
            ("demo_source2", "demo_source2"),
            ("demo_target1", "demo_target1_pre_raw"),
        ]:
            con.execute(
                f"create view stg_informatica__{name} as "
                f"select * from {source}"
            )
        for mapping, steps in [
            (2, ["sq", "lookup", "expression", "router", "sequence", "update_strategy"]),
            (3, ["sq", "expression", "router"]),
        ]:
            for step in steps:
                name = f"int_m_demo_mapping{mapping}__{step}"
                path = PROJECT / f"models/intermediate/m_demo_mapping{mapping}/{name}.sql"
                con.execute(f"create view {name} as " + sql(path))
        yield con


@pytest.mark.parametrize("name,key", [
    ("DEMO_TARGET1_INS", "ID"), ("DEMO_TARGET1_UPD", "ID"),
    ("DEMO_TARGET2", "Member_Identifier"), ("DEMO_TARGET21", "Member_Identifier"),
])
def test_frozen_parity(connection, name, key):
    mapping = 2 if "TARGET1_" in name else 3
    actual = connection.execute(sql(
        PROJECT / f"models/marts/m_demo_mapping{mapping}/{name}.sql"
    )).fetch_df()
    baseline = pd.read_csv(ROOT / f"baseline/informatica/{name.lower().replace('_ins', '_INS').replace('_upd', '_UPD')}.csv")
    assert compare(baseline, actual, [key])["status"] == "GREEN"


def test_lookup_tie_and_matched_update(connection):
    connection.execute("""
        insert into demo_target1_pre_raw by name
        select * replace (999 as seed_row, 'TIE_WINNER' as LEAD_CO_MNE)
        from demo_target1_pre_raw where ID = 'REC00002' and "Key" = 99 limit 1
    """)
    assert connection.execute(
        "select lead_co_mne from int_m_demo_mapping2__lookup where id='REC00002'"
    ).fetchone() == ("TIE_WINNER",)
    assert connection.execute(
        "select changed_flag from int_m_demo_mapping2__expression where id='REC00002'"
    ).fetchone() == ("Update",)


def test_empty_inputs(connection):
    connection.execute("delete from demo_source1")
    connection.execute("delete from demo_source2")
    for name in ["int_m_demo_mapping2__sequence", "int_m_demo_mapping2__update_strategy",
                 "int_m_demo_mapping3__router"]:
        assert connection.execute(f"select count(*) from {name}").fetchone() == (0,)


def test_abort_guard_normal_filtered_and_invalid(connection):
    guard = sql(PROJECT / "tests/m_demo_mapping3_abort_null_label.sql")
    assert connection.execute(guard).fetchall() == []
    connection.execute("""
        update demo_source2 set Relationship_to_Subscriber_Code_Label = null
        where Member_Type_Code is null
    """)
    assert connection.execute(guard).fetchall() == []
    connection.execute("""
        update demo_source2 set Relationship_to_Subscriber_Code_Label = null
        where Member_Type_Code is not null
    """)
    assert len(connection.execute(guard).fetchall()) == 6
