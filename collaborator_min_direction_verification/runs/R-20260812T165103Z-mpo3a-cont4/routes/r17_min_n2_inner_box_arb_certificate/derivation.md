FINITE_COMPUTATIONAL_RESULT

# R17: rigorous compact-box signs for all four R14 coefficients

## 1. Exact physical coordinates

Use the coordinates frozen in `problem_contract.md`.  Set

```text
A=k a,   B=k b,   Q=k q,   S=k sigma.
```

The exact common-angle equations give

```text
q=Aplus sinc(k Aplus)/cos(k Aplus),
a=sinc(k Aplus) cos(Aplus)/[cos(k Aplus) sinc(Aplus)],

sigma=Aminus sinc(k Aminus)/cos(k Aminus),
b=-sinc(k Aminus) cos(Aminus)/[cos(k Aminus) sinc(Aminus)].
```

Thus the calculation never relaxes the common-angle manifold.  This scaling
also removes the leading `k -> 0` cancellation on the compact box.

## 2. Stable endpoint variables

Write

```text
Dtilde=b(1+k^2ab)+k^2(a+b)sigma^2,
rB=a sigma(1-k^2b^2)/(q Dtilde),
1-g=k^2 ebar,
ebar=(1-k^2)(b^2-a^2)/[(1-k^4b^2)(1-k^2a^2)].
```

If `X=cp*x_+=k Xbar` and `W_i=cp*w_i=Wbar_i/k`, then

```text
U_i=cp*u_i=Ubar_i/k,
H_i=cp*h_i=k Hbar_i,
L_i=cp*ell_i=k Lbar_i.
```

Consequently `U_i L_i=Ubar_i Lbar_i` has no artificial power of `k`.
The checker evaluates the exact rational formulas for `Wbar_0,Wbar_1`,
`Ubar_i,Hbar_i,Lbar_i`, `Knew`, `Pplus`, and `cp^2`.

The potentially cancelling plus quantity is evaluated through

```text
Xbar = [sinc(2k Aplus)-sinc(2 Aplus)]
       / {sin(Aplus)cos(k Aplus)
          [sinc(Aplus)cos(k Aplus)
           -k^2 sinc(k Aplus)cos(Aplus)]}.              (2.1)
```

For `0<=k<=1` and `0<=z<=pi`, the numerator in (2.1) has alternating
expansion

```text
sum_{n>=1} (-1)^(n+1)(1-k^(2n))z^(2n)/(2n+1)!.
```

Its positive term magnitudes decrease.  Indeed the consecutive ratio is at
most `pi^2/10<1` at `n=1` and decreases thereafter.  The checker therefore
uses the first sixteen signed terms as a lower endpoint and adds the
seventeenth positive term for the upper endpoint.  This is a rigorous Arb
enclosure, not a truncated approximation.

## 3. The four coefficient gaps

With `s=rB-1` and `Delta=rB^2-1`, the stable Bernstein numerators are

```text
Nhat_1=s Ubar_0 Lbar_0/2,
Nhat_2=[2s(Ubar_1Lbar_0+Ubar_0Lbar_1)
        +Delta Ubar_0Lbar_0]/6,
Nhat_3=[2s Ubar_1Lbar_1
        +Delta(Ubar_1Lbar_0+Ubar_0Lbar_1)]/4,
Nhat_4=Delta Ubar_1Lbar_1.
```

The checked gaps are exactly

```text
G_i=g Knew cp^4-Pplus Nhat_i,       i=1,2,3,4.          (3.1)
```

Their signs equal the signs of the unscaled R14 coefficients `B_i`.

## 4. Conditional interval contractor

Every ambient box is evaluated by Arb at 128-bit precision.  A box is
discarded if its upper bound proves `b-a<=0` (hence no `g<1` point) or
`rB-1<=0` (hence no `rB>1` point).

For a box that may meet the retained subset, R14 supplies

```text
ebar>=0, rB>=1, Xbar,Wbar_i,Ubar_i,Hbar_i,Lbar_i>0.
```

Intersecting the ambient balls with these proved signs is a valid contractor.
Monotone endpoint products then give an upper bound for every `Nhat_i` and a
lower bound for `g Knew cp^4`.  If all four resulting lower bounds in (3.1)
are positive, the entire retained part of that box is certified.

Unresolved boxes are bisected along their widest exact dyadic coordinate.

## 5. Complete finite covering result

The exact replay returned:

```text
visited       264863
discard_g      23007
discard_r      59251
proved         50174
split         132431
singular           0
unresolved         0
stack_remaining    0
```

There are `132432` leaves, exactly `split+1`, and
`visited=leaves+split`.  The smallest directed lower endpoints encountered
among certified leaves were

```text
G_1: 0.04340924725160458
G_2: 0.001998451910768295
G_3: 0.0004258814105750445
G_4: 0.00006727937130214070.
```

Therefore all four R14 Bernstein coefficients are strictly positive on the
frozen compact physical box.

## 6. Exact remaining frontier

No assertion is made in the six omitted boundary collars or their
intersections.  In particular, this certificate is not a proof for all
`mu>1` and all admissible phases.  The global min route remains open solely
because those collars have not been discharged here.
