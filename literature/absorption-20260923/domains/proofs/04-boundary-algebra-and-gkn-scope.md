# What a finite boundary matrix can certify here

Status: AUTHOR_DERIVATION_AND_EXACT_CHECKS_PENDING_INDEPENDENT_REVIEW. L04 supplies a general independence/GKN methodology (arXiv:1706.01539v1, Proposition 2.14 and Theorem 3.2, pp.9,12-14). The following is our regular constant-coefficient computation; it does not import its singular Legendre examples.

For the regular expression L=c-D^2 on I, the maximal domain is H^2(I), and the minimal domain is H^2_0(I), meaning zero value and first derivative at both endpoints. This follows by integration by parts against arbitrary endpoint jets, which are realized by cubic Hermite polynomials. The boundary-jet quotient has dimension four; each defect equation -u''+cu=+/-iu has two independent solutions on the finite interval. Hence deficiency indices are (2,2).

The Krein domain corresponds to f'(1)=f'(-1)=Delta f/2. Its free boundary coordinates are f(-1),f(1), so its boundary subspace has dimension two. For f,g with these traces,
\[
[-f'\overline g+f\overline{g'}]_{-1}^1
=-\tfrac12\Delta f\,\overline{\Delta g}+
\tfrac12\Delta f\,\overline{\Delta g}=0.
\]
It is therefore Lagrangian in the four-dimensional nondegenerate boundary quotient. A rank count alone would not show this isotropy.

For L^2=D^4-2cD^2+c^2 the maximal/minimal boundary jets have eight coordinates (derivatives 0 through 3 at both endpoints); regularity and the order-four defect equation give deficiency indices (4,4). The actual square of the Krein operator has
\[
D(K_c^2)=\{f\in H^4(I):\mathcal Bf=\mathcal B(f'')=0\}.
\]
This follows from f,K_cf in D(K_c), since f''=cf-K_cf and B(K_cf)=cBf-B(f''). Conversely these four conditions imply the product-domain definition. This establishes the selected extension, rather than identifying it merely by its number of conditions.

The four-trace map T=(Bf,B(f'')) has the polynomial right inverse obtained from
\[
T(x^2,x^3,x^4,x^5)=
\begin{pmatrix}2&2&4&4\\-2&2&-4&4\\0&0&24&40\\0&0&-24&40\end{pmatrix},\qquad\det=15360.
\]
Thus Rz=(x^2,x^3,x^4,x^5)B_4^{-1}z is a bounded right inverse into H^4. If ordinary H^4 polynomial approximation is supplied, subtracting R times the trace residual proves a polynomial graph core. This is the current project's existing four-trace argument, independently recalculated, not a new density theorem.

The skew boundary form for L^2 is the endpoint difference of
\[
f'''\overline g-f''\overline{g'}+f'\overline{g''}-f\overline{g'''}
-2c(f'\overline g-f\overline{g'}).
\]
Substitution of f'=Delta f/2 and f'''=Delta f''/2, and the analogous g relations, makes its endpoint difference zero. Together with independence of the four conditions this checks isotropy and the correct dimension. The exact symbolic calculation in `scripts/exact_checks.py` covers complex data by treating the conjugated g jets as independent variables.

For a high divisible tail, the two-column matrix on x^L,x^{L+1}, L positive even, is [[L,L],[-L,L]], determinant 2L^2. Its right inverse corrects endpoint residuals without changing x^L divisibility. This finite algebra becomes a closure proof only after the local cutoff and Sobolev approximation estimates in proof 03.

Do not call these rectangular trace matrices the sesquilinear pairing matrix of L04. Do not replace its tested eigenfunctions by arbitrary sparse polynomials. The project eigenfunctions are affine, cosine and sine modes. The affine members p_0=1 and p_1=x are c-eigenfunctions; the nonaffine named members p_n, n>=4, are not eigenfunctions. In fact their pairings among themselves vanish when all are in the same self-adjoint domain, so an all-domain skew pairing matrix cannot have full rank. Complementary boundary directions or another justified quotient basis are needed for that GKN test.

Version limitation: the captured L04 v1 p.15 explicitly uses deficiency (1,1) for its full-interval minimal Legendre operator, whereas the both-limit-circle model has (2,2), as also stated in L06 p.6. The original v1 page was visually checked. The publisher page identifies a 2019 article, but direct publisher access returned HTTP403; equality or correction of that version's examples has not been established. We use only the general independence argument with the correct project dimensions derived above, and make no claim that v1's Legendre examples certify this project.
