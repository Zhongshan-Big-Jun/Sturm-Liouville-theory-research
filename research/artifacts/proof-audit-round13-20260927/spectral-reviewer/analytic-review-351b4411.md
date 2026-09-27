# Independent review of frozen packet 351b4411

The only project evidence read is packet.json and its seventeen listed snapshots.
The submitted audit and author derivation are claims to check, not premises.
The SHA-256 of packet.json is
351b4411775cb431fa4f75d0c2e7b37718820cfcd9737cba2820ca43738ff3c6.
All seventeen input hashes were checked before and after execution.

## Analytic contract and independent derivation

Fix finitely many positive lengths and positive finite densities, with positive
total length L and separated interfaces. Both y and y' are continuous at every
interface, since the leading coefficient of -y'' is one. The transfer of the
physical state (y,y') has entries (C,S;-mu*rho*S,C), where S is sin(k*d)/k,
d, or sinh(k*d)/k for positive, zero, or negative mu. The determinant is one.
Signed lengths also propagate the right solution backward correctly.

At a block midpoint write y=A*cos(kt)+B*sin(kt)/k. Symmetry of the integration
interval kills the mixed term. The weighted block mass is

rho*[A^2*l*(1+sinc(kl))/2 + B^2*l^3*(1-sinc(kl))/(2*(kl)^2)].

The second coefficient tends to l^3/12 and expands as
l^3*(1/12-q^2/240+q^4/10080-q^6/725760+q^8/79833600-...).
Thus the implemented midpoint mass and small-q evaluation are consistent.
Every value and derivative uses the same left IVP and sqrt(total mass).
There is no division by a sampled value and therefore no nodal singularity.
At s=0 this sampler returns a normalized linear IVP, not a DD eigenmode.

For the Green function use phi(0)=0, phi'(0)=1, and right data psi(L)=0,
psi'(L)=-1 for D, or psi(L)=1, psi'(L)=0 for N. Continuity and the derivative
jump -1 give G=-phi(min(x,y))*psi(max(x,y))/W, with
W=phi*psi'-phi'*psi. At L, -W is phi(L) or phi'(L), respectively. This proves
the coordinate-order formula, the permutation/duplicate identities and the
endpoint boundary conditions. The inverse is with respect to Lebesgue source
measure; equivalently the weighted resolvent acts by integration against rho.
Since there is a left Dirichlet condition, the energy form is coercive for all
mu<=0 under either right condition. Those parameters are not spectral poles.
The floating implementation may explicitly reject overflow and unresolved
positive poles; this is not an interval certificate. Only normalized sampling
has the documented endpoint roundoff snap; Green and unnormalized propagation
retain strict coordinate domains.

For the full DD interface derivative, normalize integral rho*u^2=1 and let
s_i=rho(x_i+)-rho(x_i-). Moving x_i gives rho_i=-s_i*delta_x_i. Differentiating
the weak eigenvalue equation, then projecting on u and on every other mode,
gives a_i=a*s_i*u(x_i)^2 and

<dot u_i,u_l>_rho=-a*s_i*u(x_i)*u_l(x_i)/(lambda_l-a), l != n.

Differentiating the mass gives <dot u_i,u>_rho=s_i*u(x_i)^2/2.
Therefore at a fixed point x,

dot u_i(x)=s_i*u(x_i)^2*u(x)/2-a*s_i*u(x_i)*Gtilde_a(x,x_i).

These point pairings are legitimate: point evaluation is continuous on H0^1;
u_l/sqrt(lambda_l) is an energy orthonormal basis; Bessel and Cauchy-Schwarz
give absolute convergence of the reduced kernel at fixed x,y. Differentiation
can also be obtained locally from the finite transfer equation and its simple
secular root. The spatial derivative of the mode is continuous at each moving
interface, so the observation derivative has no one-sided ambiguity.

With a=lambda_n, b=lambda_(n+1), f_j=a*u_j^2-b*v_j^2 and F_j=f_j/b, the result is

J_ji=delta_ji*f'_j/b+s_i/b*(2*a*u_i^2*u_j^2-2*b*v_i^2*v_j^2-f_j*v_i^2
                           -2*a^2*u_i*u_j*Gtilde_a+2*b^2*v_i*v_j*Gtilde_b).

The term -f_j*v_i^2 comes from differentiating 1/b. At f=0, the first three
terms reduce to 2*w_i*w_j*(b-a)/(a*b), w_i=a*u_i^2=b*v_i^2. Subtraction gives
s_i/b^2*(a*u_i^2*f_j+2*a*u_j^2*f_i-f_i*f_j). The current shared jacobian_terms
has exactly these row/column orientations and jump signs. It is used by all
three repaired entrypoints. Infinite Green sums justify the analytic identity;
the finite sums in the software remain approximations without a certified tail.
For R=1 the jumps vanish, but the moving-observation diagonal remains; K with
division by jumps is not defined there, and sector_data excludes R<=1.

For palindromic densities, F(1-Px)=P*F(x) implies JP=-PJ at symmetric x, even
without stationarity. Thus the Jacobian has reversal-even/odd CROSS blocks.
At a stationary point grad D=-diag(s)*b*F gives Hess D=-b*diag(s)*J. In the
alternating family with equal jump magnitudes, K=diag(1/s)*J is symmetric and
commutes with P. Adjacent-mode parity makes eps reverse sign, so conjugation
by S=diag(eps) swaps its parity subspaces. With E=diag(eps[:n]), the relations
KpOdd=E*Ke*E and KpEven=E*Ko*E hold. They do not identify raw Ko with KpOdd.

The DD/DN phase targets are n*pi and (n-1/2)*pi. The positive interface scaling
preserves half-turns and the physical transfer residual and interior zero count
independently check those indices. HalfSpectrum binds the exact represented
geometry, boundary and prefix; the reduced finite sum deletes only its validated
one-based pole mode. Floating bracket radii remain diagnostics, not certified
error bounds.

## Execution and boundaries

verify_351b4411.py compiles the listed source bytes directly, without reading
bytecode caches or importing working-tree project modules. The absent
reflection_seeds module has only fail-closed sentinels; none is invoked.
Independent reference calculations use 65-digit physical transfer, direct
Gauss quadrature, a secular sign scan with physical zero counts, and
complex-step implicit differentiation. Green reference values solve the two
continuity/jump matching equations instead of calling the formula under test.
Stationary seeds come from the constant-density switching equation followed
by continuation to R=4; no branch table is read. The independent oracle verifies
the residual at every resulting point.

The final ordinary and optimized JSON reports record the checks, interpreter,
source-module paths, script hash and finite errors. Initial infrastructure
failures are retained separately: an isolated Python import lacked user-site
packages, a syntax error in the reviewer's matching-system expression was fixed,
and random/equal-width seeds did not find the n=3 band point before the reviewer
switched to constant-density continuation. These are not source defects.

Unexecuted: unadapted imports and table-driven original CLIs (missing
reflection_seeds.py and op03_gap_table.json), unsupplied downstream callers,
author historical logs, HEAD/baseline comparisons, uniform tail certification,
interval arithmetic, Lean, and global G1/M3/KP statements. Static-impact metadata
is not independent runtime coverage or proof of equality to an unsupplied HEAD.
