select ID from (
    select ID, "KEY", 56 + row_number() over (order by ID) as EXPECTED_KEY
    from {{ ref('DEMO_TARGET1_INS') }}
)
where "KEY" != EXPECTED_KEY
