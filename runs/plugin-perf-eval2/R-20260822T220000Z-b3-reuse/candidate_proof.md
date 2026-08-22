# Candidate proof / new partial results

Status label: RIGOROUS_PARTIAL_RESULT

This file contains two self-contained STRICT results obtained in this run.
They do not close the whole B3 conjecture; the remaining gaps are listed at
the end.

---

## R1 (STRICT): exactly 2n roots for the alternating secular polynomial

### Setup

Let s = sqrt(R) > 1. Consider the balanced alternating configuration

    ρ = [1, R, 1, R, ..., 1]     (2n+1 blocks),

with each low block (density 1) of length s t and each high block (density R)
of length t, where

    t = 1/((n+1) s + n).

For an eigenvalue λ = ω^2, define the balanced phase

    y = ω s t.

The transfer matrix of the full string is

    M_n(y) = T_1(y) T_cell(y)^n,

where T_cell(y) = T_R(y) T_1(y) and

    T_c(y) = [[cos y, sin y/(ω sqrt(c))],
              [-ω sqrt(c) sin y, cos y]].

The Dirichlet secular function is F_n(y) = (M_n(y))_{01}. Zeros of F_n in
(0,π) determine the relevant eigenvalues. Since ω > 0, multiplying by ω does
not change the zeros.

### Reduction to a one-dimensional phase equation

Write C = cos y. A direct matrix computation (already represented in
scripts/op02_secular_sym.py) gives

    T_cell(y) = [[A_cell, B_cell], [C_cell, D_cell]]

with

    trace T_cell = τ(C) = ((s+1)^2 C^2 - (s^2+1))/s,
    det T_cell = 1.

Let p(C) = τ(C)/2. Define

    A(C) = ((s+1)^2 C^2 - s^2)/s.

Using the Chebyshev representation for a 2x2 symplectic matrix, for every n ≥ 1,

    ω F_n(y) = sin y [ A(C) U_{n-1}(p(C)) - U_{n-2}(p(C)) ],   (1)

where U_k are Chebyshev polynomials of the second kind (U_{-1}=0).

For C ∈ [-1,1],

    p(C) ≤ 1  always,
    p(C) ≥ -1  iff  |C| ≥ c0 := (s-1)/(s+1).

### Elliptic zone |C| ≥ c0

In this zone set p(C) = cos φ, φ ∈ [0,π]. Then

    U_{n-1}(cos φ) = sin(n φ)/sin φ,
    U_{n-2}(cos φ) = sin((n-1) φ)/sin φ.

Substituting A(C) = 2 cos φ + 1/s into (1) and using

    2 cos φ sin(nφ) = sin((n+1)φ) + sin((n-1)φ),

we obtain

    ω F_n(y) = (sin y / sin φ) [ sin((n+1)φ) + (1/s) sin(nφ) ].  (2)

Because sin y > 0 and sin φ > 0 for y,φ in (0,π), the roots of F_n in the
elliptic zone, away from the boundary φ=0,π, are exactly the roots φ∈(0,π) of

    E_n(φ) := sin((n+1)φ) + a sin(nφ),   a := 1/s ∈ (0,1).   (3)

**Phase lemma.** For every n ≥ 1 and a ∈ (0,1), E_n has exactly n simple
zeros in (0,π).

Proof. Write

    e^{iφ} + a = r(φ) e^{i θ(φ)},

with r(φ) = sqrt(1+a^2+2a cos φ) > 0 and θ chosen continuously from
θ(0)=0 to θ(π)=π. Then

    E_n(φ) = Im( e^{i nφ} (e^{iφ} + a) ) = r(φ) sin(nφ + θ(φ)).

Moreover

    θ'(φ) = (1 + a cos φ)/(1+a^2+2a cos φ) > 0,

because 1+a cos φ ≥ 1-a > 0 and the denominator is positive. Therefore

    ψ(φ) := nφ + θ(φ)

is strictly increasing, with ψ(0)=0 and ψ(π)=nπ+π=(n+1)π. Hence ψ crosses
exactly the levels π, 2π, ..., nπ once each in (0,π), and no other level.
These crossings are precisely the zeros of E_n in (0,π). The derivative
E_n'(φ) = r cosψ ψ' + r' sinψ is nonzero at a crossing because ψ'>0 and r>0;
hence each zero is simple. ∎

### Hyperbolic zone |C| < c0

For |C| < c0 we have p(C) < -1. Write p(C) = -cosh μ with μ > 0. Then

    U_{n-1}(p) = (-1)^{n-1} sinh(nμ)/sinh μ,
    U_{n-2}(p) = (-1)^{n-2} sinh((n-1)μ)/sinh μ.

If F_n(y)=0, after selecting the bracket in (1) we would need

    A(C) sinh(nμ) = sinh((n-1)μ).

But A(C) = -2 cosh μ + 1/s. By the identity

    2 cosh μ sinh(nμ) = sinh((n+1)μ) + sinh((n-1)μ),

this equation is equivalent to

    sinh((n+1)μ) = (1/s) sinh(nμ).

This is impossible because (n+1)μ > nμ > 0 and sinh is strictly increasing,
so sinh((n+1)μ) > sinh(nμ) > (1/s) sinh(nμ). Hence F_n has no zeros in the
open hyperbolic zone.

The boundary `|C| = c0` corresponds to `φ = pi`, and the boundary `|C| = 1`
corresponds to `φ = 0` / `y = 0,pi`, outside `(0,pi)`. At `φ = pi`, the
bracket in the elliptic equation has the limit

    lim_{φ→pi} [ sin((n+1)φ) + (1/s) sin(nφ) ] / sin φ
      = (-1)^{n+1} [ (n+1) - n/s ] != 0,

because `s > 1` implies `n+1 > n/s`. Hence `φ = pi` is not a root of
`F_n` either, and the boundary is harmless.

### Counting

For every k=1,...,n, the phase lemma gives one φ_k ∈ (0,π). The map from
φ ∈ (0,π) to C in the elliptic zone is two-to-one:

    C = ± sqrt( (2s cos φ + s^2+1)/(s+1)^2 ),

the plus branch giving one y in (0,π/2) side near 0 and the minus branch the
reflected y. Thus each φ_k yields exactly two roots y in (0,π). The nested
roots are all in the two elliptic side intervals, and no root exists in the
hyperbolic middle. Therefore F_n has exactly

    2n

roots in (0,π), all simple. This closes obligation 3. ∎

---

## R2 (STRICT): every global ratio maximizer is a 2n-switch alternating [1,R,1,...,1]

### Existence

Existence of a maximizer follows from the known weak-* compactness of
K_R and continuity of each fixed λ_k under weak-* convergence (these are
proven in the project's finite-reduction documents; see
docs/SL_gap_nge2_finite_reduction_proof.tex). The ratio λ_{n+1}/λ_n is
positive and continuous, so its supremum is attained.

### First variation and saturation

Normalize eigenfunctions by

    ∫_0^1 ρ u_k^2 dx = 1,    u_k'(0) > 0,   k = n,n+1.

For a bounded direction h, Feynman-Hellmann gives

    λ_k'(ρ)[h] = -λ_k ∫_0^1 h u_k^2 dx.

Hence for r = λ_{n+1}/λ_n,

    r'(ρ)[h] = r ∫_0^1 h (u_n^2 - u_{n+1}^2) dx.

Define the ratio switch function

    G(x) := u_n(x)^2 - u_{n+1}(x)^2.

At a global maximizer, the usual one-sided box variation (same argument as in
the gap finite-reduction proof) gives the saturation law

    ρ = R  a.e. on {G > 0},    ρ = 1  a.e. on {G < 0}.   (4)

### Zero structure

Let W = u_{n+1}' u_n - u_{n+1} u_n'. The project's strict Wronskian lemma gives

    W(x) < 0 for 0 < x < 1.

On each nodal interval of u_n, set Q = u_{n+1}/u_n. Then

    Q' = W/u_n^2 < 0.

Since G = u_n^2(1 - Q^2), the zeros of G in (0,1) are exactly the crossings
Q = ±1. Because Q is strictly decreasing on each of the n nodal intervals,
there are at most two such crossings per interval, so

    #Z(G;(0,1)) ≤ 2n.

Moreover, at a crossing Q' ≠ 0 and u_n ≠ 0, so each zero is simple and changes
the sign of G.

### Ratio block-energy invariant

Define

    K(x) := (u_n'(x)^2/λ_n + ρ(x) u_n(x)^2)
          - (u_{n+1}'(x)^2/λ_{n+1} + ρ(x) u_{n+1}(x)^2).

On every constant-density block, K is constant, because

    d/dx (u_k'^2/λ_k + ρ u_k^2) = 2 u_k' u_k''/λ_k + 2ρ u_k u_k'
                                = 2ρ u_k u_k'(-1+1) = 0.

At a switch point s where ρ jumps from r_- to r_+, the continuity of u_k,u_k'
gives

    K(s_+) - K(s_-) = (r_+ - r_-) G(s).

By (4) and the finite-zero structure, every switch of a maximizer is exactly a
zero of G, and every zero of G is a switch. Hence this jump is always zero, so
K is globally constant.

Integrating K over (0,1), using the normalization and

    ∫_0^1 u_k'^2 dx = λ_k ∫_0^1 ρ u_k^2 dx = λ_k,

we get

    K ≡ ∫_0^1 K dx = (1+1) - (1+1) = 0.   (5)

### Endpoint rigidity and exact count

At x=0, Dirichlet boundary conditions give u_k(0)=0, so (5) evaluated at 0
yields

    u_n'(0)^2/λ_n = u_{n+1}'(0)^2/λ_{n+1}.

With the orientation u_k'(0)>0,

    q_0 := u_{n+1}'(0)/u_n'(0) = sqrt(λ_{n+1}/λ_n) > 1.   (6)

At x=1, similarly

    q_1 := u_{n+1}'(1)/u_n'(1) = -sqrt(λ_{n+1}/λ_n) < -1.  (7)

For the switch function G with threshold ±1, the exact zero count on the
intervals (first, middle, last) is

    #Z(G;(0,1)) = 2n - 2 + 1_{q_0 > 1} + 1_{q_1 < -1}.

By (6), (7), both indicators are 1, so

    #Z(G;(0,1)) = 2n.   (8)

### Conclusion

Every global maximizer of λ_{n+1}/λ_n is bang-bang, has exactly 2n effective
switches, and because G(0+)<0, G(1-)<0 with an even number of simple zeros,
the signs of G alternate and start/end negative. By the saturation law (4),
the materials start and end at 1 and alternate. Hence the maximizer is an
alternating configuration

    ρ = [1, R, 1, R, ..., 1]        (2n+1 blocks, alternating).

This is the structural half of obligation 1. It does not yet prove that the
widths are equal or that the balanced width ratio sqrt(R) is optimal inside
this family. Those are the remaining gaps listed below. ∎

---

## Remaining obligations

1. Among all alternating [1,R,1,...,1] bang-bang configurations (2n+1 blocks
   with positive widths), prove that the ratio λ_{n+1}/λ_n is maximized at the
   configuration with all same-material widths equal and w_1/w_2 = sqrt(R).
2. Prove the monotonicity/uniqueness of the ratio inside the one-parameter
   alternating family when the same-material widths are equal.
3. Optional: verify/turn the topological-degree framework for the ratio
   self-consistency system into a proof of uniqueness/symmetry/equal widths.

## Status

R1 and R2 are STRICT partial results. The overall problem remains
RIGOROUS_PARTIAL_RESULT; the complete B3 conjecture is still open.
