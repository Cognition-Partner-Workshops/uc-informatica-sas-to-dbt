"""Land frozen Informatica inputs and outputs into a shared token database."""

import argparse
import json
import os
import sys
from pathlib import Path

import duckdb

import informatica_baseline
from sf_nfr_common import column_identifier, comment, connect, identifier

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / 'baseline/informatica'
DEFAULT_EXPIRES = '2026-11-12T23:59:00Z'


def source_queries():
    queries = {f'DEMO_SOURCE{i}': f'SELECT * FROM demo_source{i}' for i in range(1, 6)}
    for name, raw in [('DEMO_TARGET1', 'demo_target1_pre_raw'), *[(f'LKP_DEMO_SOURCE{i}', f'lkp_demo_source{i}_raw') for i in range(1, 4)]]:
        queries[name] = f'SELECT __seed_row AS SEED_ROW, * EXCLUDE (__seed_row) FROM {raw}'
    return queries


def csv_query(path, con):
    path = str(path).replace("'", "''")
    query = f"SELECT * FROM read_csv_auto('{path}', header=true, sample_size=-1)"
    booleans = [r[0] for r in con.execute('DESCRIBE ' + query).fetchall() if r[1] == 'BOOLEAN']
    if booleans:
        types = ', '.join(f"'{c}': 'VARCHAR'" for c in booleans)
        query = f"SELECT * FROM read_csv_auto('{path}', header=true, sample_size=-1, types={{{types}}})"
    return query


def load_inputs(con):
    original = informatica_baseline.DATA
    try:
        informatica_baseline.DATA = str(ROOT / 'legacy/informatica/data')
        informatica_baseline.load(con)
    finally:
        informatica_baseline.DATA = original


def contracts(con):
    load_inputs(con)
    queries = {'INFA_SOURCE': source_queries(), 'INFA_BASELINE': {}}
    for path in sorted(BASELINE.glob('*.csv')):
        queries['INFA_BASELINE'][path.stem.upper()] = csv_query(path, con)
    expected = {n.upper() for n in json.loads((ROOT / 'tools/keys/informatica_keys.json').read_text())}
    if set(queries['INFA_BASELINE']) != expected:
        raise ValueError('Baseline CSVs must cover every Informatica target in the keys specification')
    return queries


def sf_type(kind):
    if kind.startswith('TIMESTAMP'):
        return 'TIMESTAMP_NTZ'
    if kind in {'SMALLINT', 'INTEGER', 'BIGINT', 'HUGEINT'}:
        return 'NUMBER(38,0)'
    if kind.startswith('DECIMAL'):
        return 'NUMBER' + kind[len('DECIMAL'):]
    if kind in {'DOUBLE', 'FLOAT'}:
        return 'FLOAT'
    return kind


def landing_sql(token, con, expires=DEFAULT_EXPIRES, reload=False, selected=None, directory=None):
    db, wh = identifier(token + '_DB'), identifier(token + '_WH')
    tag = comment(token, expires)
    queries = contracts(con)
    selected = set(selected or [])
    known = {f'{schema}.{table}' for schema, items in queries.items() for table in items}
    if selected - known:
        raise ValueError('Unknown qualified table(s): ' + ', '.join(sorted(selected - known)))
    if selected and not reload:
        raise ValueError('--tables requires --reload')
    directory = Path(directory or ROOT / '.warehouse-exit' / token).resolve()
    sql = [
        f'CREATE WAREHOUSE IF NOT EXISTS {wh} WAREHOUSE_SIZE=XSMALL AUTO_SUSPEND=60 AUTO_RESUME=TRUE INITIALLY_SUSPENDED=TRUE COMMENT={tag}',
        f'CREATE DATABASE IF NOT EXISTS {db} DATA_RETENTION_TIME_IN_DAYS=0 COMMENT={tag}',
    ]
    for schema in ['INFA_SOURCE', 'INFA_BASELINE', 'INFA_TARGET']:
        sql.append(f'CREATE SCHEMA IF NOT EXISTS {db}.{schema} DATA_RETENTION_TIME_IN_DAYS=0 COMMENT={tag}')
    sql.append(f'USE WAREHOUSE {wh}')
    exports = []
    for schema, items in queries.items():
        stage = f'{db}.{schema}.FIXTURE_STAGE'
        sql.append(f'CREATE STAGE IF NOT EXISTS {stage} COMMENT={tag}')
        for name, query in items.items():
            if selected and f'{schema}.{name}' not in selected:
                continue
            table = f'{db}.{schema}.{identifier(name)}'
            columns = con.execute('DESCRIBE ' + query).fetchall()
            ddl = ', '.join(f'{column_identifier(c[0].upper())} {sf_type(c[1])}' for c in columns)
            sql.append(f'CREATE TABLE IF NOT EXISTS {table} ({ddl}) DATA_RETENTION_TIME_IN_DAYS=0 COMMENT={tag}')
            if reload:
                sql.append(f'TRUNCATE TABLE {table}')
            path = directory / (schema + '_' + name + '.parquet')
            exports.append((query, path))
            sql.extend([
                f"PUT 'file://{path}' @{stage}/{name}/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE",
                f"COPY INTO {table} FROM @{stage}/{name}/ FILE_FORMAT=(TYPE=PARQUET USE_LOGICAL_TYPE=TRUE) MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE FORCE={'TRUE' if reload else 'FALSE'} ON_ERROR=ABORT_STATEMENT",
            ])
    return sql, exports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--token', required=True)
    parser.add_argument('--expires', default=DEFAULT_EXPIRES)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--reload', action='store_true')
    parser.add_argument('--tables', nargs='+', help='Qualified INFA_SOURCE.TABLE or INFA_BASELINE.TABLE names')
    args = parser.parse_args()
    with duckdb.connect() as con:
        sql, exports = landing_sql(args.token, con, args.expires, args.reload, args.tables)
        if args.dry_run:
            try:
                print(';\n'.join(sql) + ';', flush=True)
            except BrokenPipeError:
                sys.stdout = open(os.devnull, 'w')
            return
        directory = ROOT / '.warehouse-exit' / args.token
        directory.mkdir(parents=True, exist_ok=True)
        for query, path in exports:
            con.execute(f"COPY ({query}) TO '{str(path).replace(chr(39), chr(39)*2)}' (FORMAT PARQUET)")
    with connect() as connection:
        with connection.cursor() as cursor:
            for statement in sql:
                cursor.execute(statement)
    print('Landing complete: ' + args.token + '_DB (INFA_TARGET remains empty).')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('Landing failed: ' + type(exc).__name__) from None
