# Research ledger

## 2026-08-22T22:00Z (UTC)

- Pre-scan completed: read required docs, tools, LEMMA_INDEX, op02 scripts.
- Recorded REUSE hits/misses in approach_registry.md.

## Derivation: 2n-root count

- Noticed F_n(y) = sin y * G_n(cos y) / (positive factor).
- Cell transfer matrix T_cell has symplectic structure; trace τ = 2T(C), with
  T(C) = ((s+1)^2 C^2 - (s^2+1))/(2s), s=sqrt(R).
- In elliptic zone |T|≤1 (equivalently |C| ≥ (s-1)/(s+1)), with φ=arccos T(C),
  the secular equation simplifies to
      sin((n+1)φ) + (1/s) sin(nφ) = 0.
- Set a=1/s∈(0,1), E(φ)=sin((n+1)φ)+a sin(nφ). Write E(φ)=r(φ) sin(nφ+θ(φ)),
  where θ(φ)=Arg(e^{iφ}+a) ∈ (0,π), θ'(φ)=(1+a cosφ)/(1+a^2+2a cosφ)>0.
  Hence nφ+θ is strictly increasing from 0 to (n+1)π; E has exactly n simple
  zeros in (0,π).
- In hyperbolic zone T<-1, with μ>0 and T=-cosh μ, the secular equation would
  require sinh((n+1)μ)=(1/s)sinh(nμ), impossible because 1/s<1. So no roots there.
- The two-sided mapping y→φ is two-to-one, giving exactly 2n roots in (0,π).
- Numerically rechecked n=1..6, R∈{2,4,10,100}: all roots lie in elliptic zone.

## Derivation: ratio finite reduction and exact 2n switches

- For r=λ_{n+1}/λ_n, with L^2(ρ) normalization, FH gives
  r'[h]=r ∫ h (u_n^2 - u_{n+1}^2) dx.
- Define G=u_n^2-u_{n+1}^2. Maximizer saturation: ρ=R on {G>0}, ρ=1 on {G<0}.
- Reuse W<0 => Q'<0 on each u_n-nodal interval; hence G zeros are simple and at
  most 2n.
- Define K_ratio = (u_n'^2/λ_n + ρ u_n^2) - (u_{n+1}'^2/λ_{n+1} + ρ u_{n+1}^2).
  On constant-density blocks K_ratio is constant; at switches the jump is
  (r_+ - r_-)G(s), zero because every switch is a G zero. Therefore K_ratio is
  globally constant.
- Integration gives K_ratio = 0. At endpoints this forces
  q0 = u_{n+1}'(0)/u_n'(0) = sqrt(λ_{n+1}/λ_n) > 1 and
  q1 = u_{n+1}'(1)/u_n'(1) = -sqrt(λ_{n+1}/λ_n) < -1.
- Thus in the exact zero-count formula for G both endpoint indicators are active:
  #Z(G;(0,1)) = 2n. Every global ratio maximizer is bang-bang with exactly 2n
  switches, alternating 1,R,1,...,1 (maximizer starts/ends at 1).

## Next

- Investigate whether the ratio self-consistency system for the alternating
  pattern has a unique solution, and whether uniqueness implies equal widths +
  balanced widths. This is R3.
- Investigate the one-parameter monotonicity inside the alternating family (R4).

## Mid-run update: baseline discovery

- Read runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/candidate_proof.md
  (after AGENTS.md session-log update). Baseline contains the same two STRICT
  results; its O3 proof uses Cayley-Hamilton recurrence + Jacobi matrix, our R1
  uses an elliptic-zone phase lemma. Both are consistent.
- The baseline `probe_alternating_family.py` provides EVIDENCE for the
  one-parameter alternating-family peak at r=sqrt(R).
- Our ratio self-consistency solver found an asymmetric self-consistent
  [1,R,1,R,1] solution for n=2,R=4 with ratio ~2.5486 (lower than balanced
  4.2847), indicating multiple self-consistent configurations and that
  self-consistency + alternating pattern is not enough to force equal widths.
