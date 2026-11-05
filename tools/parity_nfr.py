"""NFR JWT reconciliation for the token's Informatica baseline and target schemas."""

import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pandas as pd

from parity_diff import NUMERIC_TOL, load_actual, load_baseline, normalize
from parity_snowflake import _cell
from sf_nfr_common import connect, identifier

ROOT = Path(__file__).resolve().parents[1]


def frame(columns, rows):
    return normalize(pd.DataFrame([[_cell(v) for v in row] for row in rows], columns=columns))


def canonical(value):
    if value is None or pd.isna(value):
        return None
    try:
        number = Decimal(str(value))
        if number.is_finite():
            return number
    except InvalidOperation:
        pass
    return str(value).strip()


def equal(a, b):
    if isinstance(a, Decimal) and isinstance(b, Decimal):
        return abs(a - b) <= Decimal(str(NUMERIC_TOL))
    return a == b


def compare(base, actual, keys):
    base, actual = normalize(base), normalize(actual)
    keys = [k.upper() for k in keys]
    missing_columns = sorted(set(base.columns) - set(actual.columns))
    extra_columns = sorted(set(actual.columns) - set(base.columns))
    result = dict(status='RED', baseline_rows=len(base), actual_rows=len(actual), matched_rows=0, missing_columns=missing_columns, extra_columns=extra_columns, missing_keys=[], extra_keys=[], column_differences={})
    if not keys or set(keys) - set(base.columns) or set(keys) - set(actual.columns):
        result['error'] = 'Missing key columns'
        return result

    def index(df):
        indexed = {}
        duplicates = []
        for row in df.to_dict('records'):
            row = {c: canonical(v) for c, v in row.items()}
            key = tuple(row[c] for c in keys)
            if key in indexed:
                duplicates.append(str(key))
            indexed[key] = row
        return indexed, duplicates

    left, left_duplicates = index(base)
    right, right_duplicates = index(actual)
    result['duplicate_baseline_keys'] = left_duplicates
    result['duplicate_actual_keys'] = right_duplicates
    result['missing_keys'] = sorted(str(k) for k in left.keys() - right.keys())
    result['extra_keys'] = sorted(str(k) for k in right.keys() - left.keys())
    shared = set(base.columns) & set(actual.columns)
    for key in left.keys() & right.keys():
        differing = [c for c in shared if not equal(left[key][c], right[key][c])]
        for column in differing:
            result['column_differences'][column] = result['column_differences'].get(column, 0) + 1
        if not differing and not missing_columns and not extra_columns:
            result['matched_rows'] += 1
    if len(base) == len(actual) == result['matched_rows'] and not left_duplicates and not right_duplicates:
        result['status'] = 'GREEN'
    if missing_columns or extra_columns:
        result['status'] = 'RED'
    return result


def reconcile(base, actual, keys):
    report = {'full_match': bool(keys), 'tables': {}}
    for name, columns in sorted(keys.items()):
        if name not in base or name not in actual:
            result = {'status': 'RED', 'error': 'Missing baseline' if name not in base else 'Missing target', 'baseline_rows': len(base[name]) if name in base else None}
        else:
            result = compare(base[name], actual[name], columns)
        report['tables'][name] = result
        report['full_match'] &= result['status'] == 'GREEN'
    if set(base) - set(keys):
        report['full_match'] = False
        for name in sorted(set(base) - set(keys)):
            report['tables'][name] = {'status': 'RED', 'error': 'Missing key specification'}
    return report


def fetch_schema(connection, database, schema, names):
    frames, errors = {}, {}
    for name in names:
        with connection.cursor() as cursor:
            try:
                cursor.execute(f'SELECT * FROM {identifier(database)}.{identifier(schema)}.{identifier(name)}')
                frames[name] = frame([d[0] for d in cursor.description], cursor.fetchall())
            except Exception as exc:
                errors[name] = type(exc).__name__
    return frames, errors


def snowflake_report(connection, token, keys):
    identifier(token)
    database = token + '_DB'
    base, base_errors = fetch_schema(connection, database, 'INFA_BASELINE', keys)
    actual, actual_errors = fetch_schema(connection, database, 'INFA_TARGET', keys)
    report = reconcile(base, actual, keys)
    for name in base_errors.keys() | actual_errors.keys():
        report['tables'][name]['query_errors'] = {k: v for k, v in [('baseline', base_errors.get(name)), ('target', actual_errors.get(name))] if v}
    return report


def markdown(report):
    lines = ['# Reconciliation', '', '| Object | Status | Baseline rows | Actual rows | Matched rows |', '|---|---|---:|---:|---:|']
    for name, result in sorted(report['tables'].items()):
        lines.append(f"| {name} | {result['status']} | {result.get('baseline_rows', '')} | {result.get('actual_rows', '')} | {result.get('matched_rows', '')} |")
        if result['status'] != 'GREEN':
            lines.extend(['', f'`{name}`: ' + json.dumps(result, sort_keys=True), ''])
    lines.extend(['', 'Full match: ' + str(report['full_match'])])
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--token', required=True)
    parser.add_argument('--keys', type=Path, default=ROOT / 'tools/keys/informatica_keys.json')
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--duckdb', type=Path, help='Offline target copy; uses local Informatica baseline CSVs')
    parser.add_argument('--schema', default='main')
    args = parser.parse_args()
    identifier(args.token)
    keys = {n.upper(): cols for n, cols in json.loads(args.keys.read_text()).items()}
    expected = {n.upper() for n in json.loads((ROOT / 'tools/keys/informatica_keys.json').read_text())}
    if set(keys) != expected:
        parser.error('--keys must cover every Informatica baseline target')
    if args.duckdb:
        report = reconcile(load_baseline(str(ROOT / 'baseline/informatica')), load_actual(str(args.duckdb), args.schema), keys)
    else:
        with connect() as connection:
            report = snowflake_report(connection, args.token, keys)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(markdown(report))
    args.report.with_suffix('.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('Full match: ' + str(report['full_match']))
    raise SystemExit(0 if report['full_match'] else 1)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('Reconciliation failed: ' + type(exc).__name__) from None
