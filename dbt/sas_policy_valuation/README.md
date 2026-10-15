# sas_policy_valuation

dbt-on-Snowflake migration of the legacy SAS program
`legacy/sas/programs/policy_valuation.sas` — the monthly policy book
valuation that calculates in-force policy metrics, premium adequacy,
loss ratios and reserve estimates.

## Layers

- **Staging** (views): `stg_policy_valuation__raw_ins_policies`,
  `stg_policy_valuation__raw_ins_claims`,
  `stg_policy_valuation__raw_ins_premiums` — rename/cast only over
  `SOURCE_<token>.RAW_INS_*`.
- **Intermediate** (ephemeral, one per SAS step):
  - `int_policy_valuation__inforce` — Step 1 PROC SQL, in-force policies
    with policy age, months to expiry, renewal flag and YTD earned premium.
  - `int_policy_valuation__claims_exp` — Step 2 PROC SQL, 12-month claims
    experience per policy.
  - `int_policy_valuation__premium_coll` — Step 3 PROC SQL, YTD premium
    collections per policy.
  - `int_policy_valuation__valuation` — Step 4 DATA step MERGE (`if a`),
    loss/combined ratios, premium adequacy, IBNR and total reserve, plus
    `POLICY_TYPE_DESC` / `RISK_CATEGORY_DESC` via the format seeds.
  - `int_policy_valuation__loss_ratio_means` — Step 5 PROC MEANS NWAY by
    `POLICY_TYPE`.
- **Marts** (tables): `POLICY_VALUATION` (legacy `STG_INS.POLICY_VALUATION`),
  `LOSS_RATIO_SUMMARY` (legacy `REPORTS.LOSS_RATIO_SUMMARY`).
- **Seeds**: `policy_valuation__fmt_poltype` ($POLTYPE) and
  `policy_valuation__fmt_riskcat` ($RISKCAT) from
  `legacy/sas/formats/insurance_formats.sas`; the format `OTHER=` labels
  (`Unknown` / `Unrated`) are applied via `coalesce` in SQL.

## Run

```bash
cd dbt/sas_policy_valuation
dbt build --target snowflake --profiles-dir .
```

## Assumptions

- Run date is pinned via `var val_date='2024-01-31'`, `lob='ALL'`.
- `STG_INS.POLICY_VALUATION` is only read by the PROC MEANS within the same
  run; there is no prior state to merge with.
- `TERA_DW.ACTUARIAL_TABLES` and `REPORTS.RESERVE_ADEQUACY` appear in the
  program header but are never read / never created — not migrated.
- At the January valuation date `YTD_EARNED_PREMIUM` is 0 for every policy
  (month-boundary counting between 01JAN and 31JAN), so `LOSS_RATIO` and
  `COMBINED_RATIO` are null, `PREMIUM_ADEQUATE='N'` and `IBNR_ESTIMATE=0`
  (faithful legacy semantics; see docs/stm/sas_stm.md).
- SAS display formats are migrated as explicit `*_DESC` columns via seeds.
- Wall-clock columns (e.g. `LOAD_TIMESTAMP`) are not produced.
