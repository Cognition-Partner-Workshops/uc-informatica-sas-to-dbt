{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: EXPTRANS passes through demo_source1 fields and receives Key and
  lookup LEAD_CO_MNE as LEAD_CO_MNE1 from LKPTRANS on ID = ID1.
  RECOVERED: New_Flag is IIF(ISNULL(Key),'Insert'); o_CREATED_BY and
  o_UPDATED_BY are 'IDWUSER'; the time ports are SYSDATE.
  RECOVERED + defect: the legacy MD5_src local variable decrypts lookup
  LEAD_CO_MNE1 while MD5_tgt hashes source fields, so their value spaces are
  incomparable and every matched row is an Update.
  RECOVERED: Informatica string concatenation treats NULL operands as empty
  strings, so the five source ports are coalesced to empty strings before the
  MD5_tgt digest is calculated.
  DECISION: AES_DECRYPT over the lookup column has no portable equivalent and
  its plaintext is unrecoverable, so MD5_src uses the 'LEGACY_AES_VALUE'
  sentinel. It cannot equal the hexadecimal MD5 digest, preserving the
  explicit legacy predicate without implementing real change detection.
*/
with operands as (
    select
        s.LEAD_CO_MNE,
        s.BRANCH_CO_MNE,
        s.MIS_DATE,
        s.ID,
        s.DESCRIPTION,
        s.SHORT_NAME,
        p.Key,
        p.LEAD_CO_MNE as LEAD_CO_MNE1,
        case when p.Key is null then 'Insert' else null end as New_Flag,
        'LEGACY_AES_VALUE' as MD5_src,
        md5(
            coalesce(s.LEAD_CO_MNE, '') || coalesce(s.BRANCH_CO_MNE, '') ||
            coalesce(s.MIS_DATE, '') || coalesce(s.DESCRIPTION, '') ||
            coalesce(s.SHORT_NAME, '')
        ) as MD5_tgt,
        'IDWUSER' as o_CREATED_BY,
        {{ business_timestamp() }} as o_CREATED_TIME,
        'IDWUSER' as o_UPDATED_BY,
        {{ business_timestamp() }} as o_UPDATED_TIME
    from {{ ref('stg_demo_source1') }} s
    left join {{ ref('stg_demo_target1') }} p
        on p.ID = s.ID
)
select
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    Key,
    LEAD_CO_MNE1,
    New_Flag,
    MD5_src,
    MD5_tgt,
    case
        when Key is not null and MD5_tgt != MD5_src then 'Update'
        else null
    end as Changed_Flag,
    o_CREATED_BY,
    o_CREATED_TIME,
    o_UPDATED_BY,
    o_UPDATED_TIME
from operands
