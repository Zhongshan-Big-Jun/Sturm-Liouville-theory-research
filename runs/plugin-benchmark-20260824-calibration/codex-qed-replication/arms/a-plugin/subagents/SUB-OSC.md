# SUB-OSC: exact oscillation proof

**Status:** `PROVED` for the assigned Route B subclaim. This is not a claim that the coordinator's full obligation graph, in particular its independent-audit node, is complete.

## Claim proved

For every integer \(n\geq 1\) and every \(s>1\), the function \(G_{n,s}\) has exactly \(2n\) zeros in \((0,\pi)\), and every one of them is simple. The argument below is independent of a polynomial reduction.

## 1. Exact realization as a Sturm--Liouville shooting function

For \(a>0\), set
\[
A_a(y)=\begin{pmatrix}
\cos y&a^{-1}\sin y\\
-a\sin y&\cos y
\end{pmatrix}.
\]
Then \(A_1(y)=E(y)\), and direct multiplication gives
\[
A_s(y)A_1(y)=
\begin{pmatrix}
c^2-s^{-1}q^2&(1+s^{-1})cq\\
-(1+s)cq&c^2-sq^2
\end{pmatrix}=C_s(y).
\]
Consequently
\[
M_{n,s}(y)=A_1(y)\bigl(A_s(y)A_1(y)\bigr)^n. \tag{1}
\]

Put \(L=2n+1\). On \([0,L]\), define the positive piecewise-constant function
\[
p(x)=\begin{cases}
1,&j\text{ even},\\
s,&j\text{ odd},
\end{cases}\qquad j<x<j+1,\quad j=0,\ldots,2n.
\]
At integer interfaces impose continuity of \(u\) and of the flux \(z=pu'\). Consider
\[
-(pu')'=\lambda p u,\qquad u(0)=0,\qquad (pu')(0)=1. \tag{2}
\]
Write its solution as \(u(x,\lambda)\), its flux as \(z(x,\lambda)=p(x)u'(x,\lambda)\), and its terminal shooting function as
\[
F(\lambda)=u(L,\lambda).
\]
On a unit interval on which \(p=a\), for \(y>0\) and \(\lambda=y^2\), propagation of the state \((u,z/y)^T\) is exactly multiplication by \(A_a(y)\). Since transfer matrices compose from right to left, the left-to-right coefficient sequence \(1,s,1,s,\ldots,s,1\) has total transfer (1).

The column defining \(G\) starts from \((u,z/y)=(0,1)\), whereas (2) starts from \((u,z/y)=(0,1/y)\). Linearity therefore proves the exact identity
\[
G_{n,s}(y)=yF(y^2),\qquad y>0. \tag{3}
\]
Thus it is enough to count and prove simplicity of the zeros of \(F\) in \((0,\pi^2)\).

## 2. Self-contained shooting-angle lemma

The following special Sturm lemma is proved here, so no external oscillation theorem is being invoked.

**Lemma.** Let \(p\) be a positive piecewise-constant function on a finite interval \([0,L]\), with finitely many jumps, and impose continuity of \(u\) and \(pu'\) at each jump. For the solution of (2), define a continuous lifted angle \(\theta(x,\lambda)\) by
\[
u=r\sin\theta,\qquad z=r\cos\theta,\qquad r>0,\qquad \theta(0,\lambda)=0.
\]
Then:

1. \(\theta\) is strictly increasing in \(x\) for every \(\lambda\geq0\);
2. for every fixed \(x>0\), \(\theta(x,\lambda)\) is strictly increasing in \(\lambda\geq0\);
3. a terminal Dirichlet value \(F(\lambda)=0\) is equivalent to \(\theta(L,\lambda)\in\pi\mathbb Z\), and every such zero of \(F\) is simple as a zero in \(\lambda\).

**Proof.** The vector \((u,z)\) never vanishes: if it did at one point, uniqueness on each constant-coefficient interval, propagated across the flux-continuity interfaces, would contradict \((u(0),z(0))=(0,1)\). Hence the lifted angle exists globally.

Away from interfaces, the first-order equations are
\[
u'=z/p,\qquad z'=-\lambda p u.
\]
Therefore
\[
\theta_x=\frac{zu'-uz'}{u^2+z^2}
=\frac{z^2/p+\lambda p u^2}{u^2+z^2}. \tag{4}
\]
For \(\lambda>0\) the numerator cannot vanish; for \(\lambda=0\), the solution has \(z\equiv1\), so it also cannot vanish. The state and angle are continuous at interfaces. This proves (1).

For parameter monotonicity, put a dot over a quantity to denote \(\partial_\lambda\), and set
\[
K=z\dot u-u\dot z.
\]
The initial data are independent of \(\lambda\), so \(K(0)=0\). On every constant-coefficient interval, differentiating the system gives
\[
K'=p u^2.
\]
Both \((u,z)\) and their \(\lambda\)-derivatives are continuous across the interfaces, so integration over all pieces yields
\[
K(x)=\int_0^x p(t)u(t,\lambda)^2\,dt>0\qquad(x>0). \tag{5}
\]
The strict inequality follows because the nonzero solution cannot vanish identically on an interval. From the polar representation,
\[
\theta_\lambda(x,\lambda)=\frac{z\dot u-u\dot z}{u^2+z^2}
=\frac{K(x)}{u^2+z^2}>0, \tag{6}
\]
which proves (2).

Finally, \(F=0\) exactly when \(u(L)=0\), hence exactly when the lifted angle is a multiple of \(\pi\). At such a point, \(z(L)\ne0\), and (5) reduces to
\[
K(L)=z(L)\,\partial_\lambda u(L,\lambda)>0.
\]
Thus \(\partial_\lambda F(\lambda)\ne0\), proving (3). \(\square\)

All differentiations used above are justified directly interval by interval: on each piece the solution is an elementary matrix exponential depending smoothly on \(\lambda\), and the finite product and interface matching preserve that differentiability.

## 3. Exact angle calibration and root count

At \(\lambda=0\), equation (2) gives \(z\equiv1\) and
\[
u(L,0)=\int_0^L\frac{dx}{p(x)}=(n+1)+\frac ns>0.
\]
Thus, with the lift fixed by \(\theta(0,0)=0\) and using its strict spatial increase,
\[
0<\theta(L,0)<\frac\pi2. \tag{7}
\]

At \(\lambda=\pi^2\), propagation across any unit interval of coefficient \(a\) is \(A_a(\pi)=-I\) in the normalized state. Starting at a zero of \(u\), the solution on the interior of that interval is a nonzero constant multiple of \(\sin(\pi(x-j))\); hence it has no zero inside the interval, while its flux reverses sign at the other endpoint. Formula (4) says that the lifted angle increases, so it increases by exactly \(\pi\) on each of the \(L=2n+1\) intervals. Consequently
\[
\theta(L,\pi^2)=(2n+1)\pi. \tag{8}
\]

By (6), \(\lambda\mapsto\theta(L,\lambda)\) is continuous and strictly increasing. Equations (7)--(8) show that, for \(0<\lambda<\pi^2\), it meets precisely the multiples
\[
\pi,2\pi,\ldots,2n\pi,
\]
each exactly once. The lemma therefore gives exactly \(2n\) zeros of \(F\) in \((0,\pi^2)\), all simple. Identity (3) bijects them with the zeros of \(G_{n,s}\) in \((0,\pi)\). If \(F(\lambda_0)=0\) and \(y_0=\sqrt{\lambda_0}>0\), then
\[
G'_{n,s}(y_0)=2y_0^2F'(\lambda_0)\ne0,
\]
so simplicity is preserved. This proves the assigned claim.

## 4. Required audits

### \(n=1\)

Direct multiplication gives
\[
G_{1,s}(y)=\sin y\left[\left(2+\frac1s\right)\cos^2y-s\sin^2y\right].
\]
In \((0,\pi)\), the bracket vanishes exactly when
\[
\tan^2y=\frac{2s+1}{s^2}.
\]
There is one solution in each of \((0,\pi/2)\) and \((\pi/2,\pi)\), and both are simple because at a root \(\sin y\cos y\ne0\) and the derivative of the bracket is
\[
-2\sin y\cos y\left(2+\frac1s+s\right)\ne0.
\]

### \(y=0\) and \(y=\pi\)

For every \(a>0\), \(A_a(0)=I\) and \(A_a(\pi)=-I\). Hence
\[
M_{n,s}(0)=I,\qquad M_{n,s}(\pi)=(-I)^{2n+1}=-I,
\]
and \(G(0)=G(\pi)=0\). These endpoint zeros are excluded from the open-interval count. More precisely, (3) and the value of \(F(0)\) above show that the zero at \(0\) is simple, while the lemma at \(\lambda=\pi^2\) shows that the zero at \(\pi\) is also simple.

### \(y=\pi/2\)

Here
\[
C_s(\pi/2)=\operatorname{diag}(-s^{-1},-s),
\]
so
\[
G_{n,s}(\pi/2)=(-s)^n\ne0.
\]
Thus the midpoint is never an unaccounted multiple root (indeed, never a root).

### Boundary \(R=1\), equivalently \(s=1\)

Although excluded from the claim, when \(s=1\) one has \(C_1(y)=E(y)^2\), and hence
\[
M_{n,1}(y)=E(y)^{2n+1}=E((2n+1)y),\qquad
G_{n,1}(y)=\sin((2n+1)y).
\]
Its open-interval zeros are exactly \(k\pi/(2n+1)\), \(k=1,\ldots,2n\), all simple.

## Exact gap and failure mechanism

- **First unresolved obligation within SUB-OSC:** none. Counting, location to \((0,\pi)\), and simplicity are all proved exactly.
- **Global caveat:** this artifact does not discharge the coordinator-only independent audit or any separately required polynomial-extension claim; the oscillation proof does not need a polynomial formulation.
- **Failure mechanism:** none for this route. The key mechanism is that \(y=\pi\) is an exactly calibrated Dirichlet state with \(2n\) internal interface nodes, while the terminal shooting angle is strictly increasing in \(\lambda=y^2\).

