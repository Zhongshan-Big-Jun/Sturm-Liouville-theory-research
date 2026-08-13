# Run addendum: global eps-alternation, Green inertia, and the false parity claim (2026-08-13, R-205)

Continuation of R-20260812T090000Z-g1prime-g2.  All numerics EVIDENCE unless
flagged STRICT.  This addendum corrects a claim from the handoff that led to
the 2026-08-13 symmetry-chain plan, and records the correct global lemma plus
the Green-function reduction of (G1').

## REFUTED (EVIDENCE): eigenfunction parity is NOT global for palindromic
heights

The handoff proposed a "symmetry direct proof chain" whose first step was:

  (P1) palindromic pattern (alternating heights, sigma_i = sigma_{2n+2-i})
       => every eigenfunction has definite parity
       u_k(1-x) = (-1)^{k-1} u_k(x), "globally, independent of symmetry".

This is FALSE.  The parity u_k(1-x) = (-1)^{k-1} u_k(x) is a consequence of
the ODE being reflection invariant, which requires rho(1-x) = rho(x) as a
function of x.  The alternating height PATTERN only makes the sequence of
heights palindromic; the density rho(1-x) = rho(x) additionally requires the
WIDTHS to be palindromic (w_i = w_{2n+2-i}).  For asymmetric widths the two
are different functions of x.

Numerical refutation (scripts/_gapn2_parity_global_probe.py, inline in this
session): for random Dirichlet widths (Dirichlet distribution) with
palindromic heights, n = 2..4, R in {2,4,7}, both modes, k = 1..n+2, the
relative error max |u_k(1-x) - (-1)^{k-1} u_k(x)| / (1 + max|u_k|) is O(1)
(worst observed 1.072e+00), not O(1e-16).  The same random test gives
max |f(1-x) - f(x)| / (1+max|f|) = O(1) (worst 1.290e+00).  On the SYMMETRIC
branch the same identities hold to 1e-16 (scripts/_gapn2_symmetry_chain_audit.py).

Consequence: the mirror-sector decomposition, the bracket identities, and the
Green-kernel closed forms of H_e/H_o are currently established ONLY at
symmetric band-consistent points.  They cannot be used to prove symmetry of
all band-consistent solutions (circularity).  The symmetry conclusion in the
degree framework still follows only from (G1') + (G2) via uniqueness, not from
a parity shortcut.  The docstrings of _gapn2_bracket_identity_audit.py are
corrected accordingly.

## STRICT: global eps-alternation lemma (no symmetry needed)

Let rho > 0 be piecewise continuous on (0,1) (any shape), u_n, u_{n+1} the
normalized Dirichlet eigenfunctions for lambda_n < lambda_{n+1}, and
f = lambda_n u_n^2 - lambda_{n+1} u_{n+1}^2.  At every simple zero x_j of f
in (0,1) (ordered x_1 < ... < x_m) the ratio u_{n+1}(x_j)/u_n(x_j) = eps_j c
with c = sqrt(lambda_n/lambda_{n+1}) and eps_j in {+1,-1}.  Then

    eps_j = (-1)^{j+1}    for all j.

Proof.  This is an immediate corollary of the cell analysis used for the
exact zero count (Theorem D).  Let w_1 < ... < w_{n-1} be the interior zeros
of u_n (cells C_i = (w_{i-1}, w_i), w_0 = 0, w_n = 1) and z_i the unique zero
of u_{n+1} in C_i.  The Wronskian W = u_n u_{n+1}' - u_{n+1} u_n' satisfies
W < 0 on (0,1), so Q := u_{n+1}/u_n has Q' = W/u_n^2 < 0 on each cell.  Hence
Q is strictly decreasing on C_i; Q(z_i) = 0, and since u_n -> 0 at the cell
endpoints with u_{n+1} != 0 there, Q -> +inf at w_{i-1}+ and Q -> -inf at
w_i-.  Therefore |Q| = c has exactly two solutions in C_i: the left one has
Q = +c (eps = +1), the right one Q = -c (eps = -1).  Ordering the cells
left to right gives the alternation eps_j = (-1)^{j+1}.  QED.

Remark.  This lemma is the correct global input where the handoff's (P1) was
used: it holds for arbitrary widths and is the reason the closed forms
(C1)/(C2) of the off-diagonal of K (which only use eps, not parity) are valid
at every band-consistent point.  It does NOT imply width symmetry.

Numerical check (inline session script): n = 2, 3, R in {2, 4}, both modes,
10 random asymmetric width draws, zeros of f located by sign change on a
40001-point grid: eps pattern equals [1,-1,1,-1,...] in every case
(#zeros = 2n for all draws; the draws happened to satisfy q0 > c, q1 < -c).

## STRICT (classical, cited): Green inertia of the half problems

On the SYMMETRIC branch, split the full Dirichlet problem on [0,1] at x = 1/2.
Even eigenfunctions (u'(1/2) = 0) restrict to the Neumann half problem on
[0,1/2]; odd eigenfunctions (u(1/2) = 0) restrict to the Dirichlet half
problem.  The full spectrum interleaves as (verified n = 2, 3, both modes):

    n = 2m   even:  lambda_n = mu_m^D,        lambda_{n+1} = mu_{m+1}^N,
    n = 2m-1 odd :  lambda_n = mu_m^N,        lambda_{n+1} = mu_m^D,

where mu_k^N / mu_k^D are the k-th Neumann / Dirichlet half eigenvalues
(mu_k^N < mu_k^D < mu_{k+1}^N).  Define the odd-sector reduced resolvents on
the n left-half switches x_1 < ... < x_n < 1/2:

    R_n^bot   = sum_{l : par(l) != par(n)}     u_l u_l/(lambda_l - lambda_n),
    R_{n+1}^bot = sum_{l : par(l) != par(n+1)} u_l u_l/(lambda_l - lambda_{n+1}).

By the classical oscillation theorem for Green matrices (Gantmacher-Krein;
the negative index of the resolvent restricted to ordered points equals the
number of same-parity-class half eigenvalues strictly below the spectral
parameter):

    n even: neg R_n^bot = neg R_{n+1}^bot = n/2;
    n odd : neg R_n^bot = (n-1)/2, neg R_{n+1}^bot = (n+1)/2.

Numerically confirmed at n = 2, 3, R = 4, both modes (n=2: 1 negative each;
n=3: R_n^bot 1 negative, R_{n+1}^bot 2 negative).

## Reduction of (G1') to a Green-combination quadratic form

At a symmetric band-consistent point the bracket identities (verified 1e-15,
scripts/_gapn2_bracket_identity_audit.py) together with the exact E_o
cancellation give, for the odd sector,

    K_o = diag(d) + (4 lambda_n / lambda_{n+1}) diag(u) M diag(u),
    M = lambda_{n+1} diag(eps) R_{n+1}^bot diag(eps) - lambda_n R_n^bot,
    d_j = sigma * 2 c |W(x_j)| / (R-1),  sigma = +1 SUP / -1 INF,

with u = (u_n(x_j))_{j<=n} (nonzero at the switches) and eps_j = (-1)^{j+1}.
Since diag(u) is a congruence, (G1') on the odd sector is exactly the
definiteness of diag(d/u^2) + (4 lambda_n/lambda_{n+1}) M.  The reconstruction
is verified to rel 1e-13..1e-16 at n = 2, 3, R = 4, both modes
(scripts/_gapn2_green_inertia_probe.py).  Numerically M has mixed inertia
(n=2: 1+/1-; n=3: 1+/2-), while K_o is positive definite for SUP and negative
definite for INF; the non-uniform diagonal d supplies the missing
definiteness.  This is the precise remaining obstacle: a comparison between
diag(d) and the Green combination M, whose two resolvent blocks carry the
negative directions counted by the Green inertia lemma (n/2 each for n even;
(n-1)/2 and (n+1)/2 for n odd).

## Negative result (EVIDENCE): D_n is not globally concave/convex

As a function of the bang-bang widths (full 2n+1 coordinates projected off
the sum constraint), the Hessian of D_n = lambda_{n+1} - lambda_n at random
points has mixed-sign eigenvalues for n = 2, 3, R = 4, both modes (e.g.
n=2 sup: eigenvalues span [-608, +390], [-3183, +5400], [-649, +5314]).
There is no global convexity shortcut to (G1'): the local concavity (SUP) /
convexity (INF) is a critical-point phenomenon, not a global one.

## Honest register

- (G1') remains OPEN.  New STRICT input this session: the global
  eps-alternation lemma, the half-problem spectral interleaving, and the
  classical Green inertia lemma (floor(n/2) negative directions); plus the
  precise reduction of K_o to diag(d) + a Green combination.
- The handoff's claimed global parity (P1) is REFUTED; the proposed direct
  symmetry proof is invalid (its premise fails), and the symmetry of all
  band-consistent solutions is NOT established independently of the degree
  argument.  The sector closed forms are scoped to symmetric points.
- D_n is not globally concave/convex; no shortcut there.

## Scripts

- scripts/_gapn2_parity_global_probe.py (random asymmetric-width parity /
  f-evenness refutation; to be committed with this addendum).
- scripts/_gapn2_green_inertia_probe.py (half-problem Green inertia and the
  K_o Green-combination reduction; to be committed with this addendum).
- scripts/_gapn2_bracket_identity_audit.py (docstring corrected: the bracket
  identities are scoped to symmetric band-consistent points).
