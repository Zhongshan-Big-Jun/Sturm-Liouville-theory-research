# Obligation graph: O3a branch lemmas (run R-20260806T011500Z-o3abranch-E8E56F)

Scope: obligations within and below O3a (uniqueness of the sign-consistent
critical point of the barrier family), as delegated to this run.

## Root claim
O3a: for every R > 1, the map T (equivalently the residual system R1 = R2 = 0
with sign consistency) has at most one fixed point in 0 < a < b < 1; together
with existence (O2, separate obligation) exactly one, hence symmetric by T2.

Status: OPEN (numerically supported for R in {1.02, ..., 1e6}).

## Proven theorems (audited, with proofs in candidate_proof.md)
- P1  FH formula with eigenvalue factor:
     d lambda_k/da = (R-1) lambda_k u_k(a)^2,
     d lambda_k/db = -(R-1) lambda_k u_k(b)^2.
     PROVED (standard perturbation theory; verified numerically).
- P2  T3: dR1/db = -dR2/da on 0 < a < b < 1.
     PROVED (P1 + Schwarz on D = lambda_2 - lambda_1; D is C^2 by
     real-analyticity of the secular equation and simplicity of the spectrum).
- P3  Branch-slope identities and Hessian reduction at a good root:
     A = dR1/da, B = dR2/da, C = dR2/db; Jres = [[A, -B],[B, C]];
     g1' = A/B = -D_aa/D_ab, g2' = -B/C = -D_ab/D_bb,
     h' = -D_aa/D_ab + D_ab/D_bb (at the fp);
     at the symmetric fp, A = -C, g1'*g2' = 1;
     g1' > g2' > 0 and h' > 0 at the fp follow from
     D_aa < 0, D_bb < 0, D_ab > 0, D_aa*D_bb > D_ab^2.
     PROVED (algebraic; verified numerically at R = 4 fp and elsewhere).
- P4  R = 1 base facts: v(x;R=1) = cos(pi x), q(1) = 1/4, so the limiting
     zero positions are a0 = arccos(1/4)/pi, b0 = arccos(-1/4)/pi = 1 - a0.
     PROVED (explicit eigenfunctions at rho = 1).

## Lemma statuses (objects of the task)
- Lemma A (g1' > g2' > 0 pointwise on the common range, all R):
  REFUTED rigorously for R >= R* in (1200, 1500).  Counterexample CE-1 in
  counterexample_log.md with interval-arithmetic certificate
  (reproducibility/cert_ce1.py).  (The packet's R-uniform lower bound is
  false; the pointwise statement is also false for large R.)
- Lemma B (h(a0) < 0 < h(beta)):
  OPEN.  Verified numerically for R in {1.02, ..., 1e7} (h(b0) ~ 0.38/sqrt(R),
  h(a0) -> 0- as R -> infinity).
- Lemma C (single-graph good branches; every good root in the common range):
  OPEN.  Verified numerically for the fixed-point-relevant components (h has
  exactly one zero for R <= 1e6).  Note: extra Gamma_2 sheets (R2 = 0,
  v(b) < 0, v(a) < 0) exist at R = 1500, a = 0.57364; they are not
  sign-consistent fixed points (R1 != 0), so O3a is unaffected.
- Corrected conjecture C1 (replacement for A+B, sufficient for O3a):
  for every R > 1, h has exactly one zero in the common range.  Numerically
  supported; OPEN.

## Dependency structure
O3a  = C1 (or T4 with corrected hypotheses) + Lemma C structure.
T4   = conditional: T4(a) [Lemma C], T4(b) [g1' > g2'], T4(c) [Lemma B].
      T4(b) fails for large R -> T4 not usable there; C1 is the substitute.
P1,P2 = used by P3 and by the T3 audit.
P4   = base point for the R -> 1+ asymptotics (not completed).

## Status legend
PROVED | REFUTED (numerically) | OPEN | NUMERICALLY_SUPPORTED
