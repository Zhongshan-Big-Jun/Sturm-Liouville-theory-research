# Fixed-c Krein approximation by integrated Legendre polynomials

Status: AUTHOR_PROOF, pending independent review. This is a bounded P2 adaptation of Shen's boundary-adapted idea, with the actual coupled Krein conditions imposed and proved here. For both s=2 and s=4 the construction yields a complete Riesz basis in the genuine left-definite norm, with explicit constants independent of degree. This statement concerns the replacement systems below, not the original sparse monomials.

Throughout c>0 is fixed, L_n=P_n is the Legendre polynomial with P_n(1)=1, e_n=sqrt((2n+1)/2)P_n is L2(-1,1)-normalized, and

$$
J^r v(x)=\frac1{(r-1)!}\int_{-1}^x(x-t)^{r-1}v(t)\,dt,
\quad
C_r=\frac{2^r}{(r-1)!\sqrt{(2r-1)(2r)}}.\tag{L0}
$$

The squared integral of this kernel over -1<t<x<1 equals C_r^2, so ||J^r||_(L2->L2)<=C_r. In particular C_2=2/sqrt(3), C_4=4/(3sqrt(14)). This is a conservative Hilbert-Schmidt bound, not an assertion of the exact operator norm.

## L1. The common integration lemma

Let r be 2 or 4 and n>=r. Set b_n^(r)=J^r e_n. Then

1. (b_n^(r))^(r)=e_n, and every derivative of order 0,...,r-1 vanishes at both endpoints.
2. b_n^(r) is a combination of P_(n-r),P_(n-r+2),...,P_(n+r), with nonzero highest coefficient; its degree is n+r.
3. {b_n^(r):n>=r} is complete and orthonormal in the norm ||g^(r)||_2 on H_0^r={g in ordinary H^r:g^(j)(+/-1)=0,0<=j<r}.

Proof. All left traces vanish by integration from -1. For j<r, the right trace is a constant times integral (1-t)^(r-1-j)e_n(t) dt, which is zero by Legendre orthogonality. The antiderivative identity

$$
JP_k=\frac{P_{k+1}-P_{k-1}}{2k+1}\quad(k\ge1)\tag{L1a}
$$

has zero value at -1. Repeating it r times uses no P_0 antiderivative, because before the final step the lowest index is at least one. This proves the finite-band support and degree. If g in H_0^r, integration by parts r times shows g^(r) perpendicular to all polynomials of degree <r; all boundary terms vanish and the polynomial's rth derivative is zero. Expanding g^(r)=sum_(n>=r) z_n e_n in L2 and applying the bounded integrations J^(r-j) gives convergence to g in ordinary H^r. Conversely the sums lie in H_0^r. Parseval proves the asserted norm identity. The standard completeness of Legendre polynomials follows from polynomial density in L2.

For r=2 the concrete formula is

$$
b_n^{(2)}=\sqrt{\frac{2n+1}{2}}\left[
\frac{P_{n+2}}{(2n+1)(2n+3)}
-\frac{2P_n}{(2n-1)(2n+3)}
+\frac{P_{n-2}}{(2n+1)(2n-1)}\right].\tag{L1b}
$$

With k=n-2, this is exactly Shen's clamped basis in Lemma 3.1, (3.4), in the author PDF pp.7-8 (printed pp.1495-1496). The s=4 functions are the five-term recurrence-defined J^4 e_n; (L1a) is an unambiguous exact coefficient construction, including n=4.

## L2. s=2: two affine lifts, three-term high modes

Use the ordered family

$$
\Phi^{(2)}=(e_0,e_1,b_2^{(2)},b_3^{(2)},\ldots).
$$

Every column satisfies Bf=0. The affine columns do so directly; high columns have f=f'=0 at both endpoints. For any f in D(K_c), let ell_f be its affine endpoint interpolant. The boundary condition forces ell_f'=Delta f/2=f'(+/-1). Thus g=f-ell_f lies in H_0^2 and

$$
f=a_0e_0+a_1e_1+\sum_{n\ge2}z_n b_n^{(2)},\qquad
z_n=\langle f'',e_n\rangle_2.\tag{L2a}
$$

Here f'' is perpendicular to 1,x: integrate by parts using the coupled condition, or use g''=f'' and L1. The decomposition is unique. For degree N>=4 the finite columns with n<=N-2 span exactly

$$
\Pi_N\cap D(K_c),\qquad \dim=N-1.\tag{L2b}
$$

Indeed subtract ell_f and expand the polynomial g'' in e_2,...,e_(N-2); integration recovers g. No approximation or unproved rank assumption enters this span identity.

Here are degree-independent Riesz bounds. Put d=1/2+1/sqrt(2),

$$
L_c=\frac{1+2\sqrt3}{c}+4d,\quad
A_{2,c}=(L_c^2+4)^{-1},\quad
B_{2,c}=c^2+(1+cC_2)^2.
$$

Then for all finite coefficient vectors w=(a_0,a_1,z_2,...),

$$
\boxed{A_{2,c}\|w\|_2^2\le\|T^{(2)}w\|_{2,c}^2
\le B_{2,c}\|w\|_2^2.}\tag{L2c}
$$

Proof of the bounds. On D(K_c), integration by parts gives K_c>=cI, hence ||f||_2<=c^(-1)||K_cf||_2 and ||f''||_2<=2||K_cf||_2. The elementary interpolation and trace bounds, also established in the current cofinite source, are

$$
\|f'\|_2\le\sqrt3\|f\|_2+d\|f''\|_2,
\quad |h(t)|\le2^{-1/2}\|h\|_2+\sqrt2\|h'\|_2.\tag{L2d}
$$

For endpoint values u,v, the affine interpolant has squared L2 norm (2/3)(|u|^2+|v|^2+Re(u conjugate(v)))<=|u|^2+|v|^2. Applying (L2d) yields ||ell_f||_2<=||f||_2+2||f'||_2<=L_c||K_cf||_2. Therefore ||a||_2<=L_c||K_cf||_2 and ||z||_2=||f''||_2<=2||K_cf||_2, proving the lower bound. In the opposite direction, g=J^2(sum z_n e_n), so

$$
\|K_c f\|_2\le c\|a\|_2+(1+cC_2)\|z\|_2.
$$

Cauchy-Schwarz proves the upper bound. Completeness follows from (L2a), since ordinary H^2 convergence implies convergence under K_c. These inequalities extend to all square-summable coefficients and prove the Riesz-basis assertion. They are not uniform as c decreases to zero.

## L3. s=4: four explicit lifts, five-term high modes

The actual domain is D(K_c^2)={f in ordinary H^4:Bf=B(f'')=0}. This equality follows from f,K_cf in D(K_c), since f''=cf-K_cf in H^2 and B(K_cf)=cBf-B(f''); the converse is immediate from the same identities.

Set

$$
q_6=x^6-5x^4+7x^2,\qquad
q_7=x^7-\frac{21}5x^5+\frac{27}5x^3,
$$

$$
E=\frac{3-q_6}{16},\qquad
O=\frac{11x-5q_7}{48}.
$$

The four low lifts are ell_0=1, ell_1=x, ell_2=E, ell_3=O. Direct differentiation gives

| lift | f(1), f(-1) | f''(1), f''(-1) |
|---|---|---|
| 1 | 1,1 | 0,0 |
| x | 1,-1 | 0,0 |
| E | 0,0 | 1,1 |
| O | 0,0 | 1,-1 |

All four satisfy both Krein conditions: E'(±1)=E'''(±1)=0; O'(±1)=0 and O'''(±1)=1. Their degrees are 0,1,6,7. For f in D(K_c^2) define

$$
a=\frac{f(1)+f(-1)}2,\quad b=\frac{f(1)-f(-1)}2,\quad
d_0=\frac{f''(1)+f''(-1)}2,\quad e=\frac{f''(1)-f''(-1)}2,
$$

$$
\ell_f=a+bx+d_0E+eO,\qquad g=f-\ell_f.
$$

The values and second derivatives match by the table. Both Krein conditions also match first and third derivatives, so g in H_0^4. Consequently

$$
\Phi^{(4)}=(1,x,E,O,b_4^{(4)},b_5^{(4)},\ldots)\tag{L3a}
$$

is complete in H_c^4. For N>=8 its columns with n<=N-4 span exactly Pi_N intersect D(K_c^2), of dimension N-3. To prove this, subtract the degree-at-most-seven lift; g^(4) is a polynomial perpendicular to Pi_3 and expands in e_4,...,e_(N-4), so L1 integrates it back. Uniqueness follows first from endpoint data, then from the orthonormal derivatives.

There is a fixed-c, degree-independent stability estimate here as well. Define

$$
F_0=c^{-2},\quad F_2=2c^{-1},\quad F_4=4,\quad
F_1=\sqrt3F_0+dF_2,\quad F_3=\sqrt3F_2+dF_4,
$$

$$
D_c^2=(F_0/\sqrt2+\sqrt2F_1)^2+(F_2/\sqrt2+\sqrt2F_3)^2,
\quad M_c^2=\sum_{j=0}^3\|\ell_j^{(4)}-2c\ell_j''+c^2\ell_j\|_2^2,
$$

$$
A_{4,c}=(D_c^2+16)^{-1},\qquad
B_{4,c}=M_c^2+(1+2cC_2+c^2C_4)^2.\tag{L3b}
$$

M_c is a finite, explicitly defined polynomial integral; no numerical positive lower bound is assumed.

Its exact expanded value, obtained by integrating the four displayed polynomial lifts, is

$$
M_c^2=\frac8{405405}\left(136657c^4+24984c^3+487890c^2+4890600c+22297275\right).
$$

The private author exact-check record reproduces this polynomial identity. For every finite w,

$$
\boxed{A_{4,c}\|w\|_2^2\le\|T^{(4)}w\|_{4,c}^2
\le B_{4,c}\|w\|_2^2.}\tag{L3c}
$$

Proof. Apply the s=2 estimates to f and K_cf, using ||K_cf||_2<=c^(-1)||K_c^2 f||_2. They give ||f^(j)||_2<=F_j||K_c^2 f||_2 for j=0,2,4: for j=4 use f^(4)=cf''-(K_cf)'', so its norm is at most 4||K_c^2f||_2. Applying (L2d) to f and f'' gives j=1,3. The trace bound then gives ||(a,b,d_0,e)||_2<=D_c||K_c^2f||_2. Further, ell_f^(4) has degree at most three and g^(4) is perpendicular to Pi_3, so

$$
\|z\|_2=\|g^{(4)}\|_2\le\|f^{(4)}\|_2\le4\|K_c^2f\|_2.
$$

This proves the lower bound. The low lift contributes at most M_c||(a,b,d_0,e)||_2. For the high part use g=J^4 v, g''=J^2 v and g^(4)=v, ||v||_2=||z||_2. It contributes at most (1+2cC_2+c^2C_4)||z||_2. Cauchy-Schwarz proves the upper bound. The expansion converges in ordinary H^4 by L1 and hence in H_c^4. This proves completeness and uniform Riesz bounds in N.

## L4. Actual sparsity, errors, and the remaining limits

At s=2, K_cb_n^(2) has Legendre support {n-2,n,n+2}. Thus the high-high Gram entry is zero for |n-m|>4 and also for opposite parity. The two low columns couple only to n=2,3. At s=4, K_c^2 b_n^(4) has support {n-4,n-2,n,n+2,n+4}; hence the high-high Gram entry is zero for |n-m|>8 and for opposite parity. K_c^2 ell_j has degree at most seven, so the low lifts couple only to high indices n<=11. The low block has fixed size four. These statements follow from orthogonality and support, not from observed floating-point zeros. They concern the exact constant-c left-definite Gram matrix; variable coefficients generally change them.

Let s=r in {2,4}, Q_c=1+cC_2 for r=2 and Q_c=1+2cC_2+c^2C_4 for r=4. For f=ell_f+J^r(sum_(n>=r) z_n e_n), retain the lift and n<=N-r. Then

$$
\|f-f_N\|_{s,c}\le Q_c\left(\sum_{n>N-r}|z_n|^2\right)^{1/2}.\tag{L4a}
$$

If, as an additional quantitative hypothesis, M_t^2=sum_(n>=r)(n+1)^(2t)|z_n|^2<infinity for t>0, then

$$
\|f-f_N\|_{s,c}\le Q_c(N-r+2)^{-t}M_t.\tag{L4b}
$$

This states regularity as an exact coefficient condition. No unquantified smoothness-to-exponential-convergence step is used. With exact Gram data, every finite Gram eigenvalue lies in [A_(s,c),B_(s,c)]. Therefore choosing 0<epsilon<A_(s,c) in note 02 retains all columns, gives the best H_c^s approximation in this polynomial space, and has condition number at most B_(s,c)/A_(s,c), independent of N. For arbitrary epsilon, T1 combined with the particular coefficient vector above yields the tail bound plus sqrt(epsilon)A_(s,c)^(-1/2)||f||_(s,c).

There is no missing uniform-in-N stability premise for the systems actually constructed here: (L2c) and (L3c) provide it analytically. We have not proved bounds uniform as c->0, bounds for arbitrary constraint modifications, reliable floating-point assembly at arbitrarily large N, quadrature perturbation bounds, or all-s constructions. The two-term residual-cancelling Neumann/Robin-style recombination alone would not imply these left-definite Gram properties; the derivative-orthogonal integration structure is the additional ingredient.

Sources: [Shen author PDF](https://www.math.purdue.edu/~shen7/pub/LegendreG.pdf), especially (2.5) and Lemma 3.1, (3.4)-(3.7). The clamped basis is credited to Shen; the coupled-domain lifts, s=4 adaptation, exact span arguments, constants and conditional error transfer are the derivations above. Current project definitions and norm/domain lemmas are in docs/SL_cofinite_left_definite.tex, R5-OP, and docs/SL_fractional_left_definite.tex, square-domain/four-trace-core sections (frozen hashes in source-manifest.json). Neither source's status label substitutes for this author's pending independent review.
