# Problem contract

Run: R-20260807T163000Z-c1center-9C4E2A
Task: continue obligation O3a/C1 (unique interior critical point of D =
lambda_2 - lambda_1 over the two-parameter barrier family), closing the last
open obligation of the n=1 gap extremal theorem.
All files ASCII punctuation, UTF-8 without BOM.

## Authoritative problem source (provenance chain)

- Portfolio problem O-2026-SL-GAP-3B7A2C; task packet
  agenda/task-packets/Q-20260806-o3a-c1b-7F3A9B.md and the C1 branch run
  R-20260806T140000Z-o3ac1-42F931 (R1-R6 reduction, CANDIDATE status
  RIGOROUS_PARTIAL_RESULT).
- The main theorem document docs/SL_gap_n1_proof.tex Section 5 (O3a/C1),
  Section 6 (main theorem synthesis), Section 7 (INF limit, closed).
- Prior C1 attack run R-20260806T200000Z-o3a-c1b-7F3A9B (multi-sheet
  structure near corners for large R; fp-component S3; H2 as stated FALSE for
  large R; E1/M-shape verified on S3; contraction route refuted).
- This run reuses the exact machinery (c1_lib.py) and the branch data.

## Objects and definitions

Barrier family: rho = 1 + (R-1) 1_{(a,b)} on (0,1), 0 < a < b < 1, R > 1,
Dirichlet at 0, 1.  s_k = sqrt(lambda_k); y_k slope-normalized
(y_k(0)=0, y_k'(0)=1); u_k = y_k/||y_k||_{L^2(rho)}; n_k = ||y_k||^2;
f = s_1^2 y_1^2/n_1 - s_2^2 y_2^2/n_2 (= lambda_1 u_1^2 - lambda_2 u_2^2);
R1 = f(a), R2 = f(b); v = y_2/y_1 strictly decreasing (Wronskian identity);
q^2 = (s_1^2/n_1)/(s_2^2/n_2); x_- < x_+ the two interior zeros of f
(v(x_-) = q, v(x_+) = -q); good root = (a,b) with R1 = R2 = 0 (equivalently
a = x_-, b = x_+).

fp-component: the connected component of {R1 = 0} through the symmetric
fixed point (a_fp(R), 1 - a_fp(R)); write it as b = g_1(a) on
I_1 = [a0, a_max1] with a0 = arccos(1/4)/pi ~ 0.41957 (band endpoint at
R = 1).  g_2(a) = 1 - g_1^{-1}(1-a) (reflection R2), h = g_1 - g_2 on
I = [a0, beta], beta = min(a_max1, b0), b0 = 1 - a0.
u(a) = g_1^{-1}(1-a): involution with fixed point a_fp.
Phi(a) = g_1'(a) * g_1'(u(a)); h'(a) = g_1'(a) - 1/g_1'(u(a))
= (Phi(a) - 1)/g_1'(u(a)).

## Target conclusion

C1 (O3a): for every R > 1 the system {R1 = 0, R2 = 0} has exactly one
solution in {0 < a < b < 1}, namely the symmetric fixed point; equivalently
h has exactly one zero on I (at a_fp).

Reduction (prior runs, audited): C1 follows from
  (E1) h(a0) < 0 < h(beta);
  (U)  Phi is unimodal on I with its maximum at a_fp (strictly increasing on
       [a0, a_fp], strictly decreasing on [a_fp, beta]);
  (P0) g_1' > 0 on I (branch slope positivity).
New claim of this run: (U) + (E1) + (P0) imply C1 by the sign argument in
the obligation graph; (U) is a cleaner sufficient condition than the raw
M-shape of h'.

## Quantifiers and dependency of constants

- All statements are for every R > 1 (no uniform-in-R constants are claimed
  unless explicitly derived; the certified-computation route will partition
  (1, inf) into R-cells).
- h, g_1, g_2, Phi are real-analytic in (a, R) on their domains (secular
  roots simple; implicit function theorem).

## Boundary and degenerate cases

- a = b: rho = 1, degenerate; excluded from the interior problem.
- R -> 1+: branches become nearly vertical; handled by a perturbation
  argument with the exact R = 1 base (band fixed at (a0, b0)).
- R -> inf: concentrated barrier; odd modes s = 2 pi k exact, even
  fundamental cot(s/2) = s mu/2; the asymptotic is handled separately.
- a_fp(R) -> a0 as R -> 1+, a_fp(R) -> 1/2 as R -> inf.

## Permitted outcomes

- affirmative proof of C1 (via E1 + U + P0 or another audited mechanism);
- a rigorous partial theorem with exact remaining gap;
- a counterexample if C1 is false (numerics strongly suggest it is true).

## Completion criteria

1. C1 proved for all R > 1, or the exact remaining gap isolated.
2. Every premise rechecked (O1c structure of f, O2 KEY LEMMA for the
   symmetric fixed point, R1-R6 reflection reduction).
3. Numerical evidence clearly separated from proofs; certified computations
   recorded as such.
4. Standard artifacts delivered under RUN_ROOT; candidate proof audited.

## Tool, citation, and search constraints

- Python 3.10 (numpy, scipy, sympy, mpmath); xelatex if a formal document is
  produced.
- Do not modify files outside RUN_ROOT except scripts/ for evidence scripts.
- Do not modify upstream run artifacts.

## Ambiguities

- The fp-component convention (revised H2): for large R the component
  through (a0, a0) is NOT the fp-component; all statements are on the
  fp-component S3.  Endpoint identities at a0 are taken as one-sided limits
  on S3.
