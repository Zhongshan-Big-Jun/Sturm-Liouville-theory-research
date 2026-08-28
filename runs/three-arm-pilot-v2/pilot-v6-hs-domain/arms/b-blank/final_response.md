The key point is that two different inverses are being denoted by \(K_c^{-1}\):

- the algebraic inverse of \(c-D^2\) on polynomials, which preserves polynomials;
- the spectral inverse of the self-adjoint operator, which enforces the boundary condition and generally does not preserve polynomials.

For the stated polynomial system, the answers are:

\[
\boxed{Q_n^{(s)}\in D(K_c^{s/2})\iff n=0\text{ or }1.}
\]

Consequently, the abstract polynomial completion is not the concrete operator domain under the identity map, and the polynomial system is not an operator-domain basis.

## 1. The operator power domains

Put
\[
T=c-\frac{d^2}{dx^2},\qquad
\delta f=\frac{f(1)-f(-1)}2,
\]
and let
\[
Bf=\bigl(f'(1)-\delta f,\;f'(-1)-\delta f\bigr).
\]

The quadratic form of \(K_c\) is
\[
\mathfrak a(f,g)
 =\int_{-1}^1 f'\overline{g'}\,dx
 +c\int_{-1}^1 f\overline g\,dx
 -\frac{(f(1)-f(-1))
 \overline{(g(1)-g(-1))}}2,
\]
with domain \(H^1(-1,1)\). In particular,
\[
\mathfrak a(f,f)
 =c\|f\|_2^2+
 \int_{-1}^1\left|f'-\delta f\right|^2dx
 \ge c\|f\|_2^2.                                      \tag{1}
\]

The closed-form representation theorem says that a densely defined, closed, symmetric, lower-bounded form determines a unique self-adjoint operator \(A\), with \(D(A^{1/2})\) equal to the form domain. Integration by parts shows that here this operator is \(A=K_c\) with \(Bf=0\).

Write
\[
s=2r+\varepsilon,\qquad \varepsilon\in\{0,1\}.
\]
Spectral calculus for a positive self-adjoint operator, together with one-dimensional regularity, gives
\[
D(A^{s/2})
=
\left\{
f\in H^s(-1,1):
B(T^jf)=0,\quad 0\le j<r
\right\}.                                             \tag{2}
\]

Thus, for any polynomial \(p\),
\[
p\in D(A^{s/2})
\iff B(T^jp)=0\quad(0\le j<r).                        \tag{3}
\]

If \(p=p_e+p_o\) is its even/odd decomposition, (3) is equivalently
\[
p_e^{(2j+1)}(1)=0,\qquad
p_o^{(2j+1)}(1)=p_o^{(2j)}(1),
\quad 0\le j<r.                                      \tag{4}
\]

This follows triangularly from
\[
T^j=\sum_{k=0}^j\binom jk c^{j-k}(-D^2)^k.
\]

## 2. Membership of the SL polynomials

Let \(R=(T|_{\mathbb C[x]})^{-1}\), the algebraic polynomial inverse. Since \(c>0\),
\[
Rp=\sum_{k\ge0}c^{-k-1}p^{(2k)},                     \tag{5}
\]
where the sum terminates.

Up to nonzero normalizing constants, the polynomial construction is
\[
Q_n^{(2r)}=R^rP_n,\qquad
Q_n^{(2r+1)}=R^rS_n,                                 \tag{6}
\]
where \(P_n\) is the Legendre polynomial and \(S_n=Q_n^{(1)}\) is the degree-\(n\) polynomial orthogonal in the form \(\mathfrak a\).

### Even \(s=2r\)

If \(Q_n^{(2r)}\) belonged to \(D(A^r)\), then (2), applied at \(j=r-1\), would require
\[
RP_n\in D(A).                                        \tag{7}
\]

For even \(n\ge2\), \(RP_n\) is even, so (7) requires \((RP_n)'(1)=0\). But
\[
(RP_n)'(1)
 =\sum_{2k+1\le n}c^{-k-1}P_n^{(2k+1)}(1)>0.
\]
Here the classical endpoint formula
\[
P_n^{(m)}(1)
 =\frac{(n+m)!}{2^m m!(n-m)!},\qquad 0\le m\le n,
\]
shows every term is positive.

For odd \(n\ge3\), the boundary condition is
\[
(RP_n)'(1)=(RP_n)(1).
\]
Its left-minus-right side is
\[
\sum_k c^{-k-1}
 \left(P_n^{(2k+1)}(1)-P_n^{(2k)}(1)\right)>0.        \tag{8}
\]
Indeed,
\[
\frac{P_n^{(m+1)}(1)}{P_n^{(m)}(1)}
 =\frac{(n+m+1)(n-m)}{2(m+1)};
\]
for odd \(n\) and even \(m<n\), this is at least \(1\), and it is strictly greater than \(1\) for \(m=0\) when \(n\ge3\).

Therefore no \(n\ge2\) works.

### Odd \(s=2r+1\)

Suppose \(n\ge2\) and \(Q_n^{(2r+1)}\in D(A^{r+1/2})\). Then
\[
u:=T^{r-1}Q_n^{(2r+1)}=RS_n
\]
must lie in \(D(A)\), and
\[
Au=Tu=S_n.                                           \tag{9}
\]

Because \(S_n\) is \(\mathfrak a\)-orthogonal to every polynomial of degree below \(n\), and
\[
u-\frac1cS_n=\frac1c\,u''
\]
has degree at most \(n-2\), we have
\[
\mathfrak a(S_n,u)=\frac1c\mathfrak a(S_n,S_n).       \tag{10}
\]

On the other hand, (9) and the form identity give
\[
\mathfrak a(S_n,u)=\mathfrak a(u,S_n)
 =(Au,S_n)_{L^2}=\|S_n\|_2^2.                        \tag{11}
\]
Equations (10)–(11) imply
\[
\mathfrak a(S_n,S_n)=c\|S_n\|_2^2.
\]
By (1),
\[
\int_{-1}^1|S_n'-\delta S_n|^2dx=0,
\]
so \(S_n'\) is constant. Hence \(S_n\) has degree at most \(1\), contradicting \(n\ge2\).

Finally, \(S_0\) and \(S_1\) are scalar multiples of \(1\) and \(x\). Every affine function satisfies the Krein boundary condition, and \(T\) preserves affine functions. Therefore
\[
\boxed{Q_n^{(s)}\in D(A^{s/2})\iff n\in\{0,1\}.}      \tag{12}
\]

## 3. Abstract completion versus operator domain

On polynomials, the abstract norms are
\[
\|p\|_{\mathrm{abs},2r}=\|T^rp\|_{L^2},
\qquad
\|p\|_{\mathrm{abs},2r+1}
 =\mathfrak a(T^rp,T^rp)^{1/2}.                      \tag{13}
\]

Consequently, \(T^r\) extends from the abstract completion unitarily onto

- \(L^2(-1,1)\) when \(s=2r\);
- \(H^1(-1,1)\), with norm \(\mathfrak a^{1/2}\), when \(s=2r+1\).

Meanwhile, spectral calculus gives unitary maps
\[
A^r:D(A^r)\longrightarrow L^2,
\]
and
\[
A^r:D(A^{r+1/2})\longrightarrow D(A^{1/2})=H^1.
\]

Thus the two completions are canonically unitarily equivalent through
\[
J_s=A^{-r}T^r.                                       \tag{14}
\]
They are not equal under the identity realization as functions. For example, \(Q_2^{(s)}\) is an element of the abstract polynomial completion but, by (12), is not in \(D(A^{s/2})\).

So:
\[
\boxed{\text{abstract completion}\ne D(A^{s/2})
\text{ concretely, although they are unitarily equivalent.}}
\]

## 4. Density

Since \(Q_n^{(s)}\) has exact degree \(n\),
\[
\operatorname{span}\{Q_n^{(s)}:n\ge0\}=\mathbb C[x].
\]
But this span is not contained in \(D(A^{s/2})\): already \(Q_2^{(s)}\notin D(A^{s/2})\). Therefore it cannot literally be a dense operator-domain subspace.

If one retains only those system elements that individually belong to the domain, one obtains
\[
\operatorname{span}\{Q_0^{(s)},Q_1^{(s)}\}
 =\operatorname{span}\{1,x\},
\]
which is not dense in the infinite-dimensional space \(D(A^{s/2})\).

There is a useful distinction: constrained polynomial combinations are dense:
\[
\overline{\mathbb C[x]\cap D(A^{s/2})}^{\,\|\cdot\|_{D(A^{s/2})}}
 =D(A^{s/2}).                                        \tag{15}
\]
Indeed, (2) expresses the domain as the kernel of finitely many continuous trace functionals on \(H^s\); polynomials are dense in \(H^s\), and approximants can be corrected by finitely many fixed polynomials to satisfy those traces. The graph norm is equivalent to the \(H^s\)-norm on this kernel by the one-dimensional elliptic estimate
\[
\|f\|_{H^{2r+\varepsilon}}
 \le C\bigl(\|T^rf\|_{H^\varepsilon}+\|f\|_2\bigr),
\]
together with \(A\ge cI\).

Thus the answer to part 3 is:

\[
\boxed{\text{No, not as an operator-domain orthogonal system.}}
\]

If “dense” is instead defined as the closure of
\(\operatorname{span}\{Q_n^{(s)}\}\cap D(A^{s/2})\), that intersection is dense by (15), but this is a different assertion involving boundary-condition cancellations.

Finally, if \(K_c^{-r}\) in the definition is interpreted as the actual spectral inverse \(A^{-r}\), then
\[
\widetilde Q_n^{(2r)}=A^{-r}P_n,\qquad
\widetilde Q_n^{(2r+1)}=A^{-r}S_n
\]
all belong to the appropriate operator domain and form a complete orthogonal system there. For \(n\ge2\), however, these functions are not polynomials. This is precisely the distinction behind the three conclusions above.

As a degree-spectrum bonus, if \(r=\lfloor s/2\rfloor\), the exact degrees of nonzero polynomials in \(D(A^{s/2})\) are
\[
\boxed{\{0,1\}\cup\{N:N\ge 2r+2\}.}
\]