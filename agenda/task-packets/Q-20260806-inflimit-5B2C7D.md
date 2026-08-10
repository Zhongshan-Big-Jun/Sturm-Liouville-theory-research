# Research task packet

- **Task ID:** Q-20260806-inflimit-5B2C7D
- **Project ID:** MRP-20260731-BVE-SL
- **Created:** 2026-08-06T20:00:00Z
- **Task type:** solve
- **Portfolio problem ID:** O-2026-SL-GAP-3B7A2C
- **Task state:** DRAFT

## Project reason for this task

The n=1 adjacent-gap extremal project (O-2026-SL-GAP-3B7A2C) has a numerically
established asymptotic for the INF extremal of D = lambda_2 - lambda_1 over the box
class 1 <= rho <= R: for the symmetric well [R,1,R], D*R -> 24.9438661384 < 3*pi^2 as
R -> infinity (i.e., non-flat density beats the constant-density limit 3*pi^2 in the
limit). This is one of the two remaining open items (the other is O3a/C1). A rigorous
proof of this limit (convergence theorem + uniqueness of the limiting self-consistent
solution + verified value) would close the asymptotic item and provide a template for
the SUP-side limit and for n >= 2.

## Authoritative problem source

Section 5 "INF 的 R -> infinity 极限" of:
- docs/SL_gap_extremals.tex (and compiled docs/SL_gap_extremals.pdf), specifically
  the paragraphs around the equations
  mu_1 = pi^2/(4u^2),  tan(sqrt(mu_2) u) = sqrt(mu_2)(u - 1/2),
  mu_1 * 2/u = mu_2 * sin^2(a u)/I_2,  a = sqrt(mu_2),  I_2 = int_0^u sin^2(a x) dx,
  and the claimed values u = 0.32992251, mu_1 = 22.668139, mu_2 = 47.612005,
  D*R = 24.943866 < 3*pi^2 = 29.6088 (ratio 0.8425).
- scripts/op03_gap_inflimit.py (original numerics)
- scripts/verify_inflimit.py (manager re-verification, 2026-08-06; matches to 1e-9)

## Source bundle

| Item | Version | Path | Role | Verification note |
|---|---|---|---|---|
| Gap extremals doc | 2026-08-05 | docs/SL_gap_extremals.tex | INF limit statement + numerics | recheck derivation |
| Original limit script | 2026-08-05 | scripts/op03_gap_inflimit.py | original numerics | evidence only |
| Manager re-check | 2026-08-06 | scripts/verify_inflimit.py | independent re-verification | evidence only |
| Symmetric-well analysis | 2026-08-06 | docs/SL_gap_n1_proof.tex section 4 (O2) | machinery for symmetric family | context |
| Well-family extremals | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentC_*.py (agentC_inflim.py, agentC_inflim2.py) | limit scripts from prior run | evidence only |

## Related paper analyses

- Ashbaugh-Benguria 1993 (DOI 10.1006/jdeq.1993.1047), Keller 1976 (DOI 10.1137/0129024),
  Mahar-Willner 1976 (DOI 10.1002/cpa.3160290505): one-parameter ratio/gap context.
- Standard matched-asymptotics / singular-perturbation references for piecewise-constant
  weight strings are acceptable context; every theorem used must be rechecked.

## Relevant tool-library leads

- tools/transfer-matrix-secular.md (exact secular equation for piecewise-constant rho)
- tools/balanced-phase.md (phase-balancing used for the SUP-side closed forms)
- tools/sturm-oscillation.md (nodal structure of lambda_1, lambda_2)
Leads only; never automatically trusted premises.

## Known ambiguities and bibliographic risks

- The mode labeling: u denotes the OUTER (heavy, rho = R) block width; the light middle
  block has width v = 1 - 2u. The doc writes "wai kuai width u" (outer block). Getting
  u and v swapped breaks every equation; verify from first principles.
- The limiting equations are for the SCALED eigenvalues mu_k = lambda_k * R.
- In the heavy block the wavenumber is sqrt(lambda*R) = sqrt(mu) (finite in the limit);
  in the light middle block it is sqrt(lambda) = sqrt(mu/R) -> 0. This singular
  perturbation (degenerate light-block phase) is the main analytic content.
- mu_2(u) is the solution of tan(sqrt(mu)u) = -sqrt(mu)(1/2-u) with sqrt(mu) u in
  (pi/2, pi) (branch with tan < 0); other branches give other eigenvalues but mu_2 is
  this branch (verified numerically).
- The claimed "self-consistent" value u* is a root of S(u) := mu_1(u)*2/u -
  mu_2(u)*sin^2(sqrt(mu_2(u))u)/I_2(u); numerical root u* = 0.32992250812233237,
  D* = 24.94386613843235, mu_1 = 22.66813882399661, mu_2 = 47.61200496242896.
  Uniqueness of the root on (0, 1/2) is NOT proved.

## Untrusted manager-side leads (to attack or refute, NOT premises)

1. Exact 3-block symmetric well secular equation: with propagation matrices
   P(k,L) = [[cos(kL), sin(kL)/k], [-k sin(kL), cos(kL)]], M = P(sqrt(mu),u) *
   P(sqrt(mu/R),1-2u) * P(sqrt(mu),u) for the scaled eigenvalue mu (heavy wavenumber
   sqrt(mu), light wavenumber sqrt(mu/R)); eigenvalues are roots of M[0][1] = 0
   (y(1) = 0 with slope-normalized start). Verified numerically.
2. Even mode: in the limit the light-block solution is constant, so y'(u) = 0 at the
   interface, forcing cos(sqrt(mu_1)u) = 0 in the heavy block, i.e. sqrt(mu_1)u = pi/2.
3. Odd mode: matching at x = u gives tan(sqrt(mu)u) = -(sqrt(mu)/sqrt(mu/R)) *
   tan(sqrt(mu/R)(1/2-u)); taking R -> infinity with sqrt(mu/R)(1/2-u) -> 0 yields
   tan(sqrt(mu_2)u) = -sqrt(mu_2)(1/2-u). Verify the exact matching first, then take
   the limit with uniform error bounds.
4. Self-consistency (band matching f(u) = 0 at the interface, i.e. stationarity of D
   within the symmetric family): with L^2(rho)-normalized eigenfunctions,
   u_1(u)^2 = 1/(R*u + v) + O(1/R), u_2(u)^2 = sin^2(sqrt(mu_2)u)/(2*R*I_2) + O(1/R^2),
   v = 1-2u, I_2 = int_0^u sin^2(sqrt(mu_2)x)dx; f(u) = 0 gives, after multiplying by R,
   mu_1/u = mu_2 sin^2(sqrt(mu_2)u)/(2 I_2), i.e. S(u) = 0. Check the O() terms and the
   uniformity in u.
5. Endpoint behavior of the limiting curve D*R(u) = mu_2(u) - pi^2/(4u^2):
   D*R(u) -> +infinity as u -> 0+; D*R(u) -> 3*pi^2 as u -> 1/2 (mu_2 -> 4*pi^2,
   mu_1 -> pi^2). The interior minimum is at u* with S(u*) = 0. Proving uniqueness of
   the S-root and the minimum property is part of the task.
6. The strict inequality D* < 3*pi^2 may be proven either analytically or by rigorous
   interval arithmetic (verified computation) with explicit margins (D* ~ 24.943866
   vs 3*pi^2 ~ 29.608813; margin ~ 4.66). A rigorous bound is acceptable; a proof
   using only floating-point is NOT.

## User constraints and available resources

- Chinese final reporting; ASCII punctuation in all files; citations with clickable links.
- At least 8 hours of effective research time before concluding; all failed routes and
  lessons recorded in the ledger.
- Environment: Python 3.10 (numpy 2.2.6, scipy 1.15.3, sympy, mpmath 1.3.0);
  xelatex at D:\texlive\2024\bin\windows\xelatex.exe.
- Do NOT modify files outside RUN_ROOT except optionally scripts/ for reproducible
  evidence scripts. Do NOT modify upstream run artifacts.
- On success the manager integrates the proof into docs/SL_gap_n1_proof.tex (new
  section) and updates the overview doc.

## Required run location

runs/rigorous-open-math-research/R-20260806T200000Z-inflimit-5B2C7D/

## Upstream invocation

Use $rigorous-open-math-research on the concrete problem in this task packet. Treat
this packet as project context, not as a verified theorem contract. Independently
normalize and audit the exact statement, and recheck every theorem used as a premise
against its original source and exact version. Follow the upstream skill's own
problem-level workflow and reporting protocol. Write all standard artifacts under
RUN_ROOT. Return the upstream result status verbatim and the artifact locations. Do
not call manage-math-research-program from inside the solver run.

## Manager ingestion checklist

- [ ] Preserve upstream status verbatim.
- [ ] Index the run root and artifact paths/hashes.
- [ ] Do not copy or replace upstream standard artifacts.
- [ ] Update the portfolio, maps, tool candidates, budget, checkpoint, and resume entry.
- [ ] Promote reusable knowledge only from exact source or audited artifact locations.