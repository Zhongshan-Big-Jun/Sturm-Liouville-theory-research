# Round10: spectral identity and reflection-sector contracts

Scope: `-y''=omega^2 rho y` on `[0,L]`, Dirichlet endpoints, finitely many
strictly positive finite block lengths and densities. The mathematical algorithm
below is exact; its NumPy/mpmath implementation is numerical, with failure guards,
and supplies no outward-rounded interval certificate. This document is an author
derivation to be independently reviewed, not an acceptance receipt.

## S1. What failed

The actual original module, imported without its main routine, returns
`3.2671480773046255` as its first frequency for blocks
`[(.02,10000),(.96,1),(.02,10000)]`. The supplied rational Taylor certificates
place four distinct lower roots in the four reported brackets. The true first
frequency also satisfies `omega_1<=pi` by testing `sin(pi*x)` when `rho>=1`.
Small secular residuals, local high-precision refinement and ordered positive
lists therefore do not identify an eigenvalue's index. Historical outputs remain
unchanged; this counterexample does not by itself show the default R=4 tables
were wrong.

## S2. Lifted phase and exact indexing

Use the shooting solution `y(0)=0`, `y'(0)=1` and, for `omega>0`, write
`omega*y=r*sin(theta)`, `y'=r*cos(theta)`, with `r>0` and the continuous spatial
lift `theta(0)=0`. Simultaneous vanishing of `y,y'` is impossible by uniqueness.
Direct differentiation on each block gives

`theta_x = omega*(cos(theta)^2 + rho*sin(theta)^2)`.

Both physical coordinates are continuous at an interface, so is the lift.
This piecewise smooth scalar ODE has a unique global solution. Its right side is
positive, locally Lipschitz in theta and smooth in omega. Parameter derivatives
can be propagated across the finitely many fixed interfaces. If
`f(x,theta)=cos(theta)^2+rho(x)*sin(theta)^2`, then `z=partial_omega theta`
satisfies `z_x=f+omega*f_theta*z`, `z(0)=0`. Thus

`z(L)=int_0^L exp(int_t^L omega*f_theta(x,theta(x)) dx)*f(t,theta(t)) dt > 0`.

Consequently `Phi(omega)=theta(L,omega)` is continuous and strictly increasing.
Set `Phi(0)=0` by continuity; the bounds
`omega*L*min(1,min rho)<=Phi(omega)<=omega*L*max(1,max rho)` also show it tends
to infinity. Each level `n*pi`, `n>=1`, has exactly one positive preimage.
The endpoint is Dirichlet exactly at such a level; each such shooting solution
is an eigenfunction. Conversely every Dirichlet eigenfunction is a nonzero
multiple of the shooting solution. Integration by parts excludes nonpositive
eigenvalues. Hence these preimages enumerate the entire spectrum in order.
The corresponding eigenfunction has exactly `n-1` interior zeros.

These are the usual oscillation variables, with a frequency-dependent positive
coordinate scaling. For background, Teschl's author-hosted preliminary edition
of *Ordinary Differential Equations and Dynamical Systems*, section 5.5,
pp.166-169, equations (5.81)-(5.92), Lemma 5.14 and Theorems 5.17-5.18, gives
continuous lifting and the zero/eigenvalue count. His `atan2(x,y)` convention is
opposite NumPy's argument order; the present definition above is explicit.
[Original source](https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf).
The finite-block scaled-phase calculation and implementation adaptation here
are written out separately; no differentiability of rho across jumps is used.

## S3. Exact propagation and brackets

For `a>0`, define the increasing lift
`g_a(m*pi+r)=m*pi+atan2(a*sin(r),cos(r))`, `0<=r<pi`.
It is continuous at the half-turn seams, fixes every multiple of pi and has
inverse `g_(1/a)`. Inside a density-c block the coordinate pair
`(omega*sqrt(c)*y,y')` rotates its angle by `omega*sqrt(c)*length`.
The outgoing reference phase is therefore

`g_(1/sqrt(c))(g_sqrt(c)(theta_in)+omega*sqrt(c)*length)`.

Keeping the integer half turns is essential: repeatedly using a principal angle
alone would lose precisely the index being repaired. The physical y and y'
are continuous at interfaces; a positive coordinate change does not create a
zero. The implementation cancels adjacent coordinate changes: it carries each local
angle forward, rotates it, then changes by `g_sqrt(c_next/c_previous)` at the
next interface. At the last endpoint it retains
`Psi=g_sqrt(c_last)(Phi)`, not Phi itself. The last positive map is independent
of omega, strictly increasing and fixes n*pi, so Psi has the same indexed
roots. This avoids ill-conditioned repeated changes through density 1 in a
constant high-density medium. No frequency scan or growing amplitude product
is used. Source development preserved an initial failing constant-density
regression (relative error about 2.64e-13 at density 1e6); this cancellation
addresses the extra coordinate roundoff rather than weakening that test.

Let `m=min rho`, `M=max rho`. Scalar ODE comparison in the density parameter
(or the weighted Dirichlet min-max principle) gives
`n*pi/(L*sqrt(M))<=omega_n<=n*pi/(L*sqrt(m))`. For the ODE comparison, at equal
theta the right-hand side increases with rho, and scalar uniqueness plus the
usual integrating-factor argument prevents an order reversal. The constant
density endpoint reaches `n*pi` exactly at `n*pi/(L*sqrt(c))`.
The code starts below every level at zero and strictly above level n at 1.125
times its upper comparison bound, then bisects **against that same n*pi**.
Overlapping comparison intervals are harmless because they are not used as
secular sign brackets. Refined brackets retain their target index and numerical
phase endpoints in the output. Refine counts too small to converge, unresolved
spatial widths, nonfinite scales, excessive winding or unresolved output roots
cause explicit errors. Arbitrary contrast at double precision is not certified.

## S4. High precision and consumers

`roots_of` keeps its calling signature and delegates to indexed enumeration;
`npts` is retained solely for source compatibility and has no algorithmic role.
`checked_roots` additionally compares the returned list to levels `1*pi,...,k*pi`.
`HighPrecisionTangent` and every finite-difference endpoint now pass their
one-based index to a safeguarded mpmath phase bisection. If a guess lies beside a
wrong mode, a comparison bracket replaces the local guess interval. The solver
never accepts an unconstrained Newton/secant root on residual alone.
High precision is a second arithmetic check of the same phase mathematics,
not an independent enumeration algorithm. The separate regression counter
propagates 70-digit physical `(y,y')`, explicitly lists the local zeros of
`A*cos(w*t)+B*sin(w*t)` and counts them at inter-eigenvalue test frequencies.
Finite nodal tests exercise the implementation but do not certify all inputs.

## R1. The geometric reflection

On 2n ordered interfaces let `J(v)=v[::-1]`. Physical reflection is
`R(x)=1-Jx`, whose derivative is `-J`. The orthogonal projectors are

`P_preserve=(I-J)/2`, `P_break=(I+J)/2`.

Since `J^2=I` and `J^T=J`, both are idempotent, their product is zero and their
sum is I. They have orthogonal ranges `Jd=-d` and `Jd=d`, respectively. At a
mirror-symmetric base `x0`,
`R(x0+t*d)=x0+t*d` in the preserve sector, while
`R(x0+t*d)=x0-t*d` in the break sector. The original assignment `v <- -Jv`
is invertible and preserves all dimensions; it is neither projector.
The older explicit concatenation `(a,-a[::-1])` already belongs to preserve.
The historical antigrid plane of that same form preserves geometric symmetry;
its failure to find asymmetric solutions supplies no off-symmetry evidence.

## R2. Feasible experiments and retained scope

At an admissible base append endpoints 0 and 1 and take widths `w=diff(x)`.
Assume every base width satisfies `w_i>h`, where h is the fixed softmax
floor. For displacement d append zero endpoint displacements and let
`delta_w=diff(d)`. For a nonnegative step magnitude,
`0 <= t < min_(delta_w_i<0) (w_i-h)/(-delta_w_i)` keeps all widths above h;
an empty minimum is positive infinity. This is a one-sided bound for `t>=0`,
not a bound on arbitrary signed t. Indeed each new width is `w_i+t*delta_w_i`:
nonnegative increments cannot violate the lower floor, and each negative
increment imposes exactly the displayed upper bound.

For an arbitrary signed step the exact feasible interval is
`max_(delta_w_i>0) (h-w_i)/delta_w_i < t < min_(delta_w_i<0) (w_i-h)/(-delta_w_i)`,
with empty maximum/minimum interpreted as negative/positive infinity. For
example, `w=(1/5,1/5,1/5,1/5,1/5)`, `d=(1,1,1,1)`, `h=1/10` requires
`-1/10<t<1/10`; the previously omitted lower restriction would incorrectly
admit `t=-3/20`, whose first width is `1/20<h`.

The seed generator uses a positive magnitude, a nonzero projected direction
and a safety fraction of the positive upper bound. Zero is feasible but is
not an exploratory seed. Verify the actual reconstructed widths,
interfaces and displacement after conversion to and from the optimization
coordinates. Reject a zero/unresolvable projection; resample only with a stated
finite bound. Do not sort or clip an infeasible seed and retain its sector label.
Record requested/used step and actual sector residual. This labels **initial
seeds** only: the unconstrained subsequent optimizer can leave that sector.

None of these program repairs proves G1', Hessian definiteness, global uniqueness
or any box-class optimum. The new left-definite domain, closure, replacement
Riesz-system and finite-interface analytic results have no dependency on the
broken scanner or mislabeled seed assignment. They are not withdrawn or claimed
to have received a new whole-proof audit here.
