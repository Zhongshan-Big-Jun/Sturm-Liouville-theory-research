# Proof

Let \(s=\sqrt R>1\) and
\[
t=\frac1{(n+1)s+n}.
\]
Thus the interval consists, from left to right, of \(n+1\) blocks of density \(1\) and length \(st\), alternating with \(n\) blocks of density \(s^2=R\) and length \(t\). Their total length is
\((n+1)st+nt=1\).

## 1. The transfer matrix and the characteristic function

Fix \(\lambda>0\) and put \(y=\sqrt\lambda\,st\). For a solution of
\[
-u''=\lambda\rho u,
\]
use the normalized state vector
\[
X(x)=\binom{u(x)}{u'(x)/\sqrt\lambda}.
\]
On a block on which \(\rho=a^2\) is constant, direct solution of
\(u''+\lambda a^2u=0\) shows that propagation through a length \(\ell\) is represented by
\[
T_{a,\ell}(\lambda)=
\begin{pmatrix}
\cos(a\sqrt\lambda\,\ell)&a^{-1}\sin(a\sqrt\lambda\,\ell)\\
-a\sin(a\sqrt\lambda\,\ell)&\cos(a\sqrt\lambda\,\ell)
\end{pmatrix}.
\]
The solution and its derivative are continuous at every interface, so these block matrices may be multiplied in spatial order.

Both types of blocks have phase \(y\): on a density-\(1\) block it is
\(\sqrt\lambda\,st=y\), while on a density-\(s^2\) block it is
\(s\sqrt\lambda\,t=y\). Consequently their matrices are
\[
L(y)=\begin{pmatrix}c&q\\-q&c\end{pmatrix}=E(y),
\qquad
H_s(y)=\begin{pmatrix}c&s^{-1}q\\-sq&c\end{pmatrix}.
\]
A direct multiplication gives
\[
H_s(y)L(y)=
\begin{pmatrix}
c^2-s^{-1}q^2&(1+s^{-1})cq\\
-(1+s)cq&c^2-sq^2
\end{pmatrix}=C_s(y).
\]
Because the first and last blocks have density \(1\), the full propagation matrix is
\[
L(H_sL)^n=E(y)C_s(y)^n=M_{n,s}(y).
\]

Let \(u(x,\lambda)\) be the uniquely normalized solution with
\(u(0,\lambda)=0\) and \(u'(0,\lambda)=1\), and set
\(F(\lambda)=u(1,\lambda)\). Its initial normalized state is
\((0,1/\sqrt\lambda)^T\), and hence
\[
F(\lambda)=\frac{G_{n,s}(y)}{\sqrt\lambda},
\qquad y=\sqrt\lambda\,st. \tag{1}
\]
Therefore, for \(\lambda>0\), \(G_{n,s}(y)=0\) if and only if \(\lambda\) is a Dirichlet eigenvalue.

## 2. Exact eigenvalue count below \(y=\pi\)

We use the following regular Sturm oscillation theorem.

**Sturm oscillation theorem.** Let \(w\) be a real, integrable function on a finite interval \([a,b]\), bounded above and bounded below by a positive constant. For the regular Dirichlet problem
\[
-v''+qv=\mu wv,\qquad v(a)=v(b)=0,
\]
with real integrable \(q\), the eigenvalues form a strictly increasing sequence
\(\mu_1<\mu_2<\cdots\) tending to \(+\infty\), and an eigenfunction for \(\mu_k\) has exactly \(k-1\) zeros in \((a,b)\). Each zero is counted once; in fact, every zero of a nonzero solution is simple. Under separated Dirichlet boundary conditions each eigenspace is one-dimensional.

Here \(q=0\) and \(w=\rho\) is positive and piecewise constant, with
\(1\leq \rho\leq R\), so all hypotheses hold. The eigenvalues are positive: multiplying the equation by an eigenfunction and integrating by parts gives
\[
\int_0^1 |u'|^2\,dx=\lambda\int_0^1\rho |u|^2\,dx,
\]
whose left side is positive for every nonzero Dirichlet function.

Define
\[
\lambda_* = \left(\frac{\pi}{st}\right)^2,
\]
so that \(y=\pi\). At this value, both layer matrices equal \(-I\):
\(L(\pi)=H_s(\pi)=-I\). Starting with \(u(0)=0\) and nonzero derivative, the value of \(u\) is therefore zero at every interface and at \(x=1\), while its derivative remains nonzero and merely changes sign from block to block. On each open block the solution is a nonzero constant multiple of a sine whose phase runs strictly from \(0\) to \(\pi\); hence it has no zero inside that block. There are exactly \(2n\) internal interfaces, so this eigenfunction has exactly \(2n\) zeros in \((0,1)\).

The Sturm oscillation theorem now identifies \(\lambda_*\) as the
\((2n+1)\)-st Dirichlet eigenvalue. It follows that there are exactly \(2n\) Dirichlet eigenvalues in \((0,\lambda_*)\). The change of variables
\[
\lambda=\left(\frac{y}{st}\right)^2
\]
is a strictly increasing bijection from \((0,\pi)\) to
\((0,\lambda_*)\). In view of (1), \(G_{n,s}\) therefore has exactly
\(2n\) zeros in \((0,\pi)\).

## 3. Simplicity of all the zeros

It remains to verify analytic simplicity, which is stronger than merely saying that each Dirichlet eigenspace is one-dimensional. The normalized solution \(u(x,\lambda)\) is differentiable in \(\lambda\); for example, this follows directly by differentiating its Volterra integral equation
\[
u(x,\lambda)=x-\lambda\int_0^x (x-r)\rho(r)u(r,\lambda)\,dr.
\]
Write \(\dot u=\partial u/\partial\lambda\). Differentiating
\(u''+\lambda\rho u=0\) gives
\[
\dot u''+\rho u+\lambda\rho\dot u=0.
\]
Consequently the Lagrange identity is
\[
\bigl(u'\dot u-u\dot u'\bigr)'=\rho u^2. \tag{2}
\]
The initial data are independent of \(\lambda\), so
\(\dot u(0)=\dot u'(0)=0\). If \(\lambda_k\) is an eigenvalue, then
\(u(1,\lambda_k)=0\), and integration of (2) yields
\[
u'(1,\lambda_k)F'(\lambda_k)
=\int_0^1\rho(x)u(x,\lambda_k)^2\,dx>0. \tag{3}
\]
Also \(u'(1,\lambda_k)\ne0\), since otherwise uniqueness for the initial-value problem at \(x=1\) would force \(u\equiv0\). Thus (3) implies
\(F'(\lambda_k)\ne0\).

At the corresponding \(y_k\in(0,\pi)\), differentiate (1). Since
\(G_{n,s}(y_k)=0\),
\[
F'(\lambda_k)
=\frac{G_{n,s}'(y_k)}{\sqrt{\lambda_k}}
\frac{dy}{d\lambda}(\lambda_k).
\]
Here \(dy/d\lambda=st/(2\sqrt\lambda)>0\). Therefore
\(G_{n,s}'(y_k)\ne0\), proving that every one of the \(2n\) zeros is simple.

## 4. Required special-case audits

**The case \(n=1\).** Direct multiplication gives
\[
G_{1,s}(y)
=q\left[\left(2+s^{-1}\right)c^2-sq^2\right]
=q\left[\left(s+2+s^{-1}\right)c^2-s\right].
\]
Because \(s+2+s^{-1}=(s+1)^2/s\), its two interior zeros are
\[
y=\arccos\frac{s}{s+1},
\qquad
y=\pi-\arccos\frac{s}{s+1}.
\]
They are distinct and simple, in agreement with the general result.

**The endpoint \(y=0\).** Every layer matrix is \(I\), so
\(G_{n,s}(0)=0\). Differentiating the product at zero, where all other factors are \(I\), gives
\[
G_{n,s}'(0)=(n+1)+\frac ns>0,
\]
because there are \(n+1\) low-density factors with upper-right derivative \(1\) and \(n\) high-density factors with upper-right derivative \(1/s\). This endpoint zero is simple but is not counted. It is also not a positive Dirichlet eigenvalue; it appears because (1) contains the normalizing factor \(\sqrt\lambda\).

**The endpoint \(y=\pi\).** As used above, every layer matrix is \(-I\), so
\(G_{n,s}(\pi)=0\). There are \(2n\) other factors in every term obtained by differentiating the product, and their product is \(I\). Hence
\[
G_{n,s}'(\pi)=-\left((n+1)+\frac ns\right)<0.
\]
Thus this endpoint zero is also simple and is not included in the count on the open interval.

**The midpoint \(y=\pi/2\).** At this point
\[
H_sL=\begin{pmatrix}-s^{-1}&0\\0&-s\end{pmatrix},
\]
so
\[
G_{n,s}(\pi/2)=(-s)^n\ne0.
\]
In particular the midpoint is never one of the counted zeros.

**The boundary value \(R=1\).** Here \(s=1\) and the two layer matrices coincide with \(E(y)\). Therefore
\[
M_{n,1}(y)=E(y)^{2n+1}=E((2n+1)y),
\qquad
G_{n,1}(y)=\sin((2n+1)y).
\]
Its interior zeros are \(k\pi/(2n+1)\), \(k=1,\ldots,2n\), and all are simple. Thus the same count persists at the separately audited boundary \(R=1\).

We have proved that for every \(n\ge1\) and every \(R>1\), the function
\(G_{n,s}\) has exactly \(2n\) zeros in \((0,\pi)\), all simple.
