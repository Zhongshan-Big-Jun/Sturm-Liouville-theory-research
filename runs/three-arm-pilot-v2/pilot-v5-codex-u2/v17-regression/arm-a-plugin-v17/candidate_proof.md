# Candidate proof — stopping-boundary rigorous partial result

This draft carries obligation identifiers.  It is not a completion claim while `O3` and `O4`
remain open.

## 1. Literal construction and conditional lamps (`O1`)

Let `S_0=r` and `S_i=r+xi_1+...+xi_i`, where the increments `xi_i` are independent and
uniform on `{-1,+1}`.  For step `i`, denote the independent fair switch bits at `S_{i-1}` and
`S_i` by `A_i` and `B_i`.  Conditional on the entire base path, all these bits remain mutually
independent.

Assume `t>=1`.  Every visited vertex is switched at least once: `S_0` is switched by `A_1`,
and every `S_i` with `i>=1` is switched on arrival by `B_i`.  The final lamp at a visited
vertex is the chronologically last switch bit assigned to that vertex.  Different vertices
select different variables from the independent family `(A_i,B_i)`, so their final lamps are
mutually independent and fair.  An unvisited lamp is never changed and hence retains its
forced initial value zero.  A nearest-neighbour path visits every integer between its minimum
`L_t` and maximum `U_t`; hence its visited set is exactly `[L_t,U_t] cap Z`.  Therefore,
conditional on the base path—and also conditional only on `(L_t,U_t,S_t)`—the final lamps are
i.i.d. fair on `[L_t,U_t]` and zero outside.

This explicitly accounts for the two all-zero starting configurations: at positive time the
initial base site's zero is overwritten, while zeros at unvisited sites remain forced.  At
`t=0` there is no switch and the preceding fair-lamp assertion is not used.

## 2. Translation and parity

For an integer `a`, let `T_a(eta,z)=(eta_a,z+a)`, where
`eta_a(v)=eta(v-a)`.  Translating every base location and every switch label in the construction
shows `P_t^{T_a s}=T_a P_t^s`.  Since the all-zero configuration is translation invariant,
`y=T_2x` and thus `P_t^y=T_2P_t^x`.

Both starts are even and every base step changes parity.  Consequently both endpoint supports
are `t (mod 2)`; there is no parity mismatch between the two laws.

## 3. Exact visible-hull reduction

For a final state `(eta,z)`, define

`alpha=min(supp(eta) union {z})`, `beta=max(supp(eta) union {z})`,

and `V(eta,z)=(alpha,beta,z)`.  Let

`q_t^r(l,u,z)=Pr_r(L_t=l,U_t=u,S_t=z)`

for the base walk started at `r`.  By Section 1, for `t>=1`,

`P_t^{(0,r)}(eta,z)
 = sum_{l<=min(r,alpha), u>=max(r,beta)} q_t^r(l,u,z) 2^{-(u-l+1)}.`     (3.1)

Indeed, a range `[l,u]` is compatible with the state exactly when it contains the start,
endpoint, and every lit lamp, and a particular zero/one pattern on that range has probability
`2^{-(u-l+1)}`.  Thus the right side depends on `(eta,z)` only through `V(eta,z)`.

Every fiber of `V` is finite.  On a fixed fiber, each of the two point probabilities is
constant, by (3.1).  If the constants are `a_v,b_v` and the fiber size is `n_v`, its
contribution to full `l1` distance is `n_v|a_v-b_v|`, exactly the absolute difference of the
two pushforward masses `n_va_v,n_vb_v`.  Summing fibers proves the exact identity

`||P_t^x-P_t^y||_TV = ||V_*P_t^x-V_*P_t^y||_TV`.                 (3.2)

This is stronger than merely discarding the lamps: the endpoint and outermost lit lamps form
an exact sufficient statistic for distinguishing the two starts.

## 4. Explicit lower bound (`O2`)

Projection to the base endpoint cannot increase total variation: for any event in endpoint
space, its inverse image is a state event.  Let `K` be the number of `+1` increments.  Under
`x`, `K` has probabilities

`p_k=2^{-t} binom(t,k)`, `0<=k<=t`,

and endpoint `2k-t`.  At the same endpoint, the law from `y` has mass `p_{k-1}`, with
`p_{-1}=p_{t+1}=0`.  Since

`p_{k+1}/p_k=(t-k)/(k+1)`,

the sequence increases to its central maximum and then decreases.  Therefore its successive
absolute differences telescope up and down:

`(1/2) sum_{k=0}^{t+1}|p_k-p_{k-1}| = max_k p_k`.                (4.1)

It remains only to lower-bound this maximum explicitly.  We give the elementary argument in
full.  If `X>=0` and `a>0`, then

`E[X] >= E[X 1_{X>=a}] >= a Pr(X>=a)`,

so `Pr(X>=a)<=E[X]/a` (Markov's inequality in the exact form used).  Direct independence gives
`E K=t/2` and `E(K-t/2)^2=t/4`.  Apply the displayed inequality to
`X=(K-t/2)^2` and `a=t` to obtain

`Pr(|K-t/2|>=sqrt(t)) <= 1/4`.

The strict interval `|k-t/2|<sqrt(t)` contains at most `2sqrt(t)+1<=3sqrt(t)` integers for
`t>=1`.  It carries probability at least `3/4`, so

`max_k p_k >= (3/4)/(3sqrt(t)) = 1/(4sqrt(t))`.                 (4.2)

Combining endpoint projection, (4.1), and (4.2) proves

`||P_t^x-P_t^y||_TV >= 1/(4sqrt(t))` for every integer `t>=1`.

Thus the eventual theorem may take `c=1/4`; no external estimate is used.

## 5. A self-contained logarithmic-loss upper bound (`O3-partial`)

For `N>=1`, write `H_N=sum_{k=1}^N 1/k`.  We prove that, for every integer `t>=2`, with
`n=floor(t/2)`,

`||P_t^x-P_t^y||_TV
 <= 1/sqrt(n+1) + 2 H_(n+1)/sqrt(t-n+1)`                       (5.1)

and hence

`||P_t^x-P_t^y||_TV
 <= sqrt(2) [3+2 log(t+1)]/sqrt(t)`.                           (5.2)

This is not the fixed-constant upper bound required by the frozen target.

### 5.1 One-sided survival

Let `R` be simple symmetric random walk from zero and `M_m=max_{0<=j<=m}R_j`.  For integers
`m>=0,a>=1`, reflection after the first visit to `a` maps paths ending at `b<a` that visit `a`
bijectionally to unrestricted paths ending at `2a-b`.  Summing over accessible `b<a` and using
symmetry gives the exact half-open identity

`Pr(M_m<a)=Pr(-a<=R_m<a)`.                                    (5.3)

For `m>=1`, every endpoint atom is at most `1/sqrt(m+1)`.  Here is the complete estimate.  If
`q_m=2^{-m} binom(m,floor(m/2))`, then

`q_(2r)=product_{j=1}^r (2j-1)/(2j)` and `q_(2r)^2<=1/(2r+1)`.

The inequality follows by induction: after multiplying by `((2r+1)/(2r+2))^2`, the next
step is exactly `(2r+1)(2r+3)<=(2r+2)^2`.  Also
`q_(2r+1)=((2r+1)/(2r+2))q_(2r)<=1/sqrt(2r+2)`.  The half-open interval in (5.3) has exactly
`a` accessible sites, so

`Pr(M_m<a)<=a/sqrt(m+1)`.                                     (5.4)

### 5.2 Reflected/coalescing base coupling

Let `X` start at zero and set `tau=inf{j:X_j=1}`.  Until `tau`, put `Y_j=2-X_j`; from `tau`
onward give the two walks the same fresh increments.  At every time, the next increment of `Y`
is either a fresh fair sign or its negative, according to the already observed past.  Thus its
increments are themselves independent fair signs, and `Y` is a simple symmetric walk from two.

Put `D=-min_{0<=j<=tau}X_j`.  Before coalescence the visited intervals are exactly `[-D,1]`
and `[1,D+2]`.  If the common tail visits both `-D` and `D+2`, the endpoint and the two complete
visited intervals agree.  By Section 1, the same fair bits can then be used on that common
interval, coupling the complete frozen lamplighter states.

We need two exact consequences of (5.3).  First,

`Pr(tau>N)<=1/sqrt(N+1)`.                                      (5.5)

Second, for every integer `d>=1`, a first-step recursion in the finite interval `[-d,1]`
shows that the probability, from zero, of hitting `-d` before `1` is `1/(d+1)`: the unique
linear function with boundary values one and zero is `(1-k)/(d+1)`.  Absorption is almost
sure because every block of `d+1` steps has a fixed positive probability of reaching a
boundary.  Hence

`Pr(D>=d)=1/(d+1)`.                                           (5.6)

On `{tau<=N}`, `D<=N`; expanding an integer variable as the sum of its tail indicators yields

`E[(D+1) 1_{tau<=N}] <= 1+sum_{d=1}^N Pr(D>=d)=H_(N+1)`.       (5.7)

Take `n=floor(t/2)` and declare coupling failure if `tau>n`.  On `{tau<=n}`, the fresh common
tail has `m=t-tau>=t-n` steps from site one.  Each required extreme is at distance `D+1`.
By (5.4) on the two sides and a union bound, its conditional probability of missing at least
one extreme is at most

`2(D+1)/sqrt(t-n+1)`.

Equations (5.5) and (5.7) prove that the state-coupling mismatch probability is bounded by the
right side of (5.1).  For any coupling `(V,W)` and event `A`, the discrepancy of the two event
probabilities is at most `Pr(V!=W)`; taking the supremum proves the coupling inequality and
therefore (5.1).

Finally, `H_N<=1+log N`, since `sum_{k=2}^N 1/k<=integral_1^N dx/x`, while
`n+1>=t/2`, `t-n+1>=t/2`, and `n+1<=t+1`.  These inequalities give (5.2).  Both starts are even,
reflection occurs about site one, and coalescence is at site one at an allowed time, so the
coupling respects the common endpoint parity `t mod 2`.

## 6. Exact normalized-range frontier and a falsified shortcut

Let `N_t^0(l,u,z)` be the number of length-`t` base paths from zero to `z` with exact minimum
`l` and maximum `u`.  For `0<=a,j<=r`, set

`h_t^r(a,j)=N_t^0(-a,r-a,j-a)`,                               (6.1)

and set it to zero outside that index range.  At the actual triple `(l,u,z)`, put
`r=u-l`, `a=-l`, `j=z-l`.  Translation by two changes the normalized starting coordinate from
`a` to `a+2` but leaves `(r,j)` fixed.  Since each base path has mass `2^{-t}`, summing all
actual triples gives the exact identity

`||Law_0(L_t,U_t,S_t)-Law_2(L_t,U_t,S_t)||_TV
 = 2^{-t-1} sum_{r=0}^t sum_{j=0}^r sum_{a in Z}
     |h_t^r(a,j)-h_t^r(a+2,j)|`.                             (6.2)

By the common conditional-lamp kernel of Section 1, this triple TV upper-bounds the full-state
TV.  Thus an explicit fixed `C_*` and threshold in

`sum_{r,j,a}|h_t^r(a,j)-h_t^r(a+2,j)| <= 2 C_* 2^t/sqrt(t)`    (6.3)

would be a sufficient proof of the still-open frozen upper bound.

The simplest proposed proof of (6.3) is false.  Exact killed-walk recurrence and
inclusion-exclusion give, at `t=10,r=4,j=2`, the accessible-parity values

`(h_10^4(0,2),h_10^4(2,2),h_10^4(4,2))=(26,16,26)`.

Hence the slice is V-shaped, not unimodal; its translated differences do not have one sign.
The replay check is `python3 reproducibility/verify_route_claims.py`.

## 7. Strongest exact partial theorem and first unresolved obligation

Combining Sections 4 and 5 proves, for every integer `t>=2`,

`1/(4sqrt(t)) <= ||P_t^x-P_t^y||_TV
 <= 1/sqrt(floor(t/2)+1)
    + 2H_(floor(t/2)+1)/sqrt(ceil(t/2)+1)`.                   (7.1)

The upper bound is `O(log(t)/sqrt(t))`, not the requested `C/sqrt(t)`.  The first unresolved
load-bearing obligation is a fixed-constant full-state upper bound.  Inequality (6.3) is one
explicit sufficient subobligation; the counterexample above shows that parity-class
unimodality cannot prove it.
