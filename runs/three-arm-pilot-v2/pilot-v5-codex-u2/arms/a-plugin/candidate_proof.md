# Candidate proof

Status: rigorous partial draft; `O1` and `O2` are proved below, while `O3` is open.

## Lemma 1 (exact conditional lamp law; `O1`)

Fix either all-zero start and a deterministic admissible base path
`z_0,z_1,...,z_t`, with `t>=1`, minimum `L`, maximum `U`, and endpoint `Z=z_t`.
Conditional on this path, the final lamps at the sites of `[L,U]` are mutually
independent `Bernoulli(1/2)` variables, and every lamp outside `[L,U]` is zero.

**Proof.** Attach independent fair departure and arrival resampling coins to
each step. Every visited site is resampled at least once: the starting site by
the departure switch at time zero, and a site first reached later by that
step's arrival switch. Its final value is its chronologically last resampling
coin. Last coins belonging to distinct sites are distinct members of the
independent coin family, so those final values are independent and fair.
Unvisited lamps retain their initial value zero. A nearest-neighbour path on
the integers visits every integer between its minimum and maximum. This also
shows why the forced initial zero at 0 or 2 leaves no exception for `t>=1`.
Repeated visits merely replace an earlier coin by a later independent one. ∎

Thus if `Q_t^a` is the law of the physical triple `(L,U,Z)` for base start
`a`, and `K((l,u,z),.)` puts endpoint `z`, iid fair lamps on `[l,u]`, and zeros
outside, then

`P_t^(0,a) = Q_t^a K` for `a in {0,2}` and `t>=1`.              (1)

For any two countable laws `mu,nu` and any Markov kernel `K`,

`||mu K-nu K||_TV <= ||mu-nu||_TV`.                            (2)

Indeed, for every event `A`, the function `f(s)=K(s,A)` lies in `[0,1]`.
Writing the positive and negative parts of the signed mass `mu-nu`, whose
total masses both equal `||mu-nu||_TV`, gives
`|sum_s f(s)(mu-nu)(s)|<=||mu-nu||_TV`.  Taking the supremum proves (2).

## Lemma 2 (explicit endpoint lower bound; `O2`)

For every integer `t>=1`,

`||P_t^x-P_t^y||_TV >= 1/(4 sqrt(t))`.                         (3)

**Proof.** Project a lamplighter state to its base coordinate; total variation
cannot increase under a deterministic map, by the same argument as (2). Let
`S_t` be a length-`t` simple symmetric walk from zero. The projected laws are
those of `S_t` and `S_t+2`.

If `t` is even, use the event `{z<=0}`. Its probability difference is
`P(S_t=0)`. If `t` is odd, use `{z<=1}`. Its probability difference is
`P(S_t=1)`. In both cases this is the modal atom

`p_t = 2^(-t) binom(t,floor(t/2))`.                            (4)

The parity has been retained: reachable endpoint atoms have spacing two.
The binomial-coefficient ratio on either side of the center shows directly
that (4) is maximal.

It remains to give an explicit lower estimate without a local limit theorem.
The independent increments have mean zero and variance one, hence
`E[S_t^2]=t`. Markov's inequality applied to the nonnegative variable `S_t^2`
states `P(S_t^2>=4t)<=E[S_t^2]/(4t)=1/4`. Therefore
`P(|S_t|<2 sqrt(t))>=3/4`. The open interval has length `4 sqrt(t)` and the
reachable lattice has spacing two, so it contains at most `2 sqrt(t)+1 <=
3 sqrt(t)` reachable values when `t>=1`. Since each atom is at most `p_t`,

`3/4 <= 3 sqrt(t) p_t`,

which gives `p_t>=1/(4 sqrt(t))` and proves (3). ∎

## Lemma 3 (explicit near-target upper bound)

For every integer `t>=16`,

`||P_t^x-P_t^y||_TV <= (2 log(t)+15)/sqrt(t)`.                (5)

Here and below `log` is natural. This lemma does not close the requested
constant-over-`sqrt(t)` upper bound, but it is a rigorous quantitative partial
result.

**Proof.** Reflection-couple the bases until they meet: before meeting put
`Y_n=2-X_n`, and afterward use identical fresh increments. Thus they meet at
site 1 at the odd hitting time `tau=inf{n:X_n=1}`. Each coordinate has fresh
conditionally fair increments, so both base marginals are exact.

On `{tau<infinity}`, put

`D=1-min_{0<=j<=tau} X_j`.

The two pre-meeting visited intervals, relative to the meeting site, are
`[-D,0]` and `[0,D]`. The elementary gambler's-ruin equation on
`{-k+1,...,1}` gives

`P(D>=k)=1/k`, and hence `P(D=k)=1/[k(k+1)]`, `k>=1`.         (6)

Indeed the function giving the probability, from `i`, of hitting `-k+1`
before 1 is affine with boundary values 1 and 0, so its value at 0 is `1/k`.

Conditional on the two base paths, couple their fair interval-lamp kernels
maximally. For finite intervals `I,J`, their overlap is

`2^(-max(|I\J|,|J\I|))`: common configurations must vanish off `I intersect J`,
there are `2^|I intersect J|` of them, and the smaller point mass is
`2^(-max(|I|,|J|))`. In particular, once the common post-meeting walk has hit
both levels `-D` and `D` relative to site 1, the two visited intervals and
endpoints coincide, and the lamp configurations can be made identical.

For a simple walk from zero and `T_k=inf{n:S_n=k}`, reflection at its first
visit to `k` gives exactly

`P(T_k>n)=P(-k<=S_n<k)`.                                    (7)

The half-open interval in (7) contains exactly `k` reachable parity atoms.
If `p_n^*` is the modal atom, the elementary central-binomial induction
recorded below gives `p_n^*<=sqrt(2/n)` for `n>=1`; hence

`P(T_k>n)<=min(1,k sqrt(2/n))`.                              (8)

Let `n=floor(t/2)`. On `{tau<=n}`, at least `ceil(t/2)` common increments
remain. A union bound for missing `D` or `-D`, (8), and independence of the
fresh continuation give a conditional failure bound
`2 min(1,2D/sqrt(t))`. Also (7) at `k=1` and
`n>=t/3` give `P(tau>n)<=3/sqrt(t)`. Therefore

`||P_t^x-P_t^y||_TV`

` <= 3/sqrt(t) + 2 E[min(1,2D/sqrt(t))]`.                   (9)

For `J=floor(sqrt(t)/2)`, (6) gives, for `t>=16`,

`E[min(1,2D/sqrt(t))]`

` <= (2/sqrt(t)) sum_{k=1}^J 1/(k+1) + P(D>J)`

` <= (log(t)+6)/sqrt(t)`.                                  (10)

The last bound uses `sum_{k=1}^J 1/(k+1)<=log(J+1)`, with a harmless
one-unit enlargement, and `1/(J+1)<=3/sqrt(t)` for `t>=16`.
Combining (9)-(10) proves (5). The terminal lamp coupling has exact marginals
by Lemma 1 and the displayed overlap decomposition. ∎

For completeness, the modal-atom estimate used above is elementary. At even
time `2q`, set `a_q=4^{-q} binom(2q,q)`. Then
`a_(q+1)/a_q=(2q+1)/(2q+2)`, and induction against `1/sqrt(q+1)` uses
`[(2q+1)/(2q+2)]^2 <= (q+1)/(q+2)`. The odd modal atom is no larger than the
preceding even one. Thus `p_n^*<=sqrt(2/n)`.

## Exact remaining constant-order upper-bound obligation (`O3`)

By (1)-(2), it is enough to prove with explicit constants that

`||Q_t^0-Q_t^2||_TV <= C/sqrt(t)`.                            (11)

Writing a zero-start path's triple as

`A=-L`, `R=U-L`, `e=Z-L`,

and letting `H_t^R(A,e)` be the number of length-`t` paths in `[0,R]` from
`A` to `e` which visit both 0 and `R`, exact path counting gives

`2 ||Q_t^0-Q_t^2||_TV`

` = 2^(-t) sum_{R>=0} sum_{e=0}^R sum_{A in Z}`
`       |H_t^R(A,e)-H_t^R(A+2,e)|`,                          (12)

where `H` is extended by zero outside `0<=A,e<=R`. To verify (12), a physical
triple `[l,u],z` has `A=-l,R=u-l,e=z-l`; for the walk started at 2, translating
to a zero-start path replaces `(l,u,z)` by `(l-2,u-2,z-2)`, hence replaces
`A` by `A+2` while leaving `R,e` fixed. Each sign sequence has mass `2^-t`.

The first unresolved obligation is a self-contained explicit bound of order
`2^t/sqrt(t)` for the sum in (12), or a different full-state coupling. Exact
computation supports such a bound but is not used as proof. The standard
reflection-then-synchronization full-state coupling is insufficient: the
hash-verified route analysis in `subagents/direct_coupling.md` proves its
optimal conditional mismatch has a logarithmic loss from residual old lamps.
