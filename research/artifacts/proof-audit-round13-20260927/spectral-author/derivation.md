# Round13 author derivation (not an independent approval)

Scope: finite positive piecewise constant density on [0,L], strictly ordered interfaces, left Dirichlet and right Dirichlet or Neumann where stated. The Jacobian uses the full DD problem on [0,1], simple modes a=lambda_n, b=lambda_{n+1} and integral rho*u_k^2=1. Physical interface coordinates x_i, not softmax z_i, are differentiated. s_i=rho(x_i+)-rho(x_i-). Claims in the supplied REPORT/analytic_notes were inputs to check, not premises proving the repair.

## One physical solution and one mass

For -y''=mu*rho*y, constant-density propagation on a block of signed length d is

P(d) = [[C(d), S(d)],[-mu*rho*S(d), C(d)]].

For mu>0, k=sqrt(mu*rho), C=cos(k*d), S=sin(k*d)/k. At mu=0, C=1,S=d. For mu<0, k=sqrt(-mu*rho), C=cosh(k*d),S=sinh(k*d)/k. These matrices solve the same physical state equation for (y,y'), have determinant one and compose in physical order. Both state components are continuous at interfaces because the coefficient of y'' is one. Initial state (0,1) fixes the common sign.

On a positive-frequency block of length l, let (A,B) be the state at its midpoint and q=k*l. In coordinates t centered at that midpoint,

y=A*cos(k*t)+B*sin(k*t)/k.

The cross term integrates to zero. The block mass is

rho * [ A^2*l*(1+sinc(q))/2 + B^2*l^3*(1-sinc(q))/(2*q^2) ],

where sinc(q)=sin(q)/q. The continuous second coefficient at q=0 is l^3/12. Its implemented small-q expansion is l^3*(1/12-q^2/240+q^4/10080-q^6/725760). For |q|<.01, the first omitted coefficient is l^3*q^8/(2*11!), with subsequent terms decreasing, far below binary64 relative resolution of this coefficient. This is a stable floating evaluation of an analytic identity, not outward-rounded arithmetic. Sum block masses once, and divide all values and derivatives from the same initial-value solution by sqrt(mass). No point-value ratio enters, so nodes do not change the scale. R=1 causes no singularity in this construction or the general Jacobian (all s_i vanish).

## Real Green kernel and coordinate covariance

Let phi have left data (0,1). Let psi have right data (0,-1) for D, or (1,0) for N. The Wronskian W=phi*psi'-phi'*psi is constant. For the operator -d^2/dx^2-mu*rho, the derivative jump of G at x=y is -1, so

G_mu(x,y) = -phi(min(x,y))*psi(max(x,y))/W.

At x=L, -W=phi(L) for D, or phi'(L) for N. Evaluating the denominator there avoids subtracting two potentially close products. The coordinate min/max gives G(Px)=P*G(x)*P^T and symmetry even for duplicate or reversed coordinates. Dirichlet endpoints give zero rows. Neumann endpoints are retained. Invalid coordinates are rejected rather than extrapolated. For mu<=0 both DD and DN operators are strictly positive by integration by parts/Poincare, so there is no pole: the same linear/hyperbolic formula applies. The unscaled binary64 implementation may raise ArithmeticError for overflow; it does not claim arbitrary-range accuracy or return silent nan. Positive numerically unresolved poles also raise. The reduced half-Green formula is specifically for positive eigenvalues; it now explicitly rejects nonpositive parameters and directs them to green_regular.

## General residual Jacobian

Moving interface i to the right gives delta_i rho=-s_i*delta(x-x_i). Differentiate -u''=a*rho*u, project against normalized u, and integrate by parts using fixed DD endpoints:

a_i = a*s_i*u_i^2.

Differentiating integral rho*u^2=1 gives integral rho*u*u_i(dot)=s_i*u_i^2/2. Projection of the differentiated equation onto any other normalized mode u_l yields

< u_l, u_i(dot) >_rho = -a*s_i*u_i*u_l(x_i)/(lambda_l-a).

Consequently, at a fixed observation point x,

d_i u(x) = s_i*u_i^2*u(x)/2 - a*s_i*u_i*Gtilde_a(x,x_i),

where Gtilde_a=sum_{l != n} u_l(x)u_l(y)/(lambda_l-a). This defines the exact reduced resolvent; the code approximates it by a finite sum. The observation point x_j itself moves only if i=j. Write f_j=a*u_j^2-b*v_j^2 and F_j=f_j/b. The full derivative is

J_ji = delta_ji*f'_j/b + s_i/b * (
  2*a*u_i^2*u_j^2 - 2*b*v_i^2*v_j^2 - f_j*v_i^2
  - 2*a^2*u_i*u_j*Gtilde_a(x_i,x_j)
  + 2*b^2*v_i*v_j*Gtilde_b(x_i,x_j)).

The term -f_j*v_i^2 is the derivative of 1/b. No stationarity is used here. This is the expression implemented by jacobian_terms, used by all three repaired public entrypoints. At f=0, setting w_j=a*u_j^2=b*v_j^2 reduces the first three terms to 2*w_i*w_j*(b-a)/(a*b), exactly the existing stationary formula and sign. Subtracting that specialization from the general expression gives

Delta J_ji = s_i/b^2 * (a*u_i^2*f_j + 2*a*u_j^2*f_i - f_i*f_j).

Thus the audit's proposed correction is confirmed by differentiation, separately from its numerical examples. The fprime_id return remains a stationary-only diagnostic and is not used in J. term_breakdown.M1 now includes the full quotient/normalization term; M1_stationary and correction expose the difference without changing old keys.

## Evidence separation

reference.py imports no project code. It enumerates low physical modes by sign brackets, refines physical transfer zeros at 70 decimal digits, normalizes by direct block quadrature, and computes lambda_i=-D_i/D_lambda by high-precision implicit differentiation. Differentiating those normalized residuals supplies the numerical Jacobian reference, without the reduced-Green/source shape formula. This remains numerical evidence, including the independent mode scan, not interval or Lean verification. Test comparison of the correction algebra is additional consistency evidence, not the Jacobian oracle.

No uniform spectral tail bound, interval propagation, complete global G1/M3/KP theorem, or independent author approval is claimed. Analytic identities above are an author derivation for review.

Normalized-sampling compatibility: legacy unit-interval callers form floating block lengths whose sum can differ from 1 by a few ulps. Only eigenfunction_states/eigfun allow endpoint snapping within 8*m*eps*L; farther points are rejected. The mass still uses the supplied blocks and the same physical solution. real_green_matrix/green_kernel/green_regular/solution_states do not inherit this tolerance and reject all coordinates beyond their represented interval. The paired regression tests exercise both contracts.

The point-source expansion used above is meaningful at the interfaces. The energy space is H_0^1(0,1), whose point evaluations are bounded; the weighted eigenbasis divided by sqrt(lambda_l) is orthonormal for the energy inner product. Bessel's inequality for evaluation therefore gives sum_l |u_l(x)|^2/lambda_l < infinity. After omitting the selected pole, large denominators |lambda_l-a| are comparable to lambda_l, and Cauchy-Schwarz gives absolute convergence of the Green pairing at each (x,y). The differentiated weak equation has a point source in H^-1 and its reduced solution belongs to H_0^1. Smooth dependence follows locally from finite block transfer and a simple secular zero. Interface observation uses the continuous physical y' on either side, so the additional delta_ij*f'_j term has no side convention ambiguity.
