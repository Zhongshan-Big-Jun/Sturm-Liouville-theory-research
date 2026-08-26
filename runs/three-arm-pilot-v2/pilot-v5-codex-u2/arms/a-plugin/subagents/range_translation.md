PARTIAL

# Range-translation subproblem

## Exact subclaim addressed

Let (S_0=0) and (S_j=\xi_1+\cdots+\xi_j), where the
(\xi_i)'s are independent uniform signs.  Put

\[
 L_t=\min_{0\le j\le t}S_j,\qquad
 U_t=\max_{0\le j\le t}S_j,\qquad Z_t=S_t.
\]

If (Q_t^a) is the law of the physical triple (minimum, maximum,
endpoint) for the walk started at (a), the requested estimate is

\[
 \|Q_t^0-Q_t^2\|_{\rm TV}\le C t^{-1/2}.
\]

I did not close this estimate.  The strongest proved quantitative result here
is the completely explicit logarithmic-loss bound

\[
 \boxed{\quad
 \|Q_t^0-Q_t^2\|_{\rm TV}
 \le {2+4H_{\lfloor t/2\rfloor+1}\over\sqrt t}
 \le {6+4\log(t+1)\over\sqrt t},\qquad t\ge2,
 \quad}                                                     \tag{1}
\]

where (H_n=\sum_{j=1}^n j^{-1}).  I also prove below an exact
finite-array identity which isolates the first missing inequality for the
desired (t^{-1/2}) estimate.

## Exact range-shape identity

For integers (R,K,A), define the integer path count

\[
 h_t(R,K,A)=\#\bigl\{(\xi_1,\ldots,\xi_t)\in\{-1,1\}^t:
 -L_t=A, U_t-L_t=R, Z_t-L_t=K\bigr\},                    \tag{2}
\]

and set it equal to zero outside its natural support.  Necessarily
(0\le A,K\le R) and (t+K-A) is even.

For every (t\ge0),

\[
 \boxed{\quad
 \|Q_t^0-Q_t^2\|_{\rm TV}
 ={1\over 2^{t+1}}
 \sum_{R,K,A\in\mathbb Z}
    |h_t(R,K,A)-h_t(R,K,A+2)|.
 \quad}                                                     \tag{3}
\]

Indeed, for a physical triple ((l,u,z)), put
(R=u-l, K=z-l, A=-l).  Its count for the walk started at zero is
(h_t(R,K,A)).  Translating the relative zero-start path by 2 shows that its
count for the walk started at 2 is (h_t(R,K,A+2)).  The map
((l,u,z)\leftrightarrow(R,K,A)) is bijective, and (3) follows from the
definition of total variation.

Two further exact identities useful for an eventual proof are

\[
 \sum_{R,K}h_t(R,K,A)=\#\{-L_t=A\},                         \tag{4}
\]

and the path-reversal symmetry

\[
 h_t(R,K,A)=h_t(R,R-A,R-K).                                 \tag{5}
\]

For (5), reverse the path in time and translate its initial point back to
zero: (\widehat S_j=S_{t-j}-S_t).  Then its new origin height above its
minimum is (K), and its endpoint height above its minimum is (A).  Applying
also sign reversal gives the displayed equivalent form.  (Equivalently, time
reversal alone says (h_t(R,K,A)=h_t(R,A,K)); sign reversal says
(h_t(R,K,A)=h_t(R,R-K,R-A)); their composition gives (5).)

The following aggregate bounded-variation inequality would immediately close
the requested estimate:

\[
 \sum_{R,K,A}|h_t(R,K,A)-h_t(R,K,A+2)|
 \mathrel{\le} 8{t\choose\lfloor t/2\rfloor}.               \tag{AVI}
\]

It would give, from (3),

\[
 \|Q_t^0-Q_t^2\|_{\rm TV}
 \le 4{ {t\choose\lfloor t/2\rfloor}\over 2^t}
 \le {4\over\sqrt t},\qquad t\ge1.                        \tag{6}
\]

The last elementary inequality follows as follows.  If
(c_q={2q\choose q}/4^q), then (c_0=1) and

\[
 c_{q+1}=c_q{2q+1\over2q+2},\qquad
 { (2q+1)^2(3q+4)}\le{(2q+2)^2(3q+1)}.
\]

Induction gives (c_q\le(3q+1)^{-1/2}).  This is at most
((2q)^{-1/2}) for (q\ge1); the odd central atom is no larger than
(c_q\le(2q+1)^{-1/2}).

I have not proved (AVI).  In particular, it cannot be replaced by fiberwise
unimodality: for ((t,R,K)=(6,4,2)), the nonzero parity fiber in (A) is
([1,0,1]).  At larger times a fiber can have at least four monotonicity runs.
Thus any proof of (AVI) must be genuinely aggregate, or must establish a more
subtle uniform variation-diminishing statement.

## A proved one-sided \(t^{-1/2}\) estimate

Although it does not by itself control the triple, each min/endpoint or
max/endpoint marginal has the desired order.  If \(Q_t^{a,LZ}\) and
\(Q_t^{a,UZ}\) denote these marginals, then

\[
 \boxed{\quad
 \|Q_t^{0,LZ}-Q_t^{2,LZ}\|_{\rm TV}\le {12\over\sqrt t},
 \qquad
 \|Q_t^{0,UZ}-Q_t^{2,UZ}\|_{\rm TV}\le {12\over\sqrt t},
 \quad t\ge1.\quad}                                         \tag{7}
\]

Here is a self-contained proof.  Write

\[
 p(s)=2^{-t}{t\choose (t+s)/2},
\]

with \(p(s)=0\) when the lower binomial argument is not an integer in
\([0,t]\), and, on the parity class of \(t\), put
\(D_s=p(s)-p(s+2)\) for \(s\ge0\).  Reflection after the first visit to
\(-a-1\) gives

\[
 \mathbb P_0(L_t=-a,Z_t=z)
 =p(z+2a)-p(z+2a+2)=D_{z+2a},                               \tag{8}
\]

for \(a\ge0,\ z\ge-a\).  At the same physical cell, the walk started at 2
has mass \(D_{z+2a+2}\).  Therefore the \(L^1\) difference over the common
support \(l\le0\) is exactly

\[
 I_t=\sum_{\substack{s\ge0\\s\equiv t\pmod2}}
       (s+1)|D_s-D_{s+2}|.                                  \tag{9}
\]

Indeed, after setting \(s=z+2a\), the constraint \(z\ge-a\) is
\(0\le a\le s\), giving exactly \(s+1\) cells for each \(s\).  The part
supported only by the start-2 law has physical minima 1 or 2.  Its total
mass is \(\mathbb P_0(L_t\ge-1)=\mathbb P_0(T_{-2}>t)\le2p_t^*\), by
the reflection estimate in Lemma 1 below.

For parity-compatible \(s\) in the support,

\[
 D_s=p(s){2(s+1)\over t+s+2},\qquad
 {D_{s+2}\over D_s}
 ={(t-s)(s+3)\over(s+1)(t+s+4)}.                            \tag{10}
\]

The last ratio is at least one exactly when
\(t\ge s^2+4s+2\).  Thus \(D_s\) is unimodal on its parity lattice.  If
\(s_*\) is a maximizing index, comparison with its preceding index (with the
first index handled directly) gives \(s_*^2\le t+2\).  For \(t\ge2\),
\((s_*+1)^2\le5t\), and hence

\[
 (s_*+1)D_{s_*}
 ={2(s_*+1)^2\over t+s_*+2}p(s_*)\le10p_t^*.                \tag{11}
\]

Summation by parts separately on the increasing and decreasing sides of a
unimodal sequence whose weights increase by 2 gives

\[
 I_t\le2(s_*+1)D_{s_*}+2\sum_sD_s.                          \tag{12}
\]

The last sum telescopes to the central atom \(p_t^*\), so
\(I_t\le22p_t^*\).  Adding the start-2-only mass gives \(L^1\le24p_t^*\),
hence TV at most \(12p_t^*\le12/\sqrt t\).  The case \(t=1\) is immediate.
Sign reversal proves the \(UZ\) assertion.

Exact enumeration also supports

\[
 \|Q_t^0-Q_t^2\|_{\rm TV}
 \le \|Q_t^{0,LZ}-Q_t^{2,LZ}\|_{\rm TV}
    +\|Q_t^{0,UZ}-Q_t^{2,UZ}\|_{\rm TV},                    \tag{MC}
\]

which, together with (7), would prove the target with \(C=24\).  I do not
have a proof of (MC).  Such an inequality is false for general bivariate
arrays, so it requires a path-specific mixed-difference, coarea, or monotone
transport argument.  Thus (MC) is a second precise sufficient formulation of
the first gap, alongside (AVI).

## Proof of the explicit logarithmic-loss bound

I use three elementary lemmas, all proved here.

### Lemma 1: a one-sided hitting tail

Let (T_d=\inf\{j\ge0:S_j=d\}), where (d\ge1).  For (n\ge1),

\[
 \mathbb P_0(T_d>n)\le d\,p_n^*\le {d\over\sqrt n},
 \qquad p_n^*=2^{-n}{n\choose\lfloor n/2\rfloor}.            \tag{7}
\]

To prove the first inequality, reflect a path after its first visit to (d).
For every parity-compatible (j<d), this bijects paths with
(\max_{s\le n}S_s\ge d, S_n=j) and paths with (S_n=2d-j).  Hence

\[
 \mathbb P(T_d>n)
 =\sum_{j<d}\bigl(\mathbb P(S_n=j)-\mathbb P(S_n=2d-j)\bigr).
\]

By symmetry the right side is a central interval containing exactly (d)
parity-compatible endpoint atoms.  Each is at most (p_n^*), proving the
first inequality.  The proof following (6) gives (p_n^*\le n^{-1/2}).

The case (d=1) also gives the exact survival identity

\[
 \mathbb P_0(T_1>n)=p_n^*.                                  \tag{8}
\]

### Lemma 2: depth before first hitting 1

Let (\tau=T_1), and on (\{\tau<\infty\}) put

\[
 A=-\min_{0\le j\le\tau}S_j.
\]

Then, for every integer (a\ge1),

\[
 \mathbb P(A\ge a)={1\over a+1}.                            \tag{9}
\]

This is the elementary gambler's-ruin calculation on
(\{-a,-a+1,\ldots,1\}).  If (g(i)) is the probability, from (i), of
hitting (-a) before 1, then (g(i)=(1-i)/(a+1)), as is checked directly
from (g(i)=(g(i-1)+g(i+1))/2) and the two boundary values.  Thus
(g(0)=1/(a+1)).  Also (\tau<\infty) almost surely by (8).

Consequently, for every integer (m\ge1),

\[
 \mathbb E[(A+1)\mathbf 1_{\{\tau\le m\}}]
 \le \mathbb E[\min(A+1,m+1)]
 =\sum_{a=0}^m\mathbb P(A\ge a)
 =H_{m+1}.                                                   \tag{10}
\]

### Lemma 3: coupling the triples

Couple a walk (X) from 0 and a walk (Y) from 2 as follows.  Until
(\tau=\inf\{j:X_j=1\}), use opposite increments, so that (Y_j=2-X_j).
At and after the meeting at 1, use identical increments.

Both marginals are simple random walks.  One direct verification is to start
with iid fair signs (\xi_j), use (\xi_j) for (X), and use either
(-\xi_j) before the predictable meeting decision or (\xi_j) afterward
for (Y).  Conditional on the past, each next (Y)-increment is still a
fresh fair sign; induction gives the product fair-sign law.

At the meeting time, if the depth in Lemma 2 is (A), the two historical
ranges are respectively

\[
 [-A,1]\quad\hbox{and}\quad[1,2+A].                         \tag{11}
\]

The positions and all later increments agree.  Once the common continuation
has visited both levels (-A) and (2+A), the two minima, maxima, and
endpoints agree, and they agree forever afterward.  Therefore, with
(m=\lfloor t/2\rfloor) and (N=t-m\),

\[
\begin{aligned}
 \mathbb P(\hbox{triples differ at time }t)
 &\le \mathbb P(\tau>m)
   +\mathbb E\left[\mathbf 1_{\{\tau\le m\}}
       {2(A+1)\over\sqrt{t-\tau}}\right] \\[2mm]
 &\le {1\over\sqrt m}+{2H_{m+1}\over\sqrt N}.             \tag{12}
\end{aligned}
\]

Here (8) and (7) were used; conditional on the pre-meeting path, the future is
independent and each of the two target levels is distance (A+1) from 1.
The union bound accounts for the factor 2.

For (t\ge2), (m\ge t/4) and (N\ge t/2), so (12) is at most

\[
 {2+2\sqrt2 H_{m+1}\over\sqrt t}
 \le {2+4H_{m+1}\over\sqrt t}.
\]

Finally (H_n\le1+\log n\), and the coupling inequality for total variation
proves (1).

## Exact edge tests

The defining recurrence used for exact checks is

\[
 C_{s+1}(l,u,z)=
 C_s(l,u,z+1)\mathbf1_{z+1\in[l,u]}
 +C_s(l,u,z-1)\mathbf1_{z-1\in[l,u]},                       \tag{13}
\]

with the appropriate update of a newly reached minimum or maximum (equivalently,
iterate every existing triple by its two possible next steps).  Integer
enumeration gives the following exact values; these are checks, not premises
of any general assertion:

| (t) | numerator in (3) | (\|Q_t^0-Q_t^2\|_{\rm TV}) |
|---:|---:|---:|
| 0 | 2 | (1) |
| 1 | 4 | (1) |
| 2 | 8 | (1) |
| 3 | 14 | (7/8) |
| 4 | 28 | (7/8) |
| 5 | 50 | (25/32) |
| 6 | 100 | (25/32) |

These tests cover the zero-time singleton ranges, odd/even parity, and the
first non-unimodal fiber.  The proof of (1), rather than these finite checks,
covers every integer (t\ge2).

## First unresolved step and failure mechanism

The first unresolved load-bearing statement is (AVI), or any alternative
uniform (O(2^t/\sqrt t)) bound for the absolute diagonal variation in (3).
No external theorem is being invoked for it.

The proved coupling loses the logarithm at exactly (10): the pre-meeting depth
has the harmonic tail (\mathbb P(A\ge a)=1/(a+1)), while the elementary
hitting estimate for erasing a depth-(a) historical range costs
((a+1)/\sqrt t).  Averaging those costs produces (H_{m+1}).  Removing this
factor requires a coupling that repairs the two old range endpoints
concurrently, or an aggregate cancellation/variation argument for (3);
reflection followed by a common continuation does not supply either
mechanism.

## Audit

- Semantic scope: the physical min/max/endpoint laws for starts 0 and 2, all
  integer times, and the parity shift by 2 were retained.
- Proved status: identities (3)--(5), the hitting/depth lemmas, and bound (1).
- Computational status: the displayed small cases are exact integer checks
  only and are not used as proof.
- Open status: the target (C/\sqrt t) estimate remains unproved; (AVI) is a
  precise sufficient first gap.
- No literature or internet result is used.
