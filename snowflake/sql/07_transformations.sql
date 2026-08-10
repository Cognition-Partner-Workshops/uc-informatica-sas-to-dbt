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
order by acct_id;

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
order by acct_id;

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
order by acct_id;

-- 4. m_demo_mapping2 insert/update detection, and the two different Key provenances.
--    A source ID absent from the demo_target1 lookup is an Insert and draws the sequence
--    (bigint, renders 57..60); a matched ID is an Update and carries the lookup's double Key
--    (renders 1.0 / 99.0 / 3.0). Same physical column, two upstream connectors.
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
order by s."SRC_ORDINAL"::number;

-- 5. m_demo_mapping3: exactly one row (Member_ID 30005) is dropped by the SQL override; DEFAULT1 catches nothing because the router groups are complementary.
--    NEWGROUP1 (SSN is null) -> demo_target2; NEWGROUP2 (SSN not null) -> demo_target21;
--    a NULL Member_Type_Code is dropped by the SQL override, and DEFAULT1 has no connectors.
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
order by s."SRC_ORDINAL"::number;

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
order by product_id;
