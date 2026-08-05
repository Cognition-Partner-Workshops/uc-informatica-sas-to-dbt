# m_demo_mapping3 abort demo

## dbt abort run
Command:
```text
/home/ubuntu/venv-dbt/bin/dbt build --project-dir dbt/informatica --profiles-dir dbt/informatica --vars '{abort_demo: true, m3_source: demo_source2_abort}'
```

Relevant failure output:
```text
[ERROR]: in test exptrans_o_relationship_to_subscriber_code_label_abort (tests/exptrans_o_relationship_to_subscriber_code_label_abort.sql)
  Got 1 result, configured to fail if != 0
```

Exit code: `1`

## legacy baseline abort
Command:
```text
python3 tools/informatica_baseline.py --trigger-abort
```

Exit code: `1`

stderr:
```text
ABORT('Relationship_to_Subscriber_Code_Labe valuel is null') — 1 filtered-in rows have a NULL label
```
