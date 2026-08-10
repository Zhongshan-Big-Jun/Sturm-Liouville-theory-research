# Problem contract

Run: R-20260806T050000Z-keylemma2-5A35E5
Task packet: agenda/task-packets/Q-20260806-keylemma2-5A35E5.md
Authoritative sources (rechecked in this run):
- runs/rigorous-open-math-research/R-20260806T011500Z-keylemma-E58FB1/candidate_proof.md
  (Sections 0, 2, 5, 6, 7) and audit_report.md (gap list G1-G4).
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/
  agentA_O2_single_crossing.md (Sections 2.1-2.9 origin of G, H, F~).

Status of this contract: independent normalization and audit; matches the parent
run's statements modulo findings recorded below.  No verified theorem contract
existed; the packet is treated as untrusted project context.

## Objects and definitions

q > 1, c in (0, 1/2).

alpha_1(c) in (0, pi/2): unique root of E(alpha) = c alpha,
  E(alpha) := arctan(1/(q tan alpha)).
alpha_2(c) in (0, pi): unique root of O(alpha) = c alpha,
  O(alpha) := pi - arctan(q tan alpha) on (0, pi/2), O(pi/2) := pi/2,
  O(alpha) := arctan(-q tan alpha) on (pi/2, pi).
Both E, O strictly decreasing with slope -q/Phi(alpha).

Phi(alpha) := cos^2 alpha + q^2 sin^2 alpha.
W(alpha) := 3 + 2 alpha cot alpha.
Mtilde(alpha;c) := alpha^2 sin^2 alpha / (q + c Phi(alpha)).
G(alpha;c) := (d/dc) log Mtilde(alpha(c);c) along either curve
  = -Phi(alpha) W(alpha)/(q + c Phi(alpha))
    + 2 c alpha Phi(alpha) (q^2 - 1) sin alpha cos alpha / (q + c Phi(alpha))^2.
G_k(c) := G(alpha_k(c);c),  Mtilde_k(c) := Mtilde(alpha_k(c);c).
H(c) := G_2(c) - G_1(c).
Ftilde(c) := Mtilde_1(c) - Mtilde_2(c);  Ftilde'(c) = Mtilde_1 G_1 - Mtilde_2 G_2.
J_k(c) := dG_k/dc (total derivative along the curve); note J = G^2 + (dG/dc)|partial
  is a tautological rewriting of dG/dc used by the parent run; the operative object is
  dG_k/dc.  H'(c) = dG_2/dc - dG_1/dc.  Ftilde''(c) = Mtilde_1 J_1 - Mtilde_2 J_2
  (= dFtilde'/dc, verified).

## Hypotheses

1. q > 1, c in (0, 1/2) for the KEY LEMMA; specific sub-domains for the four lemmas.
2. alpha_1, alpha_2 are the unique intersections defined above (corrected odd form
   q tan alpha_2 + tan(c alpha_2) = 0; the packet's product-of-tangents form is false).
3. All quantities real-analytic in (q, c) on (1, inf) x (0, 1/2).

## Target conclusion (this run)

Close the four obligations inherited from the parent run, each as a complete lemma:

R1    G_2(c;q) >= 0 for all q >= 2, c in (0, 1/2).
      Tight point (2, 1/2); exact corner value G_2(1/2; 2) = 0.0691814447546...
R2    G_2(c;q) >= 0 for all q > 1, c in (0, 0.4].
      Margin >= 0.415004, tight at (q -> 1+, 0.4).
L4box H'(c;q) = dG_2/dc - dG_1/dc < 0 for all (q,c) in (1, 2] x [0.4, 0.5].
      Margin: max -7.7317 at (1.05, 0.5).
L5box Ftilde''(c;q) = Mtilde_1 J_1 - Mtilde_2 J_2 > 0 for all (q,c) in (1, 2] x [0.4, 0.5].
      Margin: min +14.167 at (2.0, 0.5).

Q1 (linchpin, priority)  dG_2/dq >= 0 on (1, inf) x (0, 1/2).
      Numerically verified; margin decays to 0 as q -> inf for fixed c.

Rationale (audited reduction, parent run): with R1 ^ R2, Region B = {G_2 < 0} is
contained in the box (1,2) x (0.4, 0.5); with L4box, H is strictly decreasing in c on
the box and B5 gives H(q, 1/2) > 0, closing the log form; with L5box, Ftilde' is
strictly increasing on the box and B4 gives Ftilde'(q, 1/2) < 0, closing the F~-prime
form.  R1 <= Q1 + B6 and R2 <= Q1 + B7, where B7 is proved (parent run) and B6
(G_2(c;2) >= 0 on (0,1/2), min at c = 1/2) is numerically verified but not yet proved.

## Quantifiers and dependency of constants

- All constants absolute (no hidden dependence on q, c).
- Endpoints included via limits; c = 1/2 corner values are exact closed forms.
- B6 is needed for the R1-via-Q1 route; if R1 is proved directly, B6 is not needed.

## Permitted outcomes

- Complete analytic proof of each of R1, R2, L4box, L5box (all four => KEY LEMMA closed);
- A strict subset with an honest remainder;
- A certified interval-arithmetic proof with an explicit, audited outward-rounding model;
- Negative result/counterexample with certificate;
- Rigorous partial result with exact gap report.

## Completion criteria

1. For each closed lemma: every step stated with hypotheses, every cited identity
   re-derived, no theorem-strength hidden lemma, computational steps certified or
   trivially checkable.
2. Final integrated statement: R1 ^ R2 ^ L4box ^ L5box ^ (parent bases B1-B5, B7)
   => (LOG) and (FP) forms of the KEY LEMMA for all q > 1, c in (0, 1/2).
3. Adversarial audit with verdict from the skill taxonomy.

## Results that do not count as completion

- Numerical verification alone (evidence only, recorded separately).
- A claim of Q1 without a proof.
- Interval arithmetic without a documented outward-rounding soundness model.
- Proving only the (LOG) form while the (FP) form consumed by T4 remains open.

## Tool, citation, and search constraints

- Python 3.10 (C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe),
  numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0, sympy 1.13.1.
- No manage-math-research-program calls inside this run.
- The KEY LEMMA is project-derived; no external theorem can be cited for it.
  Background literature (Keller 1976, Mahar-Willner 1976, AEH arXiv:2407.02459) is
  not used as a premise of these lemmas.

## Ambiguities and competing interpretations

- A1  J := G^2 + G' is a tautology for the total derivative dG/dc; the operative
      quantities H' and F~'' are dG_2/dc - dG_1/dc and Mtilde_1 (dG_1/dc) - Mtilde_2
      (dG_2/dc) respectively.  Re-derived and machine-verified in this run.
- A2  The parent run's "Hp == J2 - J1" notation hides the G^2 terms; this run uses
      explicit dG_k/dc throughout.
- A3  L4box max is at (q ~ 1.05, c = 0.5) = -7.73174 (this run re-verified at 50
      digits); the parent's max -7.7317 is confirmed.  (An earlier coarse grid in this
      run missed q = 1.05; resolved.)

## Contract audit

- Performed against the task packet and both parent artifacts.  All formulas re-derived
  from the primary definitions (secular equations) and machine-verified at 40-60 digits
  in this run (scripts verify_kl2.py, debug_dGdc*.py).
- Confirmed the parent run's identity layer E1, E2, E8 and the corner values
  G_2(1/2;2) = 0.0691814447546..., L5box min 14.167, L4box max -7.7317.
- This contract supersedes the packet where the packet defers to unverified context;
  the statements of R1, R2, L4box, L5box, Q1 are taken verbatim from the parent run's
  candidate_proof.md (Sections 5-7) after re-derivation.
