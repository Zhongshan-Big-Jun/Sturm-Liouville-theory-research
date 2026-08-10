# Problem contract

Run: R-20260806T070000Z-keylemma2b-0A6D8F
Task packet: agenda/task-packets/Q-20260806-keylemma2b-0A6D8F.md (resume of R-20260806T050000Z-keylemma2-5A35E5)
Authoritative sources (rechecked in this run):
- runs/rigorous-open-math-research/R-20260806T050000Z-keylemma2-5A35E5/problem_contract.md
  (normalized statements of R1, R2, L4box, L5box, Q1),
- research_ledger.md (entries 1-6: (q,u) reformulation, M2, CORNER, C4, tail bound),
- runs/rigorous-open-math-research/R-20260806T011500Z-keylemma-E58FB1/candidate_proof.md
  and audit_report.md (the four-lemma reduction and base lemmas L1, L2, B4, B5, B7),
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentA_O2_single_crossing.md
  (origin of G, H, F~, the KEY LEMMA, T1-T4).

Status: independent normalization and audit completed in this run.  All four
inherited obligations (R1, R2, L4box, L5box) are closed; the KEY LEMMA (both
(LOG) and (FP) forms) is proved for all q > 1, c in (0, 1/2).

## Objects and definitions

q > 1, c in (0, 1/2).

alpha_1(c) in (0, pi/2): unique root of E(alpha) = c alpha,
  E(alpha) := arctan(1/(q tan alpha)).
alpha_2(c) in (0, pi): unique root of O(alpha) = c alpha,
  O(alpha) := pi - arctan(q tan alpha) on (0, pi/2), O(pi/2) := pi/2,
  O(alpha) := arctan(-q tan alpha) on (pi/2, pi).
Both E and O are strictly decreasing with slope -q/Phi(alpha),
  Phi(alpha) := cos^2 alpha + q^2 sin^2 alpha > 0.
(The task packet's product-of-tangents form of the odd equation is FALSE; the
form above is the one verified against the transfer-matrix solver in the origin
run, Section 2.1.)

  W(alpha) := 3 + 2 alpha cot alpha.
  Mtilde(alpha;c) := alpha^2 sin^2 alpha / (q + c Phi(alpha)).
  G(alpha;c) := (d/dc) log Mtilde(alpha(c);c)
    = -Phi(alpha) W(alpha)/(q + c Phi(alpha))
      + 2 c alpha Phi(alpha) (q^2 - 1) sin alpha cos alpha / (q + c Phi(alpha))^2.
  G_k(c) := G(alpha_k(c);c),   Mtilde_k(c) := Mtilde(alpha_k(c);c).
  H(c) := G_2(c) - G_1(c).
  Ftilde(c) := Mtilde_1(c) - Mtilde_2(c);  Ftilde'(c) = Mtilde_1 G_1 - Mtilde_2 G_2.
  H'(c) := dG_2/dc - dG_1/dc (total derivatives along the curves).
  Ftilde''(c) := Mtilde_1 J_1 - Mtilde_2 J_2 with J_k := G_k^2 + dG_k/dc.
The identity Ftilde'' = dFtilde'/dc is exact (the G^2 terms cancel).

The (q,u) reformulation: gamma := pi - alpha_2 in (0, pi/2), u := q tan(gamma) =
tan(c alpha_2) in (0, sqrt(2q+1)), A := alpha_2 = pi - arctan(u/q), c = arctan(u)/A.

  IN(q,u) := (q^2+u^2) A (2 A q - 3 u + 2 arctan(u)) - 3 u q (1+u^2) arctan(u).
Identity (exact, machine-verified): IN = G_2 * POS with
  POS = D^2 A (q^2+u^2) u / (Phi(alpha_2) q) > 0,  D = q + c Phi(alpha_2),
so Sign(G_2) = Sign(IN).

## Hypotheses

1. q > 1, c in (0, 1/2) for the KEY LEMMA; the specific sub-domains for the lemmas.
2. alpha_1, alpha_2 are the unique intersections defined above (corrected odd form).
3. All quantities are real-analytic in (q,c) on (1, inf) x (0, 1/2).

## Target conclusion (this run)

The KEY LEMMA for all q > 1, c in (0, 1/2):

  (LOG)  (d/dc) log(Mtilde_1/Mtilde_2) = G_1 - G_2 < 0,  i.e. H = G_2 - G_1 > 0;
  (FP)   Ftilde'(c) = Mtilde_1 G_1 - Mtilde_2 G_2 < 0.

Finding C1 (parent audit, rechecked): (LOG) and (FP) are NOT logically equivalent;
each is proved separately.  (FP) is the form consumed by T4 in the origin report.

Closed by the four lemmas (each fully proved in candidate_proof.md):

  R1    G_2 >= 0 for all q >= 2, c in (0, 1/2).
        Tight point (2, 1/2); exact corner value G_2(1/2;2) = 0.0691814447546...
  R2    G_2 >= 0 for all q > 1, c in (0, 0.4].
        Exact corner value G_2(0.4;1) = 0.4136087142309...
  L4box H' = dG_2/dc - dG_1/dc < 0 for all (q,c) in (1,2] x [0.4,0.5].
        Certified worst upper bound -4.656924..., independent -4.841604...
  L5box Ftilde'' = Mtilde_1 J_1 - Mtilde_2 J_2 > 0 for all (q,c) in (1,2] x [0.4,0.5].
        Certified worst lower bound +6.242855..., independent +8.379383...

## Quantifiers and dependency of constants

- All constants absolute (no hidden dependence on q, c).
- Endpoints handled by closed-box certificates (supersets of the required open
  boxes) and by one-sided limits where needed (c -> 1/2 corners are exact closed
  forms, verified symbolically).

## Completion criteria

1. Every closed lemma: hypotheses stated, every identity re-derived, no
   theorem-strength hidden lemma, computational steps certified or trivially
   checkable.  (Met: M2, CORNER, C4 by elementary analysis plus certified
   interval legs; L4box, L5box by certified outward-rounded interval arithmetic
   independently re-verified with a second from-scratch engine.)
2. Final integrated statement: R1 ^ R2 ^ L4box ^ L5box ^ (parent bases L1, L2,
   B4, B5) => (LOG) and (FP) for all q > 1, c in (0, 1/2).  (Met.)
3. Adversarial audit with verdict from the skill taxonomy.  (audit_report.md.)

## Results that do not count as completion

- Numerical verification alone (recorded separately as evidence).
- Interval arithmetic without a documented outward-rounding soundness model.
- Proving only the (LOG) form while (FP) remains open.

## Tool, citation, and search constraints

- Python 3.10 (C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe),
  mpmath 1.3.0, numpy 2.2.6, sympy 1.13.1.
- No manage-math-research-program calls inside this run.
- The KEY LEMMA is project-derived; no external theorem is used as a premise.
- Background literature (Keller 1976, Mahar-Willner 1976, AEH arXiv:2407.02459)
  is not used as a premise of these lemmas.

## Contract audit

Performed against the task packet and the parent artifacts.  All formulas were
re-derived from the primary definitions and machine-verified at 50-90 digits in
this run (scripts in reproducibility/).  Semantic fidelity was additionally
spot-checked by a fresh from-scratch audit script (audit_semantics_fresh2.py):
sign(G2) = sign(IN), u = tan(c A) identities, the CORNER closed form, the C4
curve identity IN = A*K(v), the region signs (R1, R2, Box), and H/F~' signs on
the box, all with 0 failures on random and edge samples.
