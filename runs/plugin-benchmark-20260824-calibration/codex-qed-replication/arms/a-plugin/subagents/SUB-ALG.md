# SUB-ALG — exact algebraic reduction and root proof

**Status:** `PROVED` for the assigned algebraic claim and, in fact, for the scalar root-location and lifting obligations reached by this route. This artifact does not claim global completion, because the independent audit obligation is outside this subtask.

## 1. Polynomial reduction

Fix an integer `n>=1` and `s>1`, and abbreviate

\[
 r=s^{-1}\in(0,1),\qquad a=\frac{s+s^{-1}}2>1,
 \qquad z=(a+1)x^2-a.
\]

Define polynomials `U_m` by

\[
 U_{-1}(z)=0,\quad U_0(z)=1,\quad
 U_{m+1}(z)=2zU_m(z)-U_{m-1}(z)\quad(m\geq 0).
\]

For the matrix `C=C_s(y)`, direct expansion gives

\[
\begin{aligned}
\det C
&=(c^2-s^{-1}q^2)(c^2-sq^2)
 +(1+s^{-1})(1+s)c^2q^2\\
&=c^4+q^4+2c^2q^2=1,
\end{aligned}
\]

and

\[
 \frac{\operatorname {tr}C}{2}
 =c^2-\frac{s+s^{-1}}2q^2
 =(a+1)c^2-a.
\]

Thus, with `z=(a+1)c^2-a`, the elementary two-by-two characteristic identity is

\[
 C^2-2zC+I=0.
\]

Induction using the defining recurrence of `U_m` therefore proves, including the case `n=1`,

\[
 C^n=U_{n-1}(z)C-U_{n-2}(z)I. \tag{1}
\]

Moreover,

\[
\begin{aligned}
 (EC)_{12}
 &=c(1+s^{-1})cq+q(c^2-sq^2)\\
 &=q\bigl((s+2+s^{-1})c^2-s\bigr)\\
 &=q(2z+s^{-1}),
\end{aligned}
\]

whereas `E_{12}=q`. Taking the `(1,2)` entry of (1) gives

\[
\begin{aligned}
G_{n,s}(y)
 &=q\bigl((2z+s^{-1})U_{n-1}(z)-U_{n-2}(z)\bigr)\\
 &=q\bigl(U_n(z)+s^{-1}U_{n-1}(z)\bigr). \tag{2}
\end{aligned}
\]

Consequently the required polynomial extension is exactly

\[
 \boxed{\quad Q_{n,s}(x)=P_{n,r}((a+1)x^2-a),\qquad
 P_{n,r}(z)=U_n(z)+rU_{n-1}(z).\quad} \tag{3}
\]

Indeed, for `x in (-1,1)` and `y=arccos x`, one has
`sin y=sqrt(1-x^2)>0`, so (2) divided by `sin y` is precisely the
quotient in the problem statement. Hence (3) really extends that
quotient and is not merely a formally related polynomial.

The recurrence shows inductively that `U_m` has degree `m` and leading
coefficient `2^m` for every `m>=0`. Hence `P_{n,r}` has exact degree `n`
and leading coefficient `2^n`. Since `a+1>0`, (3) has exact degree

\[
 \boxed{\deg Q_{n,s}=2n}
\]

and leading coefficient `2^n(a+1)^n`.

## 2. Exact scalar root theorem

We now prove self-containedly that `P_{n,r}` has exactly `n` distinct,
hence simple, roots, all in `(-1,1)`.

For `0<theta<pi`, induction in the recurrence, using

\[
2\cos\theta\sin((m+1)\theta)-\sin(m\theta)
=\sin((m+2)\theta),
\]

gives

\[
 U_m(\cos\theta)=\frac{\sin((m+1)\theta)}{\sin\theta}. \tag{4}
\]

Also, induction directly at the endpoints gives

\[
 U_m(1)=m+1,\qquad U_m(-1)=(-1)^m(m+1). \tag{5}
\]

Put

\[
 \tau_j=\cos\frac{j\pi}{n+1}\qquad(0\leq j\leq n+1).
\]

Then `1=tau_0>tau_1>...>tau_{n+1}=-1`. For `1<=j<=n`,
(4) yields

\[
 U_n(\tau_j)=0,
 \qquad
 U_{n-1}(\tau_j)=(-1)^{j+1},
\]

and hence

\[
 P_{n,r}(\tau_j)=r(-1)^{j+1}. \tag{6}
\]

At the left endpoint, (5) gives

\[
 P_{n,r}(-1)=(-1)^n\bigl((n+1)-rn\bigr), \tag{7}
\]

whose parenthesis is strictly positive (indeed it is greater than `1`)
because `0<r<1`. Equations (6)–(7), the strict ordering of the `tau_j`,
and the intermediate value theorem exhibit one root in every one of the
following `n` pairwise disjoint intervals:

\[
 (-1,\tau_n),\qquad
 (\tau_{j+1},\tau_j)\quad(1\leq j\leq n-1). \tag{8}
\]

(For `n=1`, only the first interval occurs.) Thus a degree-`n`
polynomial has at least `n` distinct real roots in `(-1,1)`. A nonzero
degree-`n` polynomial has at most `n` distinct roots, by repeated use of
the factor theorem. Therefore these are exactly all its roots. Their
number already equals the degree, so every one has multiplicity exactly
one. This proves both location and simplicity without an unproved
interlacing assertion.

## 3. Lifting all roots and preserving simplicity

Let `zeta` be any root of `P_{n,r}`. By Section 2, `-1<zeta<1`. Solving

\[
 (a+1)x^2-a=\zeta
\]

gives exactly the two real solutions

\[
 x=\mathord\pm\sqrt{\frac{\zeta+a}{a+1}}. \tag{9}
\]

Because `a>1` and `-1<zeta<1`, their squared value lies strictly between
`(a-1)/(a+1)>0` and `1`. Thus both solutions in (9) lie in `(-1,1)` and
are nonzero. Different scalar roots have different squared values, so
the `n` scalar roots produce exactly `2n` distinct roots of `Q`.
Conversely, (3) shows that every root of `Q` arises this way. Hence there
are no additional roots.

At any such root `x`, differentiation of (3) gives

\[
 Q'_{n,s}(x)=P'_{n,r}(z)\,2(a+1)x\ne0,
\]

because the scalar root is simple and `x\ne0`. Thus all `2n` roots of
`Q` in `(-1,1)` are simple.

Finally, `y -> cos y` is a bijection from `(0,pi)` onto `(-1,1)`, and
`sin y` never vanishes there. Therefore (2) gives a bijection between
the roots of `G` in `(0,pi)` and those of `Q` in `(-1,1)`. More
explicitly, at a root `y_0`,

\[
 G'_{n,s}(y_0)
 =-\sin^2(y_0)Q'_{n,s}(\cos y_0)\ne0. \tag{10}
\]

Thus the reduction itself proves that the `2n` lifted interior roots are
all the interior roots and all are simple.

## 4. Required special audits

### `n=1`

Here `P_{1,r}(z)=2z+r`, and (3) reduces to

\[
 Q_{1,s}(x)=(s+2+s^{-1})x^2-s.
\]

Its roots are

\[
 x=\mathord\pm\frac{s}{s+1},
\]

which are two distinct simple roots in `(-1,1)` for every `s>1`.

### `y=0` and `y=pi`

At either endpoint, `q=0` and `C_s(y)=I`; hence `G=0` directly. These
zeros are excluded from the open-interval count. They cannot conceal a
degeneracy in the factorization: at `x=1` or `x=-1`, one has `z=1` and

\[
 Q_{n,s}(\mathord\pm1)=P_{n,r}(1)=(n+1)+rn>0.
\]

Thus the endpoint zeros come only from the displayed `sin y` factor
(and are simple as endpoint zeros), but are not counted.

### `y=pi/2`

Here

\[
 E=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
 C_s=\begin{pmatrix}-s^{-1}&0\\0&-s\end{pmatrix}.
\]

It follows directly that

\[
 G_{n,s}(\pi/2)=(-s)^n\ne0.
\]

Thus the vertex `x=0` of the quadratic substitution is not a root, in
agreement with (9).

### Boundary `s=1` (equivalently `R=1`)

Although excluded by the main hypotheses, this case is nondegenerate.
When `s=1`, direct substitution gives `C_1(y)=E(2y)`. The elementary
matrix multiplication identity `E(alpha)E(beta)=E(alpha+beta)` then
gives

\[
 M_{n,1}(y)=E((2n+1)y),\qquad
 G_{n,1}(y)=\sin((2n+1)y).
\]

Its open-interval zeros are exactly

\[
 y=\frac{k\pi}{2n+1}\qquad(1\leq k\leq 2n),
\]

and each is simple because its derivative there is
`(2n+1)(-1)^k`, which is nonzero.

## 5. Exact gap and scope

There is no remaining formula, exact-degree, scalar-root-location,
lifting, or simplicity gap in this route. The first obligation not
performed here is the separately assigned independent adversarial audit
of the integrated proof (`O5`); this is an audit-scope gap, not a
mathematical gap found in the algebraic argument.
