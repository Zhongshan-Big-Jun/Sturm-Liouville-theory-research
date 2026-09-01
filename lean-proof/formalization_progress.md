# Formalization progress (scaffold register)

This file tracks Lean scaffolds for partial/structural results.  Scaffolds are
**not** formally verified; they record declarations, open obligations, and the
intended statements.

## 2026-08-16

### DensBC O1 (run R-20260816T000000Z-densbc-o1)

- Verified cores:
  - `SL/ProjectionDensity.lean` -- Theorem 1 (projection density), machine-checked.
  - `SL/DensBCEmpty.lean` -- Lemma 6.1 (empty kept set => density fails), machine-checked.
- Scaffold:
  - `SL/DensBC_O1_Scaffold.lean` -- placeholders for Theorems 2-5 and open core O1'.
- Open: `O1'` (moment representability + membership).

### Left-definite density (run R-20260816T120000Z-leftdef-density)

- Scaffold:
  - `SL/LeftDefDensity_Scaffold.lean` -- placeholders for L1', L1'', L2, L3, L4, L5 and open core O1'LD.
- Open: `O1'LD`; additionally the membership of `{Q_n^{(s)}}` in `D(K_c^{s/2})` for `s >= 4`.

## Rule

Scaffold files contain `-- SCAFFOLD` headers and `sorry`; they are never
reported as `FORMALLY_VERIFIED`.  They must be replaced by real proofs or
superseded before a completion label is used.

### Min-direction audit (run R-20260816T174722Z-min-direction-audit)

- Scaffold: `SL/MinDirectionAudit_Scaffold.lean` -- placeholder for accepted claims.
- Status: audit accepted with caveats; no full formalization yet.

### H^s operator-domain vs completion (run R-20260816T200000Z-hs-operator-domain)

- Scaffold: `SL/HsOperatorDomain_Scaffold.lean` -- placeholders for MO/SPD/ND, deficit lemmas.
- Status: RIGOROUS_PARTIAL_RESULT; load-bearing STRICT theorems MO/SPD/ND, Q1a(ii) open.

## 2026-08-22

### A6 root-1 rational no-go (plugin performance experiment)

- Scaffold: `SL/A6Root1RationalNoGo_Scaffold.lean` -- root-1 higher-degree
  rational product exclusion (both parities, all c>0), after independent audit
  REPAIRABLE_GAP + repair.
- Status: RIGOROUS_PARTIAL_RESULT; root-0/minimal branch remains open.
- Sources: `runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/candidate_proof.md`,
  audit `runs/plugin-perf-eval/R-20260822T000000Z-a6-audit/audit_report.md`.

## 2026-08-22 B3 round 2

- Scaffold: `SL/B3FixedN_Scaffold.lean` -- ratio extremizer structure theorem
  and 2n-root count theorem, after independent audit REPAIRABLE_GAP + repaired.
- Status: RIGOROUS_PARTIAL_RESULT; O3 closed, O1/O2 remain open.
- Sources: `runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/candidate_proof.md`,
  audit `runs/plugin-perf-eval2/R-20260822T230000Z-b3-audit/audit_report.md`.

## 2026-08-23 (plugin perf eval round 3 baseline)

### DensBC O1' banded-shift extension (run R-20260823T000000Z-o1p-baseline)

- Scaffold: `SL/DensBCO1p3BandShift.lean` -- placeholders for the stable
  banded-shift moment-map invertibility lemma, the finite-rank criterion
  `closure(span Q_sp)=V <=> ker(T|B_fin)={0}`, and the bandwidth-2
  `v_1=x^4` non-density example.
- Status: RIGOROUS_PARTIAL_RESULT; general O1' remains open.
- Sources: `runs/plugin-perf-eval3/R-20260823T000000Z-o1p-baseline/candidate_proof.md`.

## 2026-08-23 (plugin perf eval round 3 light-reuse)

### DensBC O1' weighted-shift extension (run R-20260823T000000Z-o1p-lightreuse)

- Scaffold: `SL/DensBCO1p3WeightedShift_Scaffold.lean` -- placeholders for the
  H_{beta,lambda} density criterion and the beta>3/2 infinite-run realizability
  threshold.
- Status: RIGOROUS_PARTIAL_RESULT after independent audit REPAIRABLE_GAP repair;
  general O1' remains open.
- Sources: `runs/plugin-perf-eval3/R-20260823T000000Z-o1p-lightreuse/candidate_proof.md`,
  audit `runs/plugin-perf-eval3/R-20260823T010000Z-o1p-audit/audit_report.md`.

## 2026-08-23 (O1'LD left-definite density)

- Scaffold: `SL/O1pLD_L2_Scaffold.lean` -- L^2-descent structural results:
  finite-support moment rigidity, Cauchy-Schwarz bound, parity decomposition,
  mu_4 non-density (STRICT subset); tail rigidity / cofinite-N theorem /
  proper-V corollary / H^1 infinite-run marked NOT-YET-STRICT or EVIDENCE.
- Status: RIGOROUS_PARTIAL_RESULT; general O1'LD remains open.
- Sources: `runs/rigorous-open-math-research/R-20260823T030000Z-leftdef-o1pld/candidate_proof.md`,
  audits `.../R-20260823T040000Z-leftdef-o1pld-audit` and
  `.../R-20260823T050000Z-leftdef-o1pld-reaudit`.

## 2026-08-23 (B3 current performance benchmark)

- Scaffold: `SL/B3GeneralAlternatingChebyshev_Scaffold.lean` -- general
  equal-within-type alternating Chebyshev secular representation, fixed-delta
  root-location lemma, amplitude-equality corollary (STRICT subset).
- Status: RIGOROUS_PARTIAL_RESULT after independent audit + repair + re-audit
  PASS; O1/O2 remain open.
- Sources: `runs/plugin-perf-eval4/R-20260823T060000Z-b3-current/candidate_proof.md`,
  audits `R-20260823T070000Z-b3-current-audit`,
  `R-20260823T080000Z-b3-current-reaudit`.

## 2026-08-30 (v1.9 live recovery G1 prime sector run)

- Scaffold: `SL/KpOddFirstZero_Scaffold.lean` -- finite-dimensional
  semiseparable first-zero algebra, positive-off-diagonal double-zero exclusion,
  and the exact same-sign-kernel open obligation.
- Status: RIGOROUS_PARTIAL_RESULT after independent audit PASS; `KP-DET`,
  simultaneous odd/even singularity, and `KO-DET` remain open.
- Source: `runs/plugin-benchmark-20260830-v19-live-recovery-g1p/workspace/runs/rigorous-open-math-research/R-20260830T020000Z-g1p-live-recovery/candidate_proof.md`.

## 2026-09-01 (KP-DET common-beta sign run)

- Scaffold: `SL/KpDetCommonBeta_Scaffold.lean`.
- Machine-checked algebraic cores: positive-weight mass balance forces the
  middle coefficient negative under the audited phase implications; the exact
  `G` factorization gives `G>0` from `q<E`; the accepted `Xi` split then gives
  `Xi>0`.
- Informal audited boundary: branch-safe common-`beta` reconstruction and the
  strict chamber `c alpha<=pi/2`, including every complete tuple with
  `0<c<=1/2`.
- Status: Tier 0 algebraic core only. The transcendental reconstruction and
  statement fidelity to the complete Sturm-Liouville system are not formally
  encoded, so this is not `FORMALLY_VERIFIED`. Direct single-file compilation
  with Lean 4.31.0 exits 0 and the scaffold contains no `sorry` or `admit`.
- Source: `research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/route-08-common-beta-orientation/accepted_package.md`.
