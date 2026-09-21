# Round 8 coordinator mathematical candidate

Author: current coordinating task. These derivations are candidates for fresh independent review. They do not rely on the old 05/16/19 certificate verdicts. Sliver/T1 and exact scalar certificates are assigned to other authors.

## Global matching and mode identity

Take R>1, 0<u<1/2, ell=1/2-u, epsilon=R^(-1/2), mu_k=R lambda_k, theta_k=u sqrt(mu_k), z_k=ell sqrt(lambda_k). Simplicity and reflection symmetry make the first eigenfunction even. The second has exactly one interior zero, hence is odd: an even eigenfunction has zeros in symmetric pairs and cannot have a simple zero at the midpoint where its derivative vanishes. Each restricted half-interval mode is strictly positive in (0,1/2) after a sign choice.

In the heavy layer the solution is A sin(sqrt(R lambda)x). The even light-layer solution is B cos(sqrt(lambda)(1/2-x)); the odd one is B sin(sqrt(lambda)(1/2-x)). Eliminating A,B in the two matching equations gives, without division by any trigonometric factor,

E: cos(theta)cos(z)-epsilon sin(theta)sin(z)=0,

O: epsilon sin(theta)cos(z)+cos(theta)sin(z)=0.

Half-mode positivity implies 0<theta_k<pi. It gives 0<z_1<pi/2 and 0<z_2<pi. In E the positive light derivative at the interface forces cos(theta_1)>0, so 0<theta_1<pi/2 for all parameters. For the odd mode theta_2 need not exceed pi/2.

If w=u/epsilon>=2, then c=epsilon ell/u=1/(2w)-epsilon lies in (0,1/4). As theta_2<pi, z_2=c theta_2<pi/4; in particular sin(z_2),cos(z_2)>0. O then forces cos(theta_2)<0, hence pi/2<theta_2<pi. All denominators in the tan/cot conversion are now nonzero. These arguments justify the original large-w delta coordinates, but not a global odd-mode branch.

For R=1600,u=1/1600, rho>=1 and min-max give lambda_2<=4pi^2. Thus theta_2<=u sqrt(R*4pi^2)=pi/20<pi/2, an explicit obstruction to the old all-parameter branch.

## Fixed internal u expansion

Fix 0<u<1/2, b=ell/u>0, t=1/R. For t near zero use analytic power-series continuations

E(theta,t)=cos(theta)cos(b theta sqrt(t))-sqrt(t)sin(theta)sin(b theta sqrt(t)),

O(theta,t)=sin(theta)cos(b theta sqrt(t))+cos(theta)sin(b theta sqrt(t))/sqrt(t).

For t>0 this O is the pole-free odd determinant divided by the positive epsilon. At t=0 the apparent square roots/removable quotient are interpreted by their convergent power series; they define real analytic functions in (theta,t). At p=pi/2, E_theta=-1 and E_t=-b*p. At a in (pi/2,pi) with sin(a)+b*a*cos(a)=0, write H=1+b+b^2*a^2>0. Then O_theta=cos(a)*H !=0 and O_t=b^3*a^3*cos(a)/3. The analytic implicit function theorem gives

theta_1(t)=p-p*b*t+O_u(t^2),

theta_2(t)=a-a^3*b^3/(3H)*t+O_u(t^2).

For all sufficiently small positive t the indicated solutions have the half-mode positivity used above, so are exactly the first even and first odd roots. They are not arbitrary secular roots. Squaring and subtracting yields

G(R,u)=Dbar(u)+C(u)/R+O_u(R^(-2)),

C(u)=pi^2*b/(2u^2)-2*a^4*b^3/(3u^2*H).

The construction and a finite number of derivatives have a common neighborhood and bounds on every compact J contained in (0,1/2), by compactness, uniqueness and nonzero limiting root derivatives. Thus the remainder is O_J(R^(-2)); no endpoint-uniform estimate or infimum expansion is inferred.

The trigonometric relation implies cos(a)^2=1/(1+a^2*b^2), sin(a)^2=a^2*b^2/(1+a^2*b^2), and

I_2=u/2-u*sin(2a)/(4a)=u*(1+b*cos(a)^2)/2,

sin(a)^2/I_2=2*a^2*b^2/(u*H).

For mubar_1=pi^2/(4u^2), mubar_2=a^2/u^2 and S=2*mubar_1/u-mubar_2*sin(a)^2/I_2,

C=4*mubar_1*ell/(3u)+(ell/3)*S.

Consequently at the T2 root S(u*)=0, C(u*)=pi^2*(1/2-u*)/(3*u*^3)>0. The nonzero first term is R^(-1). In particular sqrt(R)(G(R,u*)-Dbar(u*)) tends to zero. Establishing a rate for the global minimizing parameter/value requires additional uniform derivative and localization reasoning, not this fixed-u assertion alone.

## Cotangent repair and the A'' constants

NIST DLMF4.22.3 was actually read on 2026-09-22: https://dlmf.nist.gov/4.22.E3. For 0<z<pi it gives

(1/z-cot(z))/z=2*sum_(n>=1) 1/(n^2*pi^2-z^2).

The series converges uniformly on each compact subset of (-pi,pi). Every term is strictly increasing for z>0, so their sum is strictly increasing there. This also proves positivity and cot(z)<1/z. The corrected Laurent form is cot(z)=1/z-sum_(k>=1)c_k*z^(2k-1), with positive c_k=2^(2k)|B_(2k)|/(2k)!, starting z/3. R(z)/z starts with constant1/3, not z^2/3. Extend R continuously by R(0)=0.

The supplied elementary three-piece proof of B(t)<=9 avoids the faulty floating grid. For t in (pi/2,pi), v=-t*cot(t)>0,

B(t)=2*t^4/(t^2+v^2+v)=2*t^3*sin(t)^2/(t-sin(t)cos(t))<=2*t^2*sin(t)^2.

For t<=2 this is <=8. For 2<=t<=23/10, sin(t)<=sin(2)<91/100, hence B<=2*(23/10)^2*(91/100)^2<9. For t>=23/10, q=t sin(t) has q''=2cos(t)-t sin(t)<0, and the exact scalar bounds sin(23/10)<3/4,cos(23/10)<-3/5 give q'(23/10)<0. Thus q decreases, and B<=2*((23/10)*(3/4))^2<9. Certificate author independently checks all scalar inequalities.

For K=v(v+1)>0 and theta in [pi/2,t], B(theta)=t*theta^2*(t+theta)/(t*theta+K) has derivative

t*(t^2*theta^2+2*t*theta^3+2*t*K*theta+3*K*theta^2)/(t*theta+K)^2>0.

Together with Cz<337/1000, pi>333/106, pi/2-delta_1^+>156/100, c2>99996/100000 and 1/(1-delta)<100046/100000, this gives the exact-rational upper bound <8256/10000. The complete A'' proof still requires its displayed phase and defect inequalities; the scalar certificate alone is not the theorem.

## Additional source corrections

- The T1 original near-minimizer paragraph contains the impossible string '+infinity<3pi^2'; use the two finite/endpoint comparisons separately.
- Replace the obsolete u* approximation by the new certified enclosure, without altering sealed old runs.
- Old medium-region / sampling scripts retain historical identity, but their PASS labels are not current directed-rounding certificates.
- Distinguish failure of a certificate/enclosure from a counterexample to the spectral theorem.
