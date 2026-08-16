# Final Report — R-20260816T120000Z-leftdef-density

## Status label
**RIGOROUS_PARTIAL_RESULT**

(Upstream statuses, verbatim: R-20260816T000000Z-densbc-o1 = RIGOROUS_PARTIAL_RESULT;
R-20260814T070000Z-densbc-3F8A2C = RIGOROUS_PARTIAL_RESULT.)

## Upstream result status (verbatim)
- DensBC O1 (R-20260816T000000Z-densbc-o1): `RIGOROUS_PARTIAL_RESULT` (STRICT
  structure theorems produced; reduced core O1' honestly OPEN; independent audit
  REPAIRABLE_GAP repaired and re-verified).
- DensBC original (R-20260814T070000Z-densbc-3F8A2C): `RIGOROUS_PARTIAL_RESULT`.

## Exact theorem / result proved (this run; corrected scope)

For the left-definite Krein scale H^s[-1,1] (integer s >= 1, c > 0; operator-domain
reading H^s = D(K_c^{s/2})) and closed constrained V ⊆ H^s, sparse family {p_n}:

- **S1a-S1d (structural facts, exact):** for s in {1,2,3}, all p_n in H^s and
  (s=2,3) H^s ∩ C[x] = span{p_n}; **for s >= 4, the sparse p_n (n>=4) are NOT in
  H^s** (e.g. p_4 notin H^4 because K_c p_4 fails the Krein BC), so
  H^s ∩ C[x] = span{1,x}.
- **L1' (s in {1,2,3}):** V = H^s => Q_sp = {p_n} and closure(span Q_sp) = H^s
  (whole-space recovery via the sparse family); no nonzero obstruction.
- **L1'' (s >= 4):** V = H^s => Q_sp = {1,x} and closure(span Q_sp) = span{1,x}
  != H^s — the sparse family does NOT recover H^s (density fails).  Corrects the
  packet's Q3 premise for s >= 4.
- **L2/L4 (s in {1,2,3}):** structural projection density P_V(span{p_n}) dense in V;
  every closed V containing all p_n equals H^s.
- **L3:** transfer descent: the constrained-density problem in H^s is isometrically
  equivalent to the descended problem in H^{s-2} (family {K_c p_n}); iterates to
  H^{s'}, s' in {0,1}.  Clean 3-term jump base at r=1 (s=2->L^2, s=3->H^1).
- **L5 (STRICT counterexample, s=2):** V = ker(Delta) has Q_sp = even sparse
  family and q = p_5 - 2p_7 in V ∩ Q_sp^perp, q != 0, so density fails.
- **L6 (O1' status):** decided for V = H^s (s in {1,2,3} dense; s>=4 non-dense
  via L1''), and for concrete instances (L5); reduced core O1'LD OPEN for general
  proper V.  DensBC O1 Theorem 5 finiteness NOT automatic (H^1 moment matrix
  non-diagonal; H^s monomial block vacuous for s>=2).
- **First obstruction (Q2):** s in {1,2,3} whole-space: no surviving free base.
  s >= 4: degenerate (only {1,x}) — no high-degree sparse candidate.
- **NEW structural open point:** whether the SL_hs orthogonal system {Q_n^{(s)}}
  (s >= 4) lies in the operator domain D(K_c^{s/2}) — operator-domain vs abstract
  completion reading of H^s for s >= 4 — flagged open.

## Proof or construction
See candidate_proof.md (S1a-S1d, L1', L1'', L2, L3, L4, L5, L6).  All moments in
the STRICT proofs for s in {1,2,3} are taken in L^2 or H^1 (well-defined); the
unsound denseness_criteria Theorem 8 step-(i) citation is NOT used.

## Verification performed
- **Independent adversarial audit (023d145f): REPAIRABLE_GAP** — original L1 for
  s>=2 used undefined H^s-moments (unsound); L3 remark overclaimed; L6(3)
  mis-stated.  L5 airtight; S1(s=2), L2, L4, L3-core correct.
- **Re-verification (ed2a5348): FATAL_GAP on the first L1 s>=4 repair** — the
  claim "Q_n^{(s)} in span{p_n} via S1" was false because S1's equality fails for
  s>=4 (p_n notin H^s; H^4 ∩ C[x] = span{1,x}).  This led to the decisive
  structural finding S1d/L1'' and the corrected scoping to s in {1,2,3}.
- All the corrected changed points were independently re-derived with exact
  sympy arithmetic by this run (p_4 notin H^4; K_c p_4 Krein-BC failure;
  span{1,x} not dense in H^4) — EVIDENCE corroboration of the STRICT proofs.
- Exact-arithmetic scripts: reproducibility/ld_struct_facts.py (S1a-S1d/F1-F5)
  and reproducibility/ld_counterexample.py (L5).

## Remaining gaps
- **O1'LD (open):** general proper closed V ⊆ H^s (s in {1,2,3}; or surviving
  candidates for s>=4) density decision = moment/membership problem in H^{s'}.
- **NEW (open):** membership of {Q_n^{(s)}} (s>=4) in the operator domain
  D(K_c^{s/2}); reconcile operator-domain vs abstract-completion reading of H^s.
- **O2' (inherited):** constraints guaranteeing density for all c.
- **O3 (inherited):** fractional window 3/2 <= s < 2.

## Failed / blocked routes
- Route E (finite-data decidability of O1') PARTIAL/BLOCKED at O1'LD.
- The L1 s>=4 "orthogonal-system via S1" repair was REFUTED (FATAL_GAP) and
  replaced by the honest scoping (L1' for s in {1,2,3} + L1'' negative for s>=4).

## Novelty status
POTENTIALLY_NEW (web narrative sweep 2026-08-16; no external exact
constrained-density criterion surfaced).  The most novel artifacts: L1''/S1d
(sparse family not a subset of H^s for s>=4; corrects Q3 premise), and L5
(parity/boundary obstruction).  L1'/L2/L4 are refinements of project results.

## Human/model/tool contributions
- Model performed derivation, normalization, computation, and write-up;
  independent adversarial audits by fresh-context subagents (no shared chain of
  thought).  No human numerical claims; all EVIDENCE is exact arithmetic.

## Reproducibility manifest
repro_manifest.md + run-manifest.json; scripts in reproducibility/.

## Confidence by axis
- Semantic fidelity: HIGH (normalized against SL_h2/h3/hs docs + DensBC O1; the
  s>=4 sparse-family absence is a new audited correction).
- Mathematical correctness: L1'/L2/L3/L4/L5 STRICT for s in {1,2,3}; L1''/S1d
  STRICT negative for s>=4 (exact-verified).  Independent audit(s) found and the
  run fixed real issues; the corrected artifact's changed points were
  independently re-derived exactly.
- Completeness: PARTIAL (O1'LD open; s>=4 operator-domain vs completion reading open).
- Novelty: MEDIUM (POTENTIALLY_NEW; deeper literature audit recommended).
- Reproducibility: HIGH (exact-arithmetic scripts, hashed manifest).
