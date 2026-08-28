# Candidate proof package

Status before independent audit: `CANDIDATE_COMPLETE_PROOF`.

All inner products are linear in the first argument.  Put \(L=c-D^2\),
\(\Delta f=f(1)-f(-1)\), and
\[
B(f)=\big(f'(1)-\Delta f/2,\ f'(-1)-\Delta f/2\big).
\]
The symbol \(L_{\rm poly}^{-1}\) always means algebraic inversion on
\(\mathbb C[x]\), never the operator resolvent.

## Theorem

Let \(c>0\), \(s\ge4\) be an integer, and use the polynomial/abstract definition
\[
 Q_n^{(2r)}=L_{\rm poly}^{-r}P_n,\qquad
 Q_n^{(2r+1)}=L_{\rm poly}^{-r}R_n,
\]
where \(P_n\) is the degree-\(n\) \(L^2[-1,1]\)-orthogonal polynomial and
\(R_n\) is the degree-\(n\) polynomial orthogonal for the Krein form
\[
a_c(f,g)=\int f'\overline{g'}-\tfrac12\Delta f\,\overline{\Delta g}
          +c\int f\overline g.
\]
Then:

1. \(Q_n^{(s)}\in D(K_c^{s/2})\) if and only if \(n\in\{0,1\}\).
2. The completion of all polynomials in the abstract left-definite inner
   product is not equal, under the identity on polynomial representatives, to
   \(D(K_c^{s/2})\).  It is nevertheless naturally unitarily equivalent to that
   operator domain by a boundary-correcting map.
3. The literal polynomial span \(\operatorname{span}\{Q_n^{(s)}:n\ge0\}\) is
   not a linear subspace of \(D(K_c^{s/2})\), hence is not dense there under the
   operator-domain reading.  If one keeps only the individually admissible named
   members, their span is the two-dimensional affine space and is not dense.

If the displayed \(K_c^{-r}\) in the frozen task is instead read as the genuine
operator inverse, so that
\[
 \widetilde Q_n^{(2r)}=K_c^{-r}P_n,\qquad
 \widetilde Q_n^{(2r+1)}=K_c^{-r}R_n,
\]
then every \(\widetilde Q_n^{(s)}\) lies in the required domain and its span is
dense.  These tilded functions are generally not polynomials.

## Lemma 1 (the Krein form and its equality case) [O1]

For \(f\in H^1[-1,1]\),
\[
 |\Delta f|^2=\left|\int_{-1}^1 f'\right|^2
 \le 2\int_{-1}^1|f'|^2.
\]
Consequently \(a_0(f,f):=a_c(f,f)-c\|f\|_2^2\ge0\), with equality
exactly when \(f'\) is a.e. constant, i.e. exactly when \(f\) is affine.
For \(f\in H^2\), integration by parts gives
\[
a_0(f,g)=\langle-f'',g\rangle+
(f'(1)-\Delta f/2)\overline{g(1)}+
(-f'(-1)+\Delta f/2)\overline{g(-1)}.
\]
Since the endpoint trace map on \(H^1\) is onto \(\mathbb C^2\), the associated
operator has precisely \(B(f)=0\).  Thus \(K_0:=K_c-cI\ge0\) and
\[
\ker K_0=\ker a_0=\operatorname{span}\{1,x\}.
\]

The functional-analytic input here is the first representation theorem: a
dense closed nonnegative sesquilinear form \(a\) has a unique nonnegative
self-adjoint operator \(A\) satisfying
\(a(u,v)=\langle Au,v\rangle\) for \(u\in D(A),v\in D(a)\), and
\(D(a)=D(A^{1/2})\).  Its hypotheses hold for \(a_0\) on \(H^1[-1,1]\): the
form is dense and the norm \((a_0+\|\cdot\|_2^2)^{1/2}\) is equivalent to the
\(H^1\) norm after splitting off the affine equality space (the standard
one-dimensional Poincare inequality applies on its \(L^2\)-orthogonal
complement).  Hence \(D(K_c^{1/2})=H^1[-1,1]\) with form \(a_c\).

## Lemma 2 (exact power-domain criterion for polynomials) [O2]

Let \(m\ge1\).  Recursion for integer powers gives
\[
p\in D(K_c^m)\quad\Longleftrightarrow\quad
B(L^jp)=0\quad(0\le j<m)
\tag{2.1}
\]
for every polynomial \(p\).  Indeed, whenever the preceding conditions hold,
\(K_c^jp=L^jp\), and the next operator application is allowed exactly when the
next displayed boundary condition holds.

For the odd half-power, the spectral theorem for a self-adjoint \(A\ge cI>0\)
gives
\[
D(A^{m+1/2})=\{f\in D(A^m):A^mf\in D(A^{1/2})\}.
\tag{2.2}
\]
(This follows immediately by integrating \(\lambda^{2m+1}\) against the
spectral measure.)  Since \(L^mp\) is a polynomial and hence is in \(H^1\),
the last condition is automatic.  Therefore, for any integer \(s\),
\[
p\in D(K_c^{s/2})\quad\Longleftrightarrow\quad
B(L^jp)=0\quad(0\le j<\lfloor s/2\rfloor).
\tag{2.3}
\]

## Lemma 3 (even parity obstruction) [O3E]

Let \(n\ge2\) and suppose, for contradiction, that
\(v=L_{\rm poly}^{-1}P_n\) belongs to \(D(K_c)\).  Then \(P_n=K_cv\) and
\[
P_n-cv=-v''
\]
has degree at most \(n-2\).  Orthogonality of \(P_n\) gives
\[
0=\langle P_n,P_n-cv\rangle
=\|K_cv\|_2^2-c\langle K_cv,v\rangle.
\]
Because \(K_c=K_0+cI\), the right side is
\[
\langle (K_0+cI)v,K_0v\rangle
=\|K_0v\|_2^2+c\,a_0(v,v).
\]
Both terms are nonnegative, so \(K_0v=0\).  Lemma 1 makes \(v\) affine,
contradicting \(\deg v=\deg P_n=n\).  Hence
\[
L_{\rm poly}^{-1}P_n\in D(K_c)\quad\Longleftrightarrow\quad n\le1.
\tag{3.1}
\]
The reverse implication holds because all affine functions satisfy the Krein
condition.

## Lemma 4 (odd parity obstruction) [O3O]

Let \(n\ge2\) and suppose, for contradiction, that
\(v=L_{\rm poly}^{-1}R_n\in D(K_c)\).  Then \(R_n=K_cv\), while
\(R_n-cv=-v''\) has degree at most \(n-2\).  Form orthogonality of \(R_n\)
therefore gives
\[
0=a_c(R_n,R_n-cv)=a_c(R_n,R_n)-c\,a_c(R_n,v).
\]
Since \(v\in D(K_c)\), the representation identity and symmetry yield
\[
a_c(R_n,v)=\langle R_n,K_cv\rangle=\|R_n\|_2^2.
\]
It follows that \(a_0(R_n,R_n)=0\).  Lemma 1 says that \(R_n\) is affine,
contradicting \(\deg R_n=n\).  Thus
\[
L_{\rm poly}^{-1}R_n\in D(K_c)\quad\Longleftrightarrow\quad n\le1.
\tag{4.1}
\]

## Proof of conclusion 1 [O4]

Write \(s=2r\) or \(s=2r+1\); since \(s\ge4\), \(r\ge2\).  If the even
\(Q_n^{(2r)}\) lay in \(D(K_c^r)\), Lemma 2 would imply
\[
L^{r-1}Q_n^{(2r)}=L_{\rm poly}^{-1}P_n\in D(K_c),
\]
so Lemma 3 forces \(n\le1\).  The same argument with Lemma 4 handles odd
\(s=2r+1\).  Conversely, \(P_0,P_1,R_0,R_1\) and all their algebraic inverse
images are affine; on affine functions \(L=K_c=cI\).  They therefore belong
to every positive power domain.  This proves the iff uniformly in \(c,s,n\).

## Proof of conclusion 2 [O5]

For even \(s=2r\), \(p\mapsto L^rp\) is an isometry from the abstract
polynomial pre-Hilbert space onto the polynomial subspace of \(L^2\), and it
extends to a unitary
\[
U_{\rm abs}:\mathcal H_{2r}^{\rm abs}\longrightarrow L^2[-1,1].
\]
For odd \(s=2r+1\), the same map extends to a unitary onto the form space
\(H^1[-1,1]\), because polynomials are dense in \(H^1\).  (To verify the last
fact directly, approximate \(f'\) in \(L^2\) by polynomials and integrate the
approximants, choosing one matching constant.)

On the operator side, spectral calculus makes
\[
U_{\rm op}=K_c^r:D(K_c^{r})\to L^2
\]
unitary in the even case and
\[
U_{\rm op}=K_c^r:D(K_c^{r+1/2})\to D(K_c^{1/2})=H^1
\]
unitary in the odd case, with the corresponding left-definite norms.  Thus
\[
W=U_{\rm op}^{-1}U_{\rm abs}
\tag{5.1}
\]
is a natural unitary from the abstract completion to the operator domain.
It is a boundary-correcting map, not the identity on polynomial functions.

Canonical equality is impossible: the abstract pre-Hilbert space contains the
polynomial \(x^2\), whereas \(x^2\notin D(K_c)\), since \(\Delta x^2=0\) but
its two endpoint derivatives are \(2\) and \(-2\).  Since \(s\ge4\),
\(D(K_c^{s/2})\subset D(K_c)\).  Hence the identity on polynomial
representatives cannot identify the two completions.

For an exact illustration, the polynomial solution of \(Lu=x^2\) is
\[
u_{\rm poly}=x^2/c+2/c^2,
\]
but the genuine resolvent gives, with \(k=\sqrt c\),
\[
K_c^{-1}x^2=u_{\rm poly}-\frac{2\cosh(kx)}{c\,k\sinh k},
\]
whose homogeneous correction enforces the boundary condition.

## Proof of conclusion 3 and the genuine-operator alternative [O6]

The operator-domain claim follows at once from conclusion 1: the literal span
contains \(Q_n^{(s)}\notin D(K_c^{s/2})\) for every \(n\ge2\), so it is not a
subspace of that Hilbert space and cannot be dense there as a linear subspace.
The span of the individually admissible named members is only
\(\operatorname{span}\{1,x\}\).  It is not dense because the operator domain
contains the infinitely many linearly independent elements \(K_c^{-r}P_n\)
in the even case (and \(K_c^{-r}R_n\) in the odd case).

Under the genuine-operator reading, bounded negative powers and (2.2) give
\[
K_c^{-r}P_n\in D(K_c^r),\qquad
K_c^{-r}R_n\in D(K_c^{r+1/2})
\]
for every \(n\).  Since \(\{P_n\}\) is complete in \(L^2\), \(\{R_n\}\) is
complete in the form space (its span is all polynomials, which are dense), and
the displayed inverse-power maps are unitary, the two tilded spans are dense
in the corresponding operator domains.  The explicit degree-2 resolvent above
shows why calling the tilded system polynomial is generally false.

## Bonus: polynomial degree spectrum

The matrix of \(L=c-D^2\) on \(\mathbb C[x]\), ordered by degree, is triangular
with diagonal \(c\ne0\).  Hence \(L_{\rm poly}^{-r}\) preserves the degree of
every nonzero polynomial.  Therefore \(\deg Q_n^{(s)}=n\) for every \(n\ge0\)
under the polynomial reading.  This observation is not used as a completion gate.
