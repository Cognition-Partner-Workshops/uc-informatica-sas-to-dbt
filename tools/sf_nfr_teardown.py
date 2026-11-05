"""Remove only Informatica schemas unless --all explicitly selects the shared run."""

import argparse
import json

from sf_nfr_common import connect, identifier


def teardown_sql(token, all_objects=False):
    identifier(token)
    db, wh = identifier(token + '_DB'), identifier(token + '_WH')
    sql = []
    if all_objects:
        sql.extend([
            'SHOW WAREHOUSES',
            f'ALTER WAREHOUSE IF EXISTS {wh} SUSPEND',
            f'ALTER DATABASE IF EXISTS {db} SET DATA_RETENTION_TIME_IN_DAYS=0',
            f'DROP DATABASE IF EXISTS {db}',
            f'DROP WAREHOUSE IF EXISTS {wh}',
        ])
    else:
        for schema in ['INFA_TARGET', 'INFA_BASELINE', 'INFA_SOURCE']:
            sql.extend([
                f'ALTER SCHEMA IF EXISTS {db}.{schema} SET DATA_RETENTION_TIME_IN_DAYS=0',
                f'DROP SCHEMA IF EXISTS {db}.{schema}',
            ])
    for show in ['DATABASES', 'WAREHOUSES', 'SCHEMAS IN ACCOUNT', 'TABLES IN ACCOUNT', 'VIEWS IN ACCOUNT', 'STAGES IN ACCOUNT']:
        sql.extend([
            f'SHOW {show}',
            f"""SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) WHERE CONTAINS(UPPER("name"), '{token}') OR CONTAINS(UPPER(COALESCE("comment", '')), '{token}')""",
        ])
    return sql


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--token', required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--all', action='store_true', help='Also drops the shared database, Teradata schemas and warehouse')
    args = parser.parse_args()
    sql = teardown_sql(args.token, args.all)
    if args.dry_run:
        print(';\n'.join(sql) + ';')
        return
    with connect() as connection:
        with connection.cursor() as cursor:
            suspended = False
            for index, statement in enumerate(sql):
                if statement.startswith('ALTER WAREHOUSE') and suspended:
                    continue
                cursor.execute(statement)
                if args.all and index == 0:
                    columns = [d[0].lower() for d in cursor.description]
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    exact = [r for r in rows if r['name'] == args.token + '_WH']
                    suspended = not exact or all(r['state'] == 'SUSPENDED' for r in exact)
                if statement.startswith('SELECT'):
                    columns = [d[0] for d in cursor.description]
                    print(json.dumps([dict(zip(columns, row)) for row in cursor.fetchall()], default=str))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('Teardown failed: ' + type(exc).__name__) from None
