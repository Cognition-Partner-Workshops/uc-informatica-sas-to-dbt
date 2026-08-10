# Snowflake Transformation Demonstrations

These results were captured by executing the six read-only statements in `snowflake/sql/07_transformations.sql` against the standing milestone-5 schemas.

## Statement 1

**Statement as run**

```sql
-- Demonstration queries: the PySpark transformations, visible in the warehouse.
--
-- These are not parity proofs (see 02..06 for those). Each statement puts the Snowflake
-- source rows next to the rows the PySpark pipeline wrote, so the transformation itself is
-- observable rather than inferred: what went in, what came out, and which Informatica
-- construct is responsible.
--
-- Schemas are the standing run schemas from milestone 5.

-- 1. The line-580 SQL override binds POSITIONALLY, not by name.
--    demo_target6.CR8_DT does not carry demo_source4.CR8_DT; it carries the bare SYSTIMESTAMP
--    that sits in the 5th position of the override's select list (pinned business date).
select s."ACCT_ID"                                as acct_id,
       s."CR8_DT"                                 as source_cr8_dt,
       t."CR8_DT"                                 as migrated_cr8_dt,
       case
           when t."CR8_DT"::varchar = s."CR8_DT" then 'name-matched'
           else 'positional override -> SYSTIMESTAMP'
       end                                        as binding
from DEVIN_MIGRATION_DEMO.SOURCE_INFORMATICA_20260809T234500Z.DEMO_SOURCE4 s
join DEVIN_MIGRATION_DEMO.PYSPARK_INFORMATICA_20260809T234500Z.DEMO_TARGET6 t
  on t."ACCT_ID" = s."ACCT_ID"::double
order by acct_id
```

**Rows:** 2

```text
ACCT_ID | SOURCE_CR8_DT | MIGRATED_CR8_DT | BINDING
1001 | 2023-08-18 | 2024-01-31 | positional override -> SYSTIMESTAMP
1002 | 2017-02-09 | 2024-01-31 | positional override -> SYSTIMESTAMP
```

This demonstrates that the target CR8_DT comes from the positional SYSTIMESTAMP binding rather than the same-named source CR8_DT.

## Statement 2

**Statement as run**

```sql
-- 2. agg_TRANS SUM, the sequence generator, and the unconnected lookup call, in one row each.
--    migrated_tx_amt is SUM(TX_AMT) over the account's transactions; sequence_key continues
--    the XML's Current Value = 281; migrated_tx_type_cd comes from :LKP.lkp_TRANS1(ACCT_ID)
--    (Use Last Value over lkp_demo_source3), NOT from the same-named demo_source3.TX_TYPE_CD.
with tx as (
    select "ACCT_ID"                              as acct_id,
           count(*)                               as source_tx_rows,
           sum("TX_AMT"::double)                  as source_sum_tx_amt,
           listagg(distinct "TX_TYPE_CD", ',')    as source3_tx_type_cds
    from DEVIN_MIGRATION_DEMO.SOURCE_INFORMATICA_20260809T234500Z.DEMO_SOURCE3
    group by 1
),
lkp as (
    select "ACCT_ID" as acct_id, "TX_TYPE_CD" as lookup_tx_type_cd
    from (
        select "ACCT_ID",
               "TX_TYPE_CD",
               row_number() over (partition by "ACCT_ID" order by "SRC_ORDINAL" desc) as rn
        from DEVIN_MIGRATION_DEMO.SOURCE_INFORMATICA_20260809T234500Z.LKP_DEMO_SOURCE3
    )
    where rn = 1
)
select t."ACCT_ID"            as acct_id,
       tx.source_tx_rows,
       tx.source_sum_tx_amt,
       t."TX_AMT"             as migrated_tx_amt,
       t."ACCT_KEY"           as sequence_key,
       tx.source3_tx_type_cds,
       lkp.lookup_tx_type_cd,
       t."TX_TYPE_CD"         as migrated_tx_type_cd
from DEVIN_MIGRATION_DEMO.PYSPARK_INFORMATICA_20260809T234500Z.DEMO_TARGET6 t
join tx  on tx.acct_id::double  = t."ACCT_ID"
left join lkp on lkp.acct_id::double = t."ACCT_ID"
order by acct_id
```

**Rows:** 2

```text
ACCT_ID | SOURCE_TX_ROWS | SOURCE_SUM_TX_AMT | MIGRATED_TX_AMT | SEQUENCE_KEY | SOURCE3_TX_TYPE_CDS | LOOKUP_TX_TYPE_CD | MIGRATED_TX_TYPE_CD
1001 | 2 | 2031.2399999999998 | 2031.2399999999998 | 281 | DR,CR | DR | DR
1002 | 1 | -1238.81 | -1238.81 | 282 | CR | DR | DR
```

This demonstrates the aggregate SUM, continuing sequence value, and Use Last Value unconnected lookup feeding the migrated transaction row.

## Statement 3

**Statement as run**

```sql
-- 3. RTRIM / LTRIM ports: exp_TRANS o_acc_trim, o_ACCT_DESC, o_crdt_trim.
--    Compare the raw source string lengths with the migrated ones.
select s."ACCT_ID"                as acct_id,
       '['||s."ACCT_TYP"||']'     as source_acct_typ,
       length(s."ACCT_TYP")       as source_acct_typ_len,
       '['||t."ACCT_TYP"||']'     as migrated_acct_typ,
       length(t."ACCT_TYP")       as migrated_acct_typ_len,
       '['||s."CRDT_LN"||']'      as source_crdt_ln,
       length(s."CRDT_LN")        as source_crdt_ln_len,
       '['||t."CRDT_LN"||']'      as migrated_crdt_ln,
       length(t."CRDT_LN")        as migrated_crdt_ln_len
from DEVIN_MIGRATION_DEMO.SOURCE_INFORMATICA_20260809T234500Z.DEMO_SOURCE4 s
join DEVIN_MIGRATION_DEMO.PYSPARK_INFORMATICA_20260809T234500Z.DEMO_TARGET6 t
  on t."ACCT_ID" = s."ACCT_ID"::double
order by acct_id
```

**Rows:** 2

```text
ACCT_ID | SOURCE_ACCT_TYP | SOURCE_ACCT_TYP_LEN | MIGRATED_ACCT_TYP | MIGRATED_ACCT_TYP_LEN | SOURCE_CRDT_LN | SOURCE_CRDT_LN_LEN | MIGRATED_CRDT_LN | MIGRATED_CRDT_LN_LEN
1001 | [SB] | 2 | [SB] | 2 | [  8000] | 6 | [8000] | 4
1002 | [SB] | 2 | [SB] | 2 | [48000] | 5 | [48000] | 5
```

This demonstrates the trimming transformations by showing source and migrated string lengths side by side.

## Statement 4

**Statement as run**

```sql
-- 4. m_demo_mapping2 insert/update detection, and the two different Key provenances.
--    A source ID absent from the demo_target1 lookup is an Insert and draws the sequence
--    (bigint, renders 57..60); a matched ID is an Update carrying the lookup's double Key.
--    The .0 rendering of lookup values is a local-CSV artifact, not a Snowflake result.
with lookup_last as (
    select "ID" as id, "Key" as existing_key
    from (
        select "ID",
               "Key",
               row_number() over (partition by "ID" order by "SRC_ORDINAL" desc) as rn
        from DEVIN_MIGRATION_DEMO.SOURCE_INFORMATICA_20260809T234500Z.DEMO_TARGET1
    )
    where rn = 1
)
select s."ID"                                            as source_id,
       l.existing_key                                    as lookup_key,
       case when l.existing_key is null then 'Insert' else 'Update' end as detected_as,
       coalesce(i."Key"::varchar, u."Key"::varchar)      as written_key,
       case
           when i."ID" is not null then 'demo_target1_INS (SEQTRANS.NEXTVAL, bigint)'
           when u."ID" is not null then 'demo_target1_UPD (LKPTRANS Key, double)'
           else 'not written'
       end                                               as written_to
from DEVIN_MIGRATION_DEMO.SOURCE_INFORMATICA_20260809T234500Z.DEMO_SOURCE1 s
left join lookup_last l on l.id = s."ID"
left join DEVIN_MIGRATION_DEMO.PYSPARK_INFORMATICA_20260809T234500Z.DEMO_TARGET1_INS i on i."ID" = s."ID"
left join DEVIN_MIGRATION_DEMO.PYSPARK_INFORMATICA_20260809T234500Z.DEMO_TARGET1_UPD u on u."ID" = s."ID"
order by s."SRC_ORDINAL"::number
```

**Rows:** 7

```text
SOURCE_ID | LOOKUP_KEY | DETECTED_AS | WRITTEN_KEY | WRITTEN_TO
REC00001 | 1 | Update | 1 | demo_target1_UPD (LKPTRANS Key, double)
REC00002 | 99 | Update | 99 | demo_target1_UPD (LKPTRANS Key, double)
REC00003 | 3 | Update | 3 | demo_target1_UPD (LKPTRANS Key, double)
REC00004 | NULL | Insert | 57 | demo_target1_INS (SEQTRANS.NEXTVAL, bigint)
REC00005 | NULL | Insert | 58 | demo_target1_INS (SEQTRANS.NEXTVAL, bigint)
REC00006 | NULL | Insert | 59 | demo_target1_INS (SEQTRANS.NEXTVAL, bigint)
REC00007 | NULL | Insert | 60 | demo_target1_INS (SEQTRANS.NEXTVAL, bigint)
```

This demonstrates router-style insert/update detection and the separate sequence-versus-lookup provenance of the written Key.

## Statement 5

**Statement as run**

```sql
-- 5. m_demo_mapping3: NEWGROUP1 (SSN is null) -> demo_target2; NEWGROUP2 (SSN not null) -> demo_target21.
--    The SQL override drops only Member_ID 30005; DEFAULT1 is unreachable here because the groups are complementary.
select s."Member_ID"                          as member_id,
       s."Member_Type_Code"                   as member_type_code,
       s."Social_Security_Number"             as ssn,
       case
           when t2."Member_Identifier"  is not null then 'demo_target2  (NEWGROUP1: SSN is null)'
           when t21."Member_Identifier" is not null then 'demo_target21 (NEWGROUP2: SSN not null)'
           when s."Member_Type_Code" is null        then 'discarded by SQL override (NULL Member_Type_Code)'
           else 'discarded'
       end                                    as routed_to,
       coalesce(t2."Relationship_to_Subscriber_Code_Label",
                t21."Relationship_to_Subscriber_Code_Label") as label
from DEVIN_MIGRATION_DEMO.SOURCE_INFORMATICA_20260809T234500Z.DEMO_SOURCE2 s
left join DEVIN_MIGRATION_DEMO.PYSPARK_INFORMATICA_20260809T234500Z.DEMO_TARGET2 t2
  on t2."Member_Identifier" = s."Member_ID"::double
left join DEVIN_MIGRATION_DEMO.PYSPARK_INFORMATICA_20260809T234500Z.DEMO_TARGET21 t21
  on t21."Member_Identifier" = s."Member_ID"::double
order by s."SRC_ORDINAL"::number
```

**Rows:** 7

```text
MEMBER_ID | MEMBER_TYPE_CODE | SSN | ROUTED_TO | LABEL
30001 | 1 | NULL | demo_target2  (NEWGROUP1: SSN is null) | CHILD
30002 | 2 | 100000037 | demo_target21 (NEWGROUP2: SSN not null) | SELF
30003 | 2 | NULL | demo_target2  (NEWGROUP1: SSN is null) | CHILD
30004 | 2 | 100000111 | demo_target21 (NEWGROUP2: SSN not null) | OTHER
30005 | NULL | NULL | discarded by SQL override (NULL Member_Type_Code) | NULL
30006 | 1 | 100000222 | demo_target21 (NEWGROUP2: SSN not null) | SPOUSE
30007 | 2 | NULL | demo_target2  (NEWGROUP1: SSN is null) | SELF
```

This demonstrates the complementary router groups and the single NULL Member_Type_Code row dropped by the SQL override on this dataset.

## Statement 6

**Statement as run**

```sql
-- 6. The preserved legacy defect: exp_TRANS2.o_SELL_ST_DT is TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY'),
--    a mask that cannot parse its own input, so every migrated SELL_ST_DT is NULL even though the
--    source column is populated. SELL_ED_DT, which uses a compatible mask, converts fine.
select s."PRODUCT_ID"    as product_id,
       s."SELL_ST_DT"    as source_sell_st_dt,
       t."SELL_ST_DT"    as migrated_sell_st_dt,
       s."SELL_ED_DT"    as source_sell_ed_dt,
       t."SELL_ED_DT"    as migrated_sell_ed_dt
from DEVIN_MIGRATION_DEMO.SOURCE_INFORMATICA_20260809T234500Z.DEMO_SOURCE5 s
join DEVIN_MIGRATION_DEMO.PYSPARK_INFORMATICA_20260809T234500Z.DEMO_TARGET3 t
  on t."PRODUCT_ID" = s."PRODUCT_ID"
order by product_id
```

**Rows:** 4

```text
PRODUCT_ID | SOURCE_SELL_ST_DT | MIGRATED_SELL_ST_DT | SOURCE_SELL_ED_DT | MIGRATED_SELL_ED_DT
PRD0001 | 10/02/2020 | NULL | 17/07/2024 | 2024-07-17
PRD0002 | 11/07/2021 | NULL | 28/09/2025 | 2025-09-28
PRD0003 | 03/05/2021 | NULL | 23/08/2025 | 2025-08-23
PRD0004 | 01/08/2020 | NULL | 20/01/2026 | 2026-01-20
```

This demonstrates the preserved date-conversion defect: SELL_ST_DT is NULL while the compatible SELL_ED_DT conversion succeeds.
