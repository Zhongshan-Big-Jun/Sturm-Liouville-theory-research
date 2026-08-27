# Candidate proof (live draft)

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

## 5. Full-state upper bound (`O3`)

Open at this draft stage.  Any completed version must insert an explicit uniform upper bound
for the full law (equivalently, by (3.2), the visible-hull law) and then pass `O4`.
