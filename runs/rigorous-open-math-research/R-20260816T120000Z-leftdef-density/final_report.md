# Final Report — R-20260816T120000Z-leftdef-density

## Status label
**RIGOROUS_PARTIAL_RESULT**

(Upstream statuses, verbatim: R-20260816T000000Z-densbc-o1 = RIGOROUS_PARTIAL_RESULT;
R-20260814T070000Z-densbc-3F8A2C = RIGOROUS_PARTIAL_RESULT.)

## Upstream result status (verbatim)
- DensBC O1 (R-20260816T000000Z-densbc-o1): `RIGOROUS_PARTIAL_RESULT` (STRICT
  structure theorems produced; reduced core O1' honestly OPEN; independent audit
  found REPAIRABLE_GAP which was repaired and re-verified at changed points).
- DensBC original (R-20260814T070000Z-densbc-3F8A2C): `RIGOROUS_PARTIAL_RESULT`.

## Exact theorem / result proved (this run)
For the left-definite Krein scale H^s[-1,1] (integer s >= 1, c > 0) and closed
constrained V ⊆ H^s, with the sparse family {p_n} (index D = {0,1} ∪ {n>=4}):

- **L1 (V = H^s recovery; Q3):** Q_sp = {p_n} and closure(span Q_sp) = H^s for
  every integer s >= 1; no nonzero obstruction.
- **L2 (structural projection density):** P_V(span{p_n}) is dense in V.
- **L3 (transfer descent):** the constrained-density problem in H^s is
  isometrically equivalent, via K_c : H^t -> H^{t-2}, to the descended problem
  in H^{s-2} (family {K_c p_n}); iterating descends to H^{s'} with s' in {0,1}
  where all moments are legitimate.
- **L4:** every closed V containing all p_n equals H^s; proper V excludes some p_n.
- **L5 (STRICT counterexample):** For V = ker(Delta), Delta f = f(1)-f(-1), in
  H^2, Q_sp = {p_0} ∪ {p_{2n}: n>=2} and q = p_5 - 2 p_7 lies in
  V ∩ Q_sp^perp with q != 0, so closure(span Q_sp) != V (density fails).
- **L6 (O1' status; Q1):** for V = H^s the core is decided (dense, no
  obstruction); for general proper V the problem descends to H^{s'} (s' in {0,1})
  and remains a genuine moment/membership problem (reduced core O1'LD) unless
  the DensBC O1 Theorem 5 finiteness condition holds (not automatic since the
  Krein moment matrix is non-diagonal).
- **First obstruction (Q2):** in the whole structural space there is no surviving
  free base (s=1: M_2,M_3 killed by growth; s>=2: M_2,M_3 undefined because
  x^2,x^3 not in H^s).  For proper V it lives in H^{s'} and is exactly O1'LD.


- **O1'LD (open):** decide, for a general proper closed V ⊆ H^s, whether a free
  jump-base moment sequence is realized by a nonzero element of the descended
  constraint K_c^r V in H^{s'} (s' in {0,1}).  A genuine moment problem in general.
- **O2' (inherited):** full characterization of constraints guaranteeing density
  for all c in non-coordinate left-definite H.
- **O3 (inherited):** fractional window 3/2 <= s < 2.

## Failed / blocked routes
- No route fully refuted.  Route E (finite-data decidability) is PARTIAL/BLOCKED
  at the exact gap O1'LD: proving finite-data decidability for general proper V
  would require a materially new mechanism (the moment-matrix non-diagonality
  blocks the DensBC O1 Theorem 5 sufficiency for the class).

## Novelty status
POTENTIALLY_NEW (web narrative sweep 2026-08-16; no external exact
constrained-density criterion surfaced; not claimed open as a fact).  L1-L4 are
mostly refinements of project results; L5 (parity/boundary obstruction) and L3
(transfer descent formulation) are the most novel concrete artifacts.

## Human/model/tool contributions
- Model performed the derivation, normalization, computation scripting, and
  write-up; independent adversarial audit by a fresh-context subagent (no shared
  chain of thought).  No human numerical claims; all EVIDENCE is exact arithmetic.

## Reproducibility manifest
repro_manifest.md + run-manifest.json; scripts in reproducibility/.


