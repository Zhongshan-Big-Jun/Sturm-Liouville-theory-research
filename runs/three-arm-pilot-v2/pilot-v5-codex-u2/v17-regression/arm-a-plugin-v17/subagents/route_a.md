# Route A: reflected path coupling, an exact logarithmic gap, and its obstruction

## Status and scope

This artifact addresses `SUB-O3-routeA` only.  Write

\[
T_t=(L_t,U_t,S_t),\qquad
L_t=\min_{0\leq j\leq t}S_j,\quad U_t=\max_{0\leq j\leq t}S_j,
\]

for length-`t` simple symmetric random walk started at zero, and let
`T_t+2=(L_t+2,U_t+2,S_t+2)`.  The result proved here is the explicit partial
bound

\[
 \boxed{\quad
 \|\mathcal L(T_t)-\mathcal L(T_t+2)\|_{\rm TV}
 \leq {1\over\sqrt{n+1}}+{2H_{n+1}\over\sqrt{t-n+1}},
 \qquad n=\lfloor t/2\rfloor,\ t\geq2,\quad}                 \tag{1}
\]

where `H_N=sum_{k=1}^N 1/k`.  In particular,

\[
 \|\mathcal L(T_t)-\mathcal L(T_t+2)\|_{\rm TV}
 \leq {\sqrt2\,[3+2\log(t+1)]\over\sqrt t}.                 \tag{2}
\]

The same bounds hold for the total-variation distance of the two frozen
switch-walk-switch final states, by the lamp coupling in Section 5.

This does **not** prove the requested constant-over-`sqrt(t)` upper bound.  In
fact, Section 6 proves that the failure probability of this particular reflected
coupling is at least a constant times `log(t)/sqrt(t)`.  Thus the harmonic loss
in (1) cannot be removed merely by sharpening estimates of this coupling.

No external result is invoked below: all random-walk estimates used in the proof
are proved explicitly.

## 1. Two elementary walk lemmas

For a simple symmetric walk `R` started at zero, set
`M_m=max_{0<=j<=m} R_j` and let

\[
 p_m(b)=\mathbb P(R_m=b).
\]

### Lemma 1 (exact one-sided survival identity)

For integers `m>=0` and `a>=1`,

\[
 \mathbb P(M_m<a)=\mathbb P(-a\leq R_m<a).                  \tag{3}
\]

Consequently, for `m>=1`,

\[
 \mathbb P(M_m<a)\leq {a\over\sqrt{m+1}}.                 \tag{4}
\]

**Proof.**  Fix an accessible endpoint `b<a`.  Reflection of the part of a
path after its first visit to `a` is a bijection from paths which visit `a` and
end at `b` to unrestricted paths ending at `2a-b`.  Therefore the number of
paths avoiding `a` and ending at `b` is

\[
 2^m[p_m(b)-p_m(2a-b)].
\]

Summing over accessible `b<a`, the second endpoints range over all accessible
integers strictly greater than `a`.  Hence

\[
 \mathbb P(M_m<a)=\mathbb P(R_m<a)-\mathbb P(R_m>a).
\]

Symmetry, `p_m(b)=p_m(-b)`, turns the right side into (3), including the
possible atom at `-a` and excluding the possible atom at `a`, exactly as the
half-open interval states.

The accessible integers in `[-a,a)` have spacing two, so there are exactly
`a` of them.  It remains to bound the largest atom.  Put

\[
 q_m=2^{-m}{m\choose\lfloor m/2\rfloor}.
\]

For even `m=2r`,

\[
 q_{2r}=\prod_{j=1}^r{2j-1\over2j},\qquad
 q_{2r}^2\leq {1\over2r+1}.                                \tag{5}
\]

The inequality follows by induction from equality at `r=0`: multiplication by
`((2r+1)/(2r+2))^2` preserves it because
`(2r+1)(2r+3)<=(2r+2)^2`.  Also
`q_{2r+1}=((2r+1)/(2r+2))q_{2r}`, so (5) gives
`q_{2r+1}<=1/sqrt(2r+2)`.  Thus, for every `m>=1`,
`max_b p_m(b)=q_m<=1/sqrt(m+1)`.  Combining this with (3) proves (4).  \(\square\)

### Lemma 2 (depth before first hitting `1`)

Let

\[
 \tau=\inf\{j\geq0:S_j=1\},\qquad
 D=-\min_{0\leq j\leq\tau}S_j.
\]

Then `tau<infinity` almost surely and, for every integer `d>=1`,

\[
 \mathbb P(D\geq d)={1\over d+1}.                          \tag{6}
\]

Moreover, for every integer `N>=0`,

\[
 \mathbb E[(D+1){\bf1}_{\{\tau\leq N\}}]\leq H_{N+1}.    \tag{7}
\]

**Proof.**  Lemma 1 with `a=1` gives
`P(tau>m)<=1/sqrt(m+1)`, so `tau` is finite almost surely.

Before hitting `1`, the event `D>=d` is exactly the event that the walk hits
`-d` before `1`.  Let `h(k)` be this probability from `k` in the finite interval
`[-d,1]`.  Absorption occurs almost surely: from any interior state there is a
specified sequence of at most `d+1` steps reaching a boundary, of probability
at least `2^{-(d+1)}`, so survival through successive blocks of `d+1` steps is
at most geometric.  First-step conditioning gives

\[
 h(-d)=1,\quad h(1)=0,\quad h(k)={h(k-1)+h(k+1)\over2}.
\]

The successive differences of `h` are therefore constant, and the boundary
values give `h(k)=(1-k)/(d+1)`.  In particular `h(0)=1/(d+1)`, proving (6).

On `{tau<=N}`, one has `D<=N`.  The tail-sum formula for a nonnegative
integer-valued variable, which follows by writing
`D=sum_{d>=1} 1_{D>=d}`, and (6) yield

\[
\begin{aligned}
 \mathbb E[(D+1){\bf1}_{\{\tau\leq N\}}]
 &\leq 1+\sum_{d=1}^N\mathbb P(D\geq d)\\
 &=1+\sum_{d=1}^N{1\over d+1}=H_{N+1}.
\end{aligned}
\]

This is (7).  \(\square\)

## 2. The reflected/coalescing coupling

Construct `X` as simple symmetric random walk from zero.  Until

\[
 \tau=\inf\{j:X_j=1\},
\]

put `Y_j=2-X_j`.  At and after `tau`, use the same future increments and put
`Y_j=X_j`.  More explicitly, before `tau` the increments of `Y` are the
negatives of those of `X`; after `tau` they equal those of `X`.  Negating fair
independent signs up to a stopping time and then using fresh fair independent
signs leaves a sequence of fair independent signs.  This can also be checked
directly: for any prescribed finite sign string, condition successively on the
past; the next `Y` sign is either a fresh `X` sign or its negative, and in either
case has conditional probabilities `1/2,1/2`.  Thus `Y` is a simple symmetric
walk started at two.

Let

\[
 D=-\min_{0\leq j\leq\tau}X_j.
\]

Before coalescence the two visited intervals are exactly

\[
 [-D,1]\quad\hbox{for }X,\qquad [1,D+2]\quad\hbox{for }Y.  \tag{8}
\]

After `tau` their paths and endpoints agree.  Therefore their full triples at
time `t` agree if the common tail `X_tau,...,X_t` visits both `-D` and `D+2`.
Indeed, on that event both intervals in (8) are contained in the common tail
range, and the endpoint is common.  Conversely, for this coupling, triple
agreement requires both visits: if the tail minimum is `A` and maximum is `B`,
then the two final intervals are

\[
 [\min(-D,A),B]\quad\hbox{and}\quad[A,\max(D+2,B)],
\]

so equality forces `A<=-D` and `B>=D+2`.

## 3. Proof of the explicit upper bound

Fix `t>=2` and put `n=floor(t/2)`.  Declare failure immediately on `{tau>n}`.
On `{tau<=n}`, conditional on the path through `tau`, the common tail relative
to its starting point `1` is a fresh simple symmetric walk of length
`m=t-tau`, and the two required levels are at distances

\[
 a=D+1
\]

on its two sides.  By Lemma 1 and a union bound, the conditional probability
that the tail misses at least one of the two levels is at most

\[
 {2(D+1)\over\sqrt{m+1}}
 \leq {2(D+1)\over\sqrt{t-n+1}}.                            \tag{9}
\]

Lemma 1 with `a=1` and Lemma 2 now give

\[
\begin{aligned}
 \mathbb P(\hbox{the triples fail to agree})
 &\leq \mathbb P(\tau>n)
  +{2\mathbb E[(D+1){\bf1}_{\{\tau\leq n\}}]
       \over\sqrt{t-n+1}}\\
 &\leq {1\over\sqrt{n+1}}+{2H_{n+1}\over\sqrt{t-n+1}}.    \tag{10}
\end{aligned}
\]

The coupling inequality in the exact form used here is elementary: for any
coupling `(V,W)` and event `A`,

\[
 |\mathbb P(V\in A)-\mathbb P(W\in A)|
 \leq\mathbb P(V\ne W);
\]

taking the supremum over `A` gives
`||L(V)-L(W)||_TV<=P(V!=W)`.  Applying it to the triples proves (1).

Finally, `H_N<=1+log N`, because
`sum_{k=2}^N 1/k <= integral_1^N dx/x`.  Also
`n+1>=t/2`, `t-n+1>=t/2`, and `n+1<=t+1`.  Substitution in (1) proves (2).

Parity causes no hidden singularity here.  Both endpoints have parity `t`
because the two starts are even.  Reflection about `1` and coalescence at the
odd site `1` preserve the correct time-dependent parity for both walks.

## 4. Why the harmonic loss is intrinsic to this coupling

This section proves a coupling-specific lower bound.  It is not a lower bound
on total variation, because a different coupling may be better.

### Lemma 3 (a local lower survival estimate)

If `m>=256` and `1<=a<=sqrt(m)/16`, then

\[
 \mathbb P(M_m<a)\geq {a\over4\sqrt m}.                    \tag{11}
\]

**Proof.**  First, the largest endpoint atom `q_m` satisfies
`q_m>=1/(2sqrt(m))`.  For `m=2r`, induction gives

\[
 q_{2r}=\prod_{j=1}^r{2j-1\over2j}\geq {1\over\sqrt{4r}}
 \qquad(r\geq1),                                           \tag{12}
\]

because the induction step is equivalent to
`(2r+1)^2>=4r(r+1)`.  For odd `m=2r+1`, one has exactly
`q_{2r+1}=q_{2r+2}`, and (12) gives the asserted weaker bound.

Every accessible `s` in `[-a,a)` is at distance at most `a` from zero.  Moving
in steps of two from a central accessible endpoint toward `s`, consecutive
binomial atoms have ratio

\[
 {p_m(u+2)\over p_m(u)}={m-u\over m+u+2}
 \geq1-{2a+2\over m}
\]

(use symmetry on the negative side).  At most `(a+1)/2` ratios occur.  The
elementary product inequality `prod(1-x_i)>=1-sum x_i`, proved by induction,
therefore gives

\[
 p_m(s)\geq q_m\left(1-{(a+1)^2\over m}\right)\geq {q_m\over2}.
\]

The last inequality uses `a<=sqrt(m)/16` and `m>=256` (indeed
`a+1<=sqrt(m)/8`).  Identity (3) sums exactly `a` such atoms, so (11) follows
from `q_m>=1/(2sqrt(m))`.  \(\square\)

Let `F_t` be the probability that the two triples in the reflected coupling
fail to agree.  For `t>=512`, put

\[
 n=\lfloor t/2\rfloor,\qquad R=\left\lfloor{\sqrt n\over16}\right\rfloor.
\]

From (6), for `k>=1`,

\[
 \mathbb P(D+1=k)={1\over k(k+1)}.                          \tag{13}
\]

Consequently,

\[
\begin{aligned}
 \mathbb E[(D+1){\bf1}_{\{D+1\leq R,\ \tau\leq n\}}]
 &\geq \sum_{k=1}^R {1\over k+1}-R\mathbb P(\tau>n)\\
 &\geq H_{R+1}-1-{1\over16}
   =H_{R+1}-{17\over16}.                                  \tag{14}
\end{aligned}
\]

For each history counted on the left of (14), the remaining length
`m=t-tau` lies between `n` and `t`, and `a=D+1<=R<=sqrt(m)/16`.  Failure of the
tail to hit the upper required level alone implies triple disagreement.  Lemma
3 and `m<=t` therefore show

\[
 \boxed{\quad
 F_t\geq {H_{R+1}-17/16\over4\sqrt t},
 \qquad t\geq512.\quad}                                    \tag{15}
\]

Since `H_N>=log(N+1)` (compare the sum with the integral of `1/x`), the
quantity `sqrt(t) F_t` is unbounded.  Thus no estimate of the form
`F_t<=C/sqrt(t)` with fixed `C` is true for this reflected/coalescing coupling.
The obstruction is exact: the pre-meeting depth has tail `1/(d+1)`, and asking
the common tail to erase both reflected extremes weights that depth linearly,
producing the harmonic sum.

## 5. Triple agreement is sufficient for the frozen lamps

This interface uses the literal switch-walk-switch rule and both forced initial
all-zero configurations.

Fix any nearest-neighbour base path `s_0,...,s_t` with `t>=1`.  Its visited set
is the integer interval `[min_j s_j,max_j s_j]`.  The initial site `s_0` is
resampled before the first move.  Each later newly visited site is an arrival
site and is resampled after that move.  Hence every visited site is resampled
at least once.  For each visited site, select its chronologically last switch.
These selected switches are distinct members of the independent family of
fair resampling bits.  Therefore, conditional on the entire base path, the
final lamps on the visited interval are mutually independent fair bits.  Every
lamp outside it was never switched and remains its forced initial zero.

This conditional law depends on the path only through `(L_t,U_t)`.  Thus, on
the event that the coupled base triples agree, sample one family of independent
fair bits on their common interval and use it for both final lamp
configurations.  Their base endpoints already agree, so the complete final
lamplighter states agree.  Off the triple-agreement event, use any coupling of
the two conditional lamp laws.  This constructs the correct final marginal
law for each frozen chain and proves that the right sides of (1) and (2) also
upper-bound

\[
 \|P_t^{(0,0)}-P_t^{(0,2)}\|_{\rm TV}.
\]

Here `(0,2)` has been used only as the all-zero configuration with base at
`2`; no lamp at `2` is initially lit.  Spatial translation by two identifies
the second base-triple law with `L(T_t+2)`.  The restriction `t>=2` in (1)
also avoids the `t=0` exception, when the initial site has not yet been
resampled.

## 6. Exact remaining gap and decision delta

The strongest exact result from this route is (1), an
`O(log(t)/sqrt(t))` full-state upper bound with explicit constants and valid
integer threshold `t>=2`.  Bound (15) proves that the coordinator's reflected
two-extreme-coverage coupling itself cannot remove the logarithm.

The first unresolved obligation is:

> Construct a different coupling, or prove a direct signed-count cancellation,
> that bounds the triple-law total variation by `C_A/sqrt(t)` with fixed explicit
> `C_A`; equivalently, avoid paying the linear erase-cost `D+1` against the
> harmonic pre-meeting depth distribution.

Accordingly, Route A remains `PARTIAL`: it narrows `O3` to one logarithmic
factor and rules out closure by mere constant optimization of the reflected
coverage argument, but it neither proves nor refutes the claimed
constant-over-`sqrt(t)` triple bound.
