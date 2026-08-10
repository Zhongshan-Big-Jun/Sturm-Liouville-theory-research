# -*- coding: utf-8 -*-
import io
p = r"runs\rigorous-open-math-research\R-20260809T000000Z-j2e1-e1ify-0C11DE\research_ledger.md"
src = io.open(p, encoding="utf-8-sig").read()
entry = r"""
## R-112 (2026-08-10): INF-side well-family small-R phase rigidity (theorem) + Sun 2022 closeout
- New theorem (STRICT, E1): for 1 < R <= 3/2, every sign-consistent good root of the
  well family rho = R on [0,a] u [b,1], 1 on (a,b), satisfies a+b = 1.
  Chain: (i) phase-range lemma (y2 unique zero z in (a,b); explicit sin(ms2 x)/(ms2)
  on the wells forces tau A, tau B < pi); (ii) transport invariant (middle density-1
  region is a rotation P(psi) preserving X^2+Y^2; hence y(b)^2/y(a)^2 = J~(B)/J~(A),
  J~ = sin^2/(sin^2 + m^2 cos^2)); (iii) residual elimination (R1=R2=0 => r_tau(A)=
  r_tau(B)); (iv) strict monotonicity of r_tau on (0, pi/tau) via Psi~' < 0 on (0,pi):
  factorization W~^2 sin^2x Psi~' = -(q+1)(2N0+qN1)/8, N0 = 4x-2sin2x > 0, reduction
  to H = 4N0+N1 > 0 (u = 2x substitution; h' = (1-cos u)(5+cos u)-u sin u(1+2cos u);
  G(u) = tan(u/2)(5+cos u)-u(1+2cos u) rationalized by t = tan(u/2) to N(t) =
  t(6+4t^2)-2(3-t^2) arctan t with N'' > 0, N'(0)=N(0)=0). Threshold q <= 1/2
  (R <= 3/2) is sharp for this mechanism (EVIDENCE: r_tau non-monotone at R=1.6,
  off-axis E=0 branch appears at R >= 1.52).
- Verification: scripts/_well_rigid_verify.py - 8 symbolic identities (A1-A8) all
  True (sympy); probes B1-B5 (q=0.5 max Psi~' ~ -6.9e-13, q=0.5001 positive;
  R=1.5 good root (0.40879841, 0.59120159), a+b=1 to 1e-10, |A-B| <= 4e-13,
  r_tau(A)=r_tau(B)=0.2189882504, y2(a)=+0.0837, y2(b)=-0.0837, zero at x=0.5;
  R=4 off-axis N1 in [-2.76,-2.61] < 0; symmetric-line N1 crosses 0 at v*).
  All EVIDENCE, registered in misc/_well_explore_log.md.
- Defective E3 scripts registered: scripts/_well_mc.py (Psi missing q term),
  misc/_well_fh.py (R1/R2 inconsistent with verified fval/FH), 
  scripts/_well_system_derive.py sec_value extra 1/m factor (exploration only).
- Literature closeout: Sun 2022 (JMAA 516:126513) full text unreachable; official
  abstract (colab.ws) + zbMATH review (Erdogan Sen, Zbl 1506.34110) confirm the class
  is "piecewise continuous with a bounded of jumps", NOT the full measurable box
  class; verdict: cannot close our box-class INF side; potential overlap requires
  full text. papers/ashbaugh1991_gaps.pdf downloaded (Schrodinger L^p gap extremals;
  related mechanism, not the same problem).
- Deliverables: docs/SL_gap_n1_well_rigidity_R32.pdf (11 pp, zero warnings;
  STRICT/EVID labels; honest gaps (a) symmetric-line 1D analysis, (b) R>3/2
  rigidity with N1 candidate route, (c) Theorem A independent re-verification
  CANDIDATE, (d) extremizer existence/good-root condition partial);
  misc/_well_explore_log.md; tools/well-family-rigidity.md + README; AGENTS.md
  session 51; state/current.json + RESUME.md updated.
- FH sign correction registered: dD/da = -(R-1) f(a), dD/db = +(R-1) f(b) with
  f = lam2*y2^2/n2 - lam1*y1^2/n1 (verified 1e-8 by misc/_well_fh2.py; f sign
  distribution at R=4 symmetric good root: f(0.2)=+4.12, f(0.5)=-2.28, f(a)=f(b)=0).
- Status: small-R INF well-family rigidity SOLVED (theorem); general R OPEN.
  Next: gap (a) symmetric-line 1D strict proof; gap (b) candidate route.
"""
src = src.rstrip() + "\n" + entry
io.open(p, "w", encoding="utf-8-sig", newline="\r\n").write(src)
print("ledger appended")
