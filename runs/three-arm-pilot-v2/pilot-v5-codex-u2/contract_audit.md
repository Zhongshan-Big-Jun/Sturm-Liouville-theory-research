# Frozen-contract audit

- Verdict: `PASS`.
- Reviewer model: `gpt-5.6-terra`, reasoning effort `high`.
- Reviewer received only `frozen_task.md` and `PLAN.md`.
- First error: none.
- Gap list: empty.

## Checks

- Definitions are complete: state space, finite-support lamps, initial states, transition
  kernel, time domain, and total-variation normalization are fixed.
- `(0,2)` is unambiguous: the all-zero lamp configuration with base at `2`.
- Both starts have even base position and therefore share the same base-parity class at every
  integer time. The task explicitly requires parity to be audited.
- The constants `c`, `C`, and `t_0` are fixed before the universal quantifier over every integer
  `t>=t_0`.
- Completion requires both bounds and explicit values of `c`, `C`, and `t_0`; numerical evidence
  is expressly insufficient.
- All three arms receive the same frozen mathematical task. Their differences are
  methodological, not mathematical.

## Binding instruction

Preserve `frozen_task.md` byte-for-byte for every arm.
