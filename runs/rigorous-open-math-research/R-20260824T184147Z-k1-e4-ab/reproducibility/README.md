# Reproducibility - K(1) strict anchor run

This directory contains the frozen source manifest, the solver-only token
metrics, the structured isolation audit, and the two raw solver outputs.

The benchmark protocol used identical frozen mathematical input and separate
arm directories.  The structured audit found no prohibited cross-arm path
access.  Isolation is protocol and event audited, not cryptographic.

The local command helper failed before process creation in both arms with
`helper_unknown_error: setup refresh had errors`.  The complete recurrence and
completion conditions were present in the frozen task, so the strict proof was
still independently checkable.  The Blueprint deterministic integration step
was not claimed because its file-backed runtime was unavailable.

The proof document is `docs/SL_third_order_K1_proof.tex`.  It was successfully
compiled with MiKTeX 23.4 on 2026-08-25.  Bundled Tectonic was also attempted,
but its sandbox lacked the required font resources and could not fetch them.
