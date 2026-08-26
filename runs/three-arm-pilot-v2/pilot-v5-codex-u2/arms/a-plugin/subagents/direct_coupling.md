FALSIFIED

# Reflection-then-synchronization is intrinsically logarithmically too weak

## Result and scope

The usual base reflection coupling, followed after the first meeting by synchronous
increments, cannot prove the required `C/sqrt(t)` full-state bound.  This remains
true even if, conditional on the paired base paths, the two terminal lamp
configurations are coupled maximally rather than by matching individual switch
coins.

More precisely, let `F_t` be the mismatch probability of the exact coupling
defined below.  It is the smallest possible mismatch probability among all lamp
couplings which use this fixed paired-base-path law and which, for every paired
base path, give each lamp configuration its correct conditional marginal.  With
natural logarithms,

`(log t)/(128 sqrt(t)) <= F_t <= (2 log t+15)/sqrt(t)`

for every integer `t >= ceil(exp(198))` in the lower bound and every integer
`t >= 16` in the upper bound.  Thus no fixed constant `C` can make
`F_t <= C/sqrt(t)` for all large `t`.

This falsifies only the reflection-then-synchronization route (including its
optimal conditional lamp repair), not obligation `O3` itself.  A coupling that
jointly rearranges the paired base paths, or that does not retain the conditional
lamp marginals after revealing both base paths, is not covered by the obstruction.

Along the way, the argument proves the exact conditional lamp kernel required in
`O1` and gives an explicit marginal-preserving full-state coupling with the weaker
`O(log(t)/sqrt(t))` mismatch bound.

## 1. Exact lamp kernel, including the forced zeros

Fix one deterministic nearest-neighbour base path

`z_0,z_1,...,z_t`,

with `t>=1`.  In step `n`, let the departure resampling coin at `z_n` be
`A_n` and the arrival resampling coin at `z_{n+1}` be `B_n`.  All these coins
are independent fair bits.  Every visited site receives a resampling: `z_0`
receives `A_0`, while `z_n`, `n>=1`, receives `B_{n-1}`.  The terminal bit at a
visited site is the last resampling coin attached to that site.  Last coins
selected for distinct sites are distinct members of the independent coin family.
Consequently the terminal bits at the visited sites are independent fair bits.
All unvisited sites retain their initial value zero.

Because a one-dimensional nearest-neighbour path visits every integer between
its minimum `L` and maximum `U`, its visited set is exactly `[L,U]`.  Therefore,
conditional on the base path, the terminal lamp law is

`mu_[L,U] := uniform bits on [L,U], zero off [L,U]`.

It depends on the path only through `[L,U]`.  In particular, the forced initial
zero at 0 or at 2 causes no exception when `t>=1`: the departure switch at time
zero resamples that starting lamp.  Repeated visits cause no exception because
only the last independent resampling coin matters.  At `t=0` there is no
resampling, both configurations are forced zero, and the distinct endpoints make
the two full states different with probability one.

## 2. Optimal coupling of two interval lamp kernels

For finite integer intervals `I,J`, the overlap coefficient of `mu_I` and
`mu_J` is

`alpha(I,J) = sum_eta min(mu_I(eta),mu_J(eta))`

`             = 2^(|I intersect J|-max(|I|,|J|))`

`             = 2^(-max(|I\J|,|J\I|))`.                         (2.1)

Indeed, the common support consists exactly of configurations which are zero off
`I intersect J`; it has `2^|I intersect J|` elements, and the smaller point mass
there is `2^(-max(|I|,|J|))`.

This overlap is attained by the following explicit maximal coupling.  Put
`alpha=alpha(I,J)` and let `rho` be the uniform law on configurations supported
in `I intersect J`.  Decompose

`mu_I = alpha rho + (1-alpha) mu_I'`,

`mu_J = alpha rho + (1-alpha) mu_J'`.

With probability `alpha`, draw one configuration from `rho` and use it for both
chains.  Otherwise draw from the two residual marginals (independently, for
example).  The residual supports are disjoint, so equality occurs with probability
exactly `alpha`.  This proves both attainability and optimality.  It also handles
`I=J`, when `alpha=1`.

## 3. The exact reflection/synchronous full-state coupling

Let `X_0=0` and `Y_0=2`.  Until their first meeting, use opposite increments:
conditionally on the joint past, choose `(+1,-1)` or `(-1,+1)`, each with
probability `1/2`.  Thus, before meeting, `Y_n=2-X_n`.  Put

`tau = inf{n>=0:X_n=Y_n} = inf{n>=0:X_n=1}`.

At and after the meeting, give the two walks the same fresh fair increments.
Each coordinate increment is conditionally fair at every step, hence each base
coordinate is exactly a simple random walk with its stated start.  (Equivalently,
the pre-meeting sign sequence for either coordinate is a sequence of independent
Rademacher variables, and the post-meeting sequence is fresh and independent.)
The common parity of the two starts is essential here: the meeting is at 1 and
`tau` is odd.

On `{tau<=t}`, define

`A = -min_{0<=n<=tau} X_n`,  `D=A+1`,  `N=t-tau`,

and write the common post-meeting displacement from 1 as

`W_s=X_(tau+s)-1=Y_(tau+s)-1`, `0<=s<=N`.

Let `m=min_s W_s` and `M=max_s W_s`.  Relative to the meeting point 1, the two
terminal visited intervals are

`I_X = [min(-D,m), M]`,

`I_Y = [m, max(D,M)]`.                                      (3.1)

Their exclusive-site counts are consequently

`ell=|I_X\I_Y|=(D+m)_+`,  `r=|I_Y\I_X|=(D-M)_+`.             (3.2)

Conditional on the paired base paths, apply the maximal lamp coupling of Section
2.  If `tau>t`, the endpoints differ and the states cannot agree.  If `tau<=t`,
the endpoints agree and (2.1)-(3.2) show that the conditional mismatch probability
is `1-2^(-max(ell,r))`.  Therefore the exact total mismatch probability is

`F_t = P(tau>t)`

`      + E[1_{tau<=t} {1-2^(-max((D+m)_+,(D-M)_+))}].`       (3.3)

This is a coupling of terminal full states, not merely of triples.  Its marginals
are exact: the bases were audited above, and for every paired pair of paths the
lamp marginals are exactly the interval kernels proved in Section 1.  If a literal
switch-coin realization is desired, assign the sampled terminal bits to the last
resampling coins at their sites and fill all earlier coins with fresh independent
fair bits.  Within either chain this recovers the required independent switch
family and is independent of its base path.

The maximal-overlap calculation also proves that (3.3) is optimal after the paired
base paths have been revealed: no other coupling with the correct two conditional
lamp marginals can have a smaller conditional mismatch probability.

## 4. Elementary hitting estimates

Let `S` be simple random walk from 0 and `T_k=inf{n:S_n=k}`, `k>=1`.  If
`p_n(j)=P(S_n=j)`, reflection at the first visit to `k` gives, with parity retained,

`P(T_k>n)=P(-k<=S_n<k).`                                    (4.1)

To verify (4.1), for each `j<k` reflection bijects paths which hit `k` and end at
`j` with unrestricted paths ending at `2k-j>k`.  Sum over `j<k` and use symmetry.
The half-open interval in (4.1) contains exactly `k` integers of the parity
reachable at time `n`.

Two explicit atom bounds will be used.  If `p_n^*=max_j p_n(j)`, then

`p_n^* <= sqrt(2/n)` for `n>=1`.                             (4.2)

For even `n=2q`, put `a_q=binom(2q,q)/4^q`.  Induction using
`a_(q+1)/a_q=(2q+1)/(2q+2)` and

`((2q+1)/(2q+2))^2 <= (q+1)/(q+2)`

gives `a_q<=1/sqrt(q+1)`.  The odd-time modal atom is smaller than the preceding
even-time modal atom, proving (4.2).

For `n>=16`, `1<=k<=floor(n^(1/4))`, and every reachable `j` with `|j|<=k`,

`p_n(j) >= 1/(8 sqrt(n)).`                                  (4.3)

Here is a self-contained proof.  Chebyshev gives
`P(|S_n|<2 sqrt(n))>=3/4`.  That interval contains at most `2 sqrt(n)+1`, hence
at most `3 sqrt(n)`, reachable atoms.  Unimodality therefore gives
`p_n^*>=1/(4 sqrt(n))`.  Moving `r` lattice positions of spacing two away from a
mode gives a ratio which is a product of factors `1-b_i`, with

`sum_i b_i <= r(r+1)/floor(n/2)
             <= 3/(4 sqrt(n))+3/(2 n^(3/4)) <= 1/2`.

Since `prod_i(1-b_i)>=1-sum_i b_i`, the ratio to the modal atom is at least
`1/2`, proving (4.3).  Combining (4.1) and (4.3) yields

`P(T_k>n) >= k/(8 sqrt(n))`

whenever `n>=16` and `k<=floor(n^(1/4))`.                    (4.4)

Finally, the pre-meeting depth in Section 3 has the exact law

`P(D>=k)=1/k`,  `P(D=k)=1/(k(k+1))`, `k>=1`.                (4.5)

Indeed, `D>=k` is the event that a walk from 0 hits `-(k-1)` before 1, whose
gambler's-ruin probability is `1/k`.  Subtraction gives the mass formula.  The
same finite-interval gambler's-ruin calculation, followed by a limit, also shows
`tau<infinity` almost surely.  In particular the post-meeting walk is independent
of `D` by the fresh-increment construction.

For `k=1`, (4.1) contains exactly one modal atom, so

`P(tau>n)=P(T_1>n)=p_n^* <= sqrt(2/n)`.                      (4.6)

All formulas (4.1)-(4.6) retain even/odd parity; no parity-smoothed local limit
theorem is being used.

## 5. Logarithmic lower bound: the route is falsified

Fix `t>=16`, put `n=floor(t/2)` and `K=floor(t^(1/4))`, and define
`h_t(k)=P(T_k>t)`.  If `tau<=n` and the common post-meeting walk has not hit `D`
by time `t`, then it certainly has not hit `D` during its actual `N=t-tau`
steps whenever the event `T_D>t` occurs.  On that event `M<D`, so `r>=1` in
(3.2).  Even the maximal conditional lamp coupling then mismatches with
probability at least `1/2`.  Independence of the fresh post-meeting walk gives

`F_t >= (1/2) E[1_{tau<=n} h_t(D)]`

`    >= (1/2) {E[h_t(D)]-P(tau>n)}.`                         (5.1)

By (4.4)-(4.5),

`E[h_t(D)] >= (1/(8 sqrt(t))) sum_{k=1}^K 1/(k+1)`

`             >= {log(t)/32-log(2)/8}/sqrt(t)`.             (5.2)

For the last inequality, compare the harmonic sum with
`integral_2^(K+2) dx/x` and use `K+2>=t^(1/4)`.  By (4.6) and
`floor(t/2)>=t/3`,

`P(tau>n) <= 3/sqrt(t)`.                                    (5.3)

Equations (5.1)-(5.3) imply

`F_t >= {log(t)/64-log(2)/16-3/2}/sqrt(t)`.

If `t>=ceil(exp(198))`, the right side is at least
`log(t)/(128 sqrt(t))`.  Hence `sqrt(t) F_t` is unbounded, rigorously ruling out
an `O(t^(-1/2))` estimate for this coupling class.

The failure mechanism is precisely the residual pre-meeting lamps.  The depth
has harmonic tail (4.5); a post-meeting walk of length `t` fails to reach depth
`k` with probability of order `k/sqrt(t)`; summing
`[1/(k(k+1))][k/sqrt(t)]` over `k<=t^(1/4)` produces `log(t)/sqrt(t)`.  Merely
coupling the meeting-site arrival switch, or all later switches, does not touch
the exclusive sites in (3.2).

## 6. Matching logarithmic upper bound for the same exact coupling

For completeness, (3.3) also gives a fully explicit upper bound.  On
`{tau<=floor(t/2)}`, a mismatch can occur only if the post-meeting walk fails to
hit `D` or `-D`; otherwise (3.1) gives identical intervals and the maximal lamp
coupling agrees surely.  By a union bound, symmetry, (4.1)-(4.2), and
`t-tau>=ceil(t/2)`,

`F_t <= P(tau>floor(t/2))
       +2 E[min(1,2D/sqrt(t))]`.                             (6.1)

Put `J=floor(sqrt(t)/2)`.  From (4.5), for `t>=16`,

`E[min(1,2D/sqrt(t))]`

` <= (2/sqrt(t)) sum_{k=1}^J 1/(k+1) + P(D>J)`

` <= {log(t)+6}/sqrt(t)`.                                   (6.2)

Together with (5.3), this proves

`F_t <= {2 log(t)+15}/sqrt(t)` for every integer `t>=16`.    (6.3)

Thus the logarithmic loss is sharp up to numerical constants for the audited
reflection/synchronous base pairing with optimal conditional lamps.

## 7. Boundary and interface audit

- `t=0`: no switch occurs; endpoints 0 and 2 differ, so mismatch and total
  variation are both 1.
- `t>=1`: both forced-zero starting lamps are resampled before the first move.
- Meeting parity: both bases have the same parity at every common time; under
  reflection they meet at 1 at an odd time.  Hitting identities use the exact
  reachable parity class.
- Meeting switches: the two arrival switches at the meeting may be coupled, but
  doing so cannot repair lamps at exclusive pre-meeting sites.  Conditional
  maximal coupling already makes the best possible joint choice of all terminal
  lamps.
- Repeated visits: the last-resampling proof selects distinct independent last
  coins for distinct sites.
- Marginals: every base increment is fair conditional on its coordinate past;
  every conditional lamp marginal is exactly `mu_[L,U]`; no path-dependent bias
  is introduced.
- Exact unresolved obligation: construct a different full-state coupling with
  mismatch `O(1/sqrt(t))`, or prove the corresponding translated range-triple
  `L1` bound and lift a maximal triple coupling through the common lamp kernel.
  The present result supplies neither and therefore does not close `O3`.

## Verification record

- Input hashes checked locally:
  `problem_contract.md` =
  `98d6ea8d4da0a5f121c36d7c0b2cc895ec81d7b30f6e9b2d079f212825f667f5`;
  `obligation_graph.md` =
  `8a4d374f01eae3a16538116bc2f152bef57af5b24ca2673a1092c6cfd3a5db35`.
- Proof is self-contained and uses no internet, external file, local-limit
  theorem, or unrecorded computation.
- Self-audit verdict for the claimed route obstruction: `PASS`; an independent
  verifier was not run in this subtask.
- Self-audit verdict for global obligation `O3`: `UNCERTAIN`; it remains open
  here.
