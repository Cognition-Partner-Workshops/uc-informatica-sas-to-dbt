/*=====================================================================
  sas_golden stub for %sendmail (tools/sas_golden/stubs/sendmail.sas)
  Staged by run_golden.sas in place of legacy/sas/macros/sendmail.sas when
  "sendmail" is not listed in GOLDEN_REAL_MACROS. Side-effect macro only:
  it writes nothing to any dataset, so the golden outputs do not depend
  on it. PARMBUFF with no declared parameters accepts every call form
  used by the programs (keyword args such as body=/file=/sheet= and the
  positional %lock(LIB.DS) / %lock(LIB.DS, unlock) calls).
=====================================================================*/
%macro sendmail / parmbuff;
  %put NOTE: [sas_golden stub] %nrstr(%%)sendmail not executed. Call: %superq(syspbuff);
%mend sendmail;
