/*
LKPTRANS uses ID = ID1 and "Use Any Value". The before-state contains duplicate
REC00002 rows, so this migration makes the required deterministic choice explicit:
the lookup row with the highest Key per ID wins.
*/
with ranked_lookup as (
    select
        Key,
        LEAD_CO_MNE,
        BRANCH_CO_MNE,
        MIS_DATE,
        ID,
        DESCRIPTION,
        SHORT_NAME,
        row_number() over (
            partition by ID
            order by Key desc
        ) as lookup_rank
    from {{ ref('stg_demo_target1_pre') }}
),
deduplicated_lookup as (
    select
        Key as lookup_Key,
        LEAD_CO_MNE as LEAD_CO_MNE1,
        BRANCH_CO_MNE as BRANCH_CO_MNE1,
        MIS_DATE as MIS_DATE1,
        ID as lookup_ID,
        DESCRIPTION as DESCRIPTION1,
        SHORT_NAME as SHORT_NAME1
    from ranked_lookup
    where lookup_rank = 1
),
expression_values as (
    select
        source.LEAD_CO_MNE,
        source.BRANCH_CO_MNE,
        source.MIS_DATE,
        source.ID,
        source.DESCRIPTION,
        source.SHORT_NAME,
        lookup.lookup_Key,
        lookup.LEAD_CO_MNE1,
        lookup.BRANCH_CO_MNE1,
        lookup.MIS_DATE1,
        lookup.lookup_ID,
        lookup.DESCRIPTION1,
        lookup.SHORT_NAME1,
        case
            when lookup.lookup_Key is null then 'Insert'
        end as New_Flag,
        /*
        Legacy expression shape:
        MD5_src = AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256).
        MD5_tgt = MD5(LEAD_CO_MNE || BRANCH_CO_MNE || MIS_DATE ||
                      DESCRIPTION || SHORT_NAME).
        The names are inverted: MD5_tgt uses SOURCE columns while MD5_src
        uses the LOOKUP column. The baseline preserves MD5_src as a
        target-side AES value because the comparison is MD5 hex text versus
        an AES-decrypted value. Those value spaces are incomparable.
        */
        cast('LEGACY_AES_VALUE' as varchar) as MD5_src,
        MD5(
            source.LEAD_CO_MNE
            || source.BRANCH_CO_MNE
            || source.MIS_DATE
            || source.DESCRIPTION
            || source.SHORT_NAME
        ) as MD5_tgt,
        'IDWUSER' as o_CREATED_BY,
        cast('{{ var("business_date") }} 00:00:00' as timestamp) as o_CREATED_TIME,
        'IDWUSER' as o_UPDATED_BY,
        cast('{{ var("business_date") }} 00:00:00' as timestamp) as o_UPDATED_TIME
    from {{ ref('stg_demo_source1') }} as source
    left join deduplicated_lookup as lookup
        on lookup.lookup_ID = source.ID
),
expression_flags as (
    select
        expression_values.*,
        /*
        With the placeholder MD5_src, this predicate is true for every
        matched row. Under this reading every source row is routed to Insert
        or Update; no row is dropped to the unconnected DEFAULT1 group.
        */
        case
            when lookup_Key is not null
                and MD5_tgt != MD5_src
                then 'Update'
        end as Changed_Flag
    from expression_values
)
select *
from expression_flags
