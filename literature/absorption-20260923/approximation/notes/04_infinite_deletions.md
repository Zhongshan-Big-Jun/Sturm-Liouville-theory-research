# Two infinite-deletion subclasses in the actual second left-definite space

Status: AUTHOR_PROOF with external input L07 as explicitly stated; pending fresh independent review. Fix c>0 and H_c^2=D(K_c), ||f||_(2,c)=||K_cf||_2. The current cofinite classification and full-family density for 0<=s<7/2 remain established project inputs, not reopened problems.

Write D={0,1} union {4,5,...}, p_0=1, p_1=x, and for m>=2,

$$
p_{2m}=x^{2m}-\frac m{m-1}x^{2m-2},\qquad
p_{2m+1}=x^{2m+1}-\frac m{m-1}x^{2m-1}.
$$

Given S_e,S_o subset {2,3,...} and J subset {0,1}, retain exactly

$$
N(J,S_e,S_o)=J\cup\{2m:m\in S_e\}\cup\{2m+1:m\in S_o\}.\tag{D0}
$$

The two explicit examples will be

- Arithmetic: S_e=S_o={2,4,6,...}, J={0,1}; equivalently N={0,1} union {4j,4j+1:j>=1}.
- Sparse: S_e=S_o={2^j:j>=1}, J={0,1}; equivalently N={0,1} union {2^(j+1),2^(j+1)+1:j>=1}.

Here N is a prescribed selection of generators, not the actual membership set N_V={n:p_n in V} of a closed space V. In the arithmetic example the closure contains all the omitted high generators as well. Thus (D7) is not a classification of closed spaces with an arithmetic actual membership set; it is consistent with the existing cofinite actual-membership classification.

## D1. The real polynomial and moment mapping

Set q_n=K_cp_n. Direct differentiation, with no formal higher-power substitution, gives

$$
q_{2m}=cx^{2m}-A_mx^{2m-2}+B_mx^{2m-4},\quad
A_m=2m(2m-1)+\frac{cm}{m-1},\quad B_m=2m(2m-3),
$$

$$
q_{2m+1}=cx^{2m+1}-A'_mx^{2m-1}+B'_mx^{2m-3},\quad
A'_m=2m(2m+1)+\frac{cm}{m-1},\quad B'_m=2m(2m-1).\tag{D1}
$$

Also q_0=c and q_1=cx. Since K_c:H_c^2->L2 is an isometric isomorphism, a candidate annihilator u in H_c^2 maps to an actual vector g=K_cu in L2. With M_k=<g,x^k> (first variable linear), the exact conditions are

$$
cM_{2m}-A_mM_{2m-2}+B_mM_{2m-4}=0\quad(m\in S_e),
$$

$$
cM_{2m+1}-A'_mM_{2m-1}+B'_mM_{2m-3}=0\quad(m\in S_o),\tag{D2}
$$

together with M_0=0 if 0 is retained and M_1=0 if 1 is retained. There is **no equation** at an omitted index. Extending the recurrence through a gap changes the problem.

For parity, put t=x^2, g_e(x)=h_e(x^2) and g_o(x)=x h_o(x^2). Then exactly

$$
\|g_e\|_2^2=\int_0^1|h_e(t)|^2t^{-1/2}\,dt,
\quad M_{2k}=\int_0^1h_e(t)t^{k-1/2}\,dt,
$$

$$
\|g_o\|_2^2=\int_0^1|h_o(t)|^2t^{1/2}\,dt,
\quad M_{2k+1}=\int_0^1h_o(t)t^{k+1/2}\,dt.\tag{D3}
$$

The coefficient is one, because the two half intervals cancel the Jacobian factor 1/2. Multiplication by t^(-1/4) in the even branch and t^(1/4) in the h_o representation gives unitary maps to **unweighted** L2(0,1). Under these maps the images of the actual columns are

$$
c t^{m-1/4}-A_m t^{m-5/4}+B_m t^{m-9/4},\qquad
c t^{m+1/4}-A'_m t^{m-3/4}+B'_m t^{m-7/4}.\tag{D4}
$$

The affine images are c t^(-1/4) and c t^(1/4). Every exponent is strictly greater than -1/2, including m=2. These are legitimate L2 columns, but they are prescribed three-term combinations, not freely independent monomials.

## D2. What Full Müntz actually supplies

Erdelyi--Johnson's author PDF, Theorem 1.3, p.3 (repeated as Theorem 3.6, p.11), states the unweighted Lp(A) criterion for distinct real exponents lambda_j>-1/p, 0<p<infinity, and compact A subset [0,1] with positive lower density at zero:

$$
\overline{\operatorname{span}\{t^{\lambda_j}\}}^{L_p(A)}=L_p(A)
\quad\Longleftrightarrow\quad
\sum_j\frac{\lambda_j+1/p}{1+(\lambda_j+1/p)^2}=\infty.\tag{D5}
$$

No ordering or divergence of lambda_j is assumed. For lambda_j->infinity this reduces to a reciprocal-sum condition. The lower limit -1/p is strict; equality is nonintegrable on [0,1]. Repeated exponents must be removed before using the sum. The theorem is not a Sobolev-norm theorem and is not stated for arbitrary weights. For 0<p<1 the displayed Lp quantity is a quasi-norm; the application here uses p=2.

Our elementary power-weight transfer: in L2((0,1),t^alpha dt), multiplication by t^(alpha/2) is unitary onto unweighted L2, so monomial exponent mu becomes lambda=mu+alpha/2 and integrability is mu>-(alpha+1)/2. Apply this only to the powers alpha=±1/2 in (D3), or to other explicitly checked power weights. Complex L2 density follows from the real theorem by approximating real and imaginary parts; non-density follows by the real orthogonal complement, also nonzero in the complexification.

The actual project rows (D4) lie inside the spans of the enlarged, deduplicated exponent sets

$$
\Lambda_e=\{-1/4\}\cup\bigcup_{m\in S_e}\{m-1/4,m-5/4,m-9/4\},
$$

$$
\Lambda_o=\{1/4\}\cup\bigcup_{m\in S_o}\{m+1/4,m-3/4,m-7/4\}.\tag{D6}
$$

Including an affine exponent even if its column was omitted only enlarges the comparison space. Non-density of this larger monomial space implies non-density of the difference system. Its density does not imply the converse, because its independent coefficients do not respect (D4). The two-term p family already exhibits this distinction before applying K_c. The following positive result requires a separate construction.

## D3. Arithmetic-progressions give the same trace closure

**Theorem.** Suppose S_e contains {a_e+d_e j:j>=0} and S_o contains {a_o+d_o j:j>=0}, where a_e,a_o>=2 and d_e,d_o>=1 are integers. For J subset {0,1},

$$
\boxed{\overline{\operatorname{span}\{p_n:n\in N(J,S_e,S_o)\}}^{H_c^2}
=\{f\in H_c^2:0\notin J\Rightarrow f(0)=0,\quad
1\notin J\Rightarrow f'(0)=0\}.}\tag{D7}
$$

Proof. All high columns vanish together with their first derivative at zero. Both traces are continuous in H_c^2. Thus the left side is contained in the right side. It suffices to prove that the high arithmetic columns are dense in V_*={f in H_c^2:f(0)=f'(0)=0}, branch by branch; then add the retained affine columns.

First justify the smooth test class. The local zero-trace cutoff from the current cofinite proof has f_delta=eta(x/delta)f, zero near zero, identical to f near endpoints, and tends to f in ordinary H^2. Indeed with E_delta=||f''||_(L2(-2delta,2delta)), its errors at orders 0,1,2 are bounded by C delta^2 E_delta, C delta E_delta, C E_delta; E_delta tends to zero. Fix delta and approximate f_delta in ordinary H^2 by smooth functions. Multiply these by a fixed even smooth cutoff chi, zero in a smaller central neighborhood and equal to one on the support of f_delta and near endpoints. This preserves convergence and gives smooth functions zero near zero. Correct their small boundary residual using chi x^2 in the even branch or chi x^3 in the odd branch. Near the endpoints these equal x^2,x^3 and their residual vectors are (2,-2),(2,2), respectively. The correcting coefficients tend to zero. Taking even/odd parts before correction proves that smooth, boundary-compatible, parity-pure functions vanishing near zero are dense in the respective part of V_*.

For any such even test function write f(x)=h(x^2); for an odd test function write f(x)=x h(x^2). In both cases h is smooth on [0,1], zero near zero, and the Krein endpoint condition is exactly h'(1)=0. Define

$$
b_m(t)=t^m-\frac m{m-1}t^{m-1},\qquad
b_m'(t)=m t^{m-2}(t-1),\quad b_m(0)=0.\tag{D8}
$$

Fix the relevant a,d and put

$$
k(t)=\frac{h'(t)}{(t-1)t^{a-2}},\qquad F(u)=k(u^{1/d}).
$$

The apparent singularity at t=1 is removable, since h'(1)=0; for example h'(t)/(t-1)=integral_0^1 h''(1+theta(t-1)) dtheta. Near zero k is defined as zero because h is zero there. Consequently F is smooth on [0,1] despite the root map at zero. Approximate F in C^1[0,1] by polynomials R_l. This follows by uniformly approximating F' and integrating, matching F(0). Define

$$
h_l(t)=\int_0^t(v-1)v^{a-2}R_l(v^d)\,dv.
$$

The map R -> (t-1)t^(a-2)R(t^d) is continuous in C^1 for these fixed integers. Thus h_l -> h in C^2. If R_l(u)=sum_j r_(l,j)u^j, exact integration gives

$$
h_l(t)=\sum_j\frac{r_{l,j}}{a+dj}\,b_{a+dj}(t).\tag{D9}
$$

Moreover h_l'(1)=0. Composing h_l with x^2 (and multiplying by x in the odd branch) gives precisely finite sums of the retained arithmetic p columns, and C^2 convergence on [-1,1] implies convergence in ordinary H^2, hence in H_c^2. This proves high-column density in V_* and completes both inclusions in (D7).

In particular the arithmetic example in (D0) is dense in all H_c^2 despite infinitely many deletions. Removing either affine column introduces exactly its indicated central trace constraint. This is genuinely an infinite-deletion subclass; it is not another proof restricted to cofinite sets. It gives no quantitative coefficient or approximation-rate bound, and none is needed for this closure argument.

## D4. A reciprocal-summable subclass is not dense

**Theorem.** If S_e is infinite and sum_(m in S_e) 1/m < infinity, the even retained family (even including p_0) is not dense in the even part of H_c^2. The analogous assertion holds for S_o and the odd part, even including p_1. In particular the dyadic example in (D0) is not dense in H_c^2.

Proof for the even branch. In (D6) deduplicate Lambda_e. Its finitely many low exponents exceed -1/2. For large m, each positive summand in (D5), p=2, is bounded by a constant times 1/m. Therefore the sum over Lambda_e is finite. Theorem 1.3 gives a proper closed monomial span W in L2(0,1). By the Hilbert projection theorem, choose nonzero v in W-perp. Under the inverse parity unitary set

$$
g_e(x)=|x|^{1/2}v(x^2)\quad (x\ne0),
$$

with arbitrary value at zero. It belongs to L2(-1,1), has ||g_e||_2=||v||_2, and is perpendicular to q_0 and all even q rows in S_e by (D4). Let u=K_c^(-1)g_e. Positivity and surjectivity of the genuine K_c give a nonzero u in H_c^2; reflection invariance makes u even. Then <u,p_n>_(2,c)=<g_e,q_n>_2=0 for all retained even columns. Odd columns are automatically orthogonal by parity. This is an actual function-space annihilator, not a formal moment sequence.

For the odd branch use Lambda_o and g_o(x)=sgn(x)|x|^(1/2)v(x^2). The same argument applies. For S={2^j:j>=1}, sum 1/m=sum 2^(-j)=1, so both branches are obstructed. This is an existence proof of an annihilator; no explicit closed formula for v or a full description of the sparse closure is claimed. Finite S is of course non-dense by finite dimension, independently of Müntz.

## What remains open and a concrete next task

For arbitrary retained sets with divergent reciprocal sum that contain no full arithmetic progression, neither D3 nor D4 decides the difference-family closure. A dense enlarged monomial span is not the missing reverse implication. One must control (D2) together with realization by an L2 vector.

The precise realization condition for proposed complex numbers M_k is the existence of C<infinity such that for **every** finite polynomial a(x)=sum a_k x^k,

$$
\left|\sum_k a_k\overline{M_k}\right|^2
\le C^2\sum_{k,l}a_k\overline{a_l}\int_{-1}^1x^{k+l}\,dx.\tag{D10}
$$

Necessity is Cauchy-Schwarz. Sufficiency follows by continuous extension from dense polynomials and the Riesz representation theorem. The individual moment bound |M_k|<=C sqrt(2/(2k+1)) alone is weaker than (D10). The integral on the right is zero for k+l odd and 2/(k+l+1) otherwise.

An actionable remaining task is to choose a specified divergent, nonarithmetic S and either prove density of (t-1)t^(a-2)-type derivative generators in the weighted Sobolev topology induced by f(x)=h(x^2),xh(x^2), or construct a nonzero sequence satisfying its retained recurrence and the full inequality (D10). Every gap index must remain free. Finite Hankel positivity or finite Gram spectra may screen candidates but cannot certify this all-degree condition. No arbitrary-delete criterion, s=4 named-family result, or numerical-to-infinite promotion is part of this package.

Primary source: [Erdelyi--Johnson author PDF](https://people.tamu.edu/~terdelyi/papers-online/bill.pdf), Theorem 1.3, p.3; Theorem 3.6, p.11. Journal identity: Journal d'Analyse Mathematique 84 (2001), 145-172, [DOI](https://doi.org/10.1007/BF02788108). Project input: docs/SL_cofinite_left_definite.tex, R5-OP, R5-CUT and the explicit q rows; frozen paths/hashes and actual read coverage are in source-manifest.json.
