# `m_demo_mapping3` conversion comparison

The comparison rows below are identical to
`conversion_m_demo_mapping3.csv`; the CSV is the machine-readable form.

| mapping | transformation | port | informatica_code | xml_line | pyspark_code_or_ref | confidence | reason |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping3 | SQ_demo_source2 | Sql Query | `SELECT demo_source2.Title, demo_source2.First_Name, demo_source2.Middle_Name, demo_source2.Last_Name, demo_source2.Member_ID, demo_source2.Member_Suffix, demo_source2.Birth_Date, demo_source2.Gender_Code, demo_source2.Member_Record_Number, demo_source2.Social_Security_Number, demo_source2.Member_Type_Code, demo_source2.Original_Effective_Date, demo_source2.Relationship_to_Subscriber_Code, demo_source2.Relationship_to_Subscriber_Code_Label`<br>`FROM`<br>` demo_source2 where demo_source2.Member_Type_Code is not null` | 916 | `informatica_pyspark/mappings/m_demo_mapping3.py:56` | HIGH | The SQL override is a plain projection with a Member_Type_Code IS NOT NULL predicate; the seed row 30005 proves the filter. |
| m_demo_mapping3 | SQ_demo_source2 | Source Filter | *(empty)* | 918 | *(none)* | NOT MIGRATED | The separate Source Filter TABLEATTRIBUTE is empty; it is not the SQL override and has no behavior to migrate. |
| m_demo_mapping3 | EXPTRANS | Title | `Title` | 929 | `informatica_pyspark/mappings/m_demo_mapping3.py:38` | HIGH | Identity pass-through is connected through the router to both targets and is exercised by baseline rows. |
| m_demo_mapping3 | EXPTRANS | First_Name | `First_Name` | 930 | `informatica_pyspark/mappings/m_demo_mapping3.py:38` | HIGH | Identity pass-through is connected through the router to both targets and is exercised by baseline rows. |
| m_demo_mapping3 | EXPTRANS | Middle_Name | `Middle_Name` | 931 | `informatica_pyspark/mappings/m_demo_mapping3.py:38` | HIGH | Identity pass-through is connected through the router to both targets and is exercised by baseline rows. |
| m_demo_mapping3 | EXPTRANS | Last_Name | `Last_Name` | 932 | `informatica_pyspark/mappings/m_demo_mapping3.py:38` | HIGH | Identity pass-through is connected through the router to both targets and is exercised by baseline rows. |
| m_demo_mapping3 | EXPTRANS | Member_ID | `Member_ID` | 933 | `informatica_pyspark/mappings/m_demo_mapping3.py:38` | HIGH | Connector-derived rename to Member_Identifier; baseline keys would fail if this mapping were wrong. |
| m_demo_mapping3 | EXPTRANS | Member_Suffix | `Member_Suffix` | 934 | `informatica_pyspark/mappings/m_demo_mapping3.py:38` | HIGH | Identity pass-through is connected through the router to both targets and is exercised by baseline rows. |
| m_demo_mapping3 | EXPTRANS | Birth_Date | `Birth_Date` | 935 | `informatica_pyspark/mappings/m_demo_mapping3.py:39` | HIGH | Connector-derived rename to Date_of_Birth; baseline dates would fail if this mapping were wrong. |
| m_demo_mapping3 | EXPTRANS | Gender_Code | `Gender_Code` | 936 | `informatica_pyspark/mappings/m_demo_mapping3.py:41` | HIGH | Connector-derived rename to the second target column Gender; baseline output order and values exercise it. |
| m_demo_mapping3 | EXPTRANS | Member_Record_Number | `Member_Record_Number` | 937 | `informatica_pyspark/mappings/m_demo_mapping3.py:42` | HIGH | Connector-derived rename to Member_Number; baseline output values exercise it. |
| m_demo_mapping3 | EXPTRANS | Social_Security_Number | `Social_Security_Number` | 938 | `informatica_pyspark/mappings/m_demo_mapping3.py:43` | HIGH | Connector-derived rename to Soc_Number and router predicate input; baseline separates both targets by this field. |
| m_demo_mapping3 | EXPTRANS | Member_Type_Code | `Member_Type_Code` | 939 | `informatica_pyspark/mappings/m_demo_mapping3.py:44` | HIGH | The source qualifier filter depends on this port and baseline excludes member 30005. |
| m_demo_mapping3 | EXPTRANS | Original_Effective_Date | `Original_Effective_Date` | 940 | `informatica_pyspark/mappings/m_demo_mapping3.py:45` | HIGH | Connector-derived rename to Effective_Date; baseline dates exercise it. |
| m_demo_mapping3 | EXPTRANS | Relationship_to_Subscriber_Code | `Relationship_to_Subscriber_Code` | 941 | `informatica_pyspark/mappings/m_demo_mapping3.py:38` | HIGH | Identity pass-through is connected through the router to both targets and is exercised by baseline rows. |
| m_demo_mapping3 | EXPTRANS | Relationship_to_Subscriber_Code_Label | `Relationship_to_Subscriber_Code_Label` | 942 | `informatica_pyspark/mappings/m_demo_mapping3.py:38` | NOT MIGRATED | This identically named pass-through is a dead EXPTRANS output with no downstream connector; the connected abort output is the separate port at line 943. |
| m_demo_mapping3 | EXPTRANS | o_Relationship_to_Subscriber_Code_Label | `iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label)` | 943 | `informatica_pyspark/mappings/m_demo_mapping3.py:57` | HIGH | The abort fixture proves the eager hard-failure guard; the DEFAULTVALUE ERROR('transformation error') is unreachable and is intentionally not used. |
| m_demo_mapping3 | RTRTRANS | INPUT | *(none)* | 947 | *(none)* | NOT MIGRATED | INPUT is the router's structural input group, not a routed output path. |
| m_demo_mapping3 | RTRTRANS | NEWGROUP1 | `ISNULL(Social_Security_Number)` | 948 | `informatica_pyspark/mappings/m_demo_mapping3.py:65` | HIGH | Connector graph proves NEWGROUP1 *1 ports feed demo_target2; baseline target2 rows have empty Soc_Number. |
| m_demo_mapping3 | RTRTRANS | DEFAULT1 | *(none)* | 949 | *(none)* | NOT MIGRATED | DEFAULT1 owns the *2 ports but has no target connectors; its path is unreachable because the two explicit predicates are complementary. |
| m_demo_mapping3 | RTRTRANS | NEWGROUP2 | `NOT ISNULL(Social_Security_Number)` | 950 | `informatica_pyspark/mappings/m_demo_mapping3.py:66` | HIGH | Connector graph proves NEWGROUP2 *3 ports feed demo_target21; baseline target21 rows have SSNs. |

There are no lookups, aggregators, or sequence generators in m3; therefore none
were silently omitted from the comparison rows.

## Totals and confidence split

- Total comparison rows: **21**
- Expression rows: **15**
- Source Qualifier attribute rows: **2**
- Router group rows: **4**
- Migrated rows: **17**
- Not migrated by design: **4**
- Confidence: **HIGH 17, MEDIUM 0, LOW 0, NOT MIGRATED 4**

## LOW rows grouped by decision

There are no LOW-confidence rows. The XML connector graph determines the
projection, routing, and target instance assignment without an unresolved
semantic choice. The physical row order is not used by this mapping.

## Review these first

1. **Router target assignment:** NEWGROUP1's `*1` ports feed `demo_target2`,
   while NEWGROUP2's `*3` ports feed `demo_target21`; this is intentionally not
   inferred from suffixes or group ordinals.
2. **Abort timing and message:** the null-label guard is evaluated before any
   target write and preserves the legacy typo verbatim.
3. **Dead and unreachable paths:** the line-942 pass-through and DEFAULT1's
   `*2` ports have no downstream target consumers.
