# Cofinite closure at s=3: a three-trace author theorem

Status: AUTHOR_PROVED_PENDING_INDEPENDENT_REVIEW. The sufficiency proof is provided below; this is not independent approval or canonical acceptance. Fix c>0 and the current project family

\[
\mathcal D=\{0,1\}\cup\{4,5,6,\ldots\},\quad p_0=1,\quad p_1=x,\qquad
p_{2m}=x^{2m}-\frac m{m-1}x^{2m-2},\quad
p_{2m+1}=x^{2m+1}-\frac m{m-1}x^{2m-1}\quad(m\ge2).
\]

All spans are finite complex spans. The ambient norm is precisely \(\|f\|_{3,c}=\|K_c^{3/2}f\|_{L^2(-1,1)}\). The existing s=2 argument is `docs/SL_cofinite_left_definite.tex`, lemmas `lem:algebra`, `lem:cutoff`, `lem:polyapprox`, theorem `thm:tail`, and theorem `thm:cofinite`. This proof adapts its construction and proves the new order-three estimates; it does not use the false old tail-rigidity claim.

## C1. The space and its topology

\[
\boxed{H_c^3=\{f\in H^3_{\rm Sob}(-1,1):\mathcal Bf=0\},\qquad
\|f\|_{3,c}\asymp_c\|f\|_{H^3_{\rm Sob}}.}\tag{C1}
\]

This follows from (D-NC) in proof 02. There is also the following independent elementary route, making clear exactly what analytic fact is needed for closure.

On V=H^1_Sob(I), define
\(a_c(u,v)=\int u'\overline{v'}-\Delta u\overline{\Delta v}/2+c\int u\overline v\).
Set b=Delta u/2, w=u'-b. Then \(a_c(u,u)=\|w\|_2^2+c\|u\|_2^2\). Write u(x)=u(0)+bx+r(x), r(x)=integral_0^x w(t)dt. Cauchy-Schwarz on each half gives \(\|r\|_2\le\|w\|_2\). Since \(\|a+bx\|_2^2=2|a|^2+(2/3)|b|^2\),
\[
\|u'\|_2\le\sqrt3\|u\|_2+(1+\sqrt3)\|w\|_2.
\]
Thus a_c is positive, closed, and its norm is equivalent to the ordinary H^1 norm for fixed c>0.

The operator associated with this form is exactly K_c. Indeed testing a_c(u,v)=<h,v> on compactly supported v gives -u''+cu=h in distributions, so u in H^2. Integration by parts then leaves
\((u'(1)-\Delta u/2)\overline{v(1)}-(u'(-1)-\Delta u/2)\overline{v(-1)}\).
The two endpoint values of v in H^1 are independent, so it vanishes for all v exactly when Bu=0. The closed positive form representation theorem now gives D(K_c^{1/2})=H^1 and \(\|K_c^{1/2}u\|^2=a_c(u,u)\). This use is the standard representation theorem for densely defined closed positive forms, not a numerical assertion.

The spectral product criterion gives
\(D(K_c^{3/2})=\{f\in D(K_c):K_cf\in D(K_c^{1/2})\}\).
If f belongs to this set, f''=cf-K_cf in H^1, hence f in H^3. Conversely H^3 and Bf=0 imply K_cf in H^1. For the norm equivalence, the upper bound follows from \(a_c(K_cf,K_cf)\le C_c\|K_cf\|_{H^1}^2\le C'_c\|f\|_{H^3}^2\). For the lower bound, form norm equivalence controls \(\|K_cf\|_{H^1}\) by \(\|f\|_{3,c}\); the project's H^2 estimate \(\|f\|_{H^2}\le C_c\|K_cf\|_2\), together with \(f'''=cf'-(K_cf)'\), controls the remaining third derivative. This proves (C1) without needing the entire fractional dictionary.

In particular \(\Gamma_3f=(f(0),f'(0),f''(0))\) is a bounded map from H_c^3 to C^3. All three traces exist because f'' in H^1. It is onto, since
\[
\Gamma_3p_0=(1,0,0),\quad\Gamma_3p_1=(0,1,0),\quad
\Gamma_3p_4=(0,0,-4).
\]
Let V_3=ker Gamma_3. We have the bounded topological direct sum
\[
H_c^3=V_3\dotplus\operatorname{span}\{p_0,p_1,p_4\},\qquad
f=v+f(0)p_0+f'(0)p_1-\tfrac14f''(0)p_4.\tag{C2}
\]
This is not asserted to be an orthogonal sum in the left-definite inner product.

## C2. Algebra of a sufficiently high complete tail

For any integer m0>=3 set L=2m0-2>=4 and
\(\mathcal T_{m0}=\operatorname{span}\{p_{2m},p_{2m+1}:m\ge m0\}\).
Then
\[
\mathcal T_{m0}=\mathbb C[x]\cap\ker\mathcal B\cap x^L\mathbb C[x].\tag{C3}
\]

The forward inclusion follows by substitution. Conversely subtract the leading coefficient times p_n whenever the degree n>=L+2. This strictly decreases degree and preserves both B=0 and x^L divisibility. The remaining polynomial is alpha x^L+beta x^{L+1}. Since L is positive and even,
\[
(\mathcal Bx^L,\mathcal Bx^{L+1})=
\begin{pmatrix}L&L\\-L&L\end{pmatrix},\qquad\det=2L^2\ne0.
\]
Its coefficients must vanish. This proves (C3) for every m0, without a degree bound. Every member of T_m0 has three zero centre traces, so its H_c^3 closure is contained in V_3.

## C3. Order-three cutoff estimates

Take f in V_3 and a smooth even eta equal to zero on [-1,1] and one outside (-2,2). For 0<delta<1/4 set f_delta=eta(x/delta)f. The endpoint neighbourhoods are unchanged, so Bf_delta=0. For j=0,1,2 the three zero traces give the repeated-integral identity
\[
f^{(j)}(x)=\int_0^x\frac{(x-t)^{2-j}}{(2-j)!}f'''(t)dt
\]
with the usual oriented integral when x<0. For I_r=(-r,r), Cauchy-Schwarz followed by integration yields
\[
\|f^{(j)}\|_{L^2(I_r)}\le
\frac{r^{3-j}}{(2-j)!\sqrt{(5-2j)(6-2j)}}\|f'''\|_{L^2(I_r)}.\tag{C4}
\]

Let E_delta=||f'''||_{L^2(I_{2delta})}. Leibniz's formula, the derivative bounds ||(eta(x/delta))^{(ell)}||_infinity<=C_ell delta^{-ell}, and (C4) imply for 0<=k<=3
\[
\|(f_\delta-f)^{(k)}\|_2\le C\delta^{3-k}E_\delta.\tag{C5}
\]
For k=3 each derivative falling on eta is paired with precisely the compensating power of delta from a lower derivative in (C4). All terms are supported in I_{2delta}. Absolute continuity of the integral of |f'''|^2 gives E_delta->0. Therefore f_delta->f in H^3_Sob and, by (C1), in H_c^3. A global bound ||f'''||_2 in place of E_delta would not prove convergence; the local norm is essential.

## C4. Approximation preserving divisibility and endpoint conditions

For fixed delta, f_delta/x^L, extended as zero near zero, belongs to H^3_Sob. This follows by replacing x^{-L} inside |x|<delta with a smooth multiplier before multiplying f_delta.

Polynomials are dense in ordinary H^3_Sob: approximate the third derivative in L^2 by polynomials h_j and integrate three times from -1, using the exact initial values of derivatives of order 0,1,2. The bounded integral kernels give convergence of all lower derivatives. Applied to f_delta/x^L, this yields polynomials r_j with x^L r_j=:b_j -> f_delta in H^3_Sob.

Write B b_j=(u_j,v_j)^T. Continuity of endpoint traces in H^3 and B f_delta=0 give u_j,v_j->0. Correct by
\[
\widetilde b_j=b_j-\frac{u_j-v_j}{2L}x^L-\frac{u_j+v_j}{2L}x^{L+1}.\tag{C6}
\]
The fixed matrix in (C3) gives B tilde b_j=0. Divisibility by x^L is preserved and the corrections tend to zero in H^3. Thus tilde b_j belongs to T_m0 and converges to f_delta in H_c^3. Given epsilon, first fix delta to make the cutoff error <epsilon/2, then choose j to make the polynomial/correction error <epsilon/2. Constants may depend on fixed delta,L,c; no uniform multiplier bound or exchange of limits is needed. We have proved the missing sufficiency statement:
\[
\boxed{\overline{\mathcal T_{m0}}^{\,H_c^3}=V_3\quad(m0\ge3).}\tag{C7}
\]

## C5. The cofinite theorem and exact new progress

For every N subset D with D\N finite,
\[
\boxed{\begin{split}
\overline{\operatorname{span}\{p_n:n\in N\}}^{\,H_c^3}
&=V_3\dotplus\operatorname{span}\{p_j:j\in N\cap\{0,1,4\}\}\\
&=\{f\in H_c^3:0\notin N\Rightarrow f(0)=0;\
1\notin N\Rightarrow f'(0)=0;\
4\notin N\Rightarrow f''(0)=0\}.
\end{split}}\tag{C8}
\]

Proof: cofinite N contains a complete tail with m0>=3, so (C7) puts V_3 in its closure. Every p_n other than p_0,p_1,p_4 lies in V_3: p5 begins with x^3 and every p_n for n>=6 begins with degree at least four. The three exceptional vectors have the independent traces in C1. Thus (C2) gives both inclusions in (C8). The right side is closed and has codimension |{0,1,4}\N|. In particular density is equivalent to retaining all of 0,1,4.

This is additional author progress beyond necessary conditions: C3-C4 prove sufficiency in the actual power topology. It is not being entered as an accepted theorem. Independent analysis of C1 and the cutoff/approximation argument remains the coordinator's verification task.

Deleting p4 while retaining every other named member leaves the closed hyperplane f''(0)=0, although the analogous s=2 family is dense. The witness p4 is already enough; q6=p6-(7/2)p4 also has f''(0)=14 and belongs to H_c^4, so higher endpoint compatibility does not remove this centre-trace obstruction. Deleting only p5 has no effect at s=3. The complete nonaffine tail m0=2 has closure ker(f(0),f'(0)), because it includes p4 and a tail with m0>=3.

Remaining scope gaps: no classification at s=5/2, other nonintegral orders, infinite deletions, or arbitrary projected/constraint-generated families is proved here; no Riesz/Schauder/frame assertion follows. The original whole-family density for 0<=s<7/2 is preserved. No Sobolev analysis has been formalized in Lean. The accompanying exact checks cover only the finite boundary and trace algebra.
