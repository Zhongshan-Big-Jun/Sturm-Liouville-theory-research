# Approach registry - C1 (run R-20260807T163000Z-c1center-9C4E2A)

## R1 - Phi-M-shape reduction (ACTIVE, main line)
Mechanism: prove C1 via (E1) + (U') + (P0).  U' = Phi - 1 has at most two
zeros with pattern -+- (M-shape); this replaced the stronger-and-false
"Phi unimodal" formulation.  N1 is proved (candidate_proof A1).
Progress this run:
  - E1-inf PROVED (A3): elementary inequality x > u.
  - Large-q profile equations (P-)/(P+) DERIVED in full (A4): the mechanism is
    (i) ground state s1 = alpha/sqrt(q), alpha^2 = 1/(W a (1-a));
    (ii) one-sided pinning of s2 (s2 ~ pi/a right, pi/(1-a) left);
    (iii) secular relation delta = -cot(theta) + O(1/q), theta = s2 W;
    (iv) exact norms; (v) branch equation (BR).
  - fp limit system DERIVED (A5): xi* tan(2 pi xi*) = 1/(2 sqrt2 pi).
Next: Gap 1 (uniform error bounds); U'-layer single crossing.

## R2 - Center-contraction (REFUTED, prior)
dXC/da + dXC/db < 1 fails; on the diagonal dXC/dC = 1 exactly; sign
conjecture false (counterexample at R=100).  Dead.

## R3 - Banach contraction on T (REFUTED, prior)
Spectral radius exceeds 1.  Dead.

## R4 - Certified computation + asymptotic cover (PLANNED)
Partition (1, inf) x I into cells; certify E1/U'/P0 by interval arithmetic;
close R -> 1+ and R -> inf analytically.  The analytic tail is now explicit
(A3-A5); the certified bulk remains an engineering task (blocker: interval
Newton division-width; sign-based scheme designed, untuned).

## R5 - Transition-layer profile analysis (NEW, ACTIVE)
Mechanism: parametrize a = 1/2 - xi/q; the layer branch equation gives
W(xi); G = 1 - W'(xi); Phi - 1 = (1-W'(xi))(1-W'(xi_u)) - 1 with
W(xi_u) = xi + xi_u.  The + region of Phi - 1 is the layer; the crossing
(z0) moves with q ((0.5-z0)q ~ c q^0.58).  Status: formulation complete;
single-crossing proof OPEN.

## R6 - R -> 1+ perturbation (ACTIVE, REWRITTEN this session)
The earlier "limit curve sin(2 pi b) = -sin(pi a)/2, slope 1/14" base is
REFUTED (F-016; the formula had the wrong second term and the slope of a
phantom curve).  Correct structure: S3 is the sheet a = a0 + eps phi(b) +
O(eps^2), eps = R-1, b in [a0, b_top ~ 0.936], with phi(b) = -R1_1(a0; a0,b)/
f_const'(a0) from first-order perturbation theory (closed formulas in
candidate_proof A9).  Verified: phi(a0) = 0 (exact), phi' > 0 on [a0, 0.98]
(min 0.006), g_1(a0) = a0 exactly for small R, h(a0) = -0.160861 + 0.026021
eps + O(eps^2) < 0, h(beta) -> b_top* - b0 > 0, Phi-1 > 0 and G > 0 for
R <= 1000.  Proof obligations: closed-form phi' > 0 on [a0, b_top*],
b_top* > b0, explicit O(eps) bounds (Gap 1).  Status: formulation complete;
strict calculus + error bounds OPEN.
