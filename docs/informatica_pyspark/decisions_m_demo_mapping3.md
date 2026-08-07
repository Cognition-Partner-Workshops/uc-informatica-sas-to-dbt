# Decisions for `m_demo_mapping3`

## Recovered legacy behaviour

These are defects or surprising behaviors recovered from the XML and reproduced
on purpose:

- **ABORT is a hard run failure.** The line-943 expression calls
  `ABORT('Relationship_to_Subscriber_Code_Labe valuel is null')` for a
  post-source-filter row whose label is null. The guard is evaluated eagerly
  before the caller can write either target, so the abort fixture leaves no
  target CSVs.
- **The router naming trap is preserved.** `NEWGROUP1` tests a null SSN and its
  `*1` ports are connected to `demo_target2`; `NEWGROUP2` tests a non-null SSN
  and its `*3` ports are connected to `demo_target21`. The target assignment
  follows connectors 1017-1044, not suffixes or group ordinals.
- **The dead pass-through port is not used.** EXPTRANS port
  `Relationship_to_Subscriber_Code_Label` at line 942 is not connected.
  The identically named router input receives the separate line-943 abort
  output instead.
- **The `ERROR('transformation error')` default is unreachable.** It is the
  DEFAULTVALUE metadata on the line-943 port, but the expression's null branch
  aborts first; it is not a fallback null fill.
- **DEFAULT1 is unconnected.** It owns the `*2` ports and has no target
  connectors. The two explicit router predicates are complementary, so no row
  reaches the default path.

## Decisions forced by the XML

- The SQL override at line 916 is implemented as the source read followed by
  `Member_Type_Code IS NOT NULL`. The line-918 Source Filter is a separate,
  empty attribute and is deliberately not treated as a second filter.
- The target projection follows the target definition order at lines 128-141,
  with `Gender` second. Field renames follow the connector graph rather than
  matching similarly named columns.
- Both target instances use the same target-definition projection. Only the
  router predicate differs.
- The XML transformation ports are numeric doubles even though `io.py`
  declares source numerics as longs. The five numeric target columns are
  explicitly cast to double to preserve the legacy CSV rendering.
- No lookup, aggregator, or sequence-generator semantics exist in this mapping.
  No changes to `io.py` were needed.

The XML does not specify a meaningful output ordering for the two target
instances. This conversion does not impose one: the existing writer and parity
checker compare the connector-derived target columns, while `__ROW_ORD` is
removed before returning the frames.
