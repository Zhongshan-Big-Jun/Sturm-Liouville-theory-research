# A bounded interface chain rule for the project string

Status: original author derivation, awaiting independent review. This is a local theorem for a finite regular step family. The final section gives a conditional extension contract; it is not an assertion of differentiability for arbitrary distribution-valued paths.

## Contract and notation

Fix N>=1 and constants c_0,...,c_N with 0<m<=c_j<=M<infinity. On [0,1] let a_0=0<a_1<...<a_N<a_{N+1}=1, and rho_a=c_j on (a_j,a_{j+1}). Endpoints are Dirichlet. Fix k>=1. Real eigenfunctions satisfy `integral rho_a u_k^2=1` and `u_k'(0)>0`. Set s_i=c_i-c_{i-1}; zero jumps are allowed.

Let a(t) be a C2 path in the open ordered simplex near t=0. All block widths then have a positive lower bound on a sufficiently small compact time interval. Write d_i=a_i'(0), e_i=a_i''(0), lambda=lambda_k(a(0)), u=u_k(a(0)). Derivatives u' without a time dot mean the spatial derivative. Define the signed finite measure mu and the order-one distribution eta by

`mu=-sum_i s_i d_i delta_(a_i)`,

`eta=sum_i s_i d_i^2 delta'_(a_i)-sum_i s_i e_i delta_(a_i)`.                    (P1)

These are derivatives of rho as distributions, not derivatives in L-infinity or in the TV norm. Their pairings below are well-defined because u is C1.

At the base density let Gtilde_k be the continuous Laurent finite part of the pencil Green kernel:

`G_z(x,y)=u(x)u(y)/(lambda-z)+Gtilde_k(x,y)+O(z-lambda)`.

It uses the weighted norm above and the dx forcing convention for `(-d²-z rho)^(-1)`. Define

`A_k=<mu,u²>`, `B_k=<eta,u²>`,

`E_k=double integral u(x)Gtilde_k(x,y)u(y) dmu(x)dmu(y)`.

In finite sums, `A_k=-sum s_i d_i u(a_i)^2`,

`B_k=-sum s_i [2 d_i² u(a_i)u'(a_i)+e_i u(a_i)²]`.

## Theorem P: finite fixed-value interfaces

Under exactly the contract above, lambda_k(a) is locally real analytic in the interface positions. The normalized eigenfunction has a first time derivative v in H0^1 and uniformly in x, with

`lambda'=-lambda A_k`,

`v(x)=-(A_k/2)u(x)+lambda integral Gtilde_k(x,y)u(y)dmu(y)`,                    (P2)

and along the C2 path

`lambda''=2 lambda A_k²-2 lambda² E_k-lambda B_k`.                             (P3)

No stationarity, band-consistency or optimization hypothesis is needed. There is no claim of twice differentiable u in H1, or once differentiable u in spatial C1; v' generally jumps.

For `D_n=lambda_(n+1)-lambda_n`, let `f=lambda_n u_n²-lambda_(n+1)u_(n+1)²` and

`Hbar_k(mu,mu)=2 lambda_k A_k²-2 lambda_k² E_k`.

Then the actual path derivative and its half are

`D_n''=Hbar_(n+1)(mu,mu)-Hbar_n(mu,mu)
        -sum_i s_i [d_i² f'(a_i)+e_i f(a_i)]`,                                 (P4)

`Q_path=D_n''/2`.                                                             (P5)

The diagonal term `-sum s_i d_i² f'(a_i)` is present even for an affine interface path. A stationary configuration f(a_i)=0 removes the e_i term, not the d_i² term. All of (P4), including acceleration, must be halved when reporting Q.

## Proof: regularity before differentiation

On a block of width ell and value c, the physical state (y,y') propagates by

`T_c(ell,z)=[[cos(sqrt(z c)ell), sin(sqrt(z c)ell)/sqrt(z c)],
             [-sqrt(z c)sin(sqrt(z c)ell), cos(sqrt(z c)ell)]]`.

The entries are entire in z by their power series. Their finite product is analytic in z and in all positive widths. With y(0)=0,y'(0)=1, put F(z,a)=y(1,z,a), the (0,1) entry. Differentiating the ODE in z, integration of the Wronskian gives at a Dirichlet root

`y'(1) F_z(lambda,a)=integral rho_a y² >0`.                                    (P6)

The state never has both components zero, so y'(1) is nonzero. Thus F_z is nonzero. The analytic implicit function theorem gives a local branch with fixed index k; simplicity and isolation at the base fix the index locally. Its norm is a positive sum of analytic block integrals. Dividing by its positive square root fixes the eigenfunction sign and normalization.

On each moving closed block, this representation is C2 in t and smooth in x, with uniform local bounds on all derivatives used here. Values and first spatial derivatives match at interfaces for every t. Differentiating matching of values along an interface gives

`v_+(a_i)+d_i u'_+(a_i)=v_-(a_i)+d_i u'_-(a_i)`,

so v is continuous. Difference quotients converge uniformly to this glued v: away from interfaces it is ordinary parameter differentiation; on the O(|t|) strips where the block label changes, equality of the base value and spatial slope cancels the constant and first-order branch discrepancy. The remainders are O(t²) there. The piecewise first spatial derivatives have bounded time difference quotients, converge almost everywhere away from the finitely many base interfaces, and hence converge in L2 by dominated convergence. This proves differentiation in H1 as well. Endpoint derivatives in t vanish because u(t,0)=u(t,1)=0.

More explicitly, derivative matching along the moving interface yields

`[v']_(a_i)=-d_i [u'']_(a_i)=lambda s_i d_i u(a_i)`,

confirming the finite jump that prevents a general C1-in-space claim for v. No second H1 derivative is used below.

## Proof: weak equation and the kernel component

The weak equation is `integral u_t' phi'=lambda_t integral rho_t u_t phi` for phi in H0^1. Integrating the short changed-density strips against the continuous u phi proves that the derivative of the right-hand side is the sum of the measure term and the usual function derivative. The normalization integral is differentiated block by block by the same reasoning. With L=-d²-lambda rho, this gives

`L v=lambda mu u+lambda' rho u`,

`2 integral rho u v+A_k=0`.

Testing the first equation against u and using Dirichlet integration by parts gives lambda'=-lambda A_k. Consequently

`L v=lambda(mu u-A_k rho u)`, `integral rho u v=-A_k/2`.                       (P7)

For completeness, choose left and right endpoint solutions phi_z,psi_z with phi_z'(0)=1 and psi_z'(1)=-1. The scalar kernel is phi_z(min(x,y))psi_z(max(x,y))/F(z). Its denominator has a simple zero by (P6). Subtracting its pole yields a continuous bounded function on the closed square, uniformly in the spatial variables. Its residue is fixed by the identity `(-d²-z rho)^(-1)(rho u)=u/(lambda-z)`, not by ordinary L2 normalization.

The finite-part identities are

`L_x Gtilde_k(x,y)=delta_y-rho(x)u(x)u(y)`,

`integral rho(x)u(x)Gtilde_k(x,y)dx=0`.                                       (P8)

The kernel column lies in H0^1: the endpoint construction is continuous, piecewise C1 with bounded one-sided first derivatives, and its first derivative has the usual finite Green jump. These facts are unchanged by removing the smooth rank-one pole. Applying (P8) to the finite sum of atoms in mu gives an H0^1 particular solution of (P7) in the weighted-orthogonal gauge. The difference from v lies in span(u); normalization in (P7) fixes precisely the coefficient -A_k/2. This proves (P2).

An ordinary L2(dx)-orthogonal inverse of L would instead require a further kernel correction. Dropping -A_k u/2 fails already for the fixed density scaling rho_t=(1+t)rho, where v=-u/2 and the orthogonal forcing vanishes.

## Proof: second derivative without multiplying distributions

At every nearby configuration the first-order formula holds, with

`A_k(t)=-sum_i s_i a_i'(t) u_k(t,a_i(t))²`.

The material derivative of the interface value is v(a_i)+d_i u'(a_i); both have unique values. Ordinary differentiation of this finite sum therefore gives

`A_k'(0)=B_k+2 integral u v dmu`.

Since lambda'=-lambda A_k, substitution of (P2) yields

`lambda''=lambda A_k²-lambda B_k-2lambda[-A_k²/2+lambda E_k]`,

which is (P3). Taking the difference of the two modes gives (P4). This derivation uses only legitimate traces and finite pairings. It never applies a general C2 chain rule to a map from distributions into eigenvalues.

## Relation to the fixed-density Hessian and its concentration extension

For h in L-infinity with rho+t h uniformly positive near zero, round9 V1 proves

`D²lambda_k[h,h]=2lambda_k (integral h u_k²)²
 -2lambda_k² double integral h(x)u_k(x)Gtilde_k(x,y)u_k(y)h(y) dxdy`.

Thus Hbar_k is an extension of this quadratic expression to finite measures by continuity of its kernel. For approximating signed directions with bounded TV, shrinking support clusters and convergent signed cluster masses, uniform continuity proves convergence to Hbar_k(mu,mu). The linear eta term in (P3) is separate. This is not a statement that the eigenvalue functional has a Fréchet Hessian on an open set of all distributions or positive measures. In particular the radius in t preserving positivity for a narrow signed bump may shrink with its width. No limit/differentiation interchange is needed for Theorem P.

## Coordinates and admissibility

In the physical interface coordinates the eigenvalue Hessian is

`(H_k)_ij=2lambda_k s_i s_j u_i² u_j²
 -2lambda_k² s_i s_j u_i u_j Gtilde_k(a_i,a_j)
 +2lambda_k delta_ij s_i u_i u_i'`.                                          (P9)

It is symmetric by kernel symmetry. Along a nonlinear path add `sum_i e_i partial_(a_i)lambda_k`, with `partial_(a_i)lambda_k=lambda_k s_i u_i²`. For widths w_j, the physical interfaces are their cumulative sums, so a width direction must first be transformed to d_i. A nonlinear width parametrization contributes e_i as well.

Every finite d,e is locally realizable inside the open interface simplex by `a+t d+t² e/2`; positivity/order hold for small enough two-sided t. If c_j lie in a prescribed density box, moving the interfaces preserves that box. This does not make mu a two-sided admissible L-infinity density direction at a saturated density.

Additional constraints restrict d,e. Fixed total mass `sum c_j(a_(j+1)-a_j)` imposes `sum s_i d_i=0` and `sum s_i e_i=0`. Gap tangency imposes `sum s_i d_i f(a_i)=0`, a different condition. A general equality constraint C(a(t))=0 requires `grad C dot d=0` and `grad C dot e+d^T Hess(C)d=0`. Endpoint collisions or vanishing widths are outside the theorem.

## Explicit conditional extension contract

Outside finite fixed-value interfaces, (P3) remains an algebraic consequence **if** all of the following are proved in the chosen topology: (i) a simple normalized eigenbranch with lambda C2 and u C1 in H0^1; (ii) a signed finite measure mu for which the differentiated weak equation and first normalization identity (P7) hold; (iii) a distribution eta legitimately paired with u² and the scalar product rule `A_k'= <eta,u²>+2<mu,u v>`; (iv) a finite-part inverse with identities (P8) mapping the chosen forcing to H0^1. These are conditional assumptions for a broader model, not conclusions of weak-* convergence or of L10/L11 alone. None of the results here establishes global sign, G1', uniqueness, or the behavior at interface collisions.
