# Proof

## Problem Statement

# Frozen task: U2 total-variation asymptotics

Blind benchmark. Do not inspect any repository, git history, internet source, external memory,
prior benchmark output, or prior solution to this exact problem. Scratch exact or numerical
computation may be used only for falsification. Numerical evidence does not constitute proof.

Let `Z_2 wr Z` be the lamplighter group. Write each state as `(eta,z)`, where
`eta: Z -> Z_2` has finite support and `z in Z` is the base position. Let `0` denote the
all-zero lamp configuration.

Consider the discrete-time switch-walk-switch chain. From `(eta,z)`, independently resample the
lamp at `z` from `Bernoulli(1/2)`, move the base to `z+1` or `z-1` with probability `1/2` each,
then independently resample the lamp at the arrival site from `Bernoulli(1/2)`. Let `P_t^x`
denote the law at integer time `t>=0` started from `x`.

Set

```text
x=(0,0),
y=(0,2).
```

Thus both initial lamp configurations are all zero, and the two initial base positions are `0`
and `2`.

Prove that there are explicit constants `0<c<=C<infinity` and an explicit integer `t_0` such
that, for every integer `t>=t_0`,

```text
c/sqrt(t) <= ||P_t^x-P_t^y||_TV <= C/sqrt(t).
```

Here total variation is `sup_A |P_t^x(A)-P_t^y(A)|`, equivalently one half of the `l^1`
distance on the countable state space.

State every external theorem in the exact form used and verify all hypotheses. Audit parity,
small times, the effect of the two forced initial zero lamps, and every conditioning or
coupling step. Do not replace the chain by a different lamp convention or interpret `(0,2)` as
a lamp lit at site `2`.

A complete result requires both bounds with explicit constants. If incomplete, return the
strongest exact partial result and the first unresolved obligation without claiming completion.

## Status

The decomposition’s STEP6 is not established by the material supplied. In particular, its strategy paragraph is not a proof of the asserted diagonal-variation inequality. The argument below proves all preceding reductions, the explicit lower bound, the small-time statements, and the following rigorous upper bound:
\[
 \frac{1}{2\sqrt t}
 \leq \|P_t^x-P_t^y\|_{\rm TV}
 \leq \frac{5+3\log t}{\sqrt t}
 \qquad(t\geq1),
\]
where the right side for \(t=1,2,3\) is understood as the displayed numerical expression and follows from total variation being at most \(1\).

Thus the strongest result proved here has only a logarithmic loss in the upper bound. The first unresolved obligation is exactly STEP6: removing that logarithm by proving
\[
\|Q_t^{(0)}-Q_t^{(2)}\|_{\rm TV}=O(t^{-1/2})
\]
with an explicit constant.

<cite>type=survey_status; label=Offline literature status; title=Related work under the blind offline protocol; authors=QED benchmark; source_url=related_info/related_work.md; verifier_locator=opening paragraph; statement_match=exact; statement=No external literature, citation, repository result, prior answer, or mathematical hint is available in this arm.; usage=Consequently every random-walk and combinatorial estimate used below is proved self-containedly rather than invoked externally.</cite>

## Proof

### STEP1: Conditional lamp law

**Claim:** Let \((W_s)_{0\leq s\leq t}\) be simple symmetric random walk started at \(a\), and put
\[
L_t=\min_{0\leq s\leq t}W_s,\qquad
U_t=\max_{0\leq s\leq t}W_s,
\]
and
\[
q_t^{(a)}(\ell,u,z)
 =\mathbb P_a(L_t=\ell,U_t=u,W_t=z).
\]
For every integer \(t\geq1\), every finitely supported \(\eta:\mathbb Z\to\mathbb Z_2\), and every \(z\in\mathbb Z\),
\[
P_t^{(0,a)}(\eta,z)
=\sum_{\ell,u\in\mathbb Z}
q_t^{(a)}(\ell,u,z)\,
2^{-(u-\ell+1)}
\mathbf 1_{\{\operatorname{supp}\eta\subseteq[\ell,u]\}}.
\]

**Proof:**

Fix the complete base path \(w_0,\ldots,w_t\). Because this is a nearest-neighbor path on \(\mathbb Z\), its set of visited sites is exactly
\[
\{w_0,\ldots,w_t\}=[\ell,u]\cap\mathbb Z,
\qquad
\ell=\min_s w_s,\quad u=\max_s w_s.
\]

Every visited site is resampled at least once. The starting site \(w_0\) is resampled before the first move, every newly visited site is resampled upon arrival, and the final site \(w_t\) is resampled upon the final arrival. For each \(v\in[\ell,u]\), select the chronologically last resampling performed at \(v\). These selected variables belong to distinct resampling operations and hence are independent fair Bernoulli variables. Every earlier value at \(v\), including its forced initial value zero, is overwritten by the selected variable.

Sites outside \([\ell,u]\) are never resampled and retain their initial value zero. Consequently, conditional on the base path, the final lamp configuration is uniform over the \(2^{u-\ell+1}\) configurations supported in \([\ell,u]\). This conditional law depends on the path only through \((\ell,u,w_t)\). Averaging over paths with the same minimum, maximum, and endpoint gives the formula.

This uses exactly the transition convention in the problem:
<cite>type=definition; label=Switch-walk-switch transition; title=Frozen task: U2 total-variation asymptotics; authors=QED benchmark problem setter; source_url=problem.tex; verifier_locator=transition-definition paragraph; statement_match=exact; statement=From `(eta,z)`, independently resample the lamp at `z` from `Bernoulli(1/2)`, move the base to `z+1` or `z-1` with probability `1/2` each, then independently resample the lamp at the arrival site from `Bernoulli(1/2)`.; usage=Used to identify the chronologically last independent fair resampling at every visited site.</cite>

**Dependencies:** S1.

---

### STEP2: Reduction to the range-endpoint triple

**Claim:** Define
\[
K((\ell,u,z),(\eta,w))
=\mathbf1_{\{w=z\}}\mathbf1_{\{\operatorname{supp}\eta\subseteq[\ell,u]\}}
2^{-(u-\ell+1)}.
\]
If \(Q_t^{(a)}\) is the law of \((L_t,U_t,W_t)\) for a walk started at \(a\), then
\[
P_t^{(0,a)}=Q_t^{(a)}K,
\]
and
\[
\|P_t^x-P_t^y\|_{\rm TV}
\leq\|Q_t^{(0)}-Q_t^{(2)}\|_{\rm TV}.
\]
Moreover,
\[
q_t^{(2)}(\ell,u,z)
=q_t^{(0)}(\ell-2,u-2,z-2).
\]

**Proof:**

The first identity is STEP1 written as composition with a Markov kernel.

Let \(\mu,\nu\) be probability measures on the countable space of triples. Directly from the \(\ell^1\) definition,
\[
\begin{aligned}
2\|\mu K-\nu K\|_{\rm TV}
&=\sum_s\left|\sum_r(\mu(r)-\nu(r))K(r,s)\right|\\
&\leq\sum_s\sum_r|\mu(r)-\nu(r)|K(r,s)\\
&=\sum_r|\mu(r)-\nu(r)|\sum_sK(r,s)\\
&=\sum_r|\mu(r)-\nu(r)|
=2\|\mu-\nu\|_{\rm TV}.
\end{aligned}
\]
Applying this with \(\mu=Q_t^{(0)}\) and \(\nu=Q_t^{(2)}\) proves contraction.

Finally, a walk started at \(2\) has the same law as \(2+W\), where \(W\) starts at zero. Its minimum, maximum, and endpoint are therefore all translated by \(2\), proving the last formula. This is only a translation of the base path; the initial lamp configuration in \(y=(0,2)\) remains the all-zero configuration.

<cite>type=definition; label=Total variation convention; title=Frozen task: U2 total-variation asymptotics; authors=QED benchmark problem setter; source_url=problem.tex; verifier_locator=paragraph following the displayed conjecture; statement_match=exact; statement=Here total variation is `sup_A |P_t^x(A)-P_t^y(A)|`, equivalently one half of the `l^1` distance on the countable state space.; usage=Used in the direct proof that total variation contracts under the conditional lamp kernel.</cite>

**Dependencies:** STEP1, S2.

---

### STEP3: Exact diagonal-variation formula

**Claim:** For \(d\geq0\), let \(N_t(d,a,j)\) be the number of nearest-neighbor paths \(v_0,\ldots,v_t\) such that
\[
v_0=a,\quad v_t=j,\quad \min_s v_s=0,\quad\max_s v_s=d,
\]
and put \(n_t(d,a,j)=2^{-t}N_t(d,a,j)\), extended by zero unless \(0\leq a,j\leq d\). Then
\[
A_t:=\|Q_t^{(0)}-Q_t^{(2)}\|_{\rm TV}
=\frac12\sum_{d=0}^{t}\sum_{j=0}^{d}\sum_{a=-2}^{d}
|n_t(d,a,j)-n_t(d,a+2,j)|.
\]
Also,
\[
n_t(d,a,j)=0\quad\text{unless}\quad j-a\equiv t\pmod2.
\]

**Proof:**

For a triple \((\ell,u,z)\), make the bijective change of coordinates
\[
d=u-\ell,\qquad a=-\ell,\qquad j=z-\ell.
\]
A walk from zero with range \([\ell,u]\) becomes, after translation by \(-\ell\), a walk from \(a\) to \(j\) whose minimum is zero and maximum is \(d\). Thus
\[
q_t^{(0)}(\ell,u,z)=n_t(d,a,j).
\]

A walk started at \(2\), translated by the same \(-\ell\), starts at \(a+2\), so
\[
q_t^{(2)}(\ell,u,z)=n_t(d,a+2,j).
\]
The union of the possible \(a\)-supports of these two terms is \(-2\leq a\leq d\). Since a length-\(t\) path has range width at most \(t\), summation of the \(\ell^1\) difference gives the formula.

Every nearest-neighbor step changes parity. Hence \(v_t-v_0\equiv t\pmod2\), which is \(j-a\equiv t\pmod2\). Replacing \(a\) by \(a+2\) does not change this congruence. Thus the two distributions are compared on the same parity lattice.

**Dependencies:** STEP2.

---

### STEP4: Inclusion-exclusion and the image formula

**Claim:** Let \(h_t(d;a,j)\) be \(2^{-t}\) times the number of length-\(t\) nearest-neighbor paths from \(a\) to \(j\) which remain in \([0,d]\), extended by zero when \(d<0\) or either endpoint lies outside \([0,d]\). Then
\[
n_t(d,a,j)
=h_t(d;a,j)-h_t(d-1;a-1,j-1)-h_t(d-1;a,j)
+h_t(d-2;a-1,j-1).
\]
If
\[
p_t(k)=
\begin{cases}
2^{-t}\binom{t}{(t+k)/2},
 &|k|\leq t,\ k\equiv t\pmod2,\\
0,&\text{otherwise},
\end{cases}
\]
then, for \(0\leq a,j\leq d\),
\[
h_t(d;a,j)=\sum_{r\in\mathbb Z}
\left[
p_t(j-a+2r(d+2))
-p_t(j+a+2+2r(d+2))
\right].
\]

**Proof:**

A path remaining in \([0,d]\) has exact minimum zero and maximum \(d\) unless it avoids zero or avoids \(d\). Paths avoiding zero remain in \([1,d]\), and translation downward by one gives
\[
h_t(d-1;a-1,j-1).
\]
Paths avoiding \(d\) contribute \(h_t(d-1;a,j)\). Paths avoiding both remain in \([1,d-1]\), and after translation contribute \(h_t(d-2;a-1,j-1)\). Inclusion-exclusion proves the first formula, including \(d=0,1\) under the stated zero-extension convention.

For the second formula, put \(D=d+2\) and define
\[
F_t(a,j)=\sum_{r\in\mathbb Z}
\bigl[p_t(j-a+2rD)-p_t(j+a+2+2rD)\bigr].
\]
Only finitely many terms are nonzero.

The unrestricted kernel satisfies
\[
p_{t+1}(k)=\tfrac12p_t(k-1)+\tfrac12p_t(k+1).
\]
Therefore, for \(0\leq j\leq d\),
\[
F_{t+1}(a,j)=\tfrac12F_t(a,j-1)+\tfrac12F_t(a,j+1).
\]

At the lower absorbing boundary \(j=-1\), symmetry \(p_t(k)=p_t(-k)\), followed by \(r\mapsto-r\), gives
\[
\sum_r p_t(-1-a+2rD)
=\sum_r p_t(a+1+2rD),
\]
so \(F_t(a,-1)=0\).

At \(j=d+1=D-1\), the negative of
\[
D-1-a+2rD
\]
equals
\[
D+1+a+2(-r-1)D.
\]
Thus the two image sums again cancel and \(F_t(a,d+1)=0\).

At time zero and for \(0\leq a,j\leq d\), the first image sum equals \(\mathbf1_{\{a=j\}}\), while the second is zero: \(j+a+2\) lies strictly between \(0\) and \(2D\), so it cannot equal \(-2rD\). Hence
\[
F_0(a,j)=\mathbf1_{\{a=j\}}.
\]

The killed transition probabilities \(h_t(d;a,j)\) satisfy the same recurrence, boundary values, and initial values. Induction on \(t\) therefore gives \(F_t=h_t\), proving the image formula without invoking an external reflection theorem.

**Dependencies:** STEP3.

---

### STEP5: Explicit binomial estimates

**Claim:** Let
\[
m_t=\max_kp_t(k)=2^{-t}\binom{t}{\lfloor t/2\rfloor}.
\]
For \(t\geq1\),
\[
\frac1{2\sqrt t}\leq m_t\leq\frac1{\sqrt t},
\qquad
\sum_k|p_t(k)-p_t(k-2)|=2m_t.
\]
For \(t\geq2\) and \(k\equiv t\pmod2\),
\[
|p_t(k+2)-2p_t(k)+p_t(k-2)|
\leq
\frac{16}{t}\left(1+\frac{k^2}{t}\right)
\sqrt{\frac2t}\exp\left(-\frac{k^2}{4t}\right).
\]

**Proof:**

Put
\[
c_n=4^{-n}\binom{2n}{n}.
\]
The ratio
\[
\frac{c_{n+1}}{c_n}=\frac{2n+1}{2n+2}
\]
gives, by induction,
\[
\frac1{2\sqrt n}\leq c_n\leq\frac1{\sqrt{2n+1}}
\qquad(n\geq1).
\]
Indeed, the lower-bound induction reduces to
\[
(2n+1)^2\geq4n(n+1),
\]
and the upper-bound induction reduces to
\[
(2n+1)(2n+3)\leq(2n+2)^2.
\]
Both differ from equality by \(1\).

For \(t=2n\), \(m_t=c_n\). For \(t=2n+1\),
\[
m_t
=2^{-(2n+1)}\binom{2n+1}{n}
=c_{n+1}.
\]
The displayed bounds on \(m_t\) follow, with \(t=1\) checked directly.

On the parity lattice of \(t\), the sequence \(p_t(k)\) is nondecreasing up to its mode and nonincreasing afterward. This follows from
\[
\frac{p_t(k+2)}{p_t(k)}
=\frac{t-k}{t+k+2}.
\]
Consequently, the sum of the positive increments from the left tail to the mode is \(m_t\), and the sum of the absolute negative increments from the mode to the right tail is another \(m_t\). For odd \(t\), the equal modes at \(-1\) and \(1\) contribute a zero increment. Hence
\[
\sum_k|p_t(k)-p_t(k-2)|=2m_t.
\]

We now prove the second-difference estimate. First observe the Gaussian envelope
\[
p_t(k)\leq\sqrt{\frac2t}\exp\left(-\frac{k^2}{4t}\right).
\tag{5.1}
\]
By symmetry it suffices to take \(k\geq0\). For even \(t\), writing \(k=2s\) and multiplying the exact ratios gives
\[
\log\frac{p_t(2s)}{m_t}
=\sum_{i=0}^{s-1}
\log\frac{t-2i}{t+2i+2}
\leq-\frac{2s^2}{t+1}
=-\frac{k^2}{2(t+1)}.
\]
Here we used
\[
\log\frac{1-x}{1+x}\leq-2x,\qquad0\leq x<1,
\]
which follows because the derivative of the left side plus \(2x\) is
\[
-\frac2{1-x^2}+2\leq0
\]
and the expression vanishes at zero.

For odd \(t\), beginning at the mode \(1\) gives
\[
\log\frac{p_t(2s+1)}{m_t}
\leq-\frac{2s(s+1)}{t+1}
=-\frac{k^2-1}{2(t+1)}.
\]
Together with \(m_t\leq t^{-1/2}\), these estimates imply (5.1); in the odd case the possible correction in the exponent is at most \(1/(4t)<\log\sqrt2\).

Suppose first that \(|k|\leq t/2\). The exact ratio formulas yield
\[
\frac{p_t(k+2)-2p_t(k)+p_t(k-2)}{p_t(k)}
=
\frac{4(k^2-t-2)}{(t+2)^2-k^2}.
\]
Since \(t\geq2\),
\[
(t+2)^2-k^2\geq\frac34t^2
\]
and
\[
4|k^2-t-2|\leq4(k^2+2t).
\]
It follows that
\[
\left|
\frac{p_t(k+2)-2p_t(k)+p_t(k-2)}{p_t(k)}
\right|
\leq
\frac{16}{t}\left(1+\frac{k^2}{t}\right).
\]
Combining this with (5.1) proves the claim in the central region.

Now suppose \(k>t/2\); the negative case follows by symmetry. Since \(p_t\) decreases on this part of its support,
\[
|p_t(k+2)-2p_t(k)+p_t(k-2)|\leq4p_t(k-2).
\tag{5.2}
\]
For \(t\geq8\), the preceding product estimate gives
\[
p_t(k-2)
\leq t^{-1/2}
\exp\left(
-\frac{(k-2)^2}{2(t+1)}+\frac1{2(t+1)}
\right).
\]
For \(t/2<k\leq t+2\), elementary differentiation of the quadratic exponent gives
\[
\frac{k^2}{4t}
-\frac{(k-2)^2}{2(t+1)}
+\frac1{2(t+1)}
\leq\frac13.
\]
For \(t\geq9\) the quadratic is decreasing on \(k\geq t/2\), so it suffices to substitute \(k=t/2\); the resulting expression is at most \(3/10\). For \(t=8\), the first admissible outer parity point is \(k=6\), where the expression is \(7/24\). Since \(e^{2/3}<2\), one has \(e^{1/3}<\sqrt2\), and hence
\[
p_t(k-2)\leq
\sqrt{\frac2t}\exp\left(-\frac{k^2}{4t}\right).
\]
Moreover,
\[
\frac4t\left(1+\frac{k^2}{t}\right)\geq1
\qquad(k>t/2).
\]
Using this in (5.2) proves the desired estimate.

For \(4\leq t\leq7\), the admissible positive outer points are respectively
\[
\{4,6\},\quad\{3,5,7\},\quad
\{4,6,8\},\quad\{5,7,9\}.
\]
Substitution of the corresponding binomial masses shows that
\[
\frac{p_t(k-2)}
{\frac4t(1+k^2/t)\sqrt{2/t}\,e^{-k^2/(4t)}}<\frac12
\]
at each point. For the first point in each row this follows respectively from
\[
e<3,\quad e^{1/2}<\frac74,\quad e^{2/3}<2,\quad e<3,
\]
and the ratio decreases at the later points. These elementary exponential inequalities follow directly by bounding their power series tails by geometric series. Finally, \(t=2,3\) is checked by substituting their three and four nonzero binomial masses. Outside \([-t-2,t+2]\), the second difference is zero.

This completes all parts of STEP5.

**Dependencies:** STEP3.

---

### STEP6: Diagonal variation estimate ⭐ KEY STEP — unresolved

**Claim from the decomposition:**
\[
A_t\leq
16m_t+
\frac{64}{t^{3/2}}\sum_{r=1}^{\infty}r e^{-r^2/t}
+\frac{64}{t}\sum_{r=1}^{\infty}e^{-r^2/t}
\leq\frac{144}{\sqrt t}.
\tag{6.1}
\]

**Proof status:**

The first inequality in (6.1) is not proved by STEP4 and STEP5 alone. Substitution of the image formula produces several signed families with different image periods \(2d\), \(2(d+1)\), and \(2(d+2)\). Applying the triangle inequality before reconciling these periods loses the cancellation needed for \(t^{-1/2}\). The decomposition asks for a summation-by-parts identity performing that reconciliation, but does not supply the identity or its boundary terms. Consequently, asserting (6.1) here would be circular.

The following rigorous substitute gives an upper bound with one logarithmic loss.

<key-original-step>

#### Coupling lemma

For every integer \(t\geq4\),
\[
A_t\leq\frac{5+3\log t}{\sqrt t}.
\tag{6.2}
\]

Construct two base walks \(X,Y\), started at \(0,2\), as follows. Until
\[
\tau=\inf\{s\geq0:X_s=1\},
\]
use reflected increments, so
\[
Y_s=2-X_s\qquad(0\leq s\leq\tau).
\]
At time \(\tau\), both walks equal \(1\). Thereafter give them identical fresh increments. Each marginal is simple symmetric random walk: before \(\tau\), the increments of \(Y\) are the negatives of independent fair signs, and after the stopping time both walks receive a fresh independent fair-sign sequence.

Let
\[
M=\min_{0\leq s\leq\tau}X_s,\qquad K=1-M.
\]
Before meeting, the range of \(X\) is \([M,1]\), while that of \(Y\) is
\[
[1,2-M]=[1,1+K].
\]
Relative to the meeting point \(1\), the two pre-meeting ranges therefore extend distances \(K\) to the left and right.

Let the common post-meeting walk, translated to start at zero, be \(S\). If before time \(t-\tau\) it hits both \(-K\) and \(K\), then the final ranges of \(X\) and \(Y\) are identical, and their endpoints are already identical. Thus their range-endpoint triples can be coupled to agree on this event.

We require three elementary estimates.

First, if \(T_K=\inf\{s:S_s=K\}\), reflection at the first visit to \(K\) gives
\[
\mathbb P(T_K>s)\leq K m_s\leq\frac K{\sqrt s}.
\tag{6.3}
\]
Indeed, reflection bijects paths which hit \(K\) and finish below \(K\) with paths finishing above \(K\). After cancellation using \(p_s(j)=p_s(-j)\), the remaining endpoint masses occupy exactly \(K\) sites of the parity lattice, each of mass at most \(m_s\).

Second,
\[
\mathbb P(\tau>N)\leq m_N\leq N^{-1/2}.
\tag{6.4}
\]
This is (6.3) with \(K=1\).

Third, for every \(k\geq1\),
\[
\mathbb P(K\geq k)=\frac1k.
\tag{6.5}
\]
The event \(K\geq k\) is that a walk started at zero hits \(1-k\) before it hits \(1\). If \(r(i)\) denotes this probability for a walk started at \(i\in[1-k,1]\), first-step conditioning gives
\[
r(i)=\tfrac12r(i-1)+\tfrac12r(i+1),
\]
with \(r(1-k)=1\) and \(r(1)=0\). The unique affine solution is \(r(i)=(1-i)/k\), so \(r(0)=1/k\). The exit time is almost surely finite because from every interior point there is a fixed positive probability of reaching a boundary during the next \(k\) steps.

Take \(N=\lfloor t/2\rfloor\). On \(\{\tau\leq N\}\), the post-meeting walk has at least \(t/2\) steps. By (6.3), symmetry, and the union bound, its conditional probability of failing to hit both \(-K\) and \(K\) is at most
\[
\frac{2K}{\sqrt{t/2}}
=\frac{2\sqrt2\,K}{\sqrt t}
<\frac{3K}{\sqrt t}.
\]
Also, on \(\{\tau\leq N\}\), \(K\leq N+1\). Therefore (6.5) and the tail-sum formula give
\[
\begin{aligned}
\mathbb E[K;\tau\leq N]
&=\sum_{k=1}^{N+1}\mathbb P(K\geq k,\tau\leq N)\\
&\leq\sum_{k=1}^{N+1}\frac1k
\leq1+\log(N+1)
\leq1+\log t.
\end{aligned}
\]
Since \(N\geq t/4\) for \(t\geq4\), (6.4) yields
\[
\mathbb P(\tau>N)\leq\frac2{\sqrt t}.
\]
Combining the last three estimates, the coupling fails with probability at most
\[
\frac2{\sqrt t}
+\frac3{\sqrt t}\mathbb E[K;\tau\leq N]
\leq\frac{5+3\log t}{\sqrt t}.
\]
For any coupling \((R,R')\),
\[
\|\mathcal L(R)-\mathcal L(R')\|_{\rm TV}
\leq\mathbb P(R\neq R'),
\]
because for every event \(B\),
\[
|\mathbb P(R\in B)-\mathbb P(R'\in B)|
\leq\mathbb P(R\neq R').
\]
This proves (6.2).

</key-original-step><heuristics>The reflection coupling identifies why the unresolved cancellation is subtle. Before meeting, the depth \(K\) has the exact tail \(\mathbb P(K\geq k)=1/k\). Asking the common continuation to cover that whole depth costs order \(K/\sqrt t\); summing the harmonic tail produces \((\log t)/\sqrt t\). An \(O(t^{-1/2})\) proof must therefore exploit cancellation between different possible exact ranges, rather than require pathwise equality of ranges. STEP4’s alternating boundary-attainment formula is a plausible place for this cancellation, but the required signed summation identity remains unproved.</heuristics>

**Dependencies:** STEP4 and STEP5 for the intended but unresolved claim; STEP2 and the self-contained coupling estimates for the rigorous substitute.

---

### STEP7: Upper bound

**Claim from the decomposition:** For \(t\geq2\),
\[
\|P_t^x-P_t^y\|_{\rm TV}\leq A_t\leq\frac{144}{\sqrt t}.
\]

**Proof status:**

The first inequality is proved in STEP2. The second is precisely the unresolved STEP6. What is proved unconditionally is
\[
\|P_t^x-P_t^y\|_{\rm TV}
\leq\frac{5+3\log t}{\sqrt t}
\qquad(t\geq4).
\]
For \(t=1,2,3\), the same displayed bound holds because total variation is at most \(1\), while its right side exceeds \(1\).

**Dependencies:** STEP2, partial STEP6.

---

### STEP8: Explicit lower bound

**Claim:** For every \(t\geq1\),
\[
\|P_t^x-P_t^y\|_{\rm TV}
\geq
\|\mathcal L_0(W_t)-\mathcal L_2(W_t)\|_{\rm TV}
=m_t
\geq\frac1{2\sqrt t}.
\]

**Proof:**

Projection of a lamplighter state \((\eta,z)\) onto \(z\) is a deterministic map. Total variation cannot increase under such a map, by the same direct kernel-contraction calculation as in STEP2.

The endpoint law from zero is \(p_t(k)\), while that from two is \(p_t(k-2)\). Both are supported on the same parity lattice because the initial positions differ by two. Therefore STEP5 gives
\[
\begin{aligned}
\|\mathcal L_0(W_t)-\mathcal L_2(W_t)\|_{\rm TV}
&=\frac12\sum_k|p_t(k)-p_t(k-2)|\\
&=m_t
\geq\frac1{2\sqrt t}.
\end{aligned}
\]

**Dependencies:** STEP2, STEP5.

---

### STEP9: Small times

**Claim:**
\[
\|P_0^x-P_0^y\|_{\rm TV}=1,
\qquad
\|P_1^x-P_1^y\|_{\rm TV}=\frac34.
\]

**Proof:**

At time zero, the two deterministic states \((0,0)\) and \((0,2)\) are distinct, so their laws are mutually singular.

At time one, each chain chooses one of two moves and independently chooses two fair lamp values. Thus each has eight states, each of mass \(1/8\).

From \(x\), the possible endpoints are \(-1,1\); from \(y\), they are \(1,3\). Hence overlap is possible only at endpoint \(1\). On the path \(0\to1\), the potentially nonzero lamps are \(0,1\). On the path \(2\to1\), they are \(2,1\). The resulting states coincide exactly when the lamp at \(0\) in the first chain and the lamp at \(2\) in the second chain are both zero, while the common lamp at \(1\) has the same value. There are exactly two common states, corresponding to the two values at lamp \(1\), each with mass \(1/8\) under both laws.

The overlap mass is therefore \(2/8=1/4\), and hence
\[
\|P_1^x-P_1^y\|_{\rm TV}=1-\frac14=\frac34.
\]
This calculation explicitly uses forced initial zero lamps and does not interpret the base coordinate \(2\) as a lit lamp.

**Dependencies:** STEP1, S1, S2.

---

### STEP10: Proposed explicit constants

**Claim from the decomposition:** With
\[
c=\frac12,\qquad C=144,\qquad t_0=1,
\]
one has
\[
\frac{c}{\sqrt t}
\leq\|P_t^x-P_t^y\|_{\rm TV}
\leq\frac{C}{\sqrt t}
\qquad(t\geq t_0).
\]

**Proof status:**

The lower inequality with \(c=1/2\) is proved for every \(t\geq1\). At \(t=1\), the proposed upper inequality also holds because \(3/4\leq144\). For \(t\geq2\), however, the proposed upper inequality depends on unresolved STEP6 and is therefore not established.

The complete explicit statement actually proved is
\[
\boxed{
\frac1{2\sqrt t}
\leq\|P_t^x-P_t^y\|_{\rm TV}
\leq\frac{5+3\log t}{\sqrt t}
\qquad(t\geq1).
}
\]

**Dependencies:** STEP7, STEP8, STEP9.

---

### GOAL: Main Result

**Claim:** There are explicit constants \(0<c\leq C<\infty\) and an explicit integer \(t_0\) such that
\[
\frac c{\sqrt t}
\leq\|P_t^x-P_t^y\|_{\rm TV}
\leq\frac C{\sqrt t}
\qquad(t\geq t_0).
\]

**Proof status:**

The lower bound is proved with \(c=1/2\) and \(t_0=1\). The required constant upper bound is not proved. The strongest established upper estimate is
\[
\|P_t^x-P_t^y\|_{\rm TV}
\leq\frac{5+3\log t}{\sqrt t}.
\]
Accordingly, the original main result remains incomplete.

**Dependencies:** STEP10.

## Key Ideas

The lamp randomness can be integrated out exactly: conditional on the base range, all lamps in that range are independent fair bits, including the two initially forced-zero sites once they have been visited. This reduces the upper bound to comparing the minimum, maximum, and endpoint of two translated base walks.

The endpoint projection gives the sharp-order lower bound \(m_t\geq(2\sqrt t)^{-1}\). A reflection coupling gives a self-contained upper bound with a logarithmic loss. The loss comes from the exact harmonic tail \(1/k\) of the pre-meeting excursion depth. Removing it requires the signed cancellation in the exact range-endpoint distribution asserted, but not proved, in STEP6.

## First Unresolved Obligation

Prove, self-containedly and with explicit constants, the diagonal finite-difference estimate
\[
\frac12\sum_{d=0}^{t}\sum_{j=0}^{d}\sum_{a=-2}^{d}
|n_t(d,a,j)-n_t(d,a+2,j)|
\leq\frac C{\sqrt t}.
\]
In particular, a complete proof must exhibit and verify the summation-by-parts cancellation among the image terms of periods \(2d\), \(2(d+1)\), and \(2(d+2)\), including \(d=0,1\) and the boundary values \(a=-2,-1,d-1,d\).

## Deviations from Decomposition Plan

STEP1–STEP5, STEP8, and STEP9 were followed. STEP6 was not asserted because the decomposition itself identifies it as the genuine unresolved obligation and supplies no proof of its required cancellation. A rigorous reflection-coupling estimate with upper bound \((5+3\log t)/\sqrt t\) was supplied instead.