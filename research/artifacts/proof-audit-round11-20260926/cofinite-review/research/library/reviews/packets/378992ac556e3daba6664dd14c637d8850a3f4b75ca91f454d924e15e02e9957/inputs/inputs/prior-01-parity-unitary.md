# The Krein operator: parity unitary, domains, and spectral transfer

Status: AUTHOR_PROVED_PENDING_INDEPENDENT_REVIEW. This is a project-specific derivation, not an approval. Fix c>0 throughout; complex scalars; inner products linear in the first argument. Let I=(-1,1), J=(0,1), and write H^s_Sob for ordinary Sobolev spaces.

The input is the actual current definition in `docs/SL_fractional_left_definite.tex`, equation `eq:operator-domain`:

\[
K_cf=-f''+cf,\quad D(K_c)=\{f\in H^2_{\rm Sob}(I):\mathcal Bf=0\},\qquad
\mathcal Bf=\binom{f'(1)-\Delta f/2}{f'(-1)-\Delta f/2},\quad
\Delta f=f(1)-f(-1).
\]

The project proves self-adjointness and K_c>=cI in Proposition `prop:operator`; the present proof uses that input, whose exact file hash is in `evidence/project-input-manifest.json`. Inspiration: L05, arXiv:2410.04647v2, Proposition 4.2, Theorems 4.3/4.4/4.7, especially (4.11)-(4.12), PDF pp.20-26. The computation below is independent of its generalized boundary-coordinate conventions.

## P1. The unitary on the entire Hilbert space

Let Rf(x)=f(-x), P_e=(I+R)/2, P_o=(I-R)/2. These are orthogonal projections with orthogonal ranges E and O. Define

\[
Uf=(\sqrt2(P_ef)|_J,\sqrt2(P_of)|_J):L^2(I)\longrightarrow L^2(J)\oplus L^2(J).
\]

Parity gives \(\|Uf\|^2=2\int_0^1(|P_ef|^2+|P_of|^2)=\|f\|^2\). For arbitrary (g,h) in the target, set

\[
U^{-1}(g,h)(x)=2^{-1/2}
\begin{cases}g(x)+h(x),&x>0,\\g(-x)-h(-x),&x<0.\end{cases}
\]

Values at zero are irrelevant in L^2. Direct substitution gives UU^{-1}=I and U^{-1}U=I. Thus U is onto and unitary. Omitting sqrt(2) would shrink squared norms by 1/2.

## P2. Exact operator domains, including gluing

Define the separated realizations

\[
\begin{aligned}
A_{e,c}g&=-g''+cg,&D(A_{e,c})&=\{g\in H^2_{\rm Sob}(J):g'(0)=g'(1)=0\},\\
A_{o,c}h&=-h''+ch,&D(A_{o,c})&=\{h\in H^2_{\rm Sob}(J):h(0)=0,\ h'(1)=h(1)\}.
\end{aligned}
\]

First \(\mathcal B(Rf)=-\big((\mathcal Bf)_-,(\mathcal Bf)_+\big)^T\) and K_cRf=RK_cf. Hence R preserves D(K_c), and both projections preserve it.

If f is even in D(K_c), f'(0)=0 by continuity and oddness of f'; Delta f=0 forces f'(1)=0. If f is odd, f(0)=0 and Delta f=2f(1), so f'(1)=f(1). Restriction therefore gives
\(UD(K_c)\subset D(A_{e,c})\oplus D(A_{o,c})\).

Conversely take g,h in the two displayed half-interval domains. The even extension of g has matching first derivatives at zero precisely because g'(0)=0. The odd extension of h has matching values at zero precisely because h(0)=0; its first derivatives match automatically. The piecewise H^2 extensions therefore belong to H^2(I): their weak second derivatives acquire no delta terms. For f=U^{-1}(g,h), the endpoint data are

\[
f'(1)=f'(-1)=h(1)/\sqrt2,\qquad \Delta f=\sqrt2 h(1).
\]

Thus Bf=0. This proves the reverse inclusion. Differentiation on each half gives, with equality of domains,

\[
\boxed{UK_cU^{-1}=A_{e,c}\oplus A_{o,c},\qquad
UD(K_c)=D(A_{e,c})\oplus D(A_{o,c}).}
\]

Self-adjointness and the lower bound cI transfer to each summand. Direct energy checks also give
\(\langle A_{e,c}g,g\rangle=\|g'\|^2+c\|g\|^2\) and
\(\langle A_{o,c}h,h\rangle=\|h'\|^2-|h(1)|^2+c\|h\|^2\ge c\|h\|^2\), since h(1)=integral_0^1 h'.

## P3. Unbounded functional calculus, not just spectra

For every Borel function F on [c,infinity), the spectral measures obey

\[
UE_{K_c}(S)U^{-1}=E_{A_{e,c}}(S)\oplus E_{A_{o,c}}(S).
\]

Indeed the resolvents are conjugate by P2; uniqueness of the spectral resolution gives this projection identity. The domain criterion \(\int|F|^2d\langle E(\lambda)f,f\rangle<\infty\), applied to that identity, proves both inclusions in

\[
UD(F(K_c))=D(F(A_{e,c}))\oplus D(F(A_{o,c})),\qquad
UF(K_c)U^{-1}=F(A_{e,c})\oplus F(A_{o,c}).
\]

In particular, for every s>=0, U is an exact isometry of the power norms from H_c^s=D(K_c^{s/2}) onto
\(D(A_{e,c}^{s/2})\oplus D(A_{o,c}^{s/2})\). The same U extends by completion to negative scales if those are defined as in the current project. Negative scale elements are not automatically L^2 functions with classical derivatives.

The left-definite realization of K_c in H_c^s has domain H_c^{s+2}, acts as K_c there, and is carried into the corresponding realizations of the two summands. This is the direct spectral interpretation of L01, Theorem 2.4; to use its normalization A>=I with arbitrary c>0, take A=K_c/c. The resulting norm is c^{-s/2} times the project's norm; the underlying domain is unchanged.

## P4. Low-mode and boundary consistency checks

U(1)=(sqrt(2),0), U(x)=(0,sqrt(2)x). Both have eigenvalue c and must be retained. Their full-interval norms squared are 2 and 2/3; their H_c^s norms squared are 2c^s and (2/3)c^s.

B(x^2)=(2,-2), so x^2 is not in D(K_c). In contrast p4=x^4-2x^2 has Bp4=0 but B(p4'')=(24,-24), excluding it from D(K_c^2). The compatible combination q6=p6-(7/2)p4=x^6-5x^4+7x^2 has Bq6=B(q6'')=0 and belongs to D(K_c^2). These distinguish membership of a named element from membership of its finite combinations. Exact algebra is independently replayable by `scripts/exact_checks.py`; it is not a proof of Sobolev domain theory.

This unitary does not make arbitrary coupled self-adjoint domains reflection invariant. It does not prove sparse-family density, frame bounds, or any deletion classification. The project's already established complete-family density for 0<=s<7/2 remains the input baseline.
