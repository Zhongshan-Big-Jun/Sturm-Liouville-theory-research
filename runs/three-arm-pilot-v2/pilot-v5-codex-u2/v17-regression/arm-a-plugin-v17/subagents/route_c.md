# Route C — exact state masses and a reflected-range bound

## Status and scope

`SUB-O3-routeC` is **PARTIAL**.  This note gives:

1. an exact finite formula for every full-state mass and for the full-state total
   variation, with the forced initial zero lamps treated literally;
2. an exact normalized-range formula for the translated triple total variation;
3. a coupling proof of an explicit full-state
   `O((1+log t)/sqrt(t))` upper bound; and
4. an exact counterexample to the simplest unimodality/sign argument that would remove
   the logarithm.

It does not prove the required `C/sqrt(t)` upper bound.  The first unresolved obligation is
the sign-sensitive normalized-range array estimate displayed in the last section.

## 1. Exact path and state masses

For a starting base point `s`, let

`N_t^s(ell,u,z)`

be the number of length-`t` nearest-neighbour paths `S` with `S_0=s`, `S_t=z`,
`min_{0<=k<=t} S_k=ell`, and `max_{0<=k<=t} S_k=u`.  It is zero unless all of
`ell<=s,z<=u` hold.  For `t>=1`, if `A` is the finite set of lamps which are one in the
final configuration, then

```text
p_t^s(A,z)
 = 2^{-t} sum_{ell,u: A subseteq [ell,u]}
       N_t^s(ell,u,z) 2^{-(u-ell+1)}.                 (1)
```

Proof.  A fixed base path has probability `2^{-t}`.  Its visited set is the integer
interval `[ell,u]`.  In the switch-walk-switch chain, the initial site is switched before
the first move, and every later visited site is switched upon arrival.  Therefore, when
`t>=1`, every visited site has at least one resampling.  At each site take the
chronologically last resampling variable.  These variables are distinct members of the
independent family of switch variables, so the final lamps on `[ell,u]` are independent
fair bits.  Lamps outside `[ell,u]` retain their forced initial value zero.  Thus the
conditional probability of precisely `A` is `2^{-(u-ell+1)}` if `A subseteq [ell,u]`,
and zero otherwise.  Summing over base paths proves (1).  Notice that this proof does not
replace resampling by a different lamp convention.

The path counts themselves have a finite inclusion-exclusion formula.  Let
`K_t^{[ell,u]}(s,z)` count paths from `s` to `z` which stay in `[ell,u]`, and declare it
zero if the interval is empty or either endpoint is outside the interval.  Then

```text
N_t^s(ell,u,z)
 = K_t^{[ell,u]}(s,z) - K_t^{[ell+1,u]}(s,z)
   - K_t^{[ell,u-1]}(s,z) + K_t^{[ell+1,u-1]}(s,z).   (2)
```

Indeed, (2) is inclusion-exclusion for visiting both boundary sites.  It is completely
reproducible from

```text
K_0^{[ell,u]}(v,z)=1_{v=z},
K_{n+1}^{[ell,u]}(v,z)
 = K_n^{[ell,u]}(v-1,z)+K_n^{[ell,u]}(v+1,z),         (3)
```

with values outside the interval set to zero.

For a compact exact full-state TV formula, define

```text
F_t^s(m,M;z)
 = 2^{-t} sum_{ell<=m, u>=M}
       N_t^s(ell,u,z) 2^{-(u-ell+1)}.                 (4)
```

Then (1) says

```text
p_t^s(A,z)=F_t^s(min(A union {s,z}),
                 max(A union {s,z});z),               (5)
```

where for `A=empty` the extrema are just those of `{s,z}`.  Translation gives, exactly,

```text
N_t^2(ell,u,z)=N_t^0(ell-2,u-2,z-2).                  (6)
```

There is no lit lamp in (6): translating the all-zero configuration leaves it all zero.

Let `D_t={-t,-t+1,...,t+2}` and
`E_t={-t,-t+2,...,t+2}`.  For `p<=q`, put

```text
kappa(p,q)=1                    if p=q,
kappa(p,q)=2^{q-p-1}            if p<q.
```

All nonempty lamp sets with minimum `p` and maximum `q` have the same two masses in (5),
and there are exactly `kappa(p,q)` of them.  Consequently the desired full-state TV is
the following finite exact sum:

```text
(1/2) sum_{z in E_t} [
  |F_t^0(min(0,z),max(0,z);z)-F_t^2(min(2,z),max(2,z);z)|
  + sum_{p<=q; p,q in D_t} kappa(p,q)
      |F_t^0(min(p,0,z),max(q,0,z);z)
       -F_t^2(min(p,2,z),max(q,2,z);z)| ].            (7)
```

Terms corresponding to unreachable sets automatically vanish.  Thus (2)--(7) reduce the
full-state comparison to polynomially many integer recurrences; no enumeration of the
`2^{|D_t|}` configurations is needed.

At `t=0`, (1) is deliberately not used: no switch occurs, and the two laws are distinct
point masses, so TV is one.  As a check at `t=1`, each law has eight equiprobable states.
The only common endpoint is `1`; the ranges are `[0,1]` and `[1,2]`, and equality of the
configurations forces the lamps at `0` and `2` both to be zero.  There are two common
states (the lamp at `1` is arbitrary), each of mass `1/8`.  Hence the exact full-state TV
is `1-2/8=3/4`.  In contrast, the two range triples are disjoint and have TV one.  This
also checks parity and shows that passing through the triple kernel can be a strict loss.

## 2. Exact normalized-range translation formula

For `0<=a,j<=r`, define

```text
h_t^r(a,j)=N_t^0(-a,r-a,j-a),                         (8)
```

and extend it by zero when `a` or `j` is outside `[0,r]`.  Thus `h_t^r(a,j)` counts paths
inside the normalized interval `[0,r]`, starting at `a`, ending at `j`, and visiting both
endpoints.  At a fixed actual triple `(ell,u,z)`, put
`r=u-ell`, `a=-ell`, and `j=z-ell`.  The start-zero mass is `2^{-t}h_t^r(a,j)`, while by
(6) the start-two mass is `2^{-t}h_t^r(a+2,j)`.  Therefore

```text
TV(L_t,U_t,S_t under starts 0 and 2)
 = 2^{-t-1} sum_{r=0}^t sum_{j=0}^r sum_{a in Z}
       |h_t^r(a,j)-h_t^r(a+2,j)|.                    (9)
```

This identity automatically respects the time parity, because both terms in each
difference have starting points of the same parity.

Given a triple, generate independent fair bits on its interval and zeros outside.  This is
one common Markov kernel for both triple laws.  Coupling equal triples and then using the
same bits proves directly that

```text
TV(full states) <= TV(range triples).                 (10)
```

This is a sufficient route, not an equality, as the `t=1` check above demonstrates.

## 3. An explicit logarithmic-loss upper bound

Here is a self-contained hitting estimate used below.

**Lemma 1 (one-sided hitting tail).**  If `W` is simple symmetric random walk from zero and
`H_d=inf{n>=0: W_n=d}`, where `d>=1`, then for every integer `q>=0`,

```text
P(H_d>q) <= min(1, d/sqrt(q+1)).                      (11)
```

Proof.  Reflection at the first visit to `d` bijects paths which visit `d` and end at
`k<d` with unrestricted paths ending at `2d-k`.  Hence, by symmetry,

```text
P(H_d>q)=P(-d<=W_q<d).
```

The interval on the right contains exactly `d` sites of the parity accessible at time
`q`.  Every atom of `W_q` is at most `1/sqrt(q+1)`.  For completeness, the latter claim
follows by induction.  For `q=2m`, the largest atom is
`c_m=binom(2m,m)/4^m`; `c_0=1`, and

```text
(c_{m+1}/c_m)^2=((2m+1)/(2m+2))^2 <= (2m+1)/(2m+3),
```

so `c_m<=1/sqrt(2m+1)`.  For `q=2m+1`, the largest atom is
`c_m(2m+1)/(2m+2)<=1/sqrt(2m+2)`.  This proves (11).

We now couple the two base paths.  Let `X` start at zero and, until its first visit

```text
tau=inf{n>=0:X_n=1},
```

put `Y_n=2-X_n`.  At and after `tau`, give both walks identical increments.  More
formally, before `tau` the increment of `Y` is the negative of the fresh increment of
`X`, and afterwards it is the same increment.  The sign used at each step is determined
by the past.  Multiplying a fresh fair sign by a past-measurable sign leaves it a fresh
fair sign; induction therefore verifies that `Y` is itself simple symmetric random walk
from two.  At `tau`, both walks are at one.

Put

```text
A=-min_{0<=k<=tau} X_k.
```

The pre-meeting ranges are `[-A,1]` and `[1,A+2]`.  If the common post-meeting path visits
`-A` and later visits `A+2`, the two total ranges become equal and remain equal; their
endpoints are already equal.  Conditional on equal final triples, use the same uniform
lamp bits on the common interval.  By the conditional-lamp proof in Section 1 this is a
valid coupling of the literal full-state laws.

Two elementary estimates quantify its failure.  First, Lemma 1 with `d=1` gives

```text
P(tau>m) <= 1/sqrt(m+1).                              (12)
```

Second, starting at one, allow `n` steps to visit `-a` first and `a+2` second.  Split the
time at `q=floor(n/2)`.  Lemma 1 bounds failure to reach the left endpoint by
`(a+1)/sqrt(q+1)`.  If it is reached by time `q`, the unused increments are independent
fair signs; from the stopping location the distance to the right endpoint is `2a+2`, and
at least `n-q>=q` steps remain.  Applying Lemma 1 again and taking a union bound yields

```text
P(the prescribed two-endpoint coverage fails in n steps | A=a)
 <= min(1, 3(a+1)/sqrt(floor(n/2)+1)).                (13)
```

The independence assertion here is just the finite stopping-time calculation: on each
event `{H=k}`, the increments after `k` are coordinates disjoint from those determining
`{H=k}`, hence retain their product fair-sign law.

Finally, gambler's ruin in the finite interval `[-a,1]` gives

```text
P(A>=a)=1/(a+1),
P(A=a)=1/((a+1)(a+2)),       a=0,1,2,... .            (14)
```

For clarity, (14) can be proved without an external theorem: the function
`v(x)=(1-x)/(a+1)` is harmonic at every interior integer, equals one at `-a` and zero at
`1`; first-step recursion on the finite interval makes it the probability of hitting
`-a` before `1`, evaluated at `x=0`.  Almost-sure absorption follows, for example, by
dividing time into blocks of `a+1` steps, each of which has a fixed positive chance to
hit a boundary.

Take

```text
m=floor(t/2),  n=t-m=ceil(t/2),
D=sqrt(floor(n/2)+1),  k=3/D.
```

On `{tau<=m}` at least `n` common steps remain.  When `t>=31`, `D>=3` and `k<=1`.  With
`M=floor(1/k)`, (14) gives

```text
E[min(1,k(A+1))]
 <= k sum_{a=0}^M 1/(a+2) + P(A>=M+1)
 <= k log(M+2)+1/(M+2)
 <= k[1+log(1/k+2)].                                 (15)
```

Here `sum_{a=0}^M 1/(a+2)<=log(M+2)`,
`M+2>=1/k+1`, and `M+2<=1/k+2`.  The coupling inequality
`TV(mu,nu)<=P(U!=V)` (obtained by bounding the discrepancy of every event by the
coupling's mismatch probability), together with (12)--(15), proves the explicit partial
theorem

```text
||P_t^(0,0)-P_t^(0,2)||_TV
 <= 1/sqrt(floor(t/2)+1)
    + (3/D) [1+log(D/3+2)],                           (16)

D=sqrt(floor(ceil(t/2)/2)+1),   every integer t>=31.
```

Thus the exact frozen chain has a proved `O((1+log t)/sqrt(t))` full-state upper bound.
The logarithm in this particular coupling estimate is structural: from (14), summing the
conditional cost proportional to `(A+1)/sqrt(t)` produces the harmonic sum in (15).
This observation does not assert that the target estimate is false; it identifies what
this coupling fails to exploit.

## 4. Counterexample to naive sign control and the first gap

A tempting route from (9) is to assert that, for fixed `(t,r,j)` and fixed parity, the
array `a -> h_t^r(a,j)` is unimodal, so its translated absolute differences telescope.
This is false.  Equations (2)--(3), for `t=10`, `r=4`, and `j=2`, give the following exact
four killed-path counts and their inclusion-exclusion value:

```text
a   K^[0,4]  K^[1,4]  K^[0,3]  K^[1,3]   h_10^4(a,2)
0      81        0        55        0          26
1       0        0         0        0           0
2     162       89        89       32          16
3       0        0         0        0           0
4      81       55         0        0          26
```

On the accessible parity class the array is `(26,16,26)`, so it decreases and then
increases.  In particular the signs of
`h(a,j)-h(a+2,j)` already change within one `(r,j)` slice.  Any proof based on a single
monotonicity sign is therefore invalid.

The first unresolved exact obligation produced by this route is to prove, with one
numerical constant `C_C` and an explicit threshold, the array inequality

```text
sum_{r=0}^t sum_{j=0}^r sum_{a in Z}
  |h_t^r(a,j)-h_t^r(a+2,j)|
 <= 2 C_C 2^t/sqrt(t).                               (17)
```

By (9)--(10), (17) would close the full-state upper bound.  The exact V-shaped slice above
shows that (17) needs cancellation-free control more subtle than parity-class
unimodality—likely a bounded-oscillation or direct reflection/injection estimate summed
over `(r,j)`.  At the resource boundary, (1)--(9), the explicit logarithmic bound (16),
and this precise smaller gap are the strongest proved results of Route C.
