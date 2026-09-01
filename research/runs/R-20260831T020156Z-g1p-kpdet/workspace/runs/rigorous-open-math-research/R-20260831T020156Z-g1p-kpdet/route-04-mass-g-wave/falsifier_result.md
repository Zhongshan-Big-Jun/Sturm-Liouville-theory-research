PARTIAL

# Exact falsification of a mass-free G-sign shortcut

## Input audit

All frozen inputs were verified before use.

```text
problem_contract.md                                           67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
route-01-transfer-schur/derivation.md                         a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
route-03-phi-exact/coordinator_direct.md                      de7939ba6ebbc2fd8667fcf2eb44aeb3754ff64d0c88107298cf8bff222742f3
route-03-phi-exact/worker_result.md                           6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3
route-03-phi-exact/audit/independent_audit.json               3bace4993b5a14c55950043322dd410e65f7f0135df5e03c95dde18a5ad6b3dd
```

## 1. Exact mass-defective witness

Set

```text
m=sqrt(5),  R=5,  c=4/5,
alpha=theta=pi/4,  beta=pi.
```

Write

```text
s=sin(pi/5),  q=cos(pi/5)=(1+sqrt(5))/4.
```

The elementary identity

```text
tan(pi/5)tan(2pi/5)=sqrt(5)
```

shows that this point is the `c=4/5` member of the exact family

```text
alpha=theta=pi/4,
beta=pi,
m=tan(c pi/4)tan(c pi/2).
```

At the displayed point, the transfer quantities are

```text
S=C=1/sqrt(2),
X=Z=D=-1/sqrt(2),
Y=s,
T=-q,
N=(1-3sqrt(5))/4.
```

Hence both spectral equations and the band equation hold exactly:

```text
X cos(alpha)-Z sin(alpha)=0,
Y cos(c alpha)+T sin(c alpha)=s q-q s=0,
Y=-sX/C=s.
```

All strict modal conditions also hold. Namely,

```text
0<alpha<pi,
0<c alpha=pi/5<pi,
0<theta<pi/2,
0<c theta=pi/5<pi/2,
X<0,
Y>0.
```

Moreover,

```text
delta_3=atan(1/sqrt(5)) in (0,pi/2),
delta_3<beta=pi<delta_3+pi.
```

Since

```text
s/(m q)=1/tan(2pi/5)=tan(pi/10),
```

one has

```text
delta_2=9pi/10,
0<c beta=4pi/5<delta_2.
```

The reconstructed physical switches are strictly interior because

```text
p=(alpha+m beta+theta)/L=pi(1+2sqrt(5)),
a=alpha/p>0,
b=(alpha+m beta)/p<L.
```

Thus this is an exact finite-interior point satisfying the complete spectral,
band, and modal-domain system. It is not an abstract matrix witness.

For the sign calculation, define the exact positive or signed quantities

```text
Ttheta=1/2+(4/5)s q,
Dtheta=(5/4)[1+(4/5)q/s]-Ttheta,
U=-1/sqrt(2)+sqrt(2)s(3sqrt(5)-1)/5,
K=(1/sqrt(2))[1-(4/5)q/s].
```

Then

```text
G=Dtheta U-sqrt(2)Ttheta^2,
Xi=G/2-(5/4)K Dtheta.
```

The following is an exact rational interval certificate. The input bounds

```text
2.236067<sqrt(5)<2.236068,
1.414213<sqrt(2)<1.414214,
0.587785<s<0.587786
```

follow by squaring, using `s^2=(5-sqrt(5))/8`. Outward rational interval
arithmetic in the displayed formulas gives

```text
0.880422<Ttheta<0.880424,
1.745956<Dtheta<1.745961,
0.241884<U<0.241889,
-0.071493<K<-0.071491,
-0.673901<G<-0.673889,
-0.180926<Xi<-0.180914.
```

In particular, even `U>0` does not imply `G>=0`. Both `G` and `Xi` are
strictly negative at this exact spectral-band-modal point.

## 2. The exact missing constraint

The witness fails precisely at normalization. Direct substitution into the
frozen exact mass formula gives

```text
Delta_M
=C^2 I2hat-c^3 s^2 I3hat
=(-625sqrt(10+2sqrt(5))
  +125sqrt(50+10sqrt(5))
  +250sqrt(50-10sqrt(5))
  +320sqrt(5)pi+3456pi)/3200.
```

This residual is strictly positive. Indeed, all terms except the first are
positive, `sqrt(10+2sqrt(5))<4`, and `pi>3`, so

```text
Delta_M>(-2500+10368)/3200>0.
```

Therefore the witness violates `E_mass`, equivalently `M-slope`, and is not
an admissible counterexample to the complete system. It proves instead that
no argument using only the two spectral equations, the band equation, modal
indices, denominator signs, or the weaker fact `U>0` can establish `G>=0`.
The exact mass equation is genuinely load-bearing.

Because `Xi<0` and `X<0`, the lossless identity `Xi=X Phi` also gives
`Phi>0` on this mass-defective witness. This does not change `PHI-SIGN` on
the complete admissible set.

## 3. Restricted near-one sign theorem

There is also an exact restricted region in which a complete admissible
counterexample cannot occur. Let complete admissible tuples satisfy

```text
m -> 1+,
eta<=alpha<=pi-eta
```

for a fixed `eta>0`. Then `G>0` for all sufficiently small `m-1`.

To prove this, standard Sturm continuity and the fixed mode indices give, in
the uniform-density limit,

```text
alpha+beta+theta -> 3pi/2,
c(alpha+beta+theta) -> pi,
c -> 2/3.
```

The uniform norm limits are

```text
I3hat -> 3pi/4,
I2hat -> pi/2.
```

The exact mass equation therefore forces

```text
C=(2/3)s.
```

It also keeps `theta` away from `0` and `pi/2`. At the limit,

```text
D=-cos(alpha),
N=-cos(c alpha),
c s/C=1,
U -> cos((2/3)alpha)-cos(alpha)>0.
```

The last inequality is uniform on `eta<=alpha<=pi-eta`. Furthermore,

```text
Dtheta=r[tan(theta)+c cot(c theta)]-Ttheta,
r=m^2/(m^2-1) -> +infinity,
```

while `X Ttheta^2/C^2` remains bounded. Hence

```text
G=Dtheta U+X Ttheta^2/C^2>0
```

eventually. This theorem does not cover a simultaneous near-one left-switch
collision `alpha->0`, nor does it control the finite and large `R` interior.

## 4. Exact remaining gap

No exact tuple satisfying `E_mass` with `G<0` was obtained. The first open
obligation remains to use `E_mass`, or its equivalent `M-slope`, to rule out
the negative region exhibited above on the complete admissible branch. A
successful proof cannot replace that step by spectral, band, modal, or
denominator sign bookkeeping. `PHI-SIGN` and `KP-DET` remain open.

decision_delta: The global G-sign subroute is not refuted on the complete mass-admissible set, but an exact finite-interior spectral-band-modal witness has G<0 and Xi<0, proving that E_mass is indispensable; complete near-one tuples bounded away from left collision still satisfy G>0, and PHI-SIGN is unchanged.
