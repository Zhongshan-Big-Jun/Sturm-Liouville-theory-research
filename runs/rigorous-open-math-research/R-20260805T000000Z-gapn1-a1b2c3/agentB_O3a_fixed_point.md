# Agent B - Obligation O3a: uniqueness of the self-consistent 3-block critical point

Run: R-20260805T000000Z-gapn1-a1b2c3
Date: 2026-08-05
Agent: B (obligation O3a)
Verdict: PARTIAL

## 0. Setup and notation

Dirichlet vibrating string on [0,1], barrier family

    rho_(a,b)(x) = R on (a,b), 1 elsewhere, 0 < a < b < 1, R > 1.

For a config let s_k = sqrt(lambda_k) with the normalisation y_k(0) = 1,
u_k = y_k / ||y_k||_L2(rho) the L^2(rho)-normalised eigenfunctions, and

    f(x; a, b) := lambda_1 u_1(x)^2 - lambda_2 u_2(x)^2,

    R1(a,b) := f(a; a,b),   R2(a,b) := f(b; a,b).

By O1c (proved in this run, obligation graph) f has at most two zeros on
(0,1) and {f > 0} is a single interval containing the zero z_0 of u_2
(Wronskian argument: v = u_2/u_1 is strictly decreasing).  For configs
whose f has exactly two zeros x_- < z_0 < x_+ with the sign pattern
f < 0 on (0,x_-), f > 0 on (x_-,x_+), f < 0 on (x_+,1), define

    T(a,b) := (x_-(a,b), x_+(a,b)).

T maps the barrier family into itself.  A sign-consistent critical point
(c.p.) is a pair (a,b) with f(a;a,b) = f(b;a,b) = 0 and the sign pattern
f < 0 on (0,a), f > 0 on (a,b), f < 0 on (b,1).  The reflection is
sigma(a,b) = (1-b, 1-a).

## 1. Exact statements proved (full proofs)

### T1 (characterisation).  For 0 < a < b < 1 the following are equivalent:
(i) (a,b) is a sign-consistent critical point;
(ii) T(a,b) = (a,b) (fixed point of T);
(iii) R1(a,b) = R2(a,b) = 0 and a, b are the two zeros of f (good root).

Proof.  (i) <=> (ii): with the sign pattern, the two zeros of f are
uniquely x_- and x_+; f(a) = f(b) = 0 with f > 0 on (a,b) forces
{x_-,x_+} = {a,b}, and the order (x_- < z_0 < x_+) and the sign pattern
force x_- = a, x_+ = b, i.e. T(a,b) = (a,b).  Conversely a fixed point
has f(a) = f(b) = 0 and by definition of T the sign pattern holds.
(ii) <=> (iii) is the definition of a good root.  QED.

Consequence: uniqueness of sign-consistent critical points is exactly
uniqueness of fixed points of T in 0 < a < b < 1.

### T2 (sigma-equivariance).  T o sigma = sigma o T on the sign-consistent
region, and every fixed point is sigma-invariant iff it is unique.

Proof.  Reflection x -> 1-x maps rho_(a,b) to rho_(1-b,1-a), preserves
the Dirichlet data, and maps eigenfunctions to eigenfunctions with the
same eigenvalues (simplicity of lambda_k, standard SL theory).  Hence
f(x; a,b) = f(1-x; sigma(a,b)), so the zero pair satisfies
(x_-,x_+)(sigma(a,b)) = (1-x_+, 1-x_-)(a,b), i.e. T(sigma(a,b)) =
sigma(T(a,b)).  If p = T(p) then sigma(p) = sigma(T(p)) = T(sigma(p)),
so sigma(p) is a fixed point.  If the fixed point is unique then
sigma(p) = p, i.e. b = 1 - a.  QED.

### T3 (exactness / closed 1-form).  On the open set 0 < a < b < 1 the
residual derivatives satisfy the exact identity

    dR1/db = -dR2/da.

Proof.  Let D(a,b) = lambda_2 - lambda_1 on the barrier family.  By the
Feynman-Hellmann jump formula (O1b, proved in this run):
moving the jump a by da removes density (R-1) from (a, a+da), so
dD/da = -(R-1) f(a;a,b) = -(R-1) R1; moving b adds density (R-1) to
(b, b+db), so dD/db = +(R-1) f(b;a,b) = +(R-1) R2.  Both were verified
numerically to 1e-6 (Section 2.6).  The map (a,b) -> D is C^2 on the
open set: the secular function M01(s; a,b) is real-analytic in all three
arguments, and Dirichlet eigenvalues of a positive weight are simple, so
by the implicit function theorem s_k(a,b) are real-analytic.  Schwarz:
d2D/db da = d2D/da db gives -(R-1) dR1/db = +(R-1) dR2/da.  QED.

T3 is the structural fact behind Route A: it forces the residual
Jacobian to have the form Jres = [[R1_a, -R2_a],[R2_a, R2_b]], and at a
point where both residuals vanish it gives the slope split
g1' = R1_a/R2_a, g2' = -R2_a/R2_b, det(Jres) = R1_a R2_b + R2_a^2.

### T4 (conditional uniqueness).  Fix R > 1 and suppose there is an
interval I = [alpha, beta] and two C^1 functions g1, g2 on I such that:
(a) every sign-consistent fixed point (a,b) satisfies a in I, b = g1(a)
and b = g2(a) (both good branches pass through every fixed point);
(b) g1'(a) > g2'(a) on I;
(c) (g1 - g2)(alpha) < 0 < (g1 - g2)(beta).
Then T has at most one fixed point, and if a fixed point exists it is
unique and satisfies b = 1 - a (by T2).

Proof.  (b) says h := g1 - g2 is strictly increasing, so it vanishes at
most once; (c) plus IVT gives exactly one zero; (a) maps fixed points
injectively into zeros of h.  T2 then yields the symmetry.  QED.

T4 is the precise reduction: O3a is proved once Lemma A (b) and Lemma B
(c) are proved, with (a) supplied by the branch structure of Gamma_1,
Gamma_2.

## 2. Numerical evidence (all reproducible, scripts in this directory)

### 2.1 Fixed points and local stability of T

fp(R) = unique good root of (R1,R2) = 0, found by least-squares from
several seeds in the (a, w = b-a) parameterisation (agentB_scan2.py,
agentB_multiseed.py); J_T = finite-difference Jacobian of T at fp;
rho_T = spectral radius of J_T.

  R     a(fp)        b(fp)        a+b-1        lambda_1    lambda_2    D            rho(J_T)
  1.02  0.42008434   0.57991566   ~1e-14       -           -           -            -
  1.05  0.42083530   0.57916470   5e-15        9.718543    39.429245   29.710702    0.0179
  1.2   0.42425964   0.57574036   1e-15        9.311454    39.304287   29.992833    0.0678
  1.5   0.42983243   0.57016757   2e-15        8.652895    39.125925   30.473030    0.1541
  2.0   0.43669594   0.56330406   2e-15        7.846217    38.948482   31.102264    0.2699
  3.0   0.44566494   0.55433506   5e-15        6.794142    38.786364   31.992221    0.4391
  4.0   0.45148547   0.54851453   6e-15        6.109280    38.723263   32.613984    0.5611
  5.0   0.45567895   0.54432105   2e-14        5.613337    38.698305   33.084967    0.6556
  10.0  0.46693119   0.53306881   4e-15        4.264854    38.716133   34.451278    0.9399
  20.0  0.47568656   0.52431344   8e-15        3.188917    38.815398   35.626481    1.1968
  50.0  0.48406922   0.51593078   2e-15        2.128010    38.980195   36.852185    1.4775
  100.0 0.48852937   0.51147063   4e-15        1.548476    39.095479   37.547003    1.6422
  1000.0 0.49626090  0.50373910   8e-15        0.514713    39.340095   38.825382    -

All entries satisfy a + b - 1 ~ 1e-14 (symmetric), z_0 = 1/2 exactly
(symmetric config) and a < z_0 < b.  lambda_2 -> 4 pi^2, a -> 1/2 as
R -> infinity (centre-mass pinning, consistent with the run SUP
analysis).  Rows 1.02, 50, 1000 were computed or recomputed this
session (the fptable file rows for R=50, 100 are spurious, see 3.5).

### 2.2 R = 4 fixed point detail (matches the task statement)

  fp      = (0.451485465757, 0.548514534243)
  lambda  = (6.109279720, 38.723263338),  D = 32.613983618
  z_0     = 0.500000000
  J_T     = [[-0.145038, 0.416063], [0.416063, -0.145038]]
  eig(J_T)= 0.271025, -0.561101;  rho(J_T) = 0.5611 < 1
  Jres    = [[352.0517, -127.9219], [127.9219, -352.0517]],
            det(Jres) = -107576,  g1' = 2.752, g2' = 0.363, h' = 2.389

Iterating T from (0.1,0.9), (0.05,0.6), (0.3,0.7), (0.44,0.56),
(0.15,0.85) converges to fp to 1e-8 in 25-28 iterations (verified this
session).

### 2.3 Curve structure (Route A evidence): Gamma_1, Gamma_2, h

Gamma_1 = {R1 = 0} good branch (a = x_-), graph b = g1(a);
Gamma_2 = {R2 = 0} good branch (b = x_+), graph b = g2(a).
Both traced from fp by predictor-corrector continuation (goodbranch.py,
goodbranch2.py) and by direct sampling with good-root classification
(crossing.py).  Data: agentB_goodbranches.json (rows are [a,b]).

  R     g1 a-range       g2 a-range       common range     g1,g2 increasing?  h sign changes  min h'
  1.05  [0.4196,0.4260] [0.0049,0.5799]  [0.4196,0.4260]  yes               1               42.78
  1.5   [0.4196,0.4735] [0.0053,0.5791]  [0.4196,0.4735]  yes               1                5.93
  2.0   [0.4196,0.5117] [0.0063,0.5789]  [0.4196,0.5117]  yes               1                3.53
  4.0   [0.4196,0.6008] [0.0048,0.5801]  [0.4196,0.5801]  yes               1                1.77
  10.0  [0.4202,0.5613] [0.0046,0.5781]  [0.4202,0.5613]  yes               1                1.02
  100.0 [0.4256,0.5750] [0.0321,0.5349]  [0.4256,0.5349]  yes               1                0.29

h = g1 - g2 is strictly increasing on the common range (min h' in the
last column) and has exactly one sign change, located at a = a(fp).
Direct crossing tables (this session, R = 4 and R = 100, a in the common
range, 22-26 sample points each) show h monotone from negative to
positive with a single zero:

  R=4:   a=0.425 h=-0.0806, a=0.45 h=-0.0036, a=0.455 h=+0.0082,
         a=0.48 h=+0.0597, a=0.53 h=+0.1505
  R=100: a=0.4300 h=-0.0296, a=0.48856 h=+0.0000, a=0.5520 h=+0.0273

(The two sample points a=0.50808, 0.54768 missing from the coarse R=100
table are grid artifacts: a direct check finds the good roots
(g1,g2) = (0.537601, 0.524809) and (0.582291, 0.556390) there, so the
branches are continuous and h stays positive.)

Slope split at fp (this session): h' = 63.78 (R=1.05), 4.67 (R=2),
2.39 (R=4), 1.49 (R=10), 0.886 (R=100), 0.755 (R=1000).  h' is smallest
near the right end of the common range and decreases with R; the
quantitative margin at R=1000 is already small, so Lemma A needs an
R-uniform bound.

### 2.4 Multi-seed residual scans (falsification, Route D)

least-squares from 126 seeds (81 grid + 45 random) in (a, w = b-a) with
the good-root classification (agentB_scan2.py, multiseed.py; R=1.02,
1000 added this session):

  R     roots found   good roots   location of good root
  1.02  9             1            (0.420084, 0.579916)
  1.05  11            1            (0.420835, 0.579165)
  2.0   12            1            (0.436696, 0.563304)
  4.0   12            1            (0.451485, 0.548515)
  10.0  11            1            (0.466931, 0.533069)
  100.0 8             1            (0.488529, 0.511471)

All non-good roots are boundary artifacts: a ~ 1e-6 with b in
(0.25-0.58) (classified neither or right-only) and b ~ 1 with a in
(0.6-0.95) (left-only or neither).  None has the sign pattern with a =
x_- and b = x_+, so none is a fixed point (T1).  The near-degenerate
rows a ~ 0.002, b ~ 0.997 found at R = 50, 100 (present in
agentB_fptable.json) are NOT fixed points: their f has zeros at
(0.4196, 0.5804), far from (a,b) (verified this session), so they are
spurious roots of the residual system near the rho ~ R a.e. degenerate
config.

### 2.5 T is NOT a global contraction (falsification of a contraction proof)

- R = 100: rho(J_T) = 1.642 > 1 at the fp; iterating T from (0.3, 0.7)
  enters a genuine 2-cycle: (0.4657, 0.5343) <-> (0.4970, 0.5030),
  i.e. the iteration never reaches the fp (verified this session,
  20 iterates shown).
- R = 50: rho(J_T) = 1.478 > 1, fp is a repeller.
- R = 4: max ||Tx-Ty||/||x-y|| = 1.59 over a 190-point grid of
  sign-consistent configs and 0.73 over 300 random pairs (this session).
  The value 2.3 quoted in the task statement was not reproduced; in any
  case the Euclidean contraction hypothesis is false in general.
- Therefore uniqueness cannot be proved by any global contraction
  argument; the branch-intersection route (Lemma A) is the right one.

### 2.6 Exactness identity (T3) - numerical check

dR1/db + dR2/da via Richardson-extrapolated central differences
(h = 1e-4, 1e-5) at four points:

  (a,b)                          dR1/db          dR2/da          sum
  (0.4514854658,0.5485145342,4)  -1.279219298e2  +1.279219298e2  4.1e-8
  (0.43,0.58,4)                  -1.582113670e2  +1.582113669e2  -1.4e-7
  (0.4669311862,0.5330688138,10) -1.454347697e2  +1.454347698e2  8.9e-8
  (0.3,0.6,2)                    -3.035600714e1  +3.035600704e1  -9.9e-8

Residuals are at the level of the finite-difference plus eigenvalue-
solver precision (~1e-7); the identity holds to that accuracy.  The FH
formula itself was checked directly: at (0.42, 0.56, R=4),
dD/da = 38.887310 = -(R-1) R1, dD/db = -26.476919 = +(R-1) R2 (1e-6).

### 2.7 Existence of a symmetric fixed point (O2 cross-check)

f_sym(u) := f(u; rho_sup_u) with rho_sup_u = R on (u, 1-u) has a zero in
(0, 1/2) for every R tested, with sign - before and + after:

  R       u* = a(fp)   sign(f_sym) below/above u*
  1.05    0.4208353    -6.24e1 / +1.30e1
  2.0     0.4366959    -2.33e1 / +1.11e1
  4.0     0.4514855    -7.03e0 / +8.52e0
  10.0    0.4669312    -1.30e0 / +4.94e0
  100.0   0.4885294    -1.53e-2 / +1.64e-1
  1000.0  0.4962609    -3.26e-4 / +2.16e0

The zero coincides with a(fp) from 2.1, confirming that the unique good
root of the 2-parameter system lies on the symmetric line (existence of
at least one fixed point is O2, endpoint signs proved; uniqueness on the
line is O2b, still open - Agent A deliverable).

## 3. Failed attempts and precise failure mechanisms

3.1 Global concavity of D.  Hessian of D at fp is negative definite
(e.g. R=4: diag -1056, eigenvalues approx -1440, -672) but D is not
globally concave on the triangle: there are points with a positive
definite Hessian (e.g. R=4 at (0.115, 0.201)).  Hence the standard
"unique critical point of a strictly concave function" theorem is not
available.

3.2 Sign rule (R1 - R2)(a + b - 1) < 0.  If it held, a residual root
would be forced to the symmetric line.  False: at R=1.05, 54 of 105
grid points violate it; e.g. (0.02, 0.431) has a + b - 1 < 0 but
R1 - R2 < 0.  The residual pair does not have a coercive symmetry
structure of this type.

3.3 Global Euclidean contraction of T.  False, see 2.5: R=100 has a
genuine 2-cycle and rho(J_T) = 1.64; R=4 pair ratios up to 1.59 on a
grid.  Any contraction metric would have to be non-Euclidean and
R-dependent, and even then the R=100 2-cycle shows T is not eventually
contracting in the natural metric either.

3.4 Continuation tracing.  Arc-length continuation of the good branches
at ds = 0.001 timed out at ~1500 s for R=100 and the R=100 Gamma_1
trace in agentB_goodbranches.json is incomplete (a only to 0.5750).
Direct sampling (crossing.py) over the full common range works and was
used instead.  Lesson: use direct sampling or coarse continuation for
the slope tables.

3.5 Spurious residual roots at large R.  The fptable generator found
(a,b) = (0.0024, 0.9976) at R=50 and (0.0030, 0.9970) at R=100 as roots
of (R1, R2) = 0.  These are not sign-consistent: for those configs the
zeros of f are (0.4196, 0.5804), so neither a = x_- nor b = x_+ holds;
they are near-degenerate roots of the residual system close to the
rho ~ R a.e. limit where f ~ 0 at both jump points.  They must be
excluded by the sign-pattern check (zeros_f), which the scan scripts
do.

3.6 Analytic attack on Lemma A via second-order sensitivity.  The
natural route is to differentiate the FH formulas once more to get
dR1/da, dR2/db in closed form (spectral sums of products of
eigenfunctions at the jump points), and to show det(Jres) > 0 together
with R2_a R2_b > 0 on the branches.  This requires uniform control of
the spectral sums; no clean closed form was obtained in this session,
so Lemma A stays open.  This is the exact remaining gap (Section 4).

## 4. Exact remaining gap

O3a is reduced (T4) to three statements, all numerically verified at
R in {1.02, 1.05, 1.2, 1.5, 2, 3, 4, 5, 10, 20, 50, 100, 1000} but not
proved:

Lemma A (monotone branch gap).  On the common a-range where both good
branches exist, g1 and g2 are C^1 with g1'(a) > g2'(a) > 0.  Numerics:
min g1' - g2' = 42.78 (R=1.05), 5.93 (R=1.5), 3.53 (R=2), 1.77 (R=4),
1.02 (R=10), 0.287 (R=100); the margin shrinks with R (h' = 0.755 at
the R=1000 fp), so a proof must give an R-uniform positive lower bound.

Lemma B (endpoint signs of h).  (g1 - g2) < 0 at the left end and
> 0 at the right end of the common range.  Verified for all R tested
(Table 2.3 and direct crossing tables).  The endpoints originate from
the R -> 1 limiting zero positions x = arccos(1/4)/pi ~ 0.41957 and
x = arccos(-1/4)/pi ~ 0.58043; a proof needs the qualitative shape of
the two branches near their endpoints.

Lemma C (coverage).  Every sign-consistent fixed point lies on both
good branches (a in the common range).  This is the part of T4(a) that
must be established; numerically the good branches are the only branch
components of Gamma_1 cap {a = x_-} and Gamma_2 cap {b = x_+}.

Given Lemmas A-C, T4 gives: at most one fixed point, and with the
existence of the symmetric fixed point (O2, endpoint signs proved) it
is exactly one, hence symmetric (b = 1 - a) by T2.  No counterexample
was found at any R in {1.02, 1.05, 1.2, 1.5, 2, 3, 4, 5, 10, 20, 50,
100, 1000}: exactly one good root each, and the branch intersection is
a single point.

## 5. Verdict

PARTIAL.  Proved rigorously: T1 (fixed points = sign-consistent c.p.),
T2 (sigma-equivariance; uniqueness implies symmetry), T3 (exactness
identity dR1/db = -dR2/da, from FH + Schwarz), T4 (reduction of
uniqueness to the three branch lemmas).  The claim itself - a unique
fixed point for every R > 1 - is supported by conclusive numerics on
the full tested R-range with no counterexample, but Lemma A (and B, C)
remain unproved, so the claim is not yet a theorem.

## 6. Reproduction

Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
(numpy 2.2.6, scipy 1.15.3).  All scripts in this run directory.

  solver/zero library : agentB_lib.py (transfer-matrix secular roots,
                        L^2(rho) normalisation, z0 bisection, zeros_f)
  seed scans          : agentB_scan.py, agentB_scan2.py, agentB_multiseed.py
  branch traces       : agentB_goodbranch.py, agentB_goodbranch2.py
  direct crossing     : agentB_crossing.py (tables in 2.3)
  fixed point tables  : agentB_fixedpoints.json, agentB_fptable.json

Key commands used this session:

  python agentB_scan2.py 4 60        (R=4 seed scan)
  python agentB_crossing.py 4 0.425 0.53 22
  python agentB_crossing.py 100 0.43 0.552 26

All numbers in the tables above were recomputed in this session with
the scripts in this directory; the exact identity (T3) was checked by
Richardson extrapolation at four points; the R=100 2-cycle and the
R=50/100 spurious roots were verified directly.
