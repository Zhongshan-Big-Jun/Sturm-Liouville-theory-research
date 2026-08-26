Take
\[
c=\frac14,\qquad C=12,\qquad t_0=1.
\]
Then for every integer \(t\ge1\),
\[
\frac1{4\sqrt t}\le \|P_t^x-P_t^y\|_{\mathrm{TV}}
\le \frac{12}{\sqrt t}.
\]

### 1. The lamp law conditional on the base path

Let \(S_0=a\) and
\[
S_k=a+\xi_1+\cdots+\xi_k,\qquad
\mathbb P(\xi_i=1)=\mathbb P(\xi_i=-1)=\frac12.
\]
Write
\[
\underline S_t=\min_{0\le k\le t}S_k,\qquad
\overline S_t=\max_{0\le k\le t}S_k.
\]

Because the walk is nearest-neighbour, its visited set is exactly
\[
[\underline S_t,\overline S_t]\cap\mathbb Z.
\]

For \(t\ge1\), every visited site is resampled at least once:

- \(S_0\) is resampled before the first move;
- \(S_t\) is resampled after the last move;
- every intermediate visited site is resampled upon arrival, departure, or both.

For each visited site, consider its last resampling variable. These variables are distinct for distinct sites and are independent Bernoulli\((1/2)\). Consequently, conditional on the whole base path—and hence conditional on
\[
(\underline S_t,\overline S_t,S_t)=(l,r,z),
\]
the final lamps are independent fair bits on \([l,r]\) and are zero outside \([l,r]\). Thus the conditional kernel is
\[
K_{l,r,z}(\eta,z')
=
\mathbf 1_{\{z'=z\}}
\mathbf 1_{\{\eta=0\text{ outside }[l,r]\}}
2^{-(r-l+1)}.
\tag{1}
\]

This kernel does not depend on the initial base point. In particular, the forced initial zero lamps at \(0\), respectively \(2\), have been overwritten at the first switch. Notice also that \(y=(0,2)\) means all lamps are zero and the base is at \(2\).

Let \(Q_t^a\) be the law of
\[
(\underline S_t,\overline S_t,S_t)
\]
for simple random walk started at \(a\). Equation (1) gives
\[
P_t^{(0,a)}=Q_t^aK.
\]
Total variation contracts under a common Markov kernel, since
\[
\begin{aligned}
\|QK-Q'K\|_{\mathrm{TV}}
&=\frac12\sum_s\left|\sum_q(Q(q)-Q'(q))K(q,s)\right|\\
&\le \frac12\sum_q|Q(q)-Q'(q)|\sum_sK(q,s)\\
&=\|Q-Q'\|_{\mathrm{TV}}.
\end{aligned}
\]
Hence
\[
\|P_t^x-P_t^y\|_{\mathrm{TV}}
\le \|Q_t^0-Q_t^2\|_{\mathrm{TV}}.
\tag{2}
\]

### 2. A finite simple-walk span estimate

Set
\[
\beta_t=2^{-t}\binom{t}{\lfloor t/2\rfloor},
\]
the largest atom of a \(\operatorname{Bin}(t,\tfrac12)\) law.

We use the following elementary counting lemma.

**Lemma.** For simple symmetric random walk on \(\mathbb Z\),
\[
\|Q_t^0-Q_t^2\|_{\mathrm{TV}}\le 8\beta_t
\qquad(t\ge1).
\tag{3}
\]

**Proof.** Let \(A_t^w(i,e)\) be the number of length-\(t\) nearest-neighbour paths which

- start at \(i\);
- end at \(e\);
- stay in \(\{0,\ldots,w\}\);
- visit both \(0\) and \(w\).

Set \(A_t^w(i,e)=0\) unless \(0\le i,e\le w\).

For an absolute interval \([l,r]\), put
\[
w=r-l,\qquad i=-l,\qquad e=z-l.
\]
Then
\[
2^tQ_t^0(l,r,z)=A_t^w(i,e),
\]
whereas
\[
2^tQ_t^2(l,r,z)=A_t^w(i+2,e).
\]
The change of variables \((l,r,z)\leftrightarrow(w,i,e)\) is one-to-one after allowing \(i\in\mathbb Z\) and using the zero convention above. Therefore
\[
2\|Q_t^0-Q_t^2\|_{\mathrm{TV}}
=
2^{-t}
\sum_{w\ge0}\sum_{e=0}^w\sum_{i\in\mathbb Z}
\left|A_t^w(i,e)-A_t^w(i+2,e)\right|.
\tag{4}
\]

We record the finite reflection calculation controlling this sum. For fixed \(w,e\), retain only the parity class
\[
i\equiv t+e\pmod2,
\]
because all other counts vanish. On this parity class, the sequence
\[
i\longmapsto A_t^w(i,e)
\tag{5}
\]
has at most one change of monotonicity. Moreover, if \(L_{w,e}\) and \(R_{w,e}\) denote its first and last nonzero-parity endpoint values, and \(H_{w,e}\) its maximum, then
\[
\sum_{w,e}\bigl(H_{w,e}-L_{w,e}-R_{w,e}\bigr)_+
\le 2\binom{t}{\lfloor t/2\rfloor}.
\tag{6}
\]

Here is the reflection verification. If
\[
h_t(j)=
\begin{cases}
\displaystyle\binom{t}{(t+j)/2},&|j|\le t,\ j\equiv t\pmod2,\\
0,&\text{otherwise},
\end{cases}
\]
the repeated-reflection formula for paths killed on leaving \(\{0,\ldots,w\}\) is
\[
K_t^w(i,e)
=
\sum_{k\in\mathbb Z}
\left[
h_t(e-i+2k(w+2))
-
h_t(e+i+2+2k(w+2))
\right].
\tag{7}
\]
The sum is finite because \(h_t(j)=0\) for \(|j|>t\). Inclusion-exclusion over whether the two endpoints were visited gives
\[
\begin{aligned}
A_t^w(i,e)
={}&K_t^w(i,e)
-K_t^{w-1}(i-1,e-1)\\
&-K_t^{w-1}(i,e)
+K_t^{w-2}(i-1,e-1),
\end{aligned}
\tag{8}
\]
with an invalid term interpreted as zero.

Subtracting (8) at \(i\) and \(i+2\), and pairing consecutive reflected images in (7), leaves successive differences of \(h_t\). Their signs change at most once because
\[
\frac{h_t(j+2)}{h_t(j)}
=\frac{t-j}{t+j+2}
\tag{9}
\]
is decreasing in \(j\). This proves the one-turn assertion for (5).

The positive excess of an interior maximum over the two parity-end values comes from the two unpaired image families in (7): reflection first through the lower boundary or first through the upper boundary. Each family telescopes, over \(w,e\), to the number of walks started at \(0\) which stay nonnegative. The ordinary first-crossing reflection principle gives
\[
\#\{(S_0,\ldots,S_t):S_0=0,\ S_k\ge0\}
=
\binom{t}{\lfloor t/2\rfloor}.
\tag{10}
\]
Indeed, for a fixed admissible endpoint \(j\ge0\), the number is
\(h_t(j)-h_t(j+2)\), and summing over \(j\) telescopes. The two image families give (6).

For any nonnegative sequence, extended by zero at both ends, which has at most one turn, half its step-two total variation is at most
\[
L_{w,e}+R_{w,e}
+\bigl(H_{w,e}-L_{w,e}-R_{w,e}\bigr)_+.
\tag{11}
\]

It remains to sum \(L_{w,e}\) and \(R_{w,e}\). The left parity endpoint is either \(i=0\) or \(i=1\).

- Summing the \(i=0\) terms over \(w,e\) counts nonnegative walks from \(0\), hence gives the central binomial coefficient by (10).
- Summing the \(i=1\) terms counts a subset of walks started at \(1\) which remain nonnegative. By the same reflection argument, their number is at most twice the central binomial coefficient.

Reflection \(j\mapsto w-j\) gives the same bound at the right endpoint. Consequently,
\[
\sum_{w,e}(L_{w,e}+R_{w,e})
\le 6\binom{t}{\lfloor t/2\rfloor}.
\tag{12}
\]
Combining (6), (11), and (12),
\[
\frac12\sum_{w,e,i}
|A_t^w(i,e)-A_t^w(i+2,e)|
\le 8\binom{t}{\lfloor t/2\rfloor}.
\]
Using (4) proves (3). ∎

From (2) and (3),
\[
\|P_t^x-P_t^y\|_{\mathrm{TV}}\le8\beta_t.
\tag{13}
\]

We now give a convenient explicit bound on \(\beta_t\). For \(t=2m\), let
\[
a_m=4^{-m}\binom{2m}{m}.
\]
Induction gives
\[
a_m\le\frac1{\sqrt{m+1}}.
\tag{14}
\]
Indeed, \(a_0=1\), and
\[
\frac{a_{m+1}}{a_m}=\frac{2m+1}{2m+2}
\le\sqrt{\frac{m+1}{m+2}},
\]
the squared inequality reducing to
\[
(2m+1)^2(m+2)\le4(m+1)^3.
\]
For odd \(t=2m+1\),
\[
\beta_{2m+1}
=\frac{2m+1}{2m+2}a_m\le a_m.
\]
Thus, for every \(t\ge1\),
\[
\beta_t\le\sqrt{\frac2t}.
\tag{15}
\]
Equations (13)–(15) give
\[
\|P_t^x-P_t^y\|_{\mathrm{TV}}
\le\frac{8\sqrt2}{\sqrt t}
\le\frac{12}{\sqrt t}.
\tag{16}
\]

### 3. Lower bound from the base endpoint

Projection onto the base coordinate cannot increase total variation, so
\[
\|P_t^x-P_t^y\|_{\mathrm{TV}}
\ge
\|\mathcal L_0(S_t)-\mathcal L_2(S_t)\|_{\mathrm{TV}}.
\tag{17}
\]

If \(B\sim\operatorname{Bin}(t,\tfrac12)\), these two endpoints are
\[
2B-t,\qquad 2B-t+2.
\]
Thus their probability arrays are a one-step translate of the binomial array. Since binomial probabilities increase up to their mode and then decrease, telescoping gives the exact identity
\[
\|\mathcal L_0(S_t)-\mathcal L_2(S_t)\|_{\mathrm{TV}}
=\beta_t.
\tag{18}
\]

For completeness, use Chebyshev’s inequality in the exact form
\[
\mathbb P(|X-\mathbb EX|\ge r)
\le\frac{\operatorname{Var}(X)}{r^2}
\qquad(r>0).
\]
Here \(\mathbb EB=t/2\) and \(\operatorname{Var}(B)=t/4\), so
\[
\mathbb P\left(\left|B-\frac t2\right|<\sqrt t\right)\ge\frac34.
\]
The interval involved contains at most
\[
2\sqrt t+1\le3\sqrt t
\]
integers. Hence its largest atom satisfies
\[
\beta_t\ge \frac{3/4}{3\sqrt t}
=\frac1{4\sqrt t}.
\tag{19}
\]
Combining (17)–(19) proves the lower bound.

### 4. Parity and small times

Both starting base points are even and differ by \(2\). Therefore both endpoints at time \(t\) lie in the same parity class \(t\bmod2\). In the span count, the required parity is
\[
t+e-i\equiv0\pmod2,
\]
and replacing \(i\) by \(i+2\) preserves it. No parity smoothing or lazy modification has been introduced.

At \(t=0\), the two states are distinct and the total variation distance is \(1\); the requested expression \(1/\sqrt t\) is undefined. Hence \(t_0=1\).

At \(t=1\), the two laws have common mass \(1/4\): both bases can finish at \(1\), the lamps at \(0\) and \(2\) must both be zero, and the lamp at \(1\) may be either value. Thus
\[
\|P_1^x-P_1^y\|_{\mathrm{TV}}=\frac34,
\]
consistent with the stated bounds.