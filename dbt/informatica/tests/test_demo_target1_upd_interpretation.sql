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
count_check as (
    select count(*) <> 3 as failed
    from actual_keys
),
count_failure as (
    select 'unexpected update row count' as failure
    from count_check
    where failed
),
missing_check as (
    select count(*) > 0 as failed
    from (
        select Key from expected_keys
        except
        select Key from actual_keys
    ) as differences
),
missing_keys as (
    select 'missing expected update key' as failure
    from missing_check
    where failed
),
unexpected_check as (
    select count(*) > 0 as failed
    from (
        select Key from actual_keys
        except
        select Key from expected_keys
    ) as differences
),
unexpected_keys as (
    select 'unexpected update key' as failure
    from unexpected_check
    where failed
)
select failure from count_failure
union all
select failure from missing_keys
union all
select failure from unexpected_keys
