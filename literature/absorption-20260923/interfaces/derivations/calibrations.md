# Analytic calibrations and actual author execution

These calibrations use the same Dirichlet interval [0,1], physical state (u,u'), eigenvalue variable lambda and weighted normalization as Theorem P. They establish no global sign claim. The standalone numerical program imports no project modules. It also does not reproduce an old spectral truncation or an old numerical result.

## C1. An exact single-interface configuration with a nonzero interface term

Set rho=1 to the left of a and rho=4 to the right. Write w=sqrt(lambda). The direct physical transfer product gives

`F(lambda,a)=(T_4(1-a,lambda)T_1(a,lambda))_(01)`

`=[3 sin((2-a)w)+sin((3a-2)w)]/(4w)`.                                      (C1)

At a=1/2 set theta=arccos(1/sqrt(3)). Since

`F(lambda,1/2)=sin(w/2)[3 cos²(w/2)-1]/w`,

the first two positive roots are exactly w_1=2theta and w_2=2(pi-theta). The next is 2pi, so the two selected roots have the claimed indices. The removable expression at w=0 has value 1 and is not a Dirichlet eigenvalue. The multiplying factor 4w in (C1) is nonzero at these roots; off-root derivatives of F and its numerator are not interchangeable.

Let t=w_k/2, S=sin t=sqrt(2/3), C=cos t=+1/sqrt(3) for k=1 and -1/sqrt(3) for k=2. Put H(w,a)=4w F(w²,a). At the base root a=1/2,

`H_w=-8C`, `H_a=8w C`, `H_ww=-2S`,

`H_aw=8C`, `H_aa=8w² S`.

These follow by ordinary trigonometric differentiation, using sin(3t)=S/3 and cos(3t)=-5C/3. Implicit differentiation yields

`w_a=w`, `w_aa=2w+(3/4)w² tan t`,

`lambda_a=2lambda`,

`lambda_aa=6lambda+(3/2)w³ tan t`.                                         (C2)

For the shooting normalization y'(0)=1, the norm is N=1/w²: indeed y'(1)=-3C, F_lambda=-C/w² and N=y'(1)F_lambda. Hence

`u(a)=S`, `u'(a)=w C`, `integral rho u²=1`.

The interface diagonal Green numerator is

`P(z)=sin(sqrt(z)a)/sqrt(z) * sin(2sqrt(z)(1-a))/(2sqrt(z))`.

For any simple root, Taylor division of P(z)/F(z) gives a finite part without subtracting two large numerical poles:

`Gtilde(a,a)=P'(lambda)/F'(lambda)-P(lambda)F''(lambda)/(2F'(lambda)²)`.      (C3)

The residue identity is `P(lambda)/F'(lambda)=-u(a)²`. Direct differentiation in (C3) at these two exact roots gives

`Gtilde_k(a,a)=1/(6w_k²)+tan(w_k/2)/(24w_k)`.                               (C4)

For unit interface velocity, jump s=3, Theorem P separates into

`Hbar_k(-3delta_a,-3delta_a)=6lambda_k-(1/2)w_k³ tan(w_k/2)`,

`geometric_k=2lambda_k s u(a)u'(a)=2w_k³ tan(w_k/2)`.

Their sum is exactly (C2). The geometric term is nonzero for both modes. For a(t)=1/2+(2/5)t-(1/14)t² the full derivative additionally contains `lambda_a*(-1/7)`; the velocity-squared coefficient is 4/25. This supplies a nonstationary, non-affine-path check of both acceleration terms.

## C2. Constant density scaling fixes the kernel component

For rho=c>0 and the linear density direction h=rho, the exact eigenpair is

`lambda_k(t)=k²pi²/[c(1+t)]`,

`u_k(t,x)=sqrt(2/[c(1+t)]) sin(k pi x)`.

Thus v=-u/2, lambda'=-lambda and lambda''=2lambda. The projected forcing (h-A rho)u is zero because A=1. Its particular inverse gives zero, while the normalized eigenfunction derivative is not zero. This calibration rejects deletion of the kernel component independently of interface motion.

If one merely marks an interface inside the identical densities c_-=c_+=c, all s_i vanish; Theorem P gives zero shape derivatives. Density scaling and movement of a fictitious interface are different paths.

## C3. Constant density plus a genuine midpoint mass

For dvarrho=dx+M delta_a, M>=0, dvarsigma=dx and dchi=0, the physical jump is

`J_M(lambda)=[[1,0],[-lambda M,1]]`.

The direct transfer matrix gives

`F_M(lambda)=sin(w)/w-M sin(wa)sin(w(1-a))`.                               (C5)

At a=1/2 the even branch w=2pi is locally unchanged by M. The lowest branch satisfies

`cot(w/2)=M w/2`.

Differentiating at M=0, w=pi, gives w_M=-pi and w_MM=2pi. Therefore

`lambda_1'(0+)=-2pi²`, `lambda_1''(0+)=6pi²`,

`lambda_2'(0+)=lambda_2''(0+)=0`,

`Q=(lambda_2''-lambda_1'')/2=-3pi²`.                                      (C6)

The implicit secular root has a two-sided algebraic analytic extension near M=0, but M<0 is outside this positive coefficient-measure model. Equations (C6) are valid physical right derivatives. This agrees with the fixed-base unit-mass pulse limit in round9 V3, whose spectral sum was justified analytically there. It is not an assertion about moving the atom, or a sign theorem for a constraint tangent cone.

## C4. A bounded layer-to-atom transfer limit

For fixed M>=0 and e>0 small enough, put rho_e=1+M/(2e) on (a-e,a+e), rho_e=1 elsewhere. For the inner layer set q²=lambda(1+M/(2e))(2e)²=lambda(4e²+2Me). The power series of sine and cosine give, locally uniformly for lambda in bounded complex sets and for M in bounded nonnegative sets,

`T_(1+M/(2e))(2e,lambda) -> [[1,0],[-lambda M,1]]`.

The upper-right entry is 2e+O(e²); the diagonal entries are 1+O(e); the lower-left entry is -lambda M+O(e). Multiplying by the two exterior blocks, whose lengths tend to a and 1-a, proves local uniform convergence of the **physical** secular function to (C5). Around a simple positive zero, a small complex contour and the argument principle give convergence of the unique enclosed zero. This is a specific analytic justification beyond weak-* measure convergence. It does not by itself exchange second shape derivatives with the concentration limit. We do not claim uniform control in unbounded M or spectral index.

## Actual execution and its limits

Executed `/usr/bin/python3 -B scripts/run_checks.py` from this author directory. The wrapper retained the exact subprocess argv, Python/version/platform, stdout, stderr, return code, UTC times and script SHA-256 under:

`../evidence/run-20260923T070250443181Z/`.

Result: exit code 0, 39/39 author checks passed, mpmath 70 decimal digits. Checks compare direct-matrix implicit derivatives with weighted normalization, analytic roots/derivatives, Laurent coefficients and the complete chain rule. They also exercise omission controls for normalization, geometric acceleration and the half-gap factor. The maximum absolute discrepancy among high-precision equality checks was about 4.64e-69; this is a floating-point residual, not a certified error bound.

| Mode at a=1/2 | Density quadratic term | Interface geometric term | Actual lambda_aa |
| --- | ---: | ---: | ---: |
| k=1 | 16.9711852397943 | 19.7277237638485 | 36.6989090036428 |
| k=2 | 173.829218629734 | -236.455795806954 | -62.6265771772203 |

Along the curved path in C1, the second derivatives were 4.82881990816587 and -15.4828842377836, so Q_path=-10.1558520729747. Physical root central differences at steps 1e-3, 5e-4 and 2.5e-4 had errors approximately (3.5524e-7,8.8810e-8,2.2203e-8) for mode 1 and (6.4845e-5,1.6211e-5,4.0529e-6) for mode 2. The observed fourfold decrease is consistent with second-order truncation.

For M=0.2, finite layers at e=0.1,0.05,0.025,0.0125 approached the two atomic reference roots; the final absolute discrepancies were about 0.01327 and 0.03303. This is deliberately reported as finite-width evidence, not exact equality with the atom. An off-shell matrix test at lambda=7.3 also approached the jump matrix as e decreased from 1e-2 to 1e-4.

No old project script, full-spectrum truncation, interval certificate, Lean compiler or independent acceptance reviewer was run by this author. Analytic scope comes from the proofs and hypotheses above; the finite numerical samples do not extend it.
