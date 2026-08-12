# Run addendum: (G2) endpoint obstruction reduction + slope-ratio evidence (2026-08-13)

Continuation of R-20260812T090000Z-g1prime-g2, target O-4 (boundary analysis
for (G2): no boundary accumulation of block widths).  All numerics are
EVIDENCE unless flagged STRICT.  Notation is the run standard:
sigma in {SUP, INF}, alternating bang-bang density with 2n+1 blocks of heights
in {1, R}, widths w_j > 0 summing to 1, switch points x_j = w_1 + ... + w_j,
D_n = lambda_{n+1} - lambda_n, f = lambda_n u_n^2 - lambda_{n+1} u_{n+1}^2,
c = sqrt(lambda_n / lambda_{n+1}), and the endpoint slope ratio
q0 = sqrt(lambda_{n+1}) |u_{n+1}'(0)| / (sqrt(lambda_n) |u_n'(0)|)
  = (1/c) |u_{n+1}'(0)/u_n'(0)|.

## STRICT: endpoint-collapse reduction (closes O-4 endpoint part up to a
finite-dimensional non-existence statement)

Theorem (endpoint obstruction).  Fix sigma, n >= 2, and a compact R-range
[R0, R1] with R0 > 1.  Suppose (R^(k), x^(k)) is a sequence of band-consistent
solutions of F_sigma(R,x) = 0 with R^(k) -> R* in [R0, R1] and first block
width w_1^(k) = x_1^(k) -> 0, while the remaining widths w_2,...,w_{2n+1} stay
bounded below.  Then, passing to a subsequence, the limiting configuration is
a band-matched root of the reduced (2n-block) system, and it satisfies q0 = c.
Equivalently: if no band-matched reduced root satisfies q0 = c, then no
band-consistent family has w_1 -> 0 on [R0, R1].

Proof.
(1) Convergence of the reduced configuration.  Up to a subsequence,
    w_j^(k) -> w_j* for j = 2..2n+1 with w_j* > 0 and sum w_j* = 1.  This
    defines a reduced string rho_red on [0,1] with 2n blocks and pattern
    (h_2,...,h_{2n+1}).  (If some other width also tends to 0, first pass to a
    further subsequence and then iterate the argument; the statement above
    covers the pure endpoint case.)
(2) Convergence of the eigenvalue pair.  Eigenvalues of the weighted Dirichlet
    string depend continuously on the widths, and distinct simple eigenvalues
    remain distinct under small perturbation.  Since w_1 -> 0 is a small
    perturbation of the reduced string on [0,1] (the missing block has width
    tending to 0 and bounded height), lambda_n^(k) -> lambda_n* and
    lambda_{n+1}^(k) -> lambda_{n+1}*, the n-th and (n+1)-th eigenvalues of
    rho_red, and lambda_n* < lambda_{n+1}* (simplicity persists on compact
    R-ranges at finite R*).
(3) Reduced system.  The eigenfunctions u_n, u_{n+1} (normalized in
    L^2(rho dx)) converge uniformly on [0,1] together with their first
    derivatives, because the coefficients are piecewise constant with a
    uniformly bounded number of discontinuities.  Hence f^(k) -> f*
    uniformly, f* = lambda_n* (u_n*)^2 - lambda_{n+1}* (u_{n+1}*)^2, and
    f*(x_j*) = 0 at each reduced switch x_j* (j = 2..2n).  The reduced
    configuration is therefore a root of the reduced self-consistency system.
(4) Band matching persists.  On the interior of each block the sign of f^(k)
    is the sigma-band sign (constant, nonzero), by band consistency.  The
    uniform limit f* has the same sign on the corresponding reduced block
    interior unless f* vanishes identically there; it cannot, because f* has
    only finitely many zeros (it is analytic and not identically zero: at
    x = 0 its second-order coefficient is a* = lambda_n* u_n*'(0)^2 -
    lambda_{n+1}* u_{n+1}*'(0)^2, which is nonzero on the branch, see (5)).
    Hence the reduced root is band matched.
(5) Endpoint condition q0 = c.  By band consistency f^(k)(x_1^(k)) = 0 with
    x_1^(k) = w_1^(k) -> 0.  Near the Dirichlet endpoint, u_k(x) = u_k'(0) x
    + O(x^3), so
    f(x) = [lambda_n u_n'(0)^2 - lambda_{n+1} u_{n+1}'(0)^2] x^2 + O(x^4).
    Dividing f^(k)(x_1^(k)) = 0 by (x_1^(k))^2 and passing to the limit gives
    lambda_n* u_n*'(0)^2 = lambda_{n+1}* u_{n+1}*'(0)^2, that is q0 = c.
    (The slopes are nonzero: a Dirichlet eigenfunction vanishing together with
    its derivative at an endpoint would vanish identically.)
This proves the forward implication; the reformulation is immediate.

Remark (sign structure).  Band matching at a reduced root gives q0 < 1 in both
modes, because the reduced first block carries f > 0 near x = 0 (SUP reduced
first block has height R with f > 0; INF reduced first block has height 1 with
f > 0), and sign f(x) = sign(1 - q0^2) for small x.  Since c < 1, the endpoint
condition q0 = c is compatible with band matching by sign alone; a quantitative
separation q0 != c on the band-matched reduced solution set is what remains
open (see evidence below).

## EVIDENCE: endpoint slope ratio along the branch

On the actual symmetric branch the ratio is strictly larger than c at every
checked point; the normalized margin r = q0 / c:

- n=2 SUP, R in [1.05, 100]: r in [1.986, 4.636] (positive margin; min near
  R=100).
- n=2 INF, R in [1.05, 100]: r in [1.030, 2.202] (margin decays as R grows).
- n=3 SUP, R in [1.05, 30]: r in [1.821, 15.438].
- n=3 INF, R in [1.05, 30]: r in [1.010, 1.736].
- n=4 SUP, R in [1.05, 10]: r in [1.603, 7.968].
- n=4 INF, R in [1.05, 10]: r in [1.012, 1.524].

Consistency checks: the quadratic expansion f(x) = a x^2 + O(x^4) with
a = lambda_n u_n'(0)^2 - lambda_{n+1} u_{n+1}'(0)^2 is verified to 1e-3 or
better by f(x)/(a x^2) -> 1 at x = 1e-4, 1e-3 on all scan points.  The slope
computed from the transfer-matrix normalization agrees with an independent
first-block sine fit to machine precision.  The R -> 1 limit reproduces the
constant-density value r -> ((n+1)/n)^3 (for n=2: 3.375, n=3: 2.37037, n=4:
1.953125), which is another consistency check.

## EVIDENCE: reduced-root hunt for the endpoint condition

The reduced system (2n blocks, 2n-1 switches, pattern obtained by dropping the
first block of the full alternating pattern) was solved from two seed classes:
(a) random Dirichlet seeds, (b) targeted seeds obtained from the full branch
widths (drop block 1 and renormalize).  Every root was checked for band
matching and for q0 - c.

Result: no band-matched reduced root was found in any case, and every reduced
root found has q0 - c > 0 (positive margin):

- n=2 SUP, R in {2,4}: roots have q0-c >= +0.587; INF R in {4,10,30}: q0-c
  >= +0.544 (all band-unmatched).
- n=3 SUP R=4: q0-c >= +0.322; n=3 INF R=10: q0-c = +1.028.
- n=4 SUP/INF R=10: q0-c = +0.763.
- Degenerate reduced roots (a block collapsed, min width ~ 0) reproduce the
  constant-density signature q0/c = ((n+1)/n)^3 > 1, hence q0 - c > 0.

This is consistent with the STRICT reduction: an endpoint collapse would force
a band-matched reduced root with q0 = c, and none was found (EVIDENCE, not a
proof of non-existence).

## Bug-fix register (slope computation)

Two bugs in the first draft of scripts/_gapn2_slope_ratio.py were found and
fixed; earlier slope numbers in the handoff are RETRACTED.

- eigfun_slope0 used the propagated final M01 entry as the block-start A
  coefficient instead of the block-start M01 stored in starts[bi].  This made
  every normalization wrong (e.g. n=4 INF R=1.05: reported slope 27.12 instead
  of the correct 17.90).
- part_a reported each ladder point with the R=4 pattern instead of the
  pattern of the actual R, corrupting the reported r/a for every R != 4
  (the D values and the solver itself were unaffected).

After the fixes, r and a agree with independent checks to machine precision and
all scan points satisfy the quadratic-expansion test to 1e-3 or better.

## Honest register

- STRICT new ingredient: the endpoint-collapse reduction (Theorem above),
  which lowers the O-4 endpoint part of (G2) to the finite-dimensional
  statement "no band-matched reduced root has q0 = c".
- EVIDENCE supports that statement for n = 2,3,4, SUP/INF, R up to 100, but it
  is not a proof.  The reduced solution set is not certified to be exhaustive
  (only seeded solves).
- Interior coalescence (x_j -> x_{j+1}, the other O-4 case) remains open: it
  needs a reduced root of the 2n-2-block system with a double zero of f at the
  collapsed point, a codimension-two condition not yet attacked.
- (G1') remains open as before; this addendum only advances O-4.
- Scripts added: scripts/_gapn2_slope_ratio.py (branch slope ratio scan),
  scripts/_gapn2_reduced_endpoint_hunt.py (random-seed reduced-root hunt with
  band-matching filter and first/last/both endpoint options),
  scripts/_gapn2_endpoint_targeted.py (targeted reduced-root hunt).

## Commands

python scripts/_gapn2_slope_ratio.py a 2 100
python scripts/_gapn2_slope_ratio.py a 3 30
python scripts/_gapn2_slope_ratio.py a 4 10
python scripts/_gapn2_reduced_endpoint_hunt.py 2 both 0
python scripts/_gapn2_endpoint_targeted.py 2
python scripts/_gapn2_endpoint_targeted.py 3 2,4,10
python scripts/_gapn2_endpoint_targeted.py 4 4,10
