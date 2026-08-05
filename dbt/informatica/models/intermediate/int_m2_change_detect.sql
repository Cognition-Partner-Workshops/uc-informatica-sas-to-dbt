-- m_demo_mapping2 LKPTRANS + EXPTRANS: lookup the demo_target1 pre-image by ID
-- and derive the insert/update flags. Kept faithful to the legacy expressions:
--   MD5_src = AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256) decrypts a
--   plaintext value with a 3-character passphrase, so it is always NULL;
--   therefore MD5_tgt != MD5_src is NULL and changed_flag is never 'Update'.
select
    s.lead_co_mne,
    s.branch_co_mne,
    s.mis_date,
    s.id,
    s.description,
    s.short_name,
    p.key                                          as lookup_key,
    case when p.key is null then 'Insert' end      as new_flag,
    cast(null as varchar)                          as md5_src,
    md5(s.lead_co_mne || s.branch_co_mne || s.mis_date
        || s.description || s.short_name)          as md5_tgt,
    cast(null as varchar)                          as changed_flag,
    'IDWUSER'                                      as o_created_by,
    cast('{{ var("business_date") }} 00:00:00' as timestamp) as o_created_time,
    'IDWUSER'                                      as o_updated_by,
    cast('{{ var("business_date") }} 00:00:00' as timestamp) as o_updated_time
from {{ ref('stg_demo_source1') }} s
left join {{ ref('stg_demo_target1_pre') }} p
    on p.id = s.id
