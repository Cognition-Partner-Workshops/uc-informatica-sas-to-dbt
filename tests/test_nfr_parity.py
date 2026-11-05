import csv
import json
import subprocess
import sys
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import MagicMock

import duckdb
import pandas as pd

from licence_status import markdown, status
from parity_diff import load_baseline
from parity_nfr import ROOT, compare, frame, reconcile, snowflake_report


def test_normalization_dates_nulls_numeric_and_case():
    baseline = pd.DataFrame([{'ID': 1, 'DAY': '2024-01-31', 'TS': '2024-01-31 06:00:00', 'VALUE': 1.0, 'TEXT': ' F ', 'NULL': None}])
    actual = frame(['id', 'day', 'ts', 'value', 'text', 'null'], [(Decimal('1'), date(2024, 1, 31), datetime(2024, 1, 31, 6), Decimal('1.0000001'), 'F', None)])
    assert compare(baseline, actual, ['id'])['status'] == 'GREEN'
    actual.loc[0, 'VALUE'] = 2
    assert compare(baseline, actual, ['id'])['column_differences'] == {'VALUE': 1}


def test_empty_missing_extra_columns_keys_and_duplicate_keys():
    empty = pd.DataFrame(columns=['ID', 'VALUE'])
    assert compare(empty, empty, ['ID'])['status'] == 'GREEN'
    assert compare(empty, pd.DataFrame(columns=['ID']), ['ID'])['status'] == 'RED'
    assert compare(empty, pd.DataFrame(columns=['ID', 'VALUE', 'EXTRA']), ['ID'])['status'] == 'RED'
    base = pd.DataFrame([{'ID': 1, 'VALUE': 'a'}])
    actual = pd.DataFrame([{'ID': 2, 'VALUE': 'a'}])
    result = compare(base, actual, ['ID'])
    assert result['status'] == 'RED' and result['missing_keys'] and result['extra_keys']
    assert compare(base, pd.concat([base, base]), ['ID'])['duplicate_actual_keys']
    assert compare(base, actual.drop(columns=['ID']), ['ID'])['error'] == 'Missing key columns'
    assert not reconcile({}, {}, {})['full_match']
    assert not reconcile({'UNSPECIFIED': base}, {}, {})['full_match']


def test_mixed_numeric_text_column_differences_are_not_ignored():
    base = pd.DataFrame([{'ID': 1, 'VALUE': '1'}, {'ID': 2, 'VALUE': 'ABC'}])
    actual = pd.DataFrame([{'ID': 1, 'VALUE': '1'}, {'ID': 2, 'VALUE': 'XYZ'}])
    assert compare(base, actual, ['ID'])['column_differences'] == {'VALUE': 1}


def test_cli_duckdb_green_red_and_same_licence_contract(tmp_path):
    database = tmp_path / 'target.duckdb'
    with duckdb.connect(str(database)) as con:
        for path in sorted((ROOT / 'baseline/informatica').glob('*.csv')):
            con.execute(f"CREATE TABLE {path.stem} AS SELECT * FROM read_csv_auto('{path}', all_varchar=true)")
    report = tmp_path / 'report.md'
    command = [sys.executable, str(ROOT / 'tools/parity_nfr.py'), '--token', 'FSX_20261105', '--duckdb', str(database), '--report', str(report)]
    green = subprocess.run(command, capture_output=True, text=True)
    assert green.returncode == 0, green.stderr + green.stdout
    assert green.stdout == 'Full match: True\n'
    data = json.loads(report.with_suffix('.json').read_text())
    with (ROOT / 'licence/ledger.csv').open() as stream:
        ledger = list(csv.DictReader(stream))
    lines = status(data, ledger)
    assert len(lines) == 5 and all(r['status'] == 'RETIRED' for r in lines)
    assert 'RETIRED' in markdown(lines)
    assert set(data['tables']) == {n for line in ledger for n in line['covers'].split(';')}
    with duckdb.connect(str(database)) as con:
        con.execute("UPDATE demo_target5 SET FIRST_NM='ALTERED'")
        con.execute('DELETE FROM demo_target3 WHERE PRODUCT_ID=(SELECT min(PRODUCT_ID) FROM demo_target3)')
        con.execute('DROP TABLE demo_target2')
    red = subprocess.run(command, capture_output=True, text=True)
    assert red.returncode == 1 and red.stdout == 'Full match: False\n'
    data = json.loads(report.with_suffix('.json').read_text())
    assert data['tables']['DEMO_TARGET5']['column_differences']['FIRST_NM']
    assert data['tables']['DEMO_TARGET3']['missing_keys']
    assert data['tables']['DEMO_TARGET2']['error'] == 'Missing target'
    assert status(data, ledger)[0]['status'] == 'BLOCKED'
    output = tmp_path / 'licence.md'
    licence = subprocess.run([sys.executable, str(ROOT / 'tools/licence_status.py'), '--report', str(report.with_suffix('.json')), '--output', str(output)], capture_output=True, text=True)
    assert licence.returncode == 0 and 'BLOCKED' in licence.stdout
    assert output.read_text() == licence.stdout


def test_licence_missing_or_empty_coverage_blocks():
    ledger = [{'line_id': 'A', 'description': 'Synthetic', 'annual_cost': '100', 'covers': 'ABSENT'}]
    assert status({'tables': {}}, ledger)[0]['failing_objects'] == 'ABSENT'
    ledger[0]['covers'] = ''
    assert status({'tables': {}}, ledger)[0]['status'] == 'BLOCKED'


def test_partial_keys_cannot_claim_full_match(tmp_path):
    keys = tmp_path / 'keys.json'
    keys.write_text(json.dumps({'DEMO_TARGET5': ['ACCT_ID']}))
    result = subprocess.run([sys.executable, str(ROOT / 'tools/parity_nfr.py'), '--token', 'FSX_20261105', '--keys', str(keys), '--report', str(tmp_path / 'report.md')], capture_output=True, text=True)
    assert result.returncode == 2
    assert '--keys must cover every Informatica baseline target' in result.stderr
    assert not (tmp_path / 'report.md').exists()


class FakeCursor:
    def __init__(self, frames):
        self.frames = frames

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, sql):
        self.query = sql
        if sql not in self.frames:
            raise RuntimeError('Do not expose connection details')
        df = self.frames[sql]
        self.description = [(c,) for c in df.columns]
        self.rows = list(df.itertuples(index=False, name=None))

    def fetchall(self):
        return self.rows


def test_mocked_snowflake_compares_two_schemas_and_reports_errors():
    keys = {k.upper(): v for k, v in json.loads((ROOT / 'tools/keys/informatica_keys.json').read_text()).items()}
    base = load_baseline(str(ROOT / 'baseline/informatica'))
    frames = {f'SELECT * FROM "FSX_20261105_DB"."{schema}"."{name}"': df for schema in ['INFA_BASELINE', 'INFA_TARGET'] for name, df in base.items()}
    connection = MagicMock()
    connection.cursor.side_effect = lambda: FakeCursor(frames)
    assert snowflake_report(connection, 'FSX_20261105', keys)['full_match']
    del frames['SELECT * FROM "FSX_20261105_DB"."INFA_TARGET"."DEMO_TARGET5"']
    red = snowflake_report(connection, 'FSX_20261105', keys)
    assert not red['full_match']
    assert red['tables']['DEMO_TARGET5']['query_errors'] == {'target': 'RuntimeError'}
    assert 'connection details' not in json.dumps(red)


def test_old_password_connection_path_is_unchanged(monkeypatch):
    import snowflake.connector
    from parity_snowflake import connect

    for key, value in {'SNOWFLAKE_ACCOUNT': 'legacy-account', 'SF_DEMO_USER': 'fixture-user', 'SF_DEMO_PASSWORD': 'fixture-password', 'SF_DEMO_ROLE': 'fixture-role', 'SF_DEMO_WAREHOUSE': 'fixture-wh', 'SF_DEMO_DATABASE': 'fixture-db', 'SNOWFLAKE_HOST': 'fixture-host'}.items():
        monkeypatch.setenv(key, value)
    mock = MagicMock()
    monkeypatch.setattr(snowflake.connector, 'connect', mock)
    connect()
    assert mock.call_args.kwargs['account'] == 'legacy-account'
    assert mock.call_args.kwargs['host'] == 'fixture-host'
    assert 'private_key' not in mock.call_args.kwargs
