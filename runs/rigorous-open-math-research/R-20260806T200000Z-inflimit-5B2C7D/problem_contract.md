# Problem contract

Run: R-20260806T200000Z-inflimit-5B2C7D
Task packet: agenda/task-packets/Q-20260806-inflimit-5B2C7D.md
Run type: solve (independent normalization and audit of the packet statement).
All files ASCII punctuation, UTF-8 without BOM.

## Authoritative problem source (provenance chain)

- Task packet: agenda/task-packets/Q-20260806-inflimit-5B2C7D.md (manager DRAFT
  state; explicitly labeled "project context, not a verified theorem contract").
- Primary numeric statement: docs/SL_gap_extremals.tex (2026-08-05), Section 5
  "INF 配置: R -> infinity 时 D*R -> 24.9439", subsection "极限", plus the
  equations mu_1 = pi^2/(4u^2), tan(sqrt(mu_2) u) = sqrt(mu_2)(u - 1/2),
  mu_1 * 2/u = mu_2 * sin^2(a u)/I_2 with claimed u = 0.32992251,
  mu_1 = 22.668139, mu_2 = 47.612005, D*R = 24.943866 < 3*pi^2.
- Numeric scripts (evidence only, not premises): scripts/op03_gap_inflimit.py,
  scripts/verify_inflimit.py, runs/.../R-20260805T000000Z-gapn1-a1b2c3/
  agentC_inflim.py, agentC_inflim2.py.
- Prior audited reduction (context, NOT a premise of this run): the O1 box-class
  reduction theorem (inf over the box class K = min over the two-parameter well
  family, sup = max over the barrier family), independently audited in
  R-20260806T151000Z-o1reaudit-5A1C3D (INDEPENDENTLY_AUDITED_PROOF, O1 scope).
  This run proves a limit statement for the symmetric subfamily; the equality of
  the full box-class inf with the symmetric-family inf is a separate open item
  (portfolio item O3a/C1) and is NOT part of this contract.

## Objects and definitions

- Interval I = (0,1). Dirichlet string: -y'' = lambda rho y on I, y(0) = y(1) = 0.
- R > 1. Symmetric well family: for u in (0,1/2),
  rho_{R,u}(x) = R on [0,u) union (1-u,1],  rho_{R,u}(x) = 1 on [u,1-u].
- 0 < lambda_1(R,u) < lambda_2(R,u): first two eigenvalues; D_R(u) =
  lambda_2(R,u) - lambda_1(R,u); m_R = inf_{u in (0,1/2)} D_R(u).
- Scaled eigenvalues mu_k(R,u) = R * lambda_k(R,u).
- Limiting curve: mu_1bar(u) = pi^2/(4u^2); a(u) in (pi/2, pi) the unique root
  of tan a = a(1 - 1/(2u)) for u in (0,1/2); mu_2bar(u) = (a(u)/u)^2;
  Dbar(u) = mu_2bar(u) - mu_1bar(u).
- Self-consistency function:
  S(u) = mu_1bar(u) * 2/u - mu_2bar(u) * sin^2(a(u)) / I_2(u),
  I_2(u) = int_0^u sin^2(sqrt(mu_2bar(u)) x) dx
        = (u/2) - sin(2 a(u)) * u / (4 a(u)).
- u* in (0,1/2): the (claimed unique) root of S(u) = 0 (equivalently of
  Dbar'(u) = 0).
- Claimed values (to be re-verified): u* = 0.3299225081196866,
  Dbar(u*) = 24.94386613843234, mu_1bar(u*) = 22.66813882436018,
  mu_2bar(u*) = 47.61200496279252, 3*pi^2 = 29.60881320326807.

## Hypotheses

- R > 1; u in (0,1/2). No regularity issues: rho_{R,u} is piecewise constant
  with two jump points u and 1-u.

## Target conclusion

Theorem A (symmetric-family INF limit):
  lim_{R -> infinity} R * m_R = Dbar(u*),
  where u* is the unique root of S(u) = 0 in (0,1/2), and in particular
  Dbar(u*) = 24.94386613843234... < 3*pi^2 = 29.60881320326807.

The packet decomposes the task into three components:
  (T1) convergence theorem: R * D_R(u_R) -> Dbar(u*) for the minimizers u_R
       (more precisely: lim_R R * m_R = Dbar(u*), with minimizers converging to
       u*);
  (T2) uniqueness of the limiting self-consistent solution: S(u) = 0 has exactly
       one root in (0,1/2), and it is the global minimizer of Dbar;
  (T3) verified value: Dbar(u*) < 3*pi^2 with an explicit margin, and Dbar(u*)
       enclosed in a verified interval (24.94386613, 24.94386615), say.

## Quantifiers and dependency of constants

- All constants in estimates are absolute (depend only on the indicated
  parameters, never on both R and u in a hidden way).
- The limit is as R -> infinity with u free in (0,1/2); the infimum m_R is over
  the full open interval.
- The convergence of minimizers u_R -> u* is part of the conclusion (up to
  subsequences, and with the value convergence R*m_R -> Dbar(u*)).

## Equivalent formulations that are actually proved equivalent

- S(u) = 0  <=>  Dbar'(u) = 0 (exact algebraic identity, verified symbolically;
  proved in candidate proof, Part I).
- Dbar'(u) = 0  <=>  G(a(u)) = 0 with G(a) = 8 a^3 sin^2 a - 2 pi^2 (a - sin a
  cos a), a = a(u) in (pi/2, pi).
- G(a) = 0 has a unique root a* in (pi/2, pi) with sign + then - (proved via
  the K~ -> J -> G chain, Part I).
- R * D_R(u) = mu_2(R,u) - mu_1(R,u) (definition).

## Boundary and degenerate cases

- u -> 0+: Dbar(u) -> +infinity; R * D_R(u) -> +infinity in the limiting sense
  (sliver control, Part II).  The endpoint u = 0 corresponds to rho = 1
  (constant), where D_R = 3*pi^2 and R * D_R = 3*pi^2 * R -> infinity.
- u -> 1/2-: rho -> R (constant), lambda_k -> (k pi)^2 / R, D_R -> 3*pi^2 / R,
  so R * D_R -> 3*pi^2 = 29.60881320326807 > Dbar(u*).
- R = 1: excluded (trivial string).
- The packet warns: u denotes the OUTER (heavy) block width, light middle block
  width v = 1 - 2u; swapping u and v breaks every equation.  Verified from
  first principles in this run (matching derivation in Part II gives the packet
  equations, not the swapped ones).

## Permitted outcomes

- affirmative proof of Theorem A (all three components), or
- a rigorous partial theorem with exact remaining gap (e.g. if the sliver
  control cannot be closed, the exact sublemma is reported), or
- a counterexample if the claimed limit is wrong (numerics strongly suggest it
  is right).

## Completion criteria

1. Theorem A proved with all hypotheses stated; T2 (uniqueness of u* and
   minimality) proved by hand with elementary estimates.
2. T1 (convergence) proved via exact secular equations with explicit error
   bounds (fixed-u and locally uniform convergence) plus sliver controls.
3. T3 (verified value) via rigorous interval arithmetic with explicit margins,
   and the strict inequality Dbar(u*) < 3*pi^2.
4. Every theorem used as a premise rechecked against its original source or
   proved in this run; RECALLED_UNVERIFIED material is either verified or not
   used.
5. Standard artifacts (problem_contract, repro_manifest, status_and_literature,
   obligation_graph, approach_registry, research_ledger, counterexample_log,
   candidate_proof, audit_report, reproducibility/) delivered under RUN_ROOT.
6. Chinese final reporting with ASCII punctuation in files.

## Results that do not count as completion

- Reproducing the numerics alone (evidence, not proof).
- A proof of a different statement (e.g. non-symmetric wells, or the SUP side).
- Proving the limit for fixed u only without the inf-convergence.
- Claiming closure of O3a/C1 (full box-class inf = symmetric inf) or any other
  portfolio item outside this contract.

## Tool, citation, and search constraints

- Python 3.10 (C:\Users\HuangZY\AppData\Local\Programs\Python\Python310) with
  numpy 2.2.6, scipy 1.15.3, sympy 1.13.1, mpmath 1.3.0.
- xelatex at D:\texlive\2024\bin\windows\xelatex.exe (if a LaTeX draft is
  produced under RUN_ROOT).
- Web search allowed for novelty and premise verification; every cited theorem
  rechecked.
- Do not modify files outside RUN_ROOT (evidence scripts may also be added
  under scripts/ per the packet).

## Ambiguities or competing interpretations

- The packet phrase "the INF extremal of D over the box class" must be read as
  "the INF over the symmetric well subfamily [R,1,R]": the packet's own
  "authoritative problem source" and equations describe exactly this
  subfamily, and the non-symmetric case is explicitly another open item.
- "Self-consistent solution" = root of S(u) = 0 (the limit of the scaled
  stationarity condition); equivalent to Dbar'(u) = 0 (proved in Part I).
- The branch of mu_2bar: a(u) in (pi/2, pi) (packet and doc agree); other
  branches give higher eigenvalues.
- "Verified value" = verified enclosure via interval arithmetic, not an exact
  closed form (the value is expected to be transcendental).

## Contract audit

Performed by this run against the packet and the source doc before any
research: the normalized statement matches the packet's "Authoritative problem
source" equations verbatim; the numerics reproduce (u* = 0.3299225081196866,
Dbar(u*) = 24.94386613843234); the mode labeling (u = outer heavy width) was
re-derived from first principles.  Known non-audited items: the O1 reduction
theorem is context only; the packet's untrusted manager-side leads (items 1-6)
are treated as conjectures to be proved, not premises.
