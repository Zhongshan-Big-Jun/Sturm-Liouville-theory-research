# Audit report

`RIGOROUS_PARTIAL_RESULT`

## Package audited

- Frozen contract: `problem_contract.md`, SHA-256 `98d6ea8d4da0a5f121c36d7c0b2cc895ec81d7b30f6e9b2d079f212825f667f5`.
- Candidate: `candidate_proof.md`, SHA-256 `c76537d71604f3f5402d520423bcb045b8e203b4fc967c6fb8d1ebbf8abf043b`.
- Primary coupling module: `subagents/direct_coupling.md`, SHA-256 `70315032fdc32eb1c171089ebcb9a08eb04dc9cf7e8127cb5cace9f77feee80c`.
- Module validator: `subagents/partial_validator.md`, SHA-256 `82f3f1b8261ea9c6d75af2d01cc25c6ab758713581771eab1c361006fa797542`.
- Fresh global audit: `subagents/global_audit.md`, SHA-256 `ba55ad7ed8a2f05a458b45f9ada841aa8fe28ad92fbd3c0040a6a82bace2d82a`.

## Global verdict

`PASS` for the explicitly claimed partial theorem, with zero critical errors and zero proof gaps. This is **not** a pass for the frozen target because the constant-order upper bound `O3` remains open and is not claimed.

```json
{
  "verdict": "PASS",
  "critical_errors": [],
  "gaps": [],
  "repair_hints": "No repair is required for the claimed partial theorem. Complete O3 by proving a fixed-constant order-2^t/sqrt(t) bound for candidate equation (12), or by a materially different exact-marginal full-state coupling.",
  "covered_scope": "Contract fidelity; O1 for t>=1; forced zeros, repeated visits, and t=0; O2 with c=1/4 and exact parity for t>=1; exact base/lamp marginals; maximal conditional lamp coupling; hitting and depth identities; all conditioning interfaces; upper (2 log t+15)/sqrt(t) for t>=16; small-time scope; range-triple identity; calibrated non-completion.",
  "residual_risk": "The frozen target remains incomplete because no fixed C/sqrt(t) upper is proved. No external literature or formal proof assistant was used."
}
```

## Module correction

The validator found one local error in `subagents/range_translation.md`: displayed recurrence (13) omits steps creating a new minimum or maximum. The correct forward update sends count at `(l,u,z)` to

- `(min(l,z-1),u,z-1)`, and
- `(l,max(u,z+1),z+1)`.

The erroneous display is not used in its proofs, and the independent exact program uses the corrected update. All substantive partial claims in that module passed.

## Verification matrix

| Item | Informal independent audit | Exact computation | Formal proof assistant | Paper-level recheck |
|---|---|---|---|---|
| Fixed-path lamp kernel | PASS | small cases implicit | unavailable | PASS |
| Lower `1/(4sqrt(t))` | PASS | endpoint values checked | unavailable | PASS |
| Logarithmic upper | PASS | finite checks only | unavailable | PASS |
| Range-shape identity | PASS | through `t=100` | unavailable | PASS |
| Frozen constant upper | OPEN | conjecture probes only | unavailable | NOT COMPLETE |
