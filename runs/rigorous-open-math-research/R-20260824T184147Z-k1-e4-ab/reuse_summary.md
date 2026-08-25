# Reuse Summary - K(1) strict anchor run

## Reused project material

- `docs/SL_third_order_recurrence_theory.tex` for the original recurrence,
  numerical conjecture, and open-status provenance.
- `scripts/op13_K1_definitive.py` for historical numerical evidence only.
- `scripts/op13_matched_asymp3.py` and `scripts/op13_gf_ode5.py` for source
  provenance and the statement of the former proof gap.
- Existing third-order recurrence notation and the project strictness labels.

## New result

The new proof does not rely on the numerical scripts.  It supplies an exact
factorial scaling, a finite backward formula, a complete scaled solution form,
and a positive-tail asymptotic estimate.  It therefore closes only the `c=1`
anchor and does not promote the general `K(c)` problem.

## Reproducibility

The two raw solver outputs, source hashes, token metrics, and isolation audit
are in `reproducibility/`.  The independent neutral review is summarized in
`audit_report.md`.
