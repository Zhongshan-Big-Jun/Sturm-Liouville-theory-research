# Escalation ladder

- **Run ID:** R-20260823T000000Z-o1p-baseline
- **Task packet ID:** plugin-perf-eval3/PROBLEM-O1P-GENERAL.md
- **Current cost tier:** 2 (systematic proof/writing; no Tier 3 parallel fan-out)

## Attempts

- 2026-08-23T00:00:00Z tier 0: read required context, prior proofs, tools,
  LEMMA_INDEX, research map.
  Result: gap identified: no bandwidth>=2 non-diagonal finite-rank criterion.
- 2026-08-23T00:00:00Z tier 0: wrote problem contract and initial status.
- 2026-08-23T00:00:00Z tier 1: constructed H_shift(m,lambda) family and
  verified m=1 regression symbolically.
  Result: `reproducibility/audit_banded_shift.py`.
- 2026-08-23T00:00:00Z tier 1: verified bandwidth-2 v_1=x^4 non-density
  numerically.
  Result: EVIDENCE only; STRICT proof written in candidate_proof.md.
- 2026-08-23T00:00:00Z tier 2: wrote full proof with regressions.
  Result: candidate_proof.md, RIGOROUS_PARTIAL_RESULT.

## Escalations

- tier 1 -> tier 2:
  trigger: m=1 regression and m=2 EVIDENCE confirmed the route; no external
  theorem needed for the family.
  evidence: candidate_proof.md, reproduction scripts.

## De-escalation / retries

- No heavy Tier 3 fan-out used. The route did not fail.
- General O1' and arbitrary banded H remain BLOCKED; if reopened, need a new
  mechanism (e.g. Toeplitz index / weighted moment-problem machinery).

## Avoid list (updated)

- Do not claim general banded O1' from H_shift alone; realizability in general
  banded H requires the moment map's range, not just bandedness.
- Do not present the numeric `delta_2` checks as a proof.
