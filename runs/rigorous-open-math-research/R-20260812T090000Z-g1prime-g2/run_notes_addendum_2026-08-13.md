# Run addendum: (G2) full closure (2026-08-13, R-204)

Continuation of R-20260812T090000Z-g1prime-g2, target O-4 (boundary analysis
for (G2)).  All numerics are EVIDENCE unless flagged STRICT.  This addendum
supersedes the previous endpoint addendum of the same date: the slope-ratio
convention is corrected and the endpoint part of (G2) is now closed STRICT by
the block-energy identity (K-identity) together with the exact zero count of
f and the interior-simplicity theorem.

## Notation (framework convention, matches docs/SL_gap_nge2_symmetry_local_proof.tex)

sigma in {SUP, INF}; alternating bang-bang density with 2n+1 blocks of heights
in {1, R}, widths w_j > 0 summing to 1, switch points x_j = w_1 + ... + w_j,
D_n = lambda_{n+1} - lambda_n, f = lambda_n u_n^2 - lambda_{n+1} u_{n+1}^2,
c = sqrt(lambda_n / lambda_{n+1}) in (0,1), and the endpoint slope ratios

    q0 := u_{n+1}'(0) / u_n'(0) > 0,
    q1 := u_{n+1}'(1) / u_n'(1) < 0.

The eigenfunctions are L^2(rho dx)-normalized.  The scripts previously used
the sqrt-weighted ratio r := sqrt(lambda_{n+1}) |u_{n+1}'(0)|
/ (sqrt(lambda_n) |u_n'(0)|) = q0 / c; the old evidence lines "q0 - c > 0" in
that convention are RETRACTED (see the bug-fix register below).  In the
framework convention the endpoint condition is q0 = c, which is what the
collapse argument really produces.

## STRICT: block-energy identity (K-identity)

(Provenance: this is the audited block-energy invariant of session 50,
tools/switch-saturation-k-invariant.md, proof in
docs/SL_gap_nge2_finite_reduction_proof.tex; restated here for
self-containedness, not a new claim.)

Theorem A.  Let rho > 0 be piecewise constant on [0,1] with finitely many
jumps x_1 < ... < x_m, and let u_n, u_{n+1} be the Dirichlet eigenfunctions
(normalized: integral rho u_k^2 = 1) for the eigenvalues lambda_n <
lambda_{n+1}.  If f(x_j) = 0 at every jump, then the block energy

    K := (u_n'^2 + lambda_n rho u_n^2) - (u_{n+1}'^2 + lambda_{n+1} rho u_{n+1}^2)

is constant on [0,1] and equals -2 D_n.  In particular

    u_{n+1}'(0)^2 - u_n'(0)^2 = 2 D_n > 0,   hence  q0 > 1,
    u_{n+1}'(1)^2 - u_n'(1)^2 = 2 D_n > 0,   hence  q1 < -1.

Proof.  On the interior of every block rho is constant, and

    K' = 2 u_n' u_n'' + 2 lambda_n rho u_n u_n' - 2 u_{n+1}' u_{n+1}''
         - 2 lambda_{n+1} rho u_{n+1} u_{n+1}'
       = 2 u_n' (-lambda_n rho u_n) + 2 lambda_n rho u_n u_n'
         - 2 u_{n+1}' (-lambda_{n+1} rho u_{n+1})
         - 2 lambda_{n+1} rho u_{n+1} u_{n+1}' = 0,

so K is constant on each block.  At a jump x_j the eigenfunctions and their
derivatives are continuous (rho is bounded), hence

    K(x_j+) - K(x_j-) = (rho(x_j+) - rho(x_j-))
                        (lambda_n u_n(x_j)^2 - lambda_{n+1} u_{n+1}(x_j)^2)
                     = (rho_+ - rho_-) f(x_j) = 0.

Thus K is constant on [0,1].  Integrating by parts with the Dirichlet data,

    integral_0^1 K dx = (lambda_n + lambda_n) - (lambda_{n+1} + lambda_{n+1})
                      = -2 D_n,

where integral u_k'^2 dx = [u_k u_k']_0^1 - integral u_k u_k'' dx
= lambda_k integral rho u_k^2 dx = lambda_k.  Hence K == -2D_n < 0.  At the
endpoints u_n(0) = u_{n+1}(0) = 0, so K(0) = u_n'(0)^2 - u_{n+1}'(0)^2 = -2D_n,
giving u_{n+1}'(0)^2 = u_n'(0)^2 + 2D_n > u_n'(0)^2 and, since both endpoint
slopes are positive, q0 > 1.  At x = 1 the slopes u_n'(1), u_{n+1}'(1) have
opposite signs (the eigenfunctions have n-1 and n interior zeros), so q1 < 0
and |u_{n+1}'(1)| > |u_n'(1)|, i.e. q1 < -1.  QED.

Remark.  This is the same identity as part (e) of the framework structure
theorem; the proof only uses f = 0 at the switches, not band matching, and it
applies to any pattern (full or reduced) and any R > 1.  The identity was
verified numerically to 1e-11 (script scripts/_gapn2_kidentity_audit.py).

## STRICT: endpoint-collapse reduction (corrected convention)

Theorem B.  Fix sigma, n >= 2, and a compact R-range [R0, R1] with R0 > 1.
Suppose (R^(k), x^(k)) is a sequence of band-consistent solutions of
F_sigma(R,x) = 0 with R^(k) -> R* in [R0, R1] and first block width
w_1^(k) = x_1^(k) -> 0, while the remaining widths w_2,...,w_{2n+1} stay
bounded below.  Then, passing to a subsequence, the limiting configuration is
a band-matched root of the reduced (2n-block) system, and it satisfies
q0 = c.  Equivalently: if no band-matched reduced root satisfies q0 = c, then
no band-consistent family has w_1 -> 0 on [R0, R1].

Proof.
(1) Convergence of the reduced configuration: w_j^(k) -> w_j* > 0 for
    j = 2..2n+1 with sum w_j* = 1; this defines the reduced string rho_red
    with 2n blocks and pattern (h_2,...,h_{2n+1}).
(2) Convergence of the eigenvalue pair: eigenvalues depend continuously on
    the widths; distinct simple eigenvalues stay distinct under small
    perturbation (the uniform lower bound lambda_{n+1} - lambda_n >=
    (2n+1) pi^2 / R1 > 0 on [R0,R1] holds), so lambda_n^(k) -> lambda_n* and
    lambda_{n+1}^(k) -> lambda_{n+1}*.
(3) Reduced system: the normalized eigenfunctions converge uniformly together
    with their first derivatives (piecewise-constant coefficients with a
    bounded number of discontinuities), so f^(k) -> f* in C^1 and
    f*(x_j*) = 0 at every reduced switch.  The limit is a root of the reduced
    system.
(4) Band matching persists: on each surviving block interior f^(k) has the
    constant nonzero sigma-band sign; the limit f* has the same weak sign
    there, and f* is not identically zero on any block (f* is analytic and at
    x = 0 its quadratic coefficient is lambda_n* u_n*'(0)^2 (1 - q0*^2/c*^2);
    if this vanishes, the quartic coefficient is
    (rho*_0/3) lambda_{n+1}* u_{n+1}*'(0)^2 D* > 0, so f* does not vanish
    identically near 0).  By Theorem C below, f* has no zero with f* = f*' = 0
    inside (0,1), so the weak sign is strict on every block interior: the
    limit is band matched.
(5) Endpoint condition q0 = c: by band consistency f^(k)(x_1^(k)) = 0 with
    x_1^(k) -> 0.  Near a Dirichlet endpoint u_k(x) = u_k'(0) x + O(x^3), so

        f(x) = lambda_n u_n'(0)^2 (1 - q0^2/c^2) x^2 + O(x^4).

    The O-term is uniform in k (the eigenfunctions and their derivatives up
    to order 4 are uniformly bounded), hence dividing f^(k)(x_1^(k)) = 0 by
    (x_1^(k))^2 and passing to the limit gives

        lambda_n* u_n*'(0)^2 = lambda_{n+1}* u_{n+1}*'(0)^2,  i.e.  q0* = c.

This proves the forward implication; the reformulation is immediate.

Sign remark.  Band matching on the reduced first block (height h_2, the
opposite of h_1) demands f* > 0 near x = 0, i.e. q0* <= c.  Hence the endpoint
condition q0 = c is the boundary value of the band-matching range, not
excluded by sign alone; the exclusion is Theorem A, which gives q0* > 1 > c at
every reduced root.  Consequently the m = 1 endpoint collapse is impossible:
q0 = c < 1 contradicts q0 > 1.

## STRICT: interior coalescence exclusion (independent simple-zeros proof)

Theorem C.  For any positive piecewise-continuous rho and any configuration
with lambda_n < lambda_{n+1}, the function f = lambda_n u_n^2 -
lambda_{n+1} u_{n+1}^2 has no point xbar in (0,1) with
f(xbar) = f'(xbar) = 0.  Consequently no band-consistent family can have two
adjacent interior switches coalesce: if x_j, x_{j+1} -> xbar in (0,1) with
f(x_j) = f(x_{j+1}) = 0, then continuity gives f(xbar) = 0 and Rolle's
theorem gives a point between them where f' -> 0, i.e. f'(xbar) = 0, which is
impossible.

Proof.  Suppose f(xbar) = 0.  Then lambda_n u_n(xbar)^2 =
lambda_{n+1} u_{n+1}(xbar)^2.  If u_n(xbar) = 0, then also
u_{n+1}(xbar) = 0, a common zero, impossible because the zeros of u_n and
u_{n+1} strictly interlace (Sturm).  Hence both are nonzero and
u_{n+1}(xbar) = eps c u_n(xbar), eps = +-1.  If also f'(xbar) = 0, then
lambda_n u_n(xbar) u_n'(xbar) = lambda_{n+1} u_{n+1}(xbar) u_{n+1}'(xbar);
substituting u_{n+1}(xbar) = eps c u_n(xbar) and dividing by the nonzero
u_n(xbar) gives lambda_n u_n'(xbar) = lambda_{n+1} eps c u_{n+1}'(xbar), i.e.
u_{n+1}'(xbar) = eps c u_n'(xbar) (since lambda_n = lambda_{n+1} c^2).  The
full Cauchy data coincide: (u_{n+1}, u_{n+1}')(xbar) = eps c (u_n, u_n')(xbar).
By uniqueness of solutions of -u'' = lambda rho u with given Cauchy data,
u_{n+1} is identically eps c u_n; applying the equation to both sides forces
lambda_{n+1} = lambda_n, a contradiction.  Hence every interior zero of f is
simple.  QED.

This closes the interior-coalescence part of (G2) STRICT for all R > 1 and
all n >= 2; it also re-proves (independently of the framework cell analysis)
that all interior zeros of f are simple.

## STRICT: exact zero count of f for arbitrary weights

(Provenance: audited result of session 50,
docs/SL_gap_nge2_exact_2n_switches_proof.tex and
tools/switch-saturation-k-invariant.md; restated for self-containedness.)

Theorem D.  For any positive piecewise-continuous rho and the normalized
eigenpair (u_n, lambda_n), (u_{n+1}, lambda_{n+1}) with lambda_n <
lambda_{n+1}, the number of zeros of f in (0,1) is

    #Z(f; (0,1)) = 2n - 2 + 1_{q0 > c} + 1_{q1 < -c},

all zeros simple.

Proof (cell analysis; same derivation as in the framework document, kept here
for self-containedness).  The Wronskian W = u_{n+1}' u_n - u_{n+1} u_n'
satisfies W(0) = 0 and W' = (lambda_n - lambda_{n+1}) rho u_n u_{n+1} < 0
wherever u_n u_{n+1} > 0; the standard Sturm sign chase through the cells
C_i = (w_{i-1}, w_i) of u_n (nodes w_0 = 0 < w_1 < ... < w_n = 1, and z_i the
unique zero of u_{n+1} in C_i) gives W < 0 on (0,1).  Hence
Q := u_{n+1}/u_n has Q' = W/u_n^2 < 0 on each cell interior, so
|Q| strictly decreases on (w_{i-1}, z_i) and strictly increases on
(z_i, w_i).  Since f = lambda_n u_n^2 (1 - |Q|^2/c^2), the zeros of f are
exactly the solutions of |Q| = c, all simple.  In a middle cell
(i = 2,...,n-1) |Q| runs from +infinity down to 0 and back to +infinity:
exactly two solutions.  In the first cell |Q(0+)| = q0 > 0: the
decreasing branch gives one solution iff q0 > c, the increasing branch
always gives one: 1 + 1_{q0>c}.  In the last cell |Q(1-)| = |q1| with
q1 < 0: the increasing branch gives one solution iff |q1| > c, i.e.
q1 < -c: 1 + 1_{q1<-c}.  Total: 2(n-2) + (1 + 1_{q0>c}) + (1 + 1_{q1<-c}).
QED.

## STRICT: (G2) is closed (no boundary generation)

Theorem E.  For every n >= 2, sigma in {SUP, INF}, and every compact
R-range [R0, R1] with R0 > 1, there exists eta = eta(n, R0, R1) > 0 such that
every band-consistent solution (R, x) with R in [R0, R1] has all block widths
>= eta.  Equivalently, Sigma_sigma has no accumulation point in
[R0, R1] x partial U.  Hence condition (G2) of the global classification
framework holds.

Proof.  Suppose not: take band-consistent solutions (R^(k), x^(k)) with
R^(k) -> R* in [R0, R1] and some block width tending to 0.  Pass to a
subsequence with w_j^(k) -> w_j* in [0,1] and sum w_j* = 1.

Step 1 (interior coalescence excluded).  If w_j* = 0 for some j in {2,...,2n}
with x_{j-1}* = x_j* in (0,1), then f* = f*' = 0 at the interior point
x_{j-1}* (continuity and Rolle), contradicting Theorem C.  Hence every
zero-width block is at an endpoint: there exist m, m' >= 0 with m + m' >= 1
such that w_1* = ... = w_m* = 0 (m is the largest leading block with
w_1* + ... + w_m* = 0), w_{2n+2-m'}* = ... = w_{2n+1}* = 0 (largest trailing
block), and all other widths are positive.

Step 2 (limit string).  The limit configuration is the string rho* on [0,1]
with the 2n + 1 - m - m' surviving blocks h_{m+1},...,h_{2n+1-m'} and the
surviving switches x_j*, j = m+1,...,2n-m'.  The eigenvalues
lambda_n^(k), lambda_{n+1}^(k) converge to the n-th and (n+1)-th eigenvalues
lambda_n*, lambda_{n+1}* of rho* (spectral continuity; the collapsed blocks
carry eigenvalues to infinity), the normalized eigenfunctions converge in C^1
to the normalized eigenfunctions u_n*, u_{n+1}* of rho*, and
lambda_{n+1}* - lambda_n* >= (2n+1) pi^2 / R1 > 0.  In particular
f^(k) -> f* = lambda_n* u_n*^2 - lambda_{n+1}* u_{n+1}*^2 in C^1.

Step 3 (root and K-identity).  f*(x_j*) = 0 at every surviving switch, so by
Theorem A applied to rho*,

    K* == -2D* < 0,   hence   q0* > 1  and  q1* < -1.

Step 4 (zero count).  Theorem D gives #Z(f*; (0,1)) = 2n - 2 + 1 + 1 = 2n.

Step 5 (band matching persists).  On each surviving block interior f^(k) has
the constant nonzero sigma-band sign eps_j.  Uniform convergence gives
eps_j f* >= 0 on that block; f* is analytic and not identically zero on any
block (otherwise u_{n+1}* = +-c* u_n* on an open set, forcing
lambda_{n+1}* = lambda_n*), and Theorem C forbids a zero of f* with f* = 0 and
f*' = 0 in (0,1).  Hence eps_j f* > 0 strictly on every block interior: f*
has no zeros inside any block.

Step 6 (contradiction).  The 2n - m - m' surviving switches are zeros of f*
in (0,1), and 2n - m - m' <= 2n - 1 < 2n = #Z(f*).  So f* has at least one
zero in (0,1) that is not a switch, hence inside a block, contradicting
Step 5.  QED.

Remarks.
- The argument does not need the q0 = c endpoint condition of Theorem B and
  does not distinguish the parity of m; Theorem B remains valid as a
  consistency statement (q0 = c and q0 > 1 cannot both hold).
- (G2) therefore holds STRICT for both patterns, all n >= 2, on every compact
  R-range.  Combined with the framework reduction, the global classification
  conjecture now depends only on (G1').

## EVIDENCE: re-run with the corrected convention

- Block-energy identity audit (scripts/_gapn2_kidentity_audit.py): on the full
  branch n=2, R=4, SUP/INF: K(0) + 2D at the 1e-11 level, q0 = -q1
  (reflection symmetry), SUP q0 = 2.376980 > 1, INF q0 = 1.142677 > 1.
- Reduced roots n=2, R=4 (both modes, random seeds): every root found has
  q0 > 1 and q1 < -1 (K-identity prediction) and band = False.  Values
  include q0 = 1.551847, 1.500000, 1.288458 (SUP) and 1.507292, 2.141202,
  1.500000 (INF); the exact 1.5 = (n+1)/n values come from degenerate
  (zero-width) reduced configs, the constant-density signature.
- Branch ladder scans (scripts/_gapn2_slope_ratio.py, corrected convention):
  see the scan output files scripts/_out_slope_a{2,3,4}.txt (n=2 R<=100,
  n=3 R<=30, n=4 R<=10).  The check r > 1 and a < 0 (framework q0 and the
  quadratic coefficient of f) is now the STRICT Theorem A prediction.

## Bug-fix register (2026-08-13)

- Convention bug: the previous version of this addendum defined q0 with
  sqrt(lambda) weights and simultaneously concluded "q0 = c" from the
  expansion a = 0.  In that convention a = 0 is q0 = 1, not q0 = c.  The
  framework document uses q0 := u_{n+1}'(0)/u_n'(0); with this convention
  a = 0 is exactly q0 = c.  This addendum now uses the framework convention
  throughout, and the scripts were changed accordingly
  (_gapn2_slope_ratio.py, _gapn2_reduced_endpoint_hunt.py).  All previous
  "q0 - c" evidence lines in the sqrt-weighted convention are RETRACTED.
- The previous "honest register" line "interior coalescence remains open" is
  RETRACTED: Theorem C closes it.
- The earlier slope-computation bugs (block-start transfer-matrix coefficient
  and per-R pattern in the report loop) remain fixed as registered.

## Honest register

- (G2) is CLOSED STRICT: Theorem C (interior coalescence), Theorems A and D
  (interior coalescence) and Theorem E (boundary exclusion) close O-4, using
  the K-identity and the exact zero count as premises; the latter two are
  audited session-50 results (docs/SL_gap_nge2_finite_reduction_proof.tex,
  docs/SL_gap_nge2_exact_2n_switches_proof.tex), restated above only for
  self-containedness.  New STRICT content of this addendum: Theorem B
  (endpoint-collapse reduction with the corrected q0 = c condition),
  Theorem C (interior zeros of f are simple), Theorem E ((G2) closure).
- Theorem B (endpoint-collapse reduction) is retained as a STRICT reduction
  with the corrected endpoint condition q0 = c; it is superseded in the
  closure by Theorems A/D/E but remains a valid consistency statement.
- (G1') remains OPEN; this addendum only advances O-4.
- All numerics above are EVIDENCE; the STRICT claims carry complete proofs
  in this file.

## Scripts

- scripts/_gapn2_kidentity_audit.py: block-energy identity audit (branch +
  reduced roots).
- scripts/_gapn2_slope_ratio.py: branch ladder scan, framework q0 convention
  (python scripts/_gapn2_slope_ratio.py a 2 100).
- scripts/_gapn2_reduced_endpoint_hunt.py: random-seed reduced-root hunt,
  framework q0/q1 convention (python scripts/_gapn2_reduced_endpoint_hunt.py
  2 both 4).
- scripts/_gapn2_endpoint_targeted.py: branch-seeded reduced-root hunt
  (python scripts/_gapn2_endpoint_targeted.py 2 4).
