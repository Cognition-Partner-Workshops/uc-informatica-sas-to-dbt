# Decisions for `m_demo_mapping2`

## Use Any Value tie-break

The XML says `Use Any Value` (line 285), but does not define which duplicate lookup
row wins. `REC00002` has lookup keys 2 and 99, making the ambiguity observable.
The conversion chooses the highest value of the lookup's own `Key` column before
the left join. The rejected alternatives are lowest Key, physical-first, and
physical-last. Highest Key is the most defensible deterministic choice because it
matches the current target state convention in the supplied seed and is stable
across Spark partitioning; physical order is not a semantic contract for `Use Any
Value`, and lowest Key would select the superseded row. This is a LOW-confidence
decision, not an XML fact.

## Unrecoverable AES decryption

`MD5_src` calls `AES_DECRYPT` on the lookup's `LEAD_CO_MNE1`, using the first three
characters of the source `SHORT_NAME` as the key material (XML line 177). The
repository has no ciphertext/key pair and no Informatica runtime with which to
recover the result. DESIGN.md therefore pins
`inf_aes_decrypt_unrecoverable` to the `LEGACY_AES_VALUE` sentinel. This is both an
unrecoverable function and a deliberate conversion decision; implementing a real
AES attempt or returning NULL was rejected because neither is supported by the
available evidence or the design contract.

## Recovered legacy defect: incomparable hash spaces

The live legacy expression compares `MD5_tgt`, an MD5 hash of source
`LEAD_CO_MNE || BRANCH_CO_MNE || MIS_DATE || DESCRIPTION || SHORT_NAME`, with
`MD5_src`, the AES-decrypted lookup value. These are incomparable value spaces, so
`MD5_tgt != MD5_src` is always true for matched rows and every matched row is
flagged `Update`. The conversion reproduces this observable behavior on purpose;
it does not claim to reproduce the unavailable decryption result. Fixing the
comparison to a meaningful same-space hash was rejected as a parity-breaking
business-logic change.

## Router suffix and UPDTRANS input-port trap

The router's `Update` group owns `LEAD_CO_MNE4`, `ID3`, `DESCRIPTION4`, and the
other `*4`/`*3` ports, while `DEFAULT1` owns ports such as `LEAD_CO_MNE3` and
`ID2`. UPDTRANS has input/output ports with the same names as DEFAULT1, but
connectors 411-423 explicitly feed UPDTRANS from the Update group. The conversion
models the Update group first and then aliases it to the UPDTRANS names. Name
matching was rejected because it would route the unconnected DEFAULT1 group.

## Key rendering by target instance

The EXPTRANS/UPD router Key ports are XML `double` ports (lines 170, 244, and
340), so update keys are explicitly cast to `DoubleType` and render as `1.0` and
`99.0`. The sequence `NEXTVAL` is XML `bigint` (line 315), so insert keys are
`LongType` and render as `57` through `60`. Casting both branches to one common
type was rejected because it changes the comparator-visible CSV representation.

## Sequence from physical row order

The sequence XML starts at current value 57 with increment 1 (lines 317-320), and
the insert target consumes `NEXTVAL` (line 373). The conversion uses
`56 + row_number()` ordered by `__ROW_ORD` over the Insert branch. This models
arrival order deterministically; for the supplied seed it coincides with ID order,
as shown by the baseline's `ORDER BY ID`. `monotonically_increasing_id()` was
rejected as the sequence value because it is not a contiguous Informatica
sequence.

## Other connector-derived choices

The update description is taken from source `DESCRIPTION` through the Update
group (`DESCRIPTION4 -> DESCRIPTION3`, connectors 415), not from lookup
`DESCRIPTION1`; the baseline's “General ledger account” values verify this.
The four other lookup outputs (`BRANCH_CO_MNE1`, `MIS_DATE1`, `DESCRIPTION1`,
`SHORT_NAME1`) reach the router but no target, so they are deliberately not
migrated. Unconnected target fields are emitted as typed NULLs, preserving the
legacy empty CSV cells.
