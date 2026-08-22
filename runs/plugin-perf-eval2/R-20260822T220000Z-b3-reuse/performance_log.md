# Performance log

Run: REUSE-GATE
Run root: F:\LaTeX\BVE research\runs\plugin-perf-eval2\R-20260822T220000Z-b3-reuse
Start UTC: 2026-08-22T22:00Z
End UTC: 2026-08-22T23:30Z (approx, after final writes)

## Reuse hits and misses

### Pre-scan hits

- REUSE: tools/transfer-matrix-secular.md — transfer matrix setup.
- REUSE: tools/balanced-phase.md — balanced phase and C=cos y substitution.
- REUSE: tools/keller-variational.md + tools/bang-bang.md — variational saturation framework.
- REUSE: docs/SL_gap_nge2_finite_reduction_proof.tex + docs/SL_gap_nge2_exact_2n_switches_proof.tex — Wronskian W<0, Q monotonicity, exact zero-count, saturation.
- REUSE: tools/switch-saturation-k-invariant.md — block-energy invariant template.
- REUSE: tools/band-selfconsistency-equivariance.md — future topology/equivariance framework.
- REUSE: lean-proof/ReflectionSymmetry.lean F_reflection (VERIFIED).
- REUSE: scripts/op02_secular_sym.py / op02_poly_extract.py / op02_rootcount.py.

### Pre-scan misses (no existing item)

- REUSE_MISS: strict 2n-root-count proof (only numerical evidence).
- REUSE_MISS: ratio-specific exact-2n-switch theorem and ratio energy invariant.
- REUSE_MISS: proof of alternating-family monotonicity at w1/w2=sqrt(R).
- REUSE_MISS: ratio self-consistency root-solver script.
- REUSE_MISS: alternating-family equal-width/uniqueness proof.

### Mid-run discovery

- REUSE (discovered after independent derivation): runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/candidate_proof.md contains the same R1/R2 STRICT results (Jacobi-matrix O3 proof and ratio structure proof). This is a pre-scan miss caused by baseline run not being listed in the required context at start; recorded honestly.
- REUSE: runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/probe_alternating_family.py (O2 EVIDENCE).

## Major actions

| Time | Action | Category | Result |
|------|--------|----------|--------|
| 22:00 | Start, read problem + required docs | READ | B3 context loaded |
| 22:10 | Pre-scan tools/scripts/Lean | READ | REUSE/REUSE_MISS registry |
| 22:20 | Symbolic transfer matrix and Chebyshev analysis | DERIVATION | Derived F_n = sin y * [...]; phase equation |
| 22:30 | Phase lemma + hyperbolic exclusion | DERIVATION | STRICT R1 (2n-root count) |
| 22:40 | Ratio finite reduction + ratio energy invariant | DERIVATION | STRICT R2 (2n switches, alternating pattern) |
| 22:50 | Wrote candidate_proof.md, registry/ledger | WRITE | Run artifacts |
| 23:00 | Numeric verification script | COMPUTE | EVIDENCE R1 root counts, R2 q0/q1 |
| 23:10 | Baseline discovery via AGENTS.md update | READ | Found baseline with same results |
| 23:15 | Cross-checked baseline candidate_proof | READ | Confirmed same R1/R2; baseline also proves R1 differently |
| 23:20 | Attempted O2/O1 via self-consistency solver | COMPUTE | Found multiple ratio self-consistent solutions; balanced max not implied by self-consistency alone |
| 23:25 | Web search for fixed-n ratio supremum | SEARCH | No direct match in first pass |
| 23:30 | Final artifacts and report | WRITE | RIGOROUS_PARTIAL_RESULT |

## Reuse hit/miss counts

- Pre-scan REUSE hits: 8
- Pre-scan REUSE_MISS entries: 5
- Mid-run REUSE hits (baseline): 2
- Mid-run REUSE_MISS_EXISTING: 1 (baseline not pre-scanned)

## Resource note

Python: system python3 has numpy/sympy but no scipy; Windows Python 3.10 with scipy
available at /mnt/c/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe.
No nested subagents were spawned; long background jobs were not needed.

## What was accomplished

- Independently derived and wrote STRICT proofs for:
  1. Every global fixed-n ratio maximizer is alternating [1,R,1,...,1] with exactly 2n switches.
  2. The balanced alternating secular polynomial has exactly 2n simple roots in (0,pi).
- Cross-checked these against the baseline run; both results were already in baseline, so the reuse-gate run did not add new mathematical conclusions beyond the baseline.
- No progress was made on O2 or the equal-width/uniqueness part of O1 beyond existing evidence.
