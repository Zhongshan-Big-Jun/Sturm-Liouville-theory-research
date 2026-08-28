# Closure gate

## Exact first open claim

`O1`: For the Krein realization of \(-D^2\), the closed form on \(H^1[-1,1]\) is
\[
a_0(f,f)=\int_{-1}^1|f'|^2-\tfrac12|f(1)-f(-1)|^2,
\]
it is nonnegative, and its nullspace is exactly the affine functions
\(\operatorname{span}\{1,x\}\).

## Coordinator direct attempt

For \(f\in H^1(I)\), \(\Delta f=\int_{-1}^1f'(x)\,dx\).  Hence
\[
 |\Delta f|^2\le 2\int_{-1}^1|f'|^2
\]
by Cauchy--Schwarz, so \(a_0(f,f)\ge0\).  Equality holds exactly when
\(f'\) is a.e. constant, hence exactly when \(f\) is affine.  Therefore
\(\ker a_0=\operatorname{span}\{1,x\}\).

For \(f\in H^2(I)\), integration by parts gives
\[
 a_0(f,g)=\langle-f'',g\rangle+
 (f'(1)-\Delta f/2)\overline{g(1)}+
 (-f'(-1)+\Delta f/2)\overline{g(-1)}.
\]
The endpoint trace map \(H^1(I)\to\mathbb C^2\) is onto.  Thus the boundary
term vanishes for every \(g\in H^1\) exactly when both Krein equations hold.
This identifies the operator represented by the form as the stated \(K_0\).
The standard first representation theorem (closed, densely defined,
nonnegative sesquilinear form) then yields the associated nonnegative
self-adjoint operator and \(D(K_0^{1/2})=D(a_0)=H^1(I)\).  The form is closed:
the norm \((a_0(f,f)+\|f\|_2^2)^{1/2}\) is equivalent to the \(H^1\) norm
(for example, decompose into the affine kernel and its \(L^2\)-orthogonal
complement and use the one-dimensional Poincare inequality on the complement).

## Cheapest falsification probe

Exact probes: \(a_0(1,1)=0\), \(a_0(x,x)=2-2=0\), while
\(a_0(x^2,x^2)=\int_{-1}^1 4x^2\,dx=8/3>0\).  The two independent trace
choices \((g(-1),g(1))=(0,1)\) and \((1,0)\) recover, respectively,
\(f'(1)=\Delta f/2\) and \(f'(-1)=\Delta f/2\); neither endpoint condition
can be dropped.  The equality case in Cauchy--Schwarz rules out every
non-affine zero-form probe, not only the tested quadratic.

## Gate decision

`CLOSED`: O1 is proved by the displayed calculation and equality audit.

## Next decision-changing action

Prove the recursive power-domain criterion O2, then use orthogonality plus the
strict affine-kernel statement to decide O3E and O3O.  These are parity-distinct
mechanisms and can change Q1.
