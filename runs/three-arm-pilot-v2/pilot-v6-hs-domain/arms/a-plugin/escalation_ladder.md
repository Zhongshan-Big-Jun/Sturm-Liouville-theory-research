# Escalation ladder

- **Run ID:** `arm-a-2026-08-28`
- **Task packet:** `arm-a-frozen-v1`
- **Current tier:** 1 (proof construction); Tier 3 reserved for the required
  independent package audit.

## Attempts

- Tier 0: exact probes \(1,x,x^2\) for the Krein form; result: affine equality
  kernel confirmed and non-affine strictness symbolically checked.
- Tier 1: spectral power recursion; result: exact finite boundary criterion for
  every polynomial and both parities of \(s\).
- Tier 1: even L2-orthogonality route; result: equality in \(K_c\ge cI\) forces
  the affine kernel.
- Tier 1: odd form-orthogonality route; result: equality in \(a_c\ge c\|\cdot\|^2\)
  forces the affine kernel.
- Tier 1: completion-map comparison; result: canonical non-equality separated
  from unitary equivalence.

## Escalations

- Tier 1 to Tier 3 is justified only for O7: the user requires an independent
  proof audit before any completion claim.  No research fan-out is needed because
  the parity routes closed their named gates directly.

## Avoid list

- No broad mechanism fan-out: all mathematical obligations reduced to closed
  direct calculations.
- No numerical search as a substitute for the uniform affine-kernel argument.
