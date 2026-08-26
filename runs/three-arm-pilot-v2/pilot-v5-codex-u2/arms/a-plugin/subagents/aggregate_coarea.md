RIGOROUS_PARTIAL_RESULT

# Aggregate coarea and killed-kernel reduction

## Result and scope

Let

\[
h_t(R,K,A)=\#\{S_0=0:\ -\min_{j\le t}S_j=A,\ 
\max_{j\le t}S_j-\min_{j\le t}S_j=R,\
S_t-\min_{j\le t}S_j=K\},
\]

extended by zero outside its natural integer support.  I do not prove

\[
 \sum_{R,K,A}|h_t(R,K,A)-h_t(R,K,A+2)|
 \le 8\binom t{\lfloor t/2\rfloor}.                    \tag{AVI}
\]

The strongest exact result obtained is a self-contained reduction of the
left side to (i) superlevel-set component counts and (ii) explicit mixed
differences of periodized binomial coefficients.  It retains the cancellations
which are lost by a termwise reflection/image estimate and identifies the first
remaining inequality precisely.  No fiberwise unimodality is used.

## 1. Exact killed-kernel identity

For an integer \(r\), define

\[
 q_{r,t}(a,k)=\#\{x_0=a,x_t=k:\ |x_{j+1}-x_j|=1,
                   0\le x_j\le r\ (0\le j\le t)\},
\]

and put \(q_{r,t}=0\) if \(r<0\) or either endpoint is outside
\([0,r]\).  Then, for every \(t,R,K,A\),

\[
\boxed{
h_t(R,K,A)=q_{R,t}(A,K)-q_{R-1,t}(A-1,K-1)
            -q_{R-1,t}(A,K)+q_{R-2,t}(A-1,K-1).}          \tag{1}
\]

Indeed, \(q_{R,t}(A,K)\) counts the paths in \([0,R]\).  Those which
do not visit 0 are, after translation down by one, counted by
\(q_{R-1,t}(A-1,K-1)\); those which do not visit \(R\) are counted by
\(q_{R-1,t}(A,K)\); and those which visit neither endpoint are counted
by \(q_{R-2,t}(A-1,K-1)\).  Inclusion-exclusion gives exactly the paths
whose minimum is 0 and maximum is \(R\), which are the paths counted by
\(h_t(R,K,A)\).  The zero extensions make (1) valid also for
\(R=0,1\).

Thus the difficulty is not an unproved probabilistic representation: it is
the aggregate spatial variation of the mixed boundary difference in (1).

## 2. An explicit periodized-binomial form

Put

\[
 B_t(x)=
 \begin{cases}
 \displaystyle\binom t{(t+x)/2},& |x|\le t, t+x\text{ even},\\
 0,&\text{otherwise},
 \end{cases}
 \qquad
 \Phi_n(x)=\sum_{j\in\mathbb Z}B_t(x+2jn)\quad(n\ge1).
\]

Every sum is finite.  Reflection at the first exit from \([0,R]\) gives

\[
q_{R,t}(A,K)=\Phi_{R+2}(K-A)-\Phi_{R+2}(K+A+2).            \tag{2}
\]

For completeness, the terms with endpoint \(K-A+2j(R+2)\) are the
unreflected images and those with endpoint \(K+A+2+2j(R+2)\) are the
images obtained by reflection in the lower absorbing boundary.  Translating
an exit through the upper boundary by the period \(2(R+2)\) pairs all exits;
this is the usual reflection bijection, and summing the signed image classes
proves (2).  Because \(B_t\) is finitely supported, there is no convergence
issue.

For \(R\ge2\), set \(d=K-A\), \(s=K+A\), and define

\[
\begin{aligned}
D_R(d)&=\Phi_{R+2}(d)-2\Phi_{R+1}(d)+\Phi_R(d),\\
E_R(s)&=-\Phi_{R+2}(s+2)+\Phi_{R+1}(s)
          +\Phi_{R+1}(s+2)-\Phi_R(s).
\end{aligned}                                             \tag{3}
\]

Substitution of (2) into (1) gives the exact decomposition

\[
\boxed{h_t(R,K,A)=D_R(K-A)+E_R(K+A).}                      \tag{4}
\]

The \(j=0\) image cancels identically in (4).  More explicitly, its
\(d\)-part is \(B_t(d)-2B_t(d)+B_t(d)=0\), while its
\(s\)-part is
\(-B_t(s+2)+B_t(s)+B_t(s+2)-B_t(s)=0\).  Hence exact-range
counts are carried entirely by the nonzero image classes.  This cancellation
is load-bearing: applying the triangle inequality to the four killed kernels
in (1), or to the individual images before the cancellation in (3), does not
produce the required order.

As a precise sufficient estimate, (4) and the triangle inequality give

\[
 V_t\le V_t^{D}+V_t^{E},                                  \tag{5}
\]

where \(V_t\) is the left side of (AVI) and

\[
\begin{aligned}
V_t^{D}
 &=\sum_{R\ge2}\sum_{d=-R}^{R}(R+1-|d|)
       |D_R(d)-D_R(d-2)|,\\
V_t^{E}
 &=\sum_{R\ge2}\sum_{s=0}^{2R}(R+1-|s-R|)
       |E_R(s)-E_R(s+2)|,                                 \tag{6}
\end{aligned}
\]

plus the directly finite \(R=0,1\) terms.  The weights in (6) are exact:
\(R+1-|d|\) is the number of pairs \((A,K)\in[0,R]^2\) with
\(K-A=d\), and \(R+1-|s-R|\) is the number with \(K+A=s\).
Consequently any explicit bound

\[
 V_t^D+V_t^E+V_t^{\{0,1\}}
 \le C_0\binom t{\lfloor t/2\rfloor}                     \tag{7}
\]

with a numerical \(C_0\) proves the required
\(O(2^t/\sqrt t)\) aggregate variation, even if \(C_0>8\).

## 3. Exact discrete coarea formula

Fix \((R,K)\), and on the parity lattice

\[
 \Lambda_{t,K}=\{a\in\mathbb Z:a\equiv t+K\pmod2\}
\]

put \(f(a)=h_t(R,K,a)\), extended by zero.  For \(m\ge1\), let
\(c_{R,K}(m)\) be the number of connected components (adjacency distance
two) of the finite superlevel set

\[
 \{a\in\Lambda_{t,K}:f(a)\ge m\}.
\]

Then

\[
\boxed{
\sum_{a\in\mathbb Z}|h_t(R,K,a)-h_t(R,K,a+2)|
=2\sum_{m\ge1}c_{R,K}(m).}                                \tag{8}
\]

To prove this, use for nonnegative integers \(u,v\) the layer-cake identity

\[
 |u-v|=\sum_{m\ge1}|\mathbf1_{u\ge m}-\mathbf1_{v\ge m}|.
\]

After summing in \(a\), every finite component of a superlevel set has
exactly two boundary edges on the parity lattice.  This proves (8), and then

\[
\boxed{V_t=2\sum_{R,K}\sum_{m\ge1}c_{R,K}(m).}             \tag{9}
\]

In particular, (AVI) is exactly equivalent to

\[
 \sum_{R,K,m}c_{R,K}(m)
 \le4\binom t{\lfloor t/2\rfloor}.                        \tag{10}
\]

Formula (9) also pinpoints why fiberwise unimodality is not an admissible
shortcut.  At \((t,R,K)=(6,4,2)\), the parity-compatible fiber is
\([1,0,1]\), so its level-one superlevel set has two components.  The
coarea identity remains valid; a proof must control these extra components
in aggregate.

## 4. First unresolved inequality

The first load-bearing gap is either (10), or the more analytic sufficient
estimate (7) for the explicit arrays (3).  I did not prove a numerical
constant in (7).  The obstruction is localized as follows:

* taking absolute values before the four terms in (1) are combined destroys
  the mixed boundary cancellation;
* taking absolute values image-by-image in (3) also destroys cancellation
  among winding classes and leads to a logarithmic-size overestimate;
* replacing the component count in (10) by one component per nonempty level
  is false at the displayed \(t=6\) fiber (and later fibers have still more
  monotonicity runs).

Thus the missing statement is a uniform aggregate cancellation or an
aggregate bound on the extra superlevel components, not a hidden
fiberwise-unimodality lemma.  Establishing (7) with any fixed \(C_0\), or
(10) with the displayed constant 4, is sufficient and is strictly the first
unclosed step after the exact killed-kernel and coarea reductions.

## 5. Finite falsification checks and audit

The supplied exact-integer dynamic program was run through \(t=80\).
It confirmed (1), (4), (8), and (AVI) on that finite domain, including both
parities and the nonunimodal \((6,4,2)\) fiber.  These computations are only
falsification checks and are not used as evidence for a general inequality.

Semantic audit: \(A=-L_t\), \(R=U_t-L_t\), and \(K=Z_t-L_t\) are retained
exactly; the shift is by two on the correct parity lattice; all arrays are
integer path counts rather than probabilities; and \(R=0,1\) are covered by
the zero-extension form (1).  No internet, external theorem, or reflection
coupling of the two walks is used.

Input hashes checked:

* `problem_contract.md`:
  `98d6ea8d4da0a5f121c36d7c0b2cc895ec81d7b30f6e9b2d079f212825f667f5`;
* `obligation_graph.md`:
  `b315d8cf264b32dd889a1281fa429cac39543b0594a0385813d70d8336cf61c0`;
* `subagents/range_translation.md`:
  `07f2c63d3a0670fff434b78778c35ddfecc1ffdb41dc8c7c1b3fa70b9890d5e7`;
* `reproducibility/enumerate_triples.py`:
  `fa0e24f8af0c9709f17dbfb2392000636f4b6d2bf3888e6f5c71b1c5fa8dd391`.
