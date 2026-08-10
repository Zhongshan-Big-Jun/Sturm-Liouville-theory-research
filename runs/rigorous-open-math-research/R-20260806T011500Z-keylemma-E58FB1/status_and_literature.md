# Status and literature

Run: R-20260806T011500Z-keylemma-E58FB1

## Current status (2026-08-06)

The KEY LEMMA is REDUCED to four explicit analytic inequalities, all numerically verified
with quantified margins, none yet proved analytically:

  R1    G2 >= 0 for q >= 2, c in (0, 1/2)              [min 0.06918 at (2, 1/2)]
  R2    G2 >= 0 for q > 1, c in (0, 0.4]               [grid min 0.4150 at (1+, 0.4)]
  L4box H'(c) < 0 on (1, 2] x [0.4, 0.5]               [max = -7.73]
  L5box F~''(c) > 0 on (1, 2] x [0.4, 0.5]             [min = +14.17]

Everything else needed to close O2 is proved in this run (problem_contract.md,
candidate_proof.md): the premise chain P1-P10, the region-A argument (G1 < 0, G2 >= 0
imply both target forms), the compact box reduction, the q=1 base family (B1-B3), the
c=1/2 corner closed forms (B4, B5), and the auxiliary boundary statements (B6, B7).

Result status label (skill output protocol): RIGOROUS_PARTIAL_RESULT.

## The exact target

For all q > 1, c in (0, 1/2), with alpha1, alpha2 the unique intersections defined in
problem_contract.md:
  (log form)   (d/dc) log(M1/M2) = G1 - G2 < 0,
  (F-prime form, the one consumed by T4)   F~'(c) = M~1 G1 - M~2 G2 < 0.
The two forms are NOT logically equivalent (audit finding C1); both are true numerically
and both are reduced by the same chain.

## Novelty

The KEY LEMMA is project-derived (a step inside the n=1 adjacent-gap extremal analysis of
the Dirichlet string, program MRP-20260731-BVE-SL, portfolio problem O-2026-SL-GAP-3B7A2C).
It is not a named theorem in the literature and no external theorem states it.  The
reduction structure in this run (region split + compact box + q=1/c=1/2 exact corners +
box sign lemmas) is also project-derived.

Novelty classification: POTENTIALLY_NEW (project-derived statement and proof skeleton;
final significance depends on closing R1, R2, L4box, L5box).  The components are
elementary real analysis; a future close would be a useful lemma for the gap-extremal
program, not a major standalone result.

## Literature recheck (background premises only)

The KEY LEMMA is self-contained; the only external content is the underlying reduction
(T1-T4) from the project's agent-A report, which this run re-audited (premise chain P1-P10,
problem_contract.md C0-C4).  Background results that motivated the gap-extremal program
(Keller 1976, Mahar-Willner 1976, AEH arXiv:2407.02459) are not used as premises of the
KEY LEMMA proof.  No citation is needed for any step of the reduction; all steps are
derived and machine-verified here.  No risk of citing a nonexistent or mis-stated external
result: none is cited.

## Exact known statements this run proved

- E1-E7 (identities; verified to 50-60 digits; E7 exact via sympy):
  E1 log-derivative identity; E2 F~' identity; E3 D'(c) and f_sym formulas; E4
  normalization identity; E5 f_sym form; E6 corner alpha values; E7 H(q,1/2) closed form.
- L1: G1 < 0 for all (q,c) (analytic proof).
- L2: G2 >= 0 implies both target forms (analytic proof).
- B1: J1(1,c) >= 0 on (0,1/2)  (N1(u) > 0 on (pi/3, pi/2)).
- B2: J2(1,c) <= 0 on [0.4, 0.5] (N2(w) < 0 on [2pi/3, 5pi/7]).
- B3: H'(1,c) < 0 on (0,1/2) (T decreasing on (0, pi)).
- B4: F~'(q,1/2) < 0 for all q > 1 (exact closed form with P(x) > 0).
- B5: H(q,1/2) = 2 pi q (q+1)/(2q+1)^(3/2) > 0, increasing, min 4 pi/(3 sqrt 3) at q=1.
- B6 (auxiliary): G2(c;2) >= 0 on (0,1/2) — numerically verified, proof open
  (reduces to Q2 + exact corner value).
- B7: G2(c;1) = -W(pi/(1+c))/(1+c) > 0 for c in (0, 0.4] (analytic proof).

## Open sub-obligations (the exact remaining gap)

Closing any of R1, R2, L4box, L5box is a concrete, local, real-analytic inequality in two
variables with substantial numeric slack (except R1 near (2, 1/2), slack 0.07 in G2).
Suggested routes are registered in approach_registry.md.  Until they close, the honest
label is RIGOROUS_PARTIAL_RESULT; the run does NOT claim completion of O2.

## Related prior runs

- R-20260805T000000Z-gapn1-a1b2c3: source of the statement (agentA_O2_single_crossing.md)
  and the numerical evidence; agent A left the KEY LEMMA open as the single unproven step.
- This run: independent normalization (finding C1), premise audit, refined reduction,
  q=1/c=1/2 exact bases, and the four-lemma gap report.
