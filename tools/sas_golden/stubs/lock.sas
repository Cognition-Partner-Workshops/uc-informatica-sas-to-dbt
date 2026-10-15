/*=====================================================================
  sas_golden stub for %lock (tools/sas_golden/stubs/lock.sas)
  Staged by run_golden.sas in place of legacy/sas/macros/lock.sas when
  "lock" is not listed in GOLDEN_REAL_MACROS. Side-effect macro only:
  it writes nothing to any dataset, so the golden outputs do not depend
  on it. PARMBUFF with no declared parameters accepts every call form
  used by the programs (keyword args such as body=/file=/sheet= and the
  positional %lock(LIB.DS) / %lock(LIB.DS, unlock) calls).
=====================================================================*/
%macro lock / parmbuff;
  %put NOTE: [sas_golden stub] %nrstr(%%)lock not executed. Call: %superq(syspbuff);
%mend lock;
