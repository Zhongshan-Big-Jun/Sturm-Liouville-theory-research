# Proof

## Problem Statement

# Frozen main task: H^s operator-domain vs abstract completion

Let `K_c = -d^2/dx^2 + c` on `[-1,1]` with Krein boundary condition
`f'(±1) = (f(1)-f(-1))/2`, `c > 0`. Let `H^s`, `s >= 4`, be the left-definite
space associated with `K_c`. Let `{Q_n^(s)}` be the SL_hs orthogonal polynomial
system defined via the isometries `K_c^{-r}` on `L^2` or `H^1`.

Prove or disprove, for integer `s >= 4`:

1. Give a necessary and sufficient condition for `Q_n^(s) ∈ D(K_c^(s/2))`.
2. Determine whether the operator-domain completion `D(K_c^(s/2))` equals the
   abstract completion obtained from the left-definite inner product on
   polynomials.
3. Determine whether `span{Q_n^(s)}` is dense in `D(K_c^(s/2))` under the
   operator-domain reading.

The complete polynomial degree spectrum is a bonus, not a completion gate.

Rules: do not inspect repository history, current project files, known solution,
or network. State all external theorems with hypotheses. Numerical evidence is
not proof.

## Proof

We use the convention that all inner products are linear in their first argument.

<cite>type=survey-status; label=Offline related-work status; title=Offline related-work status; authors=not supplied; source_url=related_info/related_work.md; verifier_locator=opening paragraph; statement_match=exact; statement=No external literature, repository result, prior answer, citation, or mathematical hint is available in this blind arm. Every theorem used must be proved self-containedly or identified as unverified.; usage=No external theorem is imported below; all auxiliary mathematical facts used in the proof are proved in place.</cite>

### STEP1: The operator domain, form domain, and trace conditions

**Claim:** Put \(I=(-1,1)\), \(L=c-D^2\), and
\[
 b_\pm(g)=g'(\pm1)-\frac{g(1)-g(-1)}2.
\]
For \(u,v\in H^1(I)\), define
\[
 h(u)=\int_{-1}^1|u'|^2\,dx-\frac{|u(1)-u(-1)|^2}{2}
\]
and
\[
 \mathfrak a_c(u,v)
 =\int_{-1}^1u'\overline{v'}\,dx
 +c\int_{-1}^1u\overline v\,dx
 -\frac{(u(1)-u(-1))\overline{(v(1)-v(-1))}}2.
\]
Then \(h\ge0\), \(\mathfrak a_c\) is equivalent to the \(H^1\)-inner product,
\[
 D(K_c)=\{u\in H^2(I):b_+(u)=b_-(u)=0\},\qquad
 D(K_c^{1/2})=H^1(I),
\]
and
\[
 \mathfrak a_c(u,v)=\langle K_cu,v\rangle_2
 \quad(u\in D(K_c),\ v\in H^1(I)).
\]
If \(s=2m+\varepsilon\), where \(\varepsilon\in\{0,1\}\), then
\[
 D(K_c^{s/2})
 =
 \left\{f\in H^s(I):
 b_\pm(f^{(2\ell)})=0,\ 0\le\ell<m\right\}.
\]
Moreover,
\[
 A_{s,c}\|f\|_{H^s}
 \le \|K_c^{s/2}f\|_2
 \le B_{s,c}\|f\|_{H^s}
\]
on this domain.

**Proof:**

Set
\[
 d=\frac{u(1)-u(-1)}2.
\]
Since \(\int_{-1}^1u'=2d\), expansion gives
\[
 \int_{-1}^1|u'-d|^2
 =\int_{-1}^1|u'|^2
   -2\operatorname{Re}\!\left(\overline d\int_{-1}^1u'\right)
   +2|d|^2
 =\int_{-1}^1|u'|^2-2|d|^2=h(u).
\]
Thus
\[
 h(u)=\int_{-1}^1\left|u'(x)-\frac{u(1)-u(-1)}2\right|^2dx\ge0.
\]

We next prove coercivity without invoking an elliptic estimate. Let
\[
 \mu=\frac12\int_{-1}^1u(x)\,dx,\qquad w(x)=u(x)-\mu-dx.
\]
Then \(\int_Iw=0\) and \(w'=u'-d\). If \(z\in H^1(I)\) has mean zero, then
\[
 z(x)=\frac12\int_{-1}^1(z(x)-z(y))\,dy,
\]
and the fundamental theorem of calculus and Cauchy–Schwarz give
\[
 |z(x)|\le \sqrt2\,\|z'\|_2,\qquad
 \|z\|_2\le2\|z'\|_2.
\]
Consequently,
\[
 \|w\|_2\le2h(u)^{1/2}.
\]
Also \(\|\mu\|_2\le\|u\|_2\), while
\[
 \|dx\|_2\le\|u\|_2+\|\mu\|_2+\|w\|_2
 \le2\|u\|_2+2h(u)^{1/2}.
\]
Since \(\|dx\|_2=\sqrt{2/3}|d|\), this bounds \(d\), and hence
\[
 \|u'\|_2\le\|u'-d\|_2+\sqrt2|d|
 \le C\bigl(h(u)^{1/2}+\|u\|_2\bigr).
\]
Because
\[
 \mathfrak a_c(u,u)=h(u)+c\|u\|_2^2,
\]
there is \(A_c>0\) such that
\[
 A_c\|u\|_{H^1}^2\le\mathfrak a_c(u,u).
\]
The reverse estimate follows from
\[
 0\le h(u)\le\|u'\|_2^2,
\]
so
\[
 \mathfrak a_c(u,u)\le\max\{1,c\}\|u\|_{H^1}^2.
\]

Now define
\[
 Au=Lu=-u''+cu,\qquad
 D(A)=\{u\in H^2(I):b_+(u)=b_-(u)=0\}.
\]
For \(u\in D(A)\) and \(v\in H^1(I)\), integration by parts yields
\[
 \langle Au,v\rangle_2
 =\int_Iu'\overline{v'}+c\int_Iu\overline v
   -u'(1)\overline{v(1)}+u'(-1)\overline{v(-1)}.
\]
Writing \(d=(u(1)-u(-1))/2=u'(1)=u'(-1)\), the boundary term is
\[
 -d\,\overline{v(1)-v(-1)},
\]
which proves
\[
 \langle Au,v\rangle_2=\mathfrak a_c(u,v).
\]
In particular, \(A\) is symmetric and
\[
 \langle Au,u\rangle_2=\mathfrak a_c(u,u)\ge c\|u\|_2^2.
\]

We verify self-adjointness. Suppose \(v\in D(A^*)\). There is \(g\in L^2(I)\) such that
\[
 \langle Au,v\rangle_2=\langle u,g\rangle_2
 \quad(u\in D(A)).
\]
Testing first against \(C_c^\infty(I)\subset D(A)\) shows distributionally that
\[
 -v''+cv=g.
\]
Hence \(v''=cv-g\in L^2\), and \(v\in H^2(I)\): indeed, the double integral
\[
 y(x)=\int_{-1}^x(x-t)(cv-g)(t)\,dt
\]
belongs to \(H^2\) and has \(y''=cv-g\); the distribution \(v-y\) has zero second derivative and therefore is affine.

The Green boundary expression must now vanish:
\[
 \bigl[-u'\overline v+u\overline{v'}\bigr]_{-1}^{1}=0
 \quad(u\in D(A)).
\]
The endpoint values \(\alpha=u(-1)\), \(\beta=u(1)\) can be chosen arbitrarily: a cubic Hermite polynomial realizes these values together with
\[
 u'(-1)=u'(1)=\frac{\beta-\alpha}{2}.
\]
Substitution into the boundary expression gives
\[
 \beta\left(\overline{v'(1)}
       -\frac{\overline{v(1)-v(-1)}}2\right)
 +\alpha\left(\frac{\overline{v(1)-v(-1)}}2
       -\overline{v'(-1)}\right)=0
\]
for every \(\alpha,\beta\). Thus \(b_+(v)=b_-(v)=0\), so \(v\in D(A)\). Therefore \(A=A^*\), and \(A\ge cI>0\).

For completeness, we now identify the square-root form domain self-containedly. The inequality \(A\ge cI\) implies
\[
 \|Au\|_2\ge c\|u\|_2.
\]
Since \(A\) is self-adjoint, its range is closed and
\[
 \operatorname{Ran}(A)^\perp=\ker A^*=\ker A=\{0\};
\]
hence \(A\) is onto and \(B=A^{-1}\) is bounded, positive, and self-adjoint.

For \(u\in D(A)\),
\[
 A_c\|u\|_{H^1}^2
 \le\langle Au,u\rangle
 \le\|Au\|_2\|u\|_2
 \le c^{-1}\|Au\|_2^2,
\]
and
\[
 \|u''\|_2=\|cu-Au\|_2\le2\|Au\|_2.
\]
Thus
\[
 \|u\|_{H^2}\le C_c\|Au\|_2.
\]
It follows that \(B\) maps bounded subsets of \(L^2\) to bounded subsets of \(H^2\). The embedding \(H^2(I)\hookrightarrow L^2(I)\) is compact: a bounded \(H^2\)-sequence is uniformly bounded and has a common \(1/2\)-Hölder modulus by
\[
 |u(x)-u(y)|\le\|u'\|_2|x-y|^{1/2};
\]
successive extraction on finite meshes produces a uniformly convergent subsequence. Hence \(B\) is compact.

We recall and prove the compact positive spectral fact needed here. If \(B\) is compact, positive, self-adjoint, and injective on a separable Hilbert space, it has an orthonormal basis of eigenvectors with positive eigenvalues. Indeed, the supremum
\[
 M=\sup_{\|x\|=1}\langle Bx,x\rangle
\]
is attained: take a maximizing sequence, extract a weakly convergent subsequence, and then use compactness to obtain strong convergence of its images under \(B\). The limit has norm one and maximizes the Rayleigh quotient. Varying it in real and imaginary directions orthogonal to itself shows \(Bx=Mx\). Repeating this argument on orthogonal complements gives mutually orthogonal eigenvectors. If their closed span had a nonzero orthogonal complement, the restriction of \(B\) to that complement would again have a positive maximizing eigenvector. Injectivity excludes a remaining zero-eigenspace. Compactness forces the nonzero eigenvalues to tend to zero.

Apply this to \(B=A^{-1}\). We obtain an orthonormal basis \(\{e_j\}\) and numbers
\[
 Be_j=\mu_je_j,\qquad
 Ae_j=\lambda_je_j,\qquad
 \lambda_j=\mu_j^{-1}\ge c.
\]
The powers of \(A\) are therefore
\[
 D(A^\alpha)=
 \left\{\sum_ja_je_j:\sum_j\lambda_j^{2\alpha}|a_j|^2<\infty\right\},
 \qquad
 A^\alpha\sum_ja_je_j=\sum_j\lambda_j^\alpha a_je_j.
\]
On \(D(A)\),
\[
 \mathfrak a_c(u,u)=\langle Au,u\rangle
 =\sum_j\lambda_j|a_j|^2.
\]
Moreover, \(D(A)\) is dense in \(H^1(I)\) for the form norm. To see this, if \(w\in H^1\) is form-orthogonal to \(D(A)\), then for each \(f\in L^2\), putting \(u=A^{-1}f\) gives
\[
 0=\mathfrak a_c(u,w)=\langle f,w\rangle.
\]
Thus \(w=0\). Because the form norm is complete and equivalent to the \(H^1\)-norm, its completion of \(D(A)\) is \(H^1\). On the other hand, the eigenfunction formula shows that this same completion is
\[
 \left\{\sum_ja_je_j:\sum_j\lambda_j|a_j|^2<\infty\right\}
 =D(A^{1/2}).
\]
Therefore
\[
 D(A^{1/2})=H^1(I),\qquad
 \mathfrak a_c(u,v)=\langle A^{1/2}u,A^{1/2}v\rangle_2.
\]

We now compute all integral and half-integral power domains. From the coefficient description,
\[
 D(A^{r+t})
 =\{f\in D(A^r):A^rf\in D(A^t)\}
 \qquad(r,t\ge0).
\]
Induction gives
\[
 D(A^m)
 =
 \{f\in H^{2m}(I):L^jf\in D(A),\ 0\le j<m\}.
\]
Indeed, the assertion is true for \(m=1\). If \(f\in D(A^{m+1})\), then \(f\in D(A)\), \(Lf=Af\in D(A^m)\), and \(f''=cf-Lf\) recursively gives \(f\in H^{2m+2}\). The converse follows by reversing these statements.

Now
\[
 L^j=\sum_{k=0}^j\binom jk c^{j-k}(-1)^kD^{2k},
\]
so
\[
 b_\pm(L^jf)
 =\sum_{k=0}^j\binom jk c^{j-k}(-1)^k
   b_\pm(f^{(2k)}).
\]
For \(j=0,\ldots,m-1\), this is a triangular linear system with diagonal entries \((-1)^j\). Hence
\[
 b_\pm(L^jf)=0\ (0\le j<m)
 \quad\Longleftrightarrow\quad
 b_\pm(f^{(2\ell)})=0\ (0\le\ell<m).
\]
Therefore
\[
 D(A^m)=
 \{f\in H^{2m}(I):b_\pm(f^{(2\ell)})=0,\ 0\le\ell<m\}.
\]

Likewise,
\[
 D(A^{m+1/2})
 =\{f\in D(A^m):A^mf=L^mf\in H^1(I)\}.
\]
If \(f\in H^{2m}\), then differentiating
\[
 L^mf=(-1)^mf^{(2m)}+\text{a linear combination of lower even derivatives}
\]
shows that \(L^mf\in H^1\) precisely when \(f\in H^{2m+1}\). Consequently,
\[
 D(A^{m+1/2})
 =
 \{f\in H^{2m+1}(I):b_\pm(f^{(2\ell)})=0,\ 0\le\ell<m\}.
\]
Writing out \(b_\pm=0\) gives
\[
 f^{(2\ell+1)}(1)=f^{(2\ell+1)}(-1)
 =\frac{f^{(2\ell)}(1)-f^{(2\ell)}(-1)}2.
\]

It remains to prove the stated norm equivalence. First, for \(u\in H^{r+2}(I)\),
\[
 \|u\|_{H^{r+2}}
 \le C_{r,c}\bigl(\|Lu\|_{H^r}+\|u\|_2\bigr).
 \tag{1}
\]
To justify this, the decomposition used above, now applied to \(u'\), gives
\[
 \|u'\|_2\le C(\|u\|_2+\|u''\|_2).
\]
Since \(u''=cu-Lu\), this controls the first two derivatives. Differentiating
\[
 u^{(k+2)}=cu^{(k)}-(Lu)^{(k)}
\]
then controls all derivatives through order \(r+2\), one after another.

Let \(g_j=A^jf=L^jf\). Because every spectral value is at least \(c\),
\[
 \|g_j\|_2\le c^{j-m}\|g_m\|_2,\qquad 0\le j\le m.
\]
Repeated use of (1) therefore gives
\[
 \|f\|_{H^{2m}}\le C_{m,c}\|A^mf\|_2.
\]
The reverse inequality follows immediately by expanding the differential expression \(L^m\).

In the odd case, repeated use of (1) gives
\[
 \|f\|_{H^{2m+1}}\le C_{m,c}\|L^mf\|_{H^1}.
\]
By form coercivity,
\[
 \|L^mf\|_{H^1}
 \le A_c^{-1/2}\mathfrak a_c(L^mf,L^mf)^{1/2}
 =A_c^{-1/2}\|A^{m+1/2}f\|_2.
\]
Conversely,
\[
 \|A^{m+1/2}f\|_2^2
 =\mathfrak a_c(L^mf,L^mf)
 \le B_c\|L^mf\|_{H^1}^2
 \le C_{m,c}\|f\|_{H^{2m+1}}^2.
\]
This proves the domain and norm assertions.

**Dependencies:** S1. This completes STEP1.

---

### STEP2: Algebraic left-definite polynomials

**Claim:** Let \(\mathcal P\) be the complex polynomial algebra and put
\[
 \langle u,v\rangle_0=\langle u,v\rangle_{L^2(I)},\qquad
 \langle u,v\rangle_1=\mathfrak a_c(u,v).
\]
Let \(R_n^{(\varepsilon)}\) be the unique monic degree-\(n\) polynomial orthogonal to lower-degree polynomials in \(\langle\cdot,\cdot\rangle_\varepsilon\). For \(s=2m+\varepsilon\),
\[
 [p,q]^{\mathrm{alg}}_s
 =\langle L^mp,L^mq\rangle_\varepsilon.
\]
Then
\[
 L^mQ_n^{(s)}=c^mR_n^{(\varepsilon)}
\]
and
\[
 Q_n^{(s)}
 =\left(1-\frac{D^2}{c}\right)^{-m}R_n^{(\varepsilon)}
 =\sum_{k=0}^{\lfloor n/2\rfloor}
   \binom{m+k-1}{k}c^{-k}
   \bigl(R_n^{(\varepsilon)}\bigr)^{(2k)}.
\]
In particular, \(\deg Q_n^{(s)}=n\), and the first \(N+1\) such polynomials span \(\mathcal P_N\).

**Proof:**

The form inner product is positive definite by STEP1, so ordinary finite-dimensional Gram–Schmidt gives a unique monic \(R_n^{(\varepsilon)}\).

The polynomial left-definite construction is the pullback by the formal differential expression \(L^m\): after \(m\) inverse-isometry steps, the terminal inner product is \(L^2\) when \(\varepsilon=0\) and the form inner product when \(\varepsilon=1\). Thus on algebraic polynomial vectors it is precisely
\[
 [p,q]^{\mathrm{alg}}_s
 =\langle L^mp,L^mq\rangle_\varepsilon.
\]

On \(\mathcal P_N\),
\[
 L^m=c^m\left(1-\frac{D^2}{c}\right)^m
\]
is triangular in the monomial basis and has diagonal \(c^m\ne0\). It is therefore bijective on \(\mathcal P_N\). If \(Q_n^{(s)}\) is monic and orthogonal to \(\mathcal P_{n-1}\), then \(L^mQ_n^{(s)}\) has degree \(n\), leading coefficient \(c^m\), and is orthogonal in the terminal inner product to \(L^m\mathcal P_{n-1}=\mathcal P_{n-1}\). Hence uniqueness of the monic terminal orthogonal polynomial gives
\[
 L^mQ_n^{(s)}=c^mR_n^{(\varepsilon)}.
\]

Because \(D^2\) is nilpotent on each \(\mathcal P_N\), the binomial series terminates:
\[
 (1-z)^{-m}=\sum_{k\ge0}\binom{m+k-1}{k}z^k.
\]
Substituting \(z=D^2/c\) gives the asserted formula. Its first term is \(R_n^{(\varepsilon)}\), while every other term has degree at most \(n-2\). Therefore \(Q_n^{(s)}\) is monic of degree \(n\). A sequence containing exactly one monic polynomial of each degree is triangularly related to \(1,x,\ldots,x^N\), so
\[
 \operatorname{span}\{Q_0^{(s)},\ldots,Q_N^{(s)}\}=\mathcal P_N.
\]

**Dependencies:** STEP1. This completes STEP2.

---

### STEP3: Reduction to one boundary condition

**Claim:** The trace criterion from STEP1 is necessary and sufficient for \(Q_n^{(s)}\) to lie in \(D(K_c^{s/2})\). If
\[
 U_n^{(\varepsilon)}
 =\left(1-\frac{D^2}{c}\right)^{-1}R_n^{(\varepsilon)}
 =\sum_{k=0}^{\lfloor n/2\rfloor}
   c^{-k}\bigl(R_n^{(\varepsilon)}\bigr)^{(2k)},
\]
then
\[
 LU_n^{(\varepsilon)}=cR_n^{(\varepsilon)}
\]
and
\[
 Q_n^{(s)}\in D(K_c^{s/2})
 \quad\Longrightarrow\quad
 U_n^{(\varepsilon)}\in D(K_c).
\]

**Proof:**

The necessary-and-sufficient trace condition follows immediately from STEP1:
\[
 Q_n^{(s)}\in D(K_c^{s/2})
\]
if and only if, for \(0\le\ell<m\),
\[
 \bigl(Q_n^{(s)}\bigr)^{(2\ell+1)}(1)
 =\bigl(Q_n^{(s)}\bigr)^{(2\ell+1)}(-1)
 =\frac{
  \bigl(Q_n^{(s)}\bigr)^{(2\ell)}(1)
  -\bigl(Q_n^{(s)}\bigr)^{(2\ell)}(-1)}2.
\]

The terminating geometric series gives
\[
 \left(1-\frac{D^2}{c}\right)U_n^{(\varepsilon)}
 =R_n^{(\varepsilon)},
\]
hence \(LU_n^{(\varepsilon)}=cR_n^{(\varepsilon)}\).

Algebraically, STEP2 gives
\[
 L^{m-1}Q_n^{(s)}
 =c^{m-1}\left(1-\frac{D^2}{c}\right)^{-1}
   R_n^{(\varepsilon)}
 =c^{m-1}U_n^{(\varepsilon)}.
\]
If \(s=2m\) and \(Q_n^{(s)}\in D(K_c^m)\), then
\[
 K_c^{m-1}Q_n^{(s)}\in D(K_c).
\]
If \(s=2m+1\), then
\[
 K_c^{m-1}Q_n^{(s)}\in D(K_c^{3/2})\subset D(K_c).
\]
On these domains the operator powers agree with the differential powers, so in either case \(c^{m-1}U_n^{(\varepsilon)}\in D(K_c)\), and \(c>0\) yields the conclusion.

**Dependencies:** STEP1, STEP2. This completes STEP3.

---

### STEP4: Even-order obstruction ⭐ KEY STEP

**Claim:** If \(\varepsilon=0\) and \(n\ge2\), then
\[
 U_n^{(0)}\notin D(K_c).
\]

**Proof:**

<key-original-step>
Let
\[
 U=U_n^{(0)},\qquad R=R_n^{(0)}.
\]
Assume for contradiction that \(U\in D(K_c)\). From the terminating inverse formula,
\[
 U-R=\sum_{k=1}^{\lfloor n/2\rfloor}c^{-k}R^{(2k)}
 \in\mathcal P_{n-2}.
\]
Since \(R\) is \(L^2\)-orthogonal to every polynomial of degree below \(n\),
\[
 \langle R,U-R\rangle_2=0.
 \tag{2}
\]
Thus
\[
 \langle R,U\rangle_2=\|R\|_2^2
\]
and, by the orthogonal decomposition \(U=R+(U-R)\),
\[
 \|U\|_2^2=\|R\|_2^2+\|U-R\|_2^2.
 \tag{3}
\]

By STEP3, \(K_cU=LU=cR\). Since \(U\in D(K_c)\), the form identity in STEP1 gives
\[
 \mathfrak a_c(U,U)=\langle K_cU,U\rangle_2
 =c\langle R,U\rangle_2
 =c\|R\|_2^2.
 \tag{4}
\]
On the other hand,
\[
 \mathfrak a_c(U,U)=h(U)+c\|U\|_2^2.
\]
Using (3) in (4), we obtain the exact identity
\[
 h(U)+c\|U-R\|_2^2=0.
 \tag{5}
\]
Both summands in (5) are nonnegative and \(c>0\). Therefore
\[
 U=R,\qquad h(U)=0.
\]
The identity proved in STEP1 gives
\[
 0=h(U)=\int_{-1}^1|U'-d|^2,\qquad
 d=\frac{U(1)-U(-1)}2.
\]
Hence \(U'=d\) almost everywhere, so \(U\) is affine. But \(U\) has the same leading term as the monic degree-\(n\) polynomial \(R\), and therefore \(\deg U=n\ge2\). This is a contradiction.
</key-original-step><heuristics>The inverse-polynomial correction \(U-R\) has lower degree and is therefore invisible to Legendre orthogonality. If \(U\) also satisfied the operator boundary condition, pairing its equation with \(U\) would equate its full form energy with only the \(L^2\)-energy of \(R\). The difference is exactly the sum of two nonnegative quantities in (5), so equality is possible only for an affine polynomial.</heuristics>

**Dependencies:** STEP1, STEP2, STEP3. This completes STEP4.

---

### STEP5: Odd-order obstruction ⭐ KEY STEP

**Claim:** If \(\varepsilon=1\) and \(n\ge2\), then
\[
 U_n^{(1)}\notin D(K_c).
\]

**Proof:**

<key-original-step>
Let
\[
 U=U_n^{(1)},\qquad R=R_n^{(1)},
\]
and assume \(U\in D(K_c)\). Again,
\[
 U-R\in\mathcal P_{n-2}.
\]
The defining form orthogonality of \(R\) therefore gives
\[
 \mathfrak a_c(R,U-R)=0,
\]
or equivalently
\[
 \mathfrak a_c(R,U)=\mathfrak a_c(R,R).
 \tag{6}
\]

Since \(K_cU=cR\), the form association from STEP1 gives
\[
 \mathfrak a_c(U,R)=\langle K_cU,R\rangle_2
 =c\|R\|_2^2.
\]
The form is Hermitian, and the right side is real, so
\[
 \mathfrak a_c(R,U)=c\|R\|_2^2.
\]
Combining this with (6) yields
\[
 \mathfrak a_c(R,R)=c\|R\|_2^2.
\]
Because
\[
 \mathfrak a_c(R,R)=h(R)+c\|R\|_2^2,
\]
we conclude that \(h(R)=0\). The equality characterization from STEP1 then makes \(R\) affine. This contradicts the fact that \(R\) is monic of degree \(n\ge2\).
</key-original-step><heuristics>For odd order, the relevant terminal orthogonality is form orthogonality rather than \(L^2\)-orthogonality. It removes the lower-degree correction \(U-R\) directly from the form pairing. The operator equation then forces the form energy of \(R\) to equal its \(cL^2\)-part, leaving zero boundary-corrected derivative energy and hence only an affine possibility.</heuristics>

**Dependencies:** STEP1, STEP2, STEP3. This completes STEP5.

---

### STEP6: Complete degree spectrum

**Claim:** For every integer \(s\ge4\), every \(c>0\), and every \(n\ge0\),
\[
 \boxed{
 Q_n^{(s)}\in D(K_c^{s/2})
 \quad\Longleftrightarrow\quad
 n\in\{0,1\}.}
\]

**Proof:**

For either terminal inner product,
\[
 R_0^{(\varepsilon)}=1.
\]
Also \(x\) is orthogonal to constants: in \(L^2\) this follows from oddness, while
\[
 \mathfrak a_c(x,1)
 =c\int_{-1}^1x\,dx=0.
\]
Thus
\[
 R_1^{(\varepsilon)}=x.
\]
All second and higher derivatives of these two polynomials vanish, so STEP2 gives
\[
 Q_0^{(s)}=1,\qquad Q_1^{(s)}=x.
\]

Every affine polynomial \(a+bx\) satisfies
\[
 (a+bx)'(1)=(a+bx)'(-1)=b
 =\frac{(a+b)-(a-b)}2,
\]
and all higher trace conditions vanish. Thus \(1,x\in D(K_c^{s/2})\). In fact,
\[
 K_c(a+bx)=c(a+bx).
\]

For \(n\ge2\), STEP3 says that membership of \(Q_n^{(s)}\) would imply \(U_n^{(\varepsilon)}\in D(K_c)\). STEP4 excludes this when \(\varepsilon=0\), and STEP5 excludes it when \(\varepsilon=1\).

**Dependencies:** STEP3, STEP4, STEP5. This completes STEP6.

---

### STEP7: Abstract completion versus operator-domain completion ⭐ KEY STEP

**Claim:** Let \(\mathcal A_s\) be the Hilbert completion of
\[
 (\mathcal P,[\cdot,\cdot]^{\mathrm{alg}}_s).
\]
The map
\[
 J_sp=K_c^{-m}L^mp
\]
extends to a unitary
\[
 \overline J_s:\mathcal A_s\longrightarrow D(K_c^{s/2}).
\]
Nevertheless, under the identity realization of polynomials as functions, the two completions are not equal.

**Proof:**

<key-original-step>
We first record a self-contained polynomial approximation lemma.

**Polynomial approximation lemma.** Polynomials are dense in \(H^r(-1,1)\) for every nonnegative integer \(r\).

To prove the \(L^2\) case, interval step functions are dense in \(L^2(I)\). One direct justification is as follows. Indicators of finite unions of intervals generate a class closed under \(L^2\)-limits of monotone indicator sequences; this class is a \(\sigma\)-algebra containing all intervals, hence contains every Borel set. Quantizing a bounded measurable function into finitely many values and then truncating an arbitrary \(L^2\)-function proves density of interval step functions. Every interval step function can be approximated in \(L^2\) by a continuous piecewise-linear function by replacing each jump on an interval of arbitrarily small total length.

It remains to approximate a continuous function by polynomials. After mapping \(I\) to \([0,1]\), define its Bernstein polynomial
\[
 B_Ng(t)=\sum_{k=0}^N
 g(k/N)\binom Nk t^k(1-t)^{N-k}.
\]
If \(\omega_g\) is the modulus of continuity, then for every \(\delta>0\),
\[
 |B_Ng(t)-g(t)|
 \le \omega_g(\delta)
 +2\|g\|_\infty
   \sum_{|k/N-t|\ge\delta}
   \binom Nk t^k(1-t)^{N-k}.
\]
The final sum is at most
\[
 \frac{t(1-t)}{N\delta^2}\le\frac1{4N\delta^2},
\]
because the binomial weights have mean \(t\) and variance \(t(1-t)/N\). First choose \(\delta\) so that \(\omega_g(\delta)\) is small and then \(N\) large. This proves uniform, hence \(L^2\), polynomial approximation.

For \(f\in H^r(I)\), choose polynomials \(\rho_j\) with
\[
 \rho_j\longrightarrow f^{(r)}\quad\text{in }L^2(I).
\]
Define
\[
 p_j(x)=
 \sum_{k=0}^{r-1}\frac{f^{(k)}(-1)}{k!}(x+1)^k
 +\int_{-1}^x\frac{(x-t)^{r-1}}{(r-1)!}\rho_j(t)\,dt.
\]
This is a polynomial. Repeated use of the fundamental theorem of calculus gives the same representation for \(f\) with \(f^{(r)}\) in place of \(\rho_j\). For \(0\le k<r\), Cauchy–Schwarz on the triangular integration region yields
\[
 \|(p_j-f)^{(k)}\|_2
 \le C_r\|\rho_j-f^{(r)}\|_2,
\]
while equality holds for \(k=r\). Hence \(p_j\to f\) in \(H^r\), proving the lemma.

We now analyze \(J_s\). Since \(K_c\ge cI\), \(K_c^{-m}\) is bounded on \(L^2\). Also
\[
 K_c^mJ_sp=L^mp.
 \tag{7}
\]
If \(s=2m\), (7) shows that \(J_sp\in D(K_c^m)\) and
\[
 \|J_sp\|_{D(K_c^{s/2})}^2
 :=\|K_c^mJ_sp\|_2^2
 =\|L^mp\|_2^2
 =[p,p]^{\mathrm{alg}}_s.
 \tag{8}
\]

If \(s=2m+1\), then \(L^mp\) is a polynomial and hence belongs to \(H^1=D(K_c^{1/2})\). The domain identity in STEP1 and (7) give
\[
 J_sp\in D(K_c^{m+1/2}),
\]
and
\[
 \begin{aligned}
 \|J_sp\|_{D(K_c^{s/2})}^2
 &=\|K_c^{m+1/2}J_sp\|_2^2\\
 &=\|K_c^{1/2}L^mp\|_2^2\\
 &=\mathfrak a_c(L^mp,L^mp)
 =[p,p]^{\mathrm{alg}}_s.
 \end{aligned}
 \tag{9}
\]
Thus \(J_s\) is an isometry in both parity cases.

Its range is dense. For even \(s\), the map
\[
 K_c^m:D(K_c^m)\longrightarrow L^2(I)
\]
is an onto isometry in the indicated domain norm. Since
\[
 L^m\mathcal P=\mathcal P
\]
and polynomials are dense in \(L^2\), (7) gives density of \(J_s(\mathcal P)\).

For odd \(s\), the map
\[
 K_c^m:D(K_c^{m+1/2})\longrightarrow H^1(I)
\]
is onto: for \(g\in H^1\), \(K_c^{-m}g\) is a preimage. It is an isometry when \(H^1\) is given the form norm. Since \(L^m\mathcal P=\mathcal P\) and polynomials are dense in \(H^1\), the range is again dense.

Therefore \(J_s\) extends uniquely by Cauchy sequences to a unitary
\[
 \overline J_s:\mathcal A_s\to D(K_c^{s/2}).
\]

This unitary is not the identity on polynomials. The polynomial \(x^2\) is an element of the dense copy of \(\mathcal P\) inside \(\mathcal A_s\), but
\[
 b_+(x^2)=2,\qquad b_-(x^2)=-2.
\]
Thus \(x^2\notin D(K_c)\), and therefore
\[
 x^2\notin D(K_c^{s/2})\qquad(s\ge4).
\]
Consequently the identity realization of the abstract polynomial completion cannot equal the operator domain, even though the nonidentity map \(\overline J_s\) makes them unitarily equivalent. In particular,
\[
 J_sx^2\ne x^2.
\]
</key-original-step><heuristics>The algebraic differential expression \(L\) can be applied to every polynomial, while the genuine operator \(K_c\) can be applied only after its boundary conditions are met. The map \(J_s=K_c^{-m}L^m\) first takes the formal algebraic image and then applies the genuine boundary-compatible inverse. This is exactly the transport that reconciles the two Hilbert norms, but it is not the identity transport.</heuristics>

**Dependencies:** STEP1, STEP2, STEP6. This completes STEP7.

---

### STEP8: Density under the operator-domain reading

**Claim:** If
\[
 \mathcal C_s=\mathcal P\cap D(K_c^{s/2}),
\]
then \(\mathcal C_s\) is graph-norm dense in \(D(K_c^{s/2})\). Nevertheless, the full span of the \(Q_n^{(s)}\) is not a linear subspace of the operator domain, and the span of the individually admissible \(Q_n^{(s)}\) is not dense.

**Proof:**

Let \(s=2m+\varepsilon\). Define
\[
 T_s:H^s(I)\longrightarrow\mathbb C^{2m},
 \qquad
 T_sf=
 \bigl(b_+(f^{(2\ell)}),b_-(f^{(2\ell)})\bigr)_{\ell=0}^{m-1}.
\]
Endpoint evaluation is continuous on \(H^1(I)\): for \(v\in H^1\), choose \(y\in I\) with
\[
 |v(y)|\le 2^{-1/2}\|v\|_2
\]
and use
\[
 |v(\pm1)|\le |v(y)|+\sqrt2\|v'\|_2.
\]
Applying this to the relevant derivatives proves that \(T_s\) is continuous.

We construct a polynomial right inverse. Given
\[
 z=(z_{\ell,+},z_{\ell,-})_{\ell=0}^{m-1}\in\mathbb C^{2m},
\]
prescribe endpoint jets through order \(2m-1\) by
\[
 p^{(2\ell)}(1)=p^{(2\ell)}(-1)=0,
\]
\[
 p^{(2\ell+1)}(1)=z_{\ell,+},\qquad
 p^{(2\ell+1)}(-1)=z_{\ell,-}.
\]
There is a unique polynomial \(p\in\mathcal P_{4m-1}\) with these \(4m\) prescribed jets. Indeed, the endpoint-jet map from \(\mathcal P_{4m-1}\) to \(\mathbb C^{4m}\) is injective: a polynomial in its kernel is divisible by
\[
 (x-1)^{2m}(x+1)^{2m},
\]
which has degree \(4m\), and hence must vanish. Since source and target both have dimension \(4m\), the map is bijective.

Let \(R_sz=p\). Because all prescribed even endpoint values are zero,
\[
 b_+(p^{(2\ell)})=z_{\ell,+},\qquad
 b_-(p^{(2\ell)})=z_{\ell,-}.
\]
Thus
\[
 T_sR_s=I_{\mathbb C^{2m}}.
 \tag{10}
\]

Take \(f\in D(K_c^{s/2})\). By the polynomial approximation lemma from STEP7, choose \(p_j\in\mathcal P\) with
\[
 p_j\longrightarrow f\quad\text{in }H^s(I).
\]
Since \(T_sf=0\), define
\[
 q_j=p_j-R_sT_sp_j.
\]
Equation (10) gives \(T_sq_j=0\), so STEP1 yields
\[
 q_j\in\mathcal P\cap D(K_c^{s/2})=\mathcal C_s.
\]
Furthermore,
\[
 \begin{aligned}
 \|q_j-f\|_{H^s}
 &\le\|p_j-f\|_{H^s}
   +\|R_sT_s(p_j-f)\|_{H^s}\\
 &\le
 \bigl(1+\|R_s\|\,\|T_s\|\bigr)\|p_j-f\|_{H^s}
 \longrightarrow0.
 \end{aligned}
\]
The graph norm is equivalent to the \(H^s\)-norm on the domain by STEP1. Hence
\[
 \overline{\mathcal C_s}^{\,\|\cdot\|_{D(K_c^{s/2})}}
 =D(K_c^{s/2}).
 \tag{11}
\]

On the other hand, STEP2 gives
\[
 \operatorname{span}\{Q_n^{(s)}:n\ge0\}=\mathcal P.
\]
This is not contained in the operator domain because \(x^2\in\mathcal P\) but \(x^2\notin D(K_c^{s/2})\). Thus the literal full span is not a dense linear subspace of the operator domain: it is not even a subspace of that domain.

By STEP6, the individually admissible basis elements are only
\[
 Q_0^{(s)}=1,\qquad Q_1^{(s)}=x.
\]
Their span is not dense. To see this quantitatively, set
\[
 F_m(x)=(1-x^2)^{2m}.
\]
At each endpoint \(F_m\) has a zero of order \(2m\). Hence all its derivatives through order \(2m-1\) vanish there, so \(T_sF_m=0\) and
\[
 F_m\in\mathcal C_s.
\]
It is not affine.

Moreover,
\[
 \delta_{s,c}:=
 \inf_{a,b\in\mathbb C}
 \|K_c^{s/2}(F_m-a-bx)\|_2>0.
\]
If this infimum were zero, there would be affine functions \(a_j+b_jx\) converging to \(F_m\) in the graph norm. By STEP1 they would converge in \(H^s\), hence in \(L^2\). The \(L^2\)-norm on the two-dimensional affine space controls its coefficients, so a subsequence of \((a_j,b_j)\) would converge and its limit would represent \(F_m\) as an affine polynomial, a contradiction.

Finally,
\[
 \bigl(\operatorname{span}\{Q_n^{(s)}:n\ge0\}\bigr)
 \cap D(K_c^{s/2})
 =\mathcal P\cap D(K_c^{s/2})
 =\mathcal C_s,
\]
which is dense by (11). Thus compatible cancellations among non-admissible \(Q_n^{(s)}\) do produce a graph core, even though the individual admissible subsystem is only two-dimensional.

**Dependencies:** STEP1, STEP2, STEP6, STEP7. This completes STEP8.

---

### GOAL: Main Result

**Claim:** For every integer \(s\ge4\):

1. \(Q_n^{(s)}\in D(K_c^{s/2})\) if and only if \(n=0\) or \(n=1\). Equivalently, membership is characterized by the endpoint equations
   \[
   \bigl(Q_n^{(s)}\bigr)^{(2\ell+1)}(1)
   =\bigl(Q_n^{(s)}\bigr)^{(2\ell+1)}(-1)
   =\frac{
      \bigl(Q_n^{(s)}\bigr)^{(2\ell)}(1)
      -\bigl(Q_n^{(s)}\bigr)^{(2\ell)}(-1)}2
   \]
   for \(0\le\ell<\lfloor s/2\rfloor\).

2. The abstract polynomial completion and the operator domain are canonically unitarily equivalent through
   \[
   \overline J_s,\qquad J_sp=K_c^{-m}L^mp,
   \]
   but they are not equal under the identity realization of polynomials as functions.

3. Under the literal operator-domain reading, \(\operatorname{span}\{Q_n^{(s)}\}\) is not a dense linear subspace because it is not contained in the domain. The span of individually admissible \(Q_n^{(s)}\) is \(\operatorname{span}\{1,x\}\) and is not dense. However, its domain intersection
   \[
   \operatorname{span}\{Q_n^{(s)}\}\cap D(K_c^{s/2})
   =\mathcal P\cap D(K_c^{s/2})
   \]
   is graph-norm dense.

**Proof:**

Part 1 is STEP6, with the explicit trace criterion supplied by STEP3 and STEP1. Part 2 is STEP7. All three natural operator-domain interpretations of the density question are settled in STEP8.

**Dependencies:** STEP6, STEP7, STEP8.

## Key Ideas

The decisive observation is that high-order domain membership forces the one-step inverse polynomial
\[
 U_n^{(\varepsilon)}
 =\left(1-\frac{D^2}{c}\right)^{-1}R_n^{(\varepsilon)}
\]
to satisfy the original Krein boundary condition. Terminal orthogonality then turns that assumption into a zero-energy identity. Positivity forces an affine polynomial, excluding every degree \(n\ge2\).

The abstract and operator completions differ because the formal differential expression acts on every polynomial whereas the genuine operator includes boundary conditions. The nonidentity transport \(K_c^{-m}L^m\) gives their unitary equivalence. Boundary-compatible polynomial combinations nevertheless remain graph-norm dense after a finite-dimensional Hermite trace correction.

## Deviations from Decomposition Plan

None — followed the decomposition plan.