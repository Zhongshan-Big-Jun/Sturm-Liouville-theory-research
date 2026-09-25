# A fractional-domain dictionary for the current constant-coefficient Krein model

Status: AUTHOR_PROVED_FROM_IDENTIFIED_SOURCE_PENDING_INDEPENDENT_REVIEW. Fixed c>0, I=(-1,1), complex H_c^s=D(K_c^{s/2}), s>=0. This is a derived adaptation, not a theorem quoted about Krein boundary conditions. The only substantive external domain theorem used here is Grubb, Definition 2.1/Theorem 2.2/Corollary 2.3, journal p.833 (author-posted PDF p.4), also arXiv:1412.3744v4 PDF pp.3-4: Definition 2.1/Theorem 2.2 are on p.3, and Corollary 2.3/equation (2.7) on p.4. The source pages were visually inspected. Elementary spectral calculus and ordinary one-dimensional Sobolev facts are used explicitly below.

## D1. A bridge that satisfies the cited hypotheses

A direct invocation of a uniform-order boundary theorem on the half-interval Dirichlet-Robin problem would require a mixed-boundary extension. Instead use two auxiliary operators on the smooth full interval I:

\[
\begin{aligned}
N_c&=-D^2+c,&D(N_c)&=\{u\in H^2(I):u'(\pm1)=0\},\\
R_{c+4}&=-D^2+c+4,&D(R_{c+4})&=\{u\in H^2(I):u'(1)=u(1),\ u'(-1)=-u(-1)\}.
\end{aligned}
\]

Both are ordinary separated self-adjoint realizations. Integration by parts gives the second form \(\|u'\|^2-|u(1)|^2-|u(-1)|^2+(c+4)\|u\|^2\). From integrating (x|u|^2)' one obtains

\[
|u(1)|^2+|u(-1)|^2
\le\|u\|^2+2\|u\|\|u'\|
\le\tfrac12\|u'\|^2+3\|u\|^2.
\]

Consequently R_{c+4}>=(c+1)I and N_c>=cI. They are bijective. Their coefficients are smooth; the differential principal part is -D^2. Boundary operators are gamma D and gamma(xD-1), respectively. At both endpoints the derivative coefficient is nonzero; up to a sign these have outward normal principal part, and the scalar Robin term has lower order. Thus these are normal, strongly elliptic Neumann-type boundary problems of order j=1 in Grubb's stated class. There is no junction of distinct boundary orders.

Reflection preserves both domains. The calculation in proof 01 identifies
\[
K_c|_E=N_c|_E,\qquad K_c|_O=(R_{c+4}|_O)-4I.
\]

Since K_c|_O>=cI, the weights lambda^s and (lambda+4)^s are comparable for every fixed s>=0, with constants depending on c,s. Their power domains coincide. For a reducing parity subspace, spectral projections restrict and hence \(D(T^{s/2}|_{E/O})=D(T^{s/2})\cap E/O\). It follows in both directions that

\[
\boxed{f\in H_c^s\iff f_e\in D(N_c^{s/2}),\quad f_o\in D(R_{c+4}^{s/2}),}
\]

where f_e=P_ef and f_o=P_of. This supplies the missing applicability bridge. It is a comparison of domains with equivalent norms, not equality of the Robin and Krein power norms.

## D2. The exact dictionary

Let d(x)=1-|x| and B be the two-component Krein trace from proof 01. Ordinary derivatives below are weak derivatives. If
\(s\notin\{3/2+2k:k\in\mathbb N_0\}\), then

\[
\boxed{H_c^s=\{f\in H^s_{\rm Sob}(I):\mathcal B(f^{(2j)})=0
\text{ for every integer }j\ge0\text{ with }2j+3/2<s\}.}\tag{D-NC}
\]

The power norm and the H^s_Sob norm are equivalent on this subspace. In particular, the condition list is empty for 0<=s<3/2.

At s=3/2+2k the correct statement is

\[
\boxed{\begin{split}
H_c^{2k+3/2}=\{f\in H^{2k+3/2}_{\rm Sob}(I):&\ \mathcal B(f^{(2j)})=0\ (0\le j<k),\\
&\int_{-1}^1\frac{|f_e^{(2k+1)}(x)|^2+
|x f_o^{(2k+1)}(x)-f_o^{(2k)}(x)|^2}{1-|x|}\,dx<\infty\}.
\end{split}}\tag{D-C}
\]

An equivalent norm is H^s_Sob norm squared plus this integral, followed by the square root. No ordinary value of the highest derivative at an endpoint is asserted at critical order.

For clarity near the existing research window:

| s | Additional condition beyond f in H^s_Sob(I) |
|---|---|
| 0<=s<3/2 | None |
| s=3/2 | Integral in (D-C), k=0 |
| 3/2<s<7/2 | Bf=0 |
| s=7/2 | Bf=0 and integral in (D-C), k=1 |
| 7/2<s<11/2 | Bf=B(f'')=0 |

The table includes s=5/2 in an ordinary open interval: it is an interior second-derivative trace threshold, not a new full-interval operator boundary threshold.

## D3. Proof of both inclusions and the critical simplification

The case s=0 is immediate from H_c^0=L^2. For s>0, apply Grubb with p=2, a=s/2, j=1 separately to N_c and R_{c+4}, whose hypotheses were checked in D1. Off critical orders the resulting conditions are
\(D(c-D^2)^j f_e|_{\partial I}=0\) and
\((xD-1)(c+4-D^2)^j f_o|_{\partial I}=0\), whenever 2j+3/2<s.
Each differential expression is triangular in its successive even derivatives. Its leading term has coefficient (-1)^j. Induction therefore converts the conditions to
\(f_e^{(2j+1)}(\pm1)=0\) and
\(x f_o^{(2j+1)}-f_o^{(2j)}=0\) at the endpoints. For an even derivative v=f^{(2j)}, parity says precisely that these two endpoint families are equivalent to Bv=0. Applying the same triangular argument backwards proves the reverse implication, not merely necessity.

At critical order Grubb gives the previous boundary conditions and the zero-extension H^{1/2} condition on the highest boundary expression. In the L^2 case this is equivalently d^{-1/2} times that expression in L^2. Here is also the reason for the weight: for w in H^{1/2}(I), the cross term in the Slobodeckij seminorm of its zero extension is, up to a positive constant,
\(\int_I |w(x)|^2((1-x)^{-1}+(1+x)^{-1})dx\), comparable to \(\int_I|w|^2/d\). Thus the weighted condition encodes an actual H^{1/2} extension, not a pointwise trace shorthand.

The highest expressions are
\[
D(c-D^2)^k f_e,\qquad (xD-1)(c+4-D^2)^k f_o.
\]

Subtract their leading terms \((-1)^k f_e^{(2k+1)}\) and \((-1)^k(xf_o^{(2k+1)}-f_o^{(2k)})\). Each remainder is a finite sum of lower expressions with zero endpoint trace. Each such expression lies in H^1(I) (indeed in H^{5/2} or better). If w in H^1(I) vanishes at both endpoints, integration from the nearer endpoint and Cauchy-Schwarz give
\(\int_I |w|^2/d\le C\|w'\|_2^2\).
The remainders therefore already have the required weighted integrability, bounded by the H^s norm. Adding or subtracting them preserves the critical condition in both directions. This proves (D-C), including its equivalent norm. Combining with the reducing-subspace and shift identities in D1 completes both inclusions for the full Krein space.

Equivalence of norms follows from the domain theorem/homeomorphism in Grubb, the bounded parity projections on H^s, scalar-shift comparability, and the bounded remainder estimates just given. The zero-extension argument also gives a complete norm at the critical step, so there is no replacement of a stronger graph norm by an unqualified Sobolev norm.

## D4. Point traces at the centre

For integer r>=0, evaluation f -> f^{(r)}(0) is continuous on H_c^s when s>r+1/2. This follows by a local Sobolev extension and Fourier Cauchy-Schwarz, since \(\int_{\mathbb R}|\xi|^{2r}(1+|\xi|^2)^{-s}d\xi<\infty\), together with the continuous H_c^s -> H^s_Sob embedding.

The strict inequality matters. To see failure at s=r+1/2, choose smooth chi supported in (-1/2,1/2) and identically one near zero. Put
\[
v_N(x)=\frac{\chi(x)}{\sqrt{\log(N+1)}}
\sum_{n=1}^N\frac{e^{i\pi nx}}{(i\pi n)^r n}.
\]
Its periodic H^{r+1/2} norm before cutoff is bounded, because the norm squared is O((log(N+1))^{-1} sum_{n<=N}1/n). Smooth cutoff is bounded in that Sobolev space. All endpoint conditions and critical weights are harmless on this fixed compact support, by (D-NC)/(D-C), so its H_c^{r+1/2} norm is bounded. However
\(v_N^{(r)}(0)=(\log(N+1))^{-1/2}\sum_{n<=N}1/n\to\infty\).
Lower power norms are bounded by spectral embedding as well. Thus there is no continuous extension of this point trace to all of H_c^s when 0<=s<=r+1/2. The construction uses smooth functions satisfying all power-domain boundary conditions.

In particular f''(0) is continuous at s=3; it is not a legitimate continuous trace at s=5/2. The s=3 deletion proof must not be transferred to that critical order by assertion. Half-interval Dirichlet gluing also has centre thresholds; D1 avoids dropping those conditions by working with full-interval parity functions from the start.

## D5. Tests and limits

For x^2, the k=0 even residual is 2x, whose weighted integral diverges: its exact nonnegative threshold is s<3/2. For p4, Bp4=0, but the k=1 even residual is 24x, so the threshold is s<7/2. For q6=x^6-5x^4+7x^2 that residual is 120x(x^2-1), so the critical integral is finite and B(q6'')=0; q6 belongs to H_c^4. Affine functions give zero critical residuals at every k and satisfy all lower conditions. These agree with current project spectral checks.

The theorem concerns this smooth constant-coefficient model with c>0. No nonsmooth coefficients, different self-adjoint extension, c=0 norm, uniform-in-c constants, nonlocal integral fractional Laplacian, or arbitrary constrained closure is covered. It leaves the established full-family density range 0<=s<7/2 intact; a domain dictionary does not independently reprove density or classify infinite deletions.
