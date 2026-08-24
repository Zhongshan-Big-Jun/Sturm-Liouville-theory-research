# Candidate proof

Status: candidate complete for obligations `O1`-`O4`; independent obligation `O5` remains pending.

## Theorem

For every integer `n>=1` and every `s>1` (equivalently `R=s^2>1`), the function `G_{n,s}` has exactly `2n` zeros in `(0,pi)`, and every one is simple.

## 1. Exact matrix reduction (`O1`)

Write

`r=s^{-1}`, `a=(s+r)/2`, and `z=c^2-aq^2`.

Direct expansion, using `sr=1` and `c^2+q^2=1`, gives

`det C_s=(c^2-rq^2)(c^2-sq^2)+(1+r)(1+s)c^2q^2=1`

and

`tr C_s=2c^2-(s+r)q^2=2z`.

We use only the following elementary `2x2` identity: if a `2x2` matrix `A` has trace `T` and determinant `D`, then

`A^2-TA+DI=0`.

Indeed, writing `A=[[alpha,beta],[gamma,delta]]`, expansion of the four entries proves the identity. Thus no unquoted matrix theorem is being used.

Define polynomials by

`U_{-1}(z)=0`, `U_0(z)=1`, and `U_k(z)=2zU_{k-1}(z)-U_{k-2}(z)` for `k>=1`.

The preceding matrix identity and induction on `n` give, for every `n>=1`,

`C_s^n=U_{n-1}(z)C_s-U_{n-2}(z)I`.                                      (1)

For `n=1` this is the definition of `U_{-1}`; multiplication by `C_s` and the recurrence prove the induction step.

The relevant entry of `EC_s` is

`(EC_s)_{12}=q[(2+r)c^2-sq^2]=q(2z+r)`,

where the last equality again uses `c^2+q^2=1`. Since `E_{12}=q`, equation (1) yields

`G_{n,s}(y)=q[(2z+r)U_{n-1}(z)-U_{n-2}(z)]`

and hence, by the defining recurrence,

`G_{n,s}(y)=q P_n(z)`, where `P_n(z)=U_n(z)+rU_{n-1}(z)`.                 (2)

Now take `x in (-1,1)` and `y=arccos x`. Then `q=sqrt(1-x^2)>0` and

`z=x^2-a(1-x^2)=(1+a)x^2-a`.

Consequently the quotient in the problem is exactly the restriction of the polynomial

`Q_{n,s}(x)=P_n((1+a)x^2-a)`.                                           (3)

The recurrence shows by induction that `U_k` has degree `k` and leading coefficient `2^k`. Therefore `P_n` has exact degree `n`, and (because `1+a>0`) `Q_{n,s}` has exact degree `2n`, with leading coefficient

`2^n(1+a)^n=((s+1)^2/s)^n>0`.

This proves the claimed polynomial extension rather than merely assuming it.

## 2. All roots of the scalar polynomial (`O2`)

We prove that `P_n` has exactly `n` roots, all simple and all in `(-1,1)`.

First, the recurrence and the angle-addition identity for sine imply, for `0<theta<pi`,

`U_k(cos theta)=sin((k+1)theta)/sin theta`.                              (4)

For completeness: the formula holds for `k=0,1`; the identity

`sin((k+1)theta)=2cos(theta)sin(k theta)-sin((k-1)theta)`

gives the same recurrence and therefore proves (4) by induction.

Set `F(theta)=P_n(cos theta)`, which is continuous on `[0,pi]`. The polynomial recurrence gives `U_k(1)=k+1` and `U_k(-1)=(-1)^k(k+1)`. Hence

`F(0)=n+1+rn>0`,

`F(pi)=(-1)^n[(n+1)-rn]`,                                               (5)

and the bracket in (5) is positive because `0<r<1`.

For every `j=1,...,n-1`, put `theta_j=j*pi/n`. Formula (4) gives

`U_{n-1}(cos theta_j)=0`, `U_n(cos theta_j)=(-1)^j`,

so

`F(theta_j)=(-1)^j`.                                                     (6)

Together, (5)-(6) say that the values at

`theta_j=j*pi/n`, `j=0,...,n`,

alternate in sign. This includes `n=1`, for which there are no internal mesh points and the two endpoint signs are opposite.

We use the intermediate value theorem in this exact form: if a real-valued function is continuous on `[A,B]` and its endpoint values have opposite signs, then it has a zero in `(A,B)`. Applying it to each of the `n` disjoint intervals

`(j*pi/n,(j+1)*pi/n)`, `j=0,...,n-1`,

produces `n` distinct zeros of `F`, hence `n` distinct zeros of `P_n` in `(-1,1)` because `cos` maps `(0,pi)` into `(-1,1)` injectively.

Finally, a nonzero degree-`n` polynomial has at most `n` distinct roots: this follows inductively from the factor theorem, since division by each distinct linear factor lowers the degree by one. Since `P_n` has exact degree `n`, the `n` roots just found are all its roots. If they are `alpha_1,...,alpha_n`, then

`P_n(z)=2^n product_{j=1}^n (z-alpha_j)`.

Thus

`P_n'(alpha_j)=2^n product_{k!=j}(alpha_j-alpha_k) != 0`,

so every root is simple.

## 3. Quadratic lifting and simplicity in `y` (`O3`)

Because `s>1`,

`a=(s+s^{-1})/2>1`; indeed `(s-1)^2>0` is equivalent to `s+s^{-1}>2`.

For each scalar root `alpha_j in (-1,1)`, equation (3) becomes

`x^2=(alpha_j+a)/(1+a)`.                                                 (7)

Here `alpha_j+a>a-1>0` and `alpha_j+a<1+a`, so (7) has exactly two solutions

`x=+-sqrt((alpha_j+a)/(1+a))`,

both nonzero and in `(-1,1)`. Conversely, every zero of `Q_{n,s}` must arise this way. Hence `Q_{n,s}` has exactly `2n` roots in `(-1,1)`.

They are simple. Indeed, at any such root,

`Q_{n,s}'(x)=P_n'(z(x))*2(1+a)x != 0`,

because both factors singled out above are nonzero.

On `(0,pi)`, equation (2) is

`G_{n,s}(y)=sin(y)Q_{n,s}(cos y)`,

and `sin(y)>0`. Thus `y -> cos y` gives a bijection between zeros of `G` in `(0,pi)` and zeros of `Q` in `(-1,1)`. At such a zero,

`G_{n,s}'(y)=-sin^2(y)Q_{n,s}'(cos y) != 0`.

Therefore `G_{n,s}` has exactly `2n` interior zeros and they are all simple.

## 4. Required separate audits (`O4`)

### `n=1`

Here `P_1(z)=2z+r`, and (3) simplifies to

`Q_{1,s}(x)=((s+1)^2/s)x^2-s`.

Its two roots are `x=+-s/(s+1)`, both strictly inside `(-1,1)` and simple. They correspond to two simple zeros of `G` in `(0,pi)`.

### `y=0` and `y=pi`

At both endpoints, `q=0` and `z=1`, so (2) gives `G=0`. These endpoint zeros are not counted. Moreover

`P_n(1)=n+1+rn>0`,

so they are not concealed zeros of `Q`: directly, `G'(0)=P_n(1)` and `G'(pi)=-P_n(1)`, both nonzero.

### `y=pi/2`

Here `x=c=0`, `q=1`, and `z=-a<-1`. The parity from the recurrence is `U_k(-a)=(-1)^kU_k(a)`. Let

`D_n=U_n(a)-rU_{n-1}(a)`.

Then `D_0=1`, and because `2a-r=s` and `sr=1`,

`D_n=sU_{n-1}(a)-U_{n-2}(a)=sD_{n-1}`.

Thus `D_n=s^n`, and

`G_{n,s}(pi/2)=P_n(-a)=(-1)^n s^n != 0`.

So the midpoint is never an interior zero for `s>1`.

### Boundary `R=1` (`s=1`)

This value is excluded from the main hypothesis but can be checked directly. When `s=1`,

`C_1(y)=[[cos(2y),sin(2y)],[-sin(2y),cos(2y)]]=E(2y)`.

Direct matrix multiplication gives `E(alpha)E(beta)=E(alpha+beta)`, so

`M_{n,1}(y)=E((2n+1)y)` and `G_{n,1}(y)=sin((2n+1)y)`.

Its zeros in `(0,pi)` are exactly

`y=k*pi/(2n+1)`, `k=1,...,2n`,

and their derivatives are `(2n+1)(-1)^k`, hence nonzero. The two endpoint zeros remain excluded.

## Conclusion

Obligations `O1`-`O4` are closed by exact uniform arguments. No numerical scan or finite-parameter inference is used. Global completion remains withheld until the independent first-time audit `O5` passes.
