# Escalation ladder

This run is bounded.  The ladder records the escalation paths considered and
whether they were needed.

## Tier 0: cheap probes and direct symbolic checks

- Read existing documentation and scripts.
- Extract exact coefficients.
- Compute formal power-series expansions and diagonal coefficients.
- Status: used.  Resolved the root-1 branch without escalation.

## Tier 1: specialization and simple symbolic classification

- Specialize the rational function to a finite degree (`d = 3`) and attempt an
  exact solve.
- Status: attempted (existing scripts `op13_degtest*.py`), but the general
  symbolic solve timed out at 120s.  Not needed for the final proof.
- Could be used as a cross-check but would require Groebner with a specialized
  monomial order/careful variable elimination.

## Tier 2: concrete small computation

- Symbolic verification of the diagonal-coefficient formula for `m=2..8`,
  both parities, all allowed `u`.  This is exact sympy, not floating point.
- Status: used and passed.
- Could be extended to `m=20` if desired; the proof already covers all `m`.

## Tier 3: large multi-route fan-out or heavy algebra

- Petkovsek / hypergeometric-solution theory: could independently bound the
  degree of rational hypergeometric terms via linear-recurrence algorithms.
- Direct Groebner-basis classification of all degree-3 rational functions.
- Full formalization of the theorem in Lean.
- Status: not used in this run.  These are possible follow-ups but are not
  required for the obtained partial result.

## Remaining escalation for the root-0 branch

- Higher Tier 1/Tier 2 would be needed to turn the source's numerical +
  formal-uniqueness evidence into a complete non-rationality theorem for the
  minimal branch.  This remains open.
