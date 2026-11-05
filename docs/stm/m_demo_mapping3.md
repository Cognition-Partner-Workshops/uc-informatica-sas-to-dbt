# m_demo_mapping3 — validated member streams

## Contract and transformation chain

Source: `legacy/informatica/wf_demo_mapping.XML`, mapping
`m_demo_mapping3`, target instances `demo_target2` and `demo_target21`.
Accepted semantics: `tools/informatica_baseline.py::mapping3`.
Frozen CSVs and Snowflake INFA_BASELINE each contain 3 rows per target.
Both keys are Member_Identifier, per tools/keys/informatica_keys.json.
Computation reads only INFA_SOURCE.DEMO_SOURCE2 through staging.

| Legacy step | dbt intermediate | Rule |
|---|---|---|
| SQ_demo_source2 SQL override | int_m_demo_mapping3__sq | Member_Type_Code IS NOT NULL |
| EXPTRANS | int_m_demo_mapping3__expression | Pass-through fields; label validation by error-severity singular test |
| RTRTRANS NEWGROUP1 | int_m_demo_mapping3__router -> DEMO_TARGET2 | Social_Security_Number IS NULL |
| RTRTRANS NEWGROUP2 | int_m_demo_mapping3__router -> DEMO_TARGET21 | Social_Security_Number IS NOT NULL |

No lookup, join, deduplication, sequence or aggregation occurs here.
The router groups are exhaustive and mutually exclusive after the SQ filter;
the default stream is unused.

## Abort guard

EXPTRANS evaluates:
`iif(ISNULL(Relationship_to_Subscriber_Code_Label),
ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),
Relationship_to_Subscriber_Code_Label)`.

The singular test `m_demo_mapping3_abort_null_label` has severity error
and returns every filtered-in row with a NULL label. Thus dbt build exits
nonzero for invalid labels even if the model views can be created. Unlike
a transactional Informatica abort, this does not promise rollback of already
built relations. Rows excluded by the SQ filter must not abort the build.
The XML contains no other explicit ABORT in these two mappings.
Tests characterize valid, filtered-out invalid, filtered-in invalid and
empty input cases without changing any shared Snowflake input.

## Column-level lineage (both targets, baseline order)

Every field flows DEMO_SOURCE2 -> SQ_demo_source2 -> EXPTRANS -> RTRTRANS;
only the routing condition differs between the two targets.

| Target column | Source / expression |
|---|---|
| TITLE | Title unchanged |
| GENDER | Gender_Code renamed |
| FIRST_NAME | First_Name unchanged |
| MIDDLE_NAME | Middle_Name unchanged |
| LAST_NAME | Last_Name unchanged |
| MEMBER_IDENTIFIER | Member_ID renamed |
| MEMBER_SUFFIX | Member_Suffix unchanged |
| DATE_OF_BIRTH | Birth_Date renamed |
| MEMBER_NUMBER | Member_Record_Number renamed |
| SOC_NUMBER | Social_Security_Number renamed (NULL for DEMO_TARGET2) |
| TYPE_CODE | Member_Type_Code renamed, guaranteed non-null by SQ |
| RELATIONSHIP_TO_SUBSCRIBER_CODE | Relationship_to_Subscriber_Code unchanged |
| RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL | EXPTRANS validated label, otherwise unchanged |
| EFFECTIVE_DATE | Original_Effective_Date renamed |

## Domains, anomalies and verification

Gender domain is M/F in this fixture contract and is tested in both marts.
Keys are not_null/unique; labels are not_null in both marts plus the
upstream abort singular test. Numeric type/relationship codes and titles
are passed through: the XML supplies no exhaustive value list, so no
invented domain constraint is imposed.

The baseline README documents a historical loader defect that treated F as
boolean and misread timestamps. This conversion preserves VARCHAR gender
codes and valid timestamp values, not those loader defects. SELECT * and
information_schema for current INFA_BASELINE confirmed uppercase column
names and order; all-null SOC_NUMBER in DEMO_TARGET2 was inferred as TEXT
by loading, but the model retains the source numeric type with NULL values.
No business recoding/truncation is introduced to mimic inferred CSV types.
Parity is keyed and value-normalized using the unchanged repository tool.
