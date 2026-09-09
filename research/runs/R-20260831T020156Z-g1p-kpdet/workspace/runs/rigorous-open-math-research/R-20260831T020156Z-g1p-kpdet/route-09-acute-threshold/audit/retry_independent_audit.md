# Independent retry audit of W14 and W15

## Verdict

`PASS`.

Audit ID: `AUDIT-W14-W15-ACUTE-RETRY-01`.

The reviewer did not author W14 or W15. Both submissions were treated as first-time unverified candidate content. No web search, solver rerun, or numerical inference was used. All nine bound input SHA-256 values were recomputed before mathematical use and matched exactly.

## Input integrity

| Input | Verified SHA-256 |
| --- | --- |
| `problem_contract.md` | `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d` |
| `whiteboard-20.md` | `b833173af643f13fc260b9c64631255c4c8332a55f41df105d92fe0f78a3f713` |
| `route-04-mass-g-wave/accepted_package.md` | `cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192` |
| `route-07-global-sign-coherence/accepted_package.md` | `a24a0fe82e19ef6a1aeb2e29c2379bb2f8793818940d43df9d87b9abd14ef1dc` |
| `route-08-common-beta-orientation/accepted_package.md` | `2257a61c95cdcfa58b12cae577c5097ea4f124cd5d6077b6ebe550eb0779f8ed` |
| `route-09-acute-threshold/prover_result.md` | `ef7ad48667026a5eb672c8d4bd48718903fd6dcf2102d9f16b8a6883ece948c2` |
| `route-09-acute-threshold/falsifier_result.md` | `c961bcba5931957beb2e2e60baed90e9517d2af0d3015efa8605a86e985160a2` |
| `route-09-acute-threshold/reconciliation.md` | `6b9973b8f56b06b1c254696976b9349f0bb5725745ac61e3dcadbd4901fbe959` |
| `route-09-acute-threshold/audit/NO_RETURN.md` | `6490aec6e2f7719a766df14d70ea799c2698d472c82458f9ec1910b8d2300373` |

## W14 audit

### Acute coordinates and root

Let the original switch phase be `alpha`, put `t=pi-alpha`, and write

```text
P_m(r)=atan(tan(r)/m),
H_m(r)=atan(m tan(r)).
```

On `(0,pi/2)`, these maps are smooth, strictly increasing inverses. The acute assumptions imply

```text
0<t<(pi/2),
0<(1-c)pi+ct=pi-c alpha<pi/2.
```

Therefore

```text
A=P_m(t),
B=P_m((1-c)pi+ct)
```

satisfy `0<A<B<pi/2`. Hence `sigma=sin(B)/sin(A)>1` and `kappa=B-cA` lies in `(0,pi/2)`.

For fixed `(c,m,A)`, set

```text
F(d)=sin(kappa-cd)/sin(d),
g=kappa-cd.
```

The admissible interval is

```text
0<d<min(pi/2,kappa/c).
```

On it,

```text
d log(F)/dd=-c cot(g)-cot(d)<0.
```

As `d->0+`, `F(d)->infinity`. If `kappa/c<=pi/2`, the other endpoint has `g->0` and `F->0`. If `kappa/c>pi/2`, the other endpoint has `d->pi/2` and `F->sin(kappa-cpi/2)<=1`. Both endpoint values are strictly below `sigma>1`. Thus the root `F(d)=sigma` exists and is unique in both endpoint cases.

At the root, `sin(g)=sigma sin(d)` and all angles are acute, so `g>d`. Moreover

```text
B-g=B-(B-cA-cd)=c(A+d)>0,
```

so `g<B`. The lock identity `sin(B)sin(d)=sin(A)sin(g)`, together with `B>g`, then gives `A>d`. Hence all orderings used later are strict:

```text
0<d<A<B<pi/2,
0<d<g<B<pi/2.
```

The intrinsic condition is exactly `J=0`. Indeed, with `h=H_m(d)`, one has `d=P_m(h)`, and

```text
J=H_m(d)+H_m(g)/c-pi/2=0
```

if and only if `H_m(g)=c(pi/2-h)`, equivalently `g=P_m(c(pi/2-h))`. No tangent branch or multiple of `pi` is introduced.

### Constrained derivative

Write

```text
R(r)=1+(m^2-1)sin(r)^2.
```

Since `H_m'(r)=m/R(r)`, differentiation of `B=P_m((1-c)pi+cH_m(A))` gives

```text
B'=c H_m'(A)/H_m'(B)=c R(B)/R(A)>c,
kappa'=B'-c>0.
```

Differentiating

```text
log sin(g)-log sin(d)-log sin(B)+log sin(A)=0
```

along the root gives, with `L=B'cot(B)-cot(A)` and `Lambda=c cot(g)+cot(d)`,

```text
d'=[kappa'cot(g)-L]/Lambda,
g'=kappa'-cd'.
```

To audit the sign in the numerator, put `k=m^2-1` and use `sin(B)=sigma sin(A)`. Directly collecting over the positive denominator `1+k sin(A)^2` gives

```text
kappa'cot(g)-L
=[cot(A)-c cot(B)+k sin(A)^2 T]/[1+k sin(A)^2],

T=(1-c)cot(A)
  +c[(cot(A)-cot(B))
     +(sigma^2-1)(cot(g)-cot(B))].
```

This is exactly W14 equations (4)-(5). Every summand of `T` is positive: `c<1`, `A<B`, `g<B`, and `sigma>1`. Also `cot(A)-c cot(B)>0`. Therefore `d'>0`.

The function `H_m'` is strictly decreasing on `(0,pi/2)`. Since `d<g`,

```text
J'=[H_m'(d)-H_m'(g)]d'+H_m'(g)kappa'/c>0.
```

This verifies equations (3)-(7) with the full implicit-root Jacobian. The isolated equation `J=0` is not differentiated as an identity, and no step sets `J'=0`.

### Endpoint and the ratio threshold

As `A->0+` at fixed `(c,m)`, `B->B0=P_m((1-c)pi)` and `sigma->infinity`. The lock forces `d->0`, and then `g=kappa-cd->B0`. Consequently

```text
lim J=H_m(B0)/c-pi/2
     =(1-c)pi/c-pi/2
     =pi(2-3c)/(2c).
```

Since `J` is strictly increasing, a strict acute root can exist only for `c>2/3`. At `c=2/3`, the endpoint limit is zero but `J(A)>0` for every `A>0`, so the boundary value does not enter the strict branch.

Every complete tuple has the accepted `Bcoef<0`. The accepted closed chamber gives `PHI-SIGN` and KP-DET when `c alpha<=pi/2`. The complementary chamber is precisely the acute chamber audited above. Its exclusion for `c<=2/3`, together with the already closed chamber, therefore proves complete `PHI-SIGN` and KP-DET for `0<c<=2/3`.

### Transfer norms and exact mass collapse

Let `P=cos(theta)^2+m^2 sin(theta)^2`. The definitions of `A` and `d` give the exact identities

```text
sin(A)^2=sin(t)^2/[sin(t)^2+m^2 cos(t)^2],
sin(d)^2=cos(theta)^2/P.
```

The accepted transfer norm formula `X^2=P/(1+m^2 cot(alpha)^2)` therefore yields

```text
X^2=P sin(A)^2,
cos(theta)^2=P sin(d)^2,
cos(theta)^2/X^2=sin(d)^2/sin(A)^2.
```

Now use

```text
JA=e+D/sin(A)^2,
Jd=e+D/sin(d)^2,
```

and the accepted coefficient dictionary. After division by the positive factor `s^2X^2`, the mass equation is

```text
0=alpha[e-JA/M]
  +beta[e-JA]/m
  +theta[sin(d)^2/sin(A)^2][e-Jd/M].
```

Multiplication by the positive factor `M sin(A)^2` gives, term by term,

```text
alpha[k e sin(A)^2-D],
-m beta D,
theta[k e sin(d)^2-D].
```

Thus

```text
D(alpha+theta+m beta)
=k e[alpha sin(A)^2+theta sin(d)^2].
```

All factors on the right are positive, so `D>0`. Since `m beta>0`, the weighted average on the right is strictly below `max(sin(A)^2,sin(d)^2)`, proving

```text
0<D<k e max(sin(A)^2,sin(d)^2).
```

No scaling factor has an uncertain sign.

### Psi reduction

At the unique intrinsic root, the definitions

```text
alpha=pi-H_m(A),
theta=pi/2-H_m(d),
beta=A+d
```

reconstruct the original acute tuple. Therefore the exact mass equation is precisely `Psi=0`, where

```text
Psi=DW-k e N,
W=alpha+theta+m beta,
N=alpha sin(A)^2+theta sin(d)^2.
```

The implication `q>E -> Psi>0` would contradict mass and is strictly weaker than the max threshold because `N/W<max(sin(A)^2,sin(d)^2)`. It remains open and is not asserted as proved.

At `A->0+`, one has `D->c^2`, `W->3pi/2`, and `N->0`, hence

```text
lim Psi=3pi c^2/2.
```

Finally, `D'=2sigma^(-2)L`, and ordinary product differentiation along the phase-lock root gives W14 equation (18). The displayed formulas for `W'` and `N'` contain every `d'` contribution. No derivative in the isolated compatibility direction is discarded.

## W15 audit

### Uniform compactification

Put `z=1/m`. For `z>0`,

```text
p_z(r)=atan(z tan(r))/z.
```

The Taylor series of `atan` shows that the extension `p_0(r)=tan(r)` is smooth and even in `z` on fixed neighborhoods of `r=0` and `r=pi/3`. The point `z=1` is ordinary and nonsingular. Moreover

```text
S_z(r)=sin(zp_z(r))/z
      =tan(r)/sqrt(1+z^2 tan(r)^2),
```

so `S_z` also extends smoothly and positively at both `z=0` and `z=1` near `r=pi/3`. Compactness of `z in [0,1]` makes all Taylor remainders below uniform.

The angle formulas give exactly W15 equations (C4)-(C5). At the base point `(c,t,h)=(2/3,0,0)`, let

```text
a_z=p_z'(pi/3)=4/(1+3z^2).
```

For the left side `F` of (C4),

```text
partial F/partial c=-(3pi/2)a_z,
```

which is bounded away from zero uniformly for `z in [0,1]`. The uniform implicit function theorem therefore first gives `c-2/3=O(t+h)`. The positive-lock equation, together with `S_z(r)->S_z(pi/3)>0` in both large-angle factors and `S_z(x)/x->1` uniformly at zero, gives

```text
h/t->1
```

uniformly.

Writing `delta=c-2/3`, the linear part of (C4) is

```text
-(3pi/2)a_z delta+(2/3)(a_z-1)(t+h)=o(t+h).
```

Hence

```text
delta=[(1-z^2)/(3pi)](t+h)+o(t+h)
     =[2(1-z^2)/(3pi)]t+o(t).
```

Also `p_z(x)=x+O(x^3)` uniformly, so

```text
beta=z[p_z(t)+p_z(h)]=2zt(1+o(1)).
```

This proves (C1), including coupled limits with `z->0` or `z->1`.

### The q-E and threshold limits

Let `r=(1-c)pi+ct`. The branch-safe q formula can be rewritten without a small denominator in `z` as

```text
q=c tan(r)/tan(t)^2
    *[1+z^2 tan(t)^2]/[1+z^2 tan(r)^2]
  -cot(t).
```

Therefore

```text
lim t^2q=c0 sqrt(3)/(1+3z^2).
```

For `u=tan(theta)=cot(h)` and `v=tan(c theta)`, direct substitution of `M=z^(-2)` into the accepted E gives the exact compact form

```text
E=
c u(1-z^2)(u^2v^2-1)^2
/
[(1+z^2v^2)
 {u v(1+v^2)(z^2+u^2)
  +c(1+u^2)(1+z^2v^2)}].
```

This expression is continuous at `z=0`. Since `h/t->1`, `hu->1`, and `v->sqrt(3)` uniformly,

```text
lim t^2E
=c0 3sqrt(3)(1-z^2)/[4(1+3z^2)].
```

Subtracting gives the z-independent limit

```text
lim t^2(q-E)=c0 sqrt(3)/4=sqrt(3)/6.
```

Also `sigma^(-2)=O(t^2)` uniformly, so `D->c0^2=4/9`. The exact identities

```text
(m^2-1)sin(A)^2
=(1-z^2)tan(t)^2/[1+z^2tan(t)^2],

(m^2-1)sin(d)^2
=(1-z^2)tan(h)^2/[1+z^2tan(h)^2]
```

show that both subtracted terms tend uniformly to zero. Thus both threshold margins tend to `4/9`, and (C2) is correct with strict positive margins.

### Normalized mass residual

The exact normalized residual is

```text
Mmass=alpha[e-JA/M]
     +beta[e-JA]/m
     +theta[sin(d)^2/sin(A)^2][e-Jd/M].
```

It is the original mass left side divided by the positive factor `s^2X^2`, using the audited norm ratio above. The compact identities

```text
JA/M=z^2e+D[cot(t)^2+z^2],
Jd/M=z^2e+D[cot(h)^2+z^2]
```

give

```text
JA/M=c0^2/t^2+O(1/t),
Jd/M=c0^2/h^2+O(1/t)
```

uniformly. Also

```text
sin(d)^2/sin(A)^2=(h/t)^2[1+o(1)].
```

The `alpha` and `theta` terms therefore contribute respectively `-pi c0^2/t^2` and `-(pi/2)c0^2/t^2`. Because `beta=2zt(1+o(1))`, the middle term is only `O(1/t)` uniformly, including `z->0`. Consequently

```text
t^2 Mmass->-(3pi/2)c0^2=-2pi/3.
```

This verifies (C3) and proves that no complete mass tuple approaches the collar.

### Boundary and evidence checks

W14 and W15 are compatible at `c=2/3`. W14 proves that every strict acute intrinsic root has `c>2/3`. W15's `c=2/3` point is only the compactified endpoint. Its expansion approaches that endpoint from the allowed side for exact strict roots and never inserts the boundary point as a tuple.

The binary64 scans in W15 are explicitly isolated as `EVIDENCE`. No scan count, residual, or sampled margin is used in the uniform collar theorem or in this audit verdict.

## Mandatory audit summary

- Definition audit: all inverse maps, acute branches, coefficient names, norm factors, and compactified variables agree with the bound accepted packages.
- Logic audit: all implication directions are correct. In particular, the open implication `q>E -> Psi>0` is not treated as proved.
- Boundary audit: the nonzero root endpoint, `c=2/3`, `z=0`, `z=1`, and coupled `z,t->0` limits are covered without admitting excluded modal faces.
- Adversarial audit: the weakest steps were the sign of the implicit derivative, the uniform z compactification of E, and the `z->0` middle mass term. Their exact denominator-free forms above verify the claimed signs and uniform orders.

There is no first error, critical error, or gap in the strict partial claims. Arbitrary finite `c>2/3` `PHI-SIGN` and KP-DET remain open at the stated scalar implication.
