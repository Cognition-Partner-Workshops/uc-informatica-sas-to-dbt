import os
import runpy
import subprocess
import sys
from unittest.mock import Mock

import duckdb
import pytest

from sf_nfr_common import connect
from sf_nfr_landing import ROOT, contracts, csv_query, landing_sql
from sf_nfr_teardown import teardown_sql


@pytest.mark.parametrize('token', ['', 'lowercase', 'A-B', 'A;DROP', '../ABC', "A'B", 'A B'])
def test_invalid_token_rejected_before_connection(token):
    with duckdb.connect() as con:
        with pytest.raises(ValueError):
            landing_sql(token, con)
    with pytest.raises(ValueError):
        teardown_sql(token)


def test_landing_sql_exact_shared_settings_and_scope():
    with duckdb.connect() as con:
        sql, exports = landing_sql('FSX_20261105', con)
    text = ';\n'.join(sql)
    assert sql[0] == 'CREATE WAREHOUSE IF NOT EXISTS "FSX_20261105_WH" WAREHOUSE_SIZE=XSMALL AUTO_SUSPEND=60 AUTO_RESUME=TRUE INITIALLY_SUSPENDED=TRUE COMMENT=\'run FSX_20261105 expires 2026-11-12T23:59:00Z\''
    assert sql[1] == 'CREATE DATABASE IF NOT EXISTS "FSX_20261105_DB" DATA_RETENTION_TIME_IN_DAYS=0 COMMENT=\'run FSX_20261105 expires 2026-11-12T23:59:00Z\''
    assert len(exports) == 16
    assert text.count('COPY INTO') == 16
    assert 'TYPE=PARQUET USE_LOGICAL_TYPE=TRUE' in text
    assert 'MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE' in text
    for statement in sql:
        if statement.startswith('CREATE'):
            assert "COMMENT='run FSX_20261105 expires 2026-11-12T23:59:00Z'" in statement
        if statement.startswith(('COPY INTO', 'CREATE TABLE')):
            assert '.INFA_TARGET' not in statement and '.TD_' not in statement
    assert '"GENDER" VARCHAR' in text
    assert '"GENDER_CODE" VARCHAR' in text
    assert 'BOOLEAN' not in text
    assert not any(s.startswith('TRUNCATE') for s in sql)


def test_reload_filters_and_expiry_validation():
    with duckdb.connect() as con:
        sql, exports = landing_sql('TEST', con, expires='2026-12-01T12:00:00Z', reload=True, selected=['INFA_SOURCE.DEMO_SOURCE2'])
        assert len(exports) == 1
        assert sum(s.startswith('TRUNCATE') for s in sql) == 1
        assert sum(s.startswith('COPY INTO') for s in sql) == 1
        assert 'FORCE=TRUE' in ';'.join(sql)
        assert 'expires 2026-12-01T12:00:00Z' in sql[0]
        for kwargs in [dict(selected=['INFA_SOURCE.DEMO_SOURCE1']), dict(reload=True, selected=['TD_SOURCE.UNKNOWN']), dict(expires="2026-01-01'BAD"), dict(expires='2026-01-01')]:
            with pytest.raises(ValueError):
                landing_sql('TEST', con, **kwargs)


def test_source_contract_preserves_prestate_and_lookup_order_and_parquet(tmp_path):
    with duckdb.connect() as con:
        queries = contracts(con)
        assert con.execute('SELECT count(*) FROM (' + queries['INFA_SOURCE']['DEMO_TARGET1'] + ')').fetchone()[0] == 5
        assert con.execute('SELECT count(*) FROM (' + queries['INFA_SOURCE']['LKP_DEMO_SOURCE1'] + ')').fetchone()[0] > con.execute('SELECT count(*) FROM lkp_demo_source1').fetchone()[0]
        assert con.execute('DESCRIBE ' + queries['INFA_SOURCE']['DEMO_SOURCE2']).fetchall()[7][1] == 'VARCHAR'
        for name, query in queries['INFA_BASELINE'].items():
            assert not any(r[1] == 'BOOLEAN' for r in con.execute('DESCRIBE ' + query).fetchall())
            path = tmp_path / (name + '.parquet')
            con.execute(f"COPY ({query}) TO '{path}' (FORMAT PARQUET)")
            assert con.execute(f"SELECT * FROM read_parquet('{path}') EXCEPT ALL ({query})").fetchall() == []
        assert ('F',) in con.execute('SELECT DISTINCT Gender FROM (' + queries['INFA_BASELINE']['DEMO_TARGET21'] + ')').fetchall()


def test_boolean_sniff_override_and_empty_input(tmp_path):
    with duckdb.connect() as con:
        path = tmp_path / 'codes.csv'
        path.write_text('CODE\nF\nT\n')
        query = csv_query(path, con)
        assert con.execute('DESCRIBE ' + query).fetchone()[1] == 'VARCHAR'
        assert con.execute(query).fetchall() == [('F',), ('T',)]
        path = tmp_path / 'empty.csv'
        path.write_text('CODE,AMOUNT\n')
        assert con.execute(csv_query(path, con)).fetchall() == []


def test_missing_baseline_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr('sf_nfr_landing.BASELINE', tmp_path)
    with duckdb.connect() as con:
        with pytest.raises(ValueError, match='every Informatica target'):
            contracts(con)


def test_landing_dry_run_closed_pipe():
    process = subprocess.Popen([sys.executable, str(ROOT / 'tools/sf_nfr_landing.py'), '--token', 'FSX_20261105', '--dry-run'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.stdout.close()
    assert process.wait(timeout=30) == 0
    assert process.stderr.read() == b''


def test_teardown_only_infa_by_default_and_all_is_explicit():
    sql = teardown_sql('FSX_20261105')
    drops = [s for s in sql if s.startswith('DROP')]
    assert drops == ['DROP SCHEMA IF EXISTS "FSX_20261105_DB".INFA_TARGET', 'DROP SCHEMA IF EXISTS "FSX_20261105_DB".INFA_BASELINE', 'DROP SCHEMA IF EXISTS "FSX_20261105_DB".INFA_SOURCE']
    assert not any(s.startswith('ALTER WAREHOUSE') for s in sql)
    assert ' OR CONTAINS(UPPER(COALESCE("comment"' in ';'.join(sql)
    all_sql = ';'.join(teardown_sql('FSX_20261105', True))
    assert all_sql.index(' SUSPEND') < all_sql.index(' SET DATA_RETENTION_TIME_IN_DAYS=0') < all_sql.index('DROP DATABASE')
    assert 'DROP WAREHOUSE IF EXISTS "FSX_20261105_WH"' in all_sql


@pytest.mark.parametrize('script', ['sf_nfr_landing.py', 'sf_nfr_teardown.py'])
def test_dry_run_never_connects(script, monkeypatch, capsys):
    forbidden = Mock(side_effect=AssertionError('Network forbidden'))
    monkeypatch.setattr('sf_nfr_common.connect', forbidden)
    monkeypatch.setattr(sys, 'argv', [script, '--token', 'FSX_20261105', '--dry-run'])
    runpy.run_path(str(ROOT / 'tools' / script), run_name='__main__')
    forbidden.assert_not_called()
    assert 'FSX_20261105_DB' in capsys.readouterr().out


def test_jwt_key_in_memory_and_host_removed(monkeypatch):
    import snowflake.connector
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()).decode()
    for name, value in {'ACCOUNT': 'fixture-account', 'USER': 'fixture-user', 'PRIVATE_KEY': pem, 'ROLE': 'FIXTURE_ROLE', 'WAREHOUSE': 'FIXTURE_WH'}.items():
        monkeypatch.setenv('SNOWFLAKE_NFR_' + name, value)
    monkeypatch.setenv('SNOWFLAKE_HOST', 'invalid-host')
    mock = Mock()
    monkeypatch.setattr(snowflake.connector, 'connect', mock)
    connect()
    args = mock.call_args.kwargs
    assert args['authenticator'] == 'SNOWFLAKE_JWT'
    assert isinstance(args['private_key'], bytes)
    assert args['role'] == 'FIXTURE_ROLE' and args['warehouse'] == 'FIXTURE_WH'
    assert 'SNOWFLAKE_HOST' not in os.environ


def test_invalid_key_cannot_connect(monkeypatch):
    import snowflake.connector

    monkeypatch.setenv('SNOWFLAKE_NFR_PRIVATE_KEY', 'not-a-pem-key')
    mock = Mock()
    monkeypatch.setattr(snowflake.connector, 'connect', mock)
    with pytest.raises(ValueError):
        connect()
    mock.assert_not_called()
