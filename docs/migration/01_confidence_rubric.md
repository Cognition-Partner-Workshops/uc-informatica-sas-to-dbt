# Confidence rubric

* **HIGH** — semantics are unambiguous in the XML **and** at least one baseline row would fail parity
  if the conversion were wrong.
* **MEDIUM** — unambiguous, but weakly exercised: the output is constant or degenerate in the seed
  data, so parity cannot catch a wrong conversion.
* **LOW** — the conversion rests on a judgement call the XML does not determine; the row must name the alternative that was rejected.
* **NOT MIGRATED** — deliberately not converted (e.g. a port with no outgoing CONNECTOR); every such element must be named.
