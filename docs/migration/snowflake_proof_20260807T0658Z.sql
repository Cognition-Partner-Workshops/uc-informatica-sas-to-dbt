with chk as (
select 'DEMO_TARGET1_INS' as target,
       (select count(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_INS") as baseline_rows,
       (select count(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_INS") as migrated_rows,
       (select hash_agg(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_INS") as baseline_hash,
       (select hash_agg(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_INS") as migrated_hash,
       (select count(*) from (select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_INS" minus select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_INS")) as baseline_minus_migrated,
       (select count(*) from (select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_INS" minus select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_INS")) as migrated_minus_baseline
union all
select 'DEMO_TARGET1_UPD' as target,
       (select count(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_UPD") as baseline_rows,
       (select count(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_UPD") as migrated_rows,
       (select hash_agg(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_UPD") as baseline_hash,
       (select hash_agg(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_UPD") as migrated_hash,
       (select count(*) from (select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_UPD" minus select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_UPD")) as baseline_minus_migrated,
       (select count(*) from (select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_UPD" minus select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET1_UPD")) as migrated_minus_baseline
union all
select 'DEMO_TARGET2' as target,
       (select count(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET2") as baseline_rows,
       (select count(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET2") as migrated_rows,
       (select hash_agg(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET2") as baseline_hash,
       (select hash_agg(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET2") as migrated_hash,
       (select count(*) from (select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET2" minus select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET2")) as baseline_minus_migrated,
       (select count(*) from (select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET2" minus select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET2")) as migrated_minus_baseline
union all
select 'DEMO_TARGET21' as target,
       (select count(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET21") as baseline_rows,
       (select count(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET21") as migrated_rows,
       (select hash_agg(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET21") as baseline_hash,
       (select hash_agg(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET21") as migrated_hash,
       (select count(*) from (select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET21" minus select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET21")) as baseline_minus_migrated,
       (select count(*) from (select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET21" minus select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET21")) as migrated_minus_baseline
union all
select 'DEMO_TARGET3' as target,
       (select count(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET3") as baseline_rows,
       (select count(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET3") as migrated_rows,
       (select hash_agg(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET3") as baseline_hash,
       (select hash_agg(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET3") as migrated_hash,
       (select count(*) from (select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET3" minus select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET3")) as baseline_minus_migrated,
       (select count(*) from (select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET3" minus select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET3")) as migrated_minus_baseline
union all
select 'DEMO_TARGET5' as target,
       (select count(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET5") as baseline_rows,
       (select count(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET5") as migrated_rows,
       (select hash_agg(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET5") as baseline_hash,
       (select hash_agg(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET5") as migrated_hash,
       (select count(*) from (select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET5" minus select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET5")) as baseline_minus_migrated,
       (select count(*) from (select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET5" minus select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET5")) as migrated_minus_baseline
union all
select 'DEMO_TARGET6' as target,
       (select count(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET6") as baseline_rows,
       (select count(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET6") as migrated_rows,
       (select hash_agg(*) from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET6") as baseline_hash,
       (select hash_agg(*) from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET6") as migrated_hash,
       (select count(*) from (select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET6" minus select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET6")) as baseline_minus_migrated,
       (select count(*) from (select * from "PYSPARK_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET6" minus select * from "BASELINE_INFORMATICA_20260807T0658Z"."V_DEMO_TARGET6")) as migrated_minus_baseline
)
select target, baseline_rows, migrated_rows, baseline_hash, migrated_hash,
       baseline_minus_migrated, migrated_minus_baseline,
       case when baseline_rows = migrated_rows and baseline_hash = migrated_hash
                 and baseline_minus_migrated = 0 and migrated_minus_baseline = 0
            then 'PASS' else 'FAIL' end as verdict
from chk order by target;
