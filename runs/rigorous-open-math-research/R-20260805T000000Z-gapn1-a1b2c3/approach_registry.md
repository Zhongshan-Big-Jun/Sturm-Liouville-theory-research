# Approach registry

## Route A: monotone residual curves (2-param critical point uniqueness)
- Family: direct analysis in the (a,b) plane.
- Core mechanism: show Gamma_1 = {(a,b): f(a;a,b)=0} is the graph of a
  strictly increasing function b = h1(a), Gamma_2 likewise b = h2(a),
  and h1 - h2 has a single sign change; then Gamma_1 cap Gamma_2 is a
  single point (which is the symmetric point by reflection symmetry).
- Target obligation: O3a.
- Required known results: O1c; monotonicity of v = u_2/u_1; FH for jump
  perturbation.
- First concrete deliverable: numerical tracing of Gamma_1, Gamma_2 for
  several R; check monotonicity and uniqueness of the intersection.
- Fast falsification: any R where Gamma_1, Gamma_2 cross more than once.
- Expected bottleneck: proving monotonicity of the residual curves
  requires estimates on d f(x_j)/d(a,b), i.e. second-order sensitivity of
  eigenvalues wrt config.  This is heavy but local.
- Status: ACTIVE.

## Route B: direct global bound (variational / test-function)
- Family: direct inequality; no critical point analysis.
- Core mechanism: for every (a,b) in the barrier family, exhibit a
  comparison quantity showing D(a,b) <= D_sym(u*).  Candidates: (i)
  bracket lambda_2 by a "pinned" odd test function and lambda_1 below by
  an even trial function; (ii) use the ratio bound nu(R) times a bound on
  lambda_1; (iii) monotone rearrangement in the "total mass" variable.
- Target obligation: O3 (both variants) and O3b.
- Required known results: ratio theorem (session 5), AEH Lemma 2.2.
- First concrete deliverable: check whether D(a,b) <= D(m(a,b)) for the
  symmetrized config with the same barrier width (numerics: FALSE for
  fixed small width by first-order theory, so the symmetrization must
  use a different invariant, e.g. total mass).
- Fast falsification: any (a,b) with D(a,b) > D_sym(u*).
- Expected bottleneck: gap functionals are not rearrangement-monotone in
  an obvious way.
- Status: ACTIVE (low confidence).

## Route C: phase / secular critical point analysis
- Family: analytic; 4 equations in (s1,s2,a,b); force b = 1-a.
- Core mechanism: write the critical point conditions
  sin(s_2 a) = c sin(s_1 a),  sin(s_2 b) = -c sin(s_1 b)  with
  c = s_1/s_2, plus the two secular equations for the 3-block config;
  eliminate to derive a symmetric relation, or show the system is
  invariant under (a,b) -> (1-b,1-a) with a unique solution.
- Target obligation: O3a.
- First concrete deliverable: derive the secular equations in closed
  form and count solutions symbolically/numerically as a function of R.
- Fast falsification: find two sign-consistent critical points for some R.
- Expected bottleneck: transcendental system; uniqueness needs a global
  monotonicity statement for the phases.
- Status: ACTIVE.

## Route D: disproof / structure exploration (counterexample hunter)
- Family: computational search with adversarial intent.
- Core mechanism: exhaustive + randomized search of the (a,b) families
  and of higher-block configs, aimed at finding off-center or asymmetric
  maximizers (especially for R near 1, where first-order theory says the
  fixed-width optimal placement is off-center), or at least confirming
  the symmetric conjecture to high numerical confidence.
- Target obligation: O3 (either direction).
- First concrete deliverable: global landscape D(a,b) for R in
  {1.05, 1.1, 1.2, 1.5, 2, 3, 4, 10, 100} with local refinement; report
  argmax and compare with the symmetric value.
- Fast falsification: any off-center argmax.
- Expected bottleneck: none (it is a falsification route).
- Status: ACTIVE.

## Route E: literature audit
- Family: bibliographic.
- Core mechanism: search for published results on max/min of the
  fundamental gap of the vibrating string with box-constrained density
  (pointwise 1<=rho<=R); check Sun 2022, Cheng-Kung-Law-Lian 2010,
  Huang 2007, and later work; determine novelty status.
- Target obligation: O5.
- Status: ACTIVE (background).

## Route F: symmetric 1-parameter estimates (O2)
- Family: analytic 1-parameter.
- Core mechanism: prove h(u) = g(u)/u strictly decreasing via the
  half-problem phase representation, using explicit monotonicity of the
  secular phase in u and in s; or prove d/du (f_sym) > 0 up to the root
  and < 0 after using a sign argument on the derivative identities.
- Target obligation: O2b.
- Status: ACTIVE.
