# Obligation graph - C1 (run R-20260807T163000Z-c1center-9C4E2A)

Root: C1 = {R1=0, R2=0} has exactly one solution in 0<a<b<1, for every R>1.

## O1c (structure of f) - CLOSED (prior, audited)
f has exactly two interior zeros x_- < x_+; {f > 0} is a single interval;
good roots are exactly the sign-consistent pairs (a = x_-, b = x_+).

## O2 (symmetric fixed point) - CLOSED (prior, audited)
The 1-parameter problem on the symmetric line has a unique solution
a_fp(R) in (0, 1/2); (a_fp, 1-a_fp) is a genuine critical point of D.

## R1-R6 (reflection + reduction) - CLOSED (prior, audited)
g_2(a) = 1 - g_1^{-1}(1-a); h(a) = g_1(a) - 1 + u(a); h(a) = 0 iff good
root; C1 iff h has a unique zero on I.

## N1 (reduction) - CLOSED (this run, audited)
(E1) + (U') + (P0) imply C1, where U' is the M-shape condition:
Phi - 1 has at most two zeros with pattern - + - (empty intervals allowed).
NOTE: the earlier "Phi unimodal with max at a_fp" (U) is false for large R
(Phi dips below 1 near a0) and is replaced by U'.  Proof in candidate_proof A1.

## G-E1 - PARTIAL (this run)
h(a0) < 0 < h(beta).
  - Large-q end: A2 reduces to (E1-inf); A3 PROVES (E1-inf) elementarily
    (W_R(1-a0) - W_L(a0) = 0.2474707 > 0).  Remaining: Gap 1 error bounds.
  - R -> 1+ end (REWRITTEN this run, F-016): g_1(a0) = a0 exactly for small
    R (degenerate point (a0,a0) on S3), h(a0) = u(a0) - b0 = 2a0-1 +
    phi(b0) eps + O(eps^2) = -0.160861 + 0.026021 eps + O(eps^2) < 0 (margin
    0.16); h(beta) -> b_top* - b0 > 0.  PROGRESS 2026-08-09: closed form of
    phi and factored phi' derived (DERIVATION, verified); phi' > 0 on [a0, 1)
    CERTIFIED (mpmath.iv 200-bit, 4000 cells, worst lower bound 8.896e-6) +
    STRICT (elementary tail C_tail >= 9.651926 on (0.999,1)); b_top* >= 7/10
    > b0 STRICT (implicit function theorem, margin 0.12).  REMAINING (Gap 1):
    explicit uniform O(eps) error bounds and b_top(eps) <= 1 - delta_0.

## G-U' - PARTIAL (this run)
M-shape of Phi - 1.
  - A6 reduces to U'-generic + U'-layer.
  - U'-generic: Phi - 1 = [W'(a) + W'(u(a))]/q + O(1/q^2) in the generic
    regimes; the leading term S(a) = W'_L(a) + W'_R(1-a) is < 0 (endpoint
    value -0.3843; monotonicity of the terms is part of Gap 1).  EVIDENCE:
    matches measured q(Phi-1) to ~1% where (P-) holds.
  - U'-layer: Phi - 1 > 0 on a window around the fp (EVIDENCE: Phi(fp)-1 ->
    0.99) and < 0 outside, with exactly one crossing on [a0, fp].  The crossing
    moves with q: (0.5 - z0) q ~ 4.3, 5.3, 10.5, 20.0 at q = 70.7, 100, 316,
    1000.  OPEN.

## G-P0 - PARTIAL (this run)
G > 0 on I.  Generic regimes: G = 1 + W'/q + O(1/q^2) > 0 (Gap 1).  Layer:
G = 1 - W'(xi) with measured W' in (-0.41, ~0.02).  R -> 1+: G(a0) -> 1/14.
OPEN with margin.

## G-C (fp-component) - PARTIAL (prior)
The fp-component is a graph b = g_1(a) over I; no other R1 = 0 component
carries a good root.  CAUTION: tracew_*.json rows are polluted by sheet jumps
for a > ~1/2; clean S3 data are in s33_profile.json.

## Boundary cases
- R -> inf: reduced to explicit one-variable profile equations + fp limit
  system (A4/A5); the equations and limits are derived, error bounds = Gap 1.
- R -> 1+: REDUCED (A9, rewritten; the old "limit curve sin(2 pi b) =
  -sin(pi a)/2, slope 1/14" is REFUTED, F-016).  Small-eps obligations
  (E1, U', P0) follow from phi' > 0 on [a0, b_top*] + b_top* > b0 + O(eps)
  bounds, with phi the explicit first-order sheet function (g_1(a0) = a0,
  h(a0) = 2a0-1 + phi(b0) eps + O(eps^2)).  2026-08-09: phi' > 0 on [a0, 1)
  is CERTIFIED + STRICT and b_top* >= 7/10 > b0 is STRICT; only the explicit
  O(eps) error bounds (Gap 1) remain for this end.

## Synthesis
C1 = N1 + G-E1 + G-U' + G-P0 + G-C.
Status: N1, E1-inf, and the large-q reduction are closed; the master gap is
G-EST (uniform error bounds); U'-layer and the certified bulk remain.  The
R -> 1+ strict calculus is done at the level of the sheet function: closed
form of phi, phi' > 0 on [a0, 1) (CERTIFIED + STRICT), b_top* >= 7/10 > b0
(STRICT) - only the explicit O(eps) error bounds (Gap 1) remain.  R -> 1+
formulation is rewritten and verified (F-016); see A9.
