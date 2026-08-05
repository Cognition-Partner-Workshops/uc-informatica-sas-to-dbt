{{ config(severity='error') }}

/*
This pins the baseline interpretation: AES_DECRYPT of a never-encrypted value
is not NULL-equivalent to the MD5 hex string, so every matched row updates.
If this count or key set changes, the interpretation flipped and the model and
tools/informatica_baseline.py must be revisited together.
*/
with expected_keys as (
    select 1 as Key
    union all select 3
    union all select 99
),
actual_keys as (
    select Key
    from {{ ref('demo_target1_upd') }}
),
count_failure as (
    select 'unexpected update row count' as failure
    where (select count(*) from actual_keys) <> 3
),
missing_keys as (
    select 'missing expected update key' as failure
    where exists (
        select Key from expected_keys
        except
        select Key from actual_keys
    )
),
unexpected_keys as (
    select 'unexpected update key' as failure
    where exists (
        select Key from actual_keys
        except
        select Key from expected_keys
    )
)
select failure from count_failure
union all
select failure from missing_keys
union all
select failure from unexpected_keys
