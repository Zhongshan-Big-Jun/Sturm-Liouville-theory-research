CANDIDATE_COMPLETE_PROOF

# Normalization and symbol map

## Scope and frozen sources

Everything below is restricted to the real symmetric, band-consistent, finite
nonzero `n=2` INF germ with `R>1` and

```text
u=R^(-1/6),  eps=u^3=R^(-1/2).
```

The exact four residuals and mass convention are taken from
`scripts/_gapn2_largeR_closed.py`, SHA-256
`e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4`.
The sector formulas are independently reconstructed from
`scripts/_gapn2_rawko_closed.py`, SHA-256
`8bb79393282c481a0b83332e044bf5740d0809086d7fabce3d24207242c04b6e`,
and `scripts/_gapn2_largeR_probe2.py`, SHA-256
`b0d5589920bbae963da2f6483bec85576a060b47a5351d75bab0274a5bfd00e7`.
The upstream scalar called `C` is located at lines 162-164 of
`run_notes_addendum_2026-08-14.md`, SHA-256
`a4b5c8b72b08508e9e8f1a6ead786e837d0c316a564ba6a6dd06bb7d1d7284cb`.

The file `scripts/_gapn2_largeR_Pbuild.py`, SHA-256
`58c98af44d074bdfd9412a1541d4a7a393f0cf3e074653c1108964b62ea6caea`,
is not an input: its D-side E5 cascade is defective.

## Branch coordinates

The physical variables are

```text
k2=K(u) u,
k3=K(u) u+Cbr(u) u^5,
p1=pi/2+A(u) u^2,
p3=pi/4+B(u) u^2,
p2=k2/2-eps(p1+p3).
```

Here `Cbr` is the positive branch coefficient. It is never denoted by the
bare letter `C` in this package. For the adjacent N half-mode put

```text
tau=k3/k2,
p1t=tau p1,  p2t=tau p2,  p3t=tau p3.
```

The two round-001 blow-up coordinate systems coincide as follows:

```text
q=Delta=(A K-2)/u^2,
q=q0(K)+u^2 X,
q0(K)=(18 pi-24-K^3)/(6K),
Cbr=16/(pi K)+u^2 Y.
```

Thus route-002's analytic functions `q=Q(v,K,B)` and `C=D(v,K,B)`, with
`v=u^2`, are route-001's `Delta` and `Cbr`. The exact positive seed is

```text
kappa^3=18 pi-48/pi,
K(0)=kappa,  A(0)=2/kappa,  B(0)=1/kappa,
Cbr(0)=16/(pi kappa)>0.
```

## Half-string geometry and raw modes

On the left half-string, the three blocks have densities `(R,1,R)` and
lengths

```text
l1=eps p1/k2,  l2=p2/k2,  l3=eps p3/k2,
l1+l2+l3=1/2.
```

For a spectral wavenumber `z`, set `qh=z/eps`, `ql=z` and phases
`phi_i=(z/k2)p_i`. Let `y(z)` solve `y(0)=0`, `y'(0)=1`. Its values and right
derivatives at the first two switches are

```text
y1=sin(phi1)/qh,                         y1'=cos(phi1),
y2=y1 cos(phi2)+y1' sin(phi2)/ql,
y2'=-ql y1 sin(phi2)+y1' cos(phi2).
```

`yD` means these values at `z=k2`; `yN` means them at `z=k3`. The raw
Wronskians are

```text
Wraw_j=yD_j yN'_j-yN_j yD'_j,  j=1,2.
```

## Exact masses and whole-string normalization

For phases `(a,b,c)`, wavenumber `z`, and `eps`, define

```text
m1=(a-sin(2a)/2) eps/(2 z^3),
aa=eps sin(a)/z,  bb=cos(a)/z,
mL=(aa^2+bb^2)b/(2z)
   +(aa^2-bb^2)sin(2b)/(4z)
   +aa bb(1-cos(2b))/(2z).
```

For the D half-mode,

```text
bD=-(eps cos(p2)sin(p1)/k2+sin(p2)cos(p1)/k2)/sin(p3),
m3D=bD^2 (p3-sin(2p3)/2)/(2 k2 eps),
ID=m1(k2,p1)+mL(k2,p1,p2)+m3D.
```

For the N half-mode,

```text
bN=(eps cos(p2t)sin(p1t)/k3+sin(p2t)cos(p1t)/k3)/cos(p3t),
m3N=bN^2 (p3t+sin(2p3t)/2)/(2 k3 eps),
IN=m1(k3,p1t)+mL(k3,p1t,p2t)+m3N.
```

These are raw half-masses for the slope-one solutions. The exact band
equation E5 is

```text
ID sin(p1t)^2=IN sin(p1)^2.
```

In the positive phase box it gives
`sqrt(ID IN)=ID sin(p1t)/sin(p1)`. The whole-string, `L2(rho)`-normalized D
switch vector is

```text
U=(U1,U2)=yD/sqrt(2 ID).
```

The N vector is normalized analogously by `sqrt(2 IN)`.

## Dynamic stiffness and Green matrices

At wavenumber `z`, with phases `phi_i=(z/k2)p_i`, define

```text
A_D(z) = [[qh cot(phi1)+ql cot(phi2),  -ql csc(phi2)],
          [-ql csc(phi2), ql cot(phi2)+qh cot(phi3)]],

A_N(z) = [[qh cot(phi1)+ql cot(phi2),  -ql csc(phi2)],
          [-ql csc(phi2), ql cot(phi2)-qh tan(phi3)]].
```

The ordinary half-Green matrices at the switches are

```text
GD=A_D(k3)^(-1),  GN=A_N(k2)^(-1).
```

Let `GtD` be the eigenprojection-subtracted finite part of `A_D(z)^(-1)`
at `z=k2`, and `GtN` the corresponding finite part of `A_N(z)^(-1)` at
`z=k3`. The pole convention is the source convention

```text
G(z^2)=P/(k^2-z^2)+Gt+O(k^2-z^2).
```

If `delta=z/k-1` and
`A(z)^(-1)=Lminus/delta+L0+O(delta)`, exact residue matching gives

```text
Gt=L0+Lminus/2.
```

This fixes the otherwise easy-to-miss finite-part constant.

## Orthonormal mirror bases and the two determinants

For the four switch coordinates use the orthonormal raw-K mirror bases

```text
be1=(e1+e4)/sqrt(2),  be2=(e2+e3)/sqrt(2),
bo1=(e1-e4)/sqrt(2),  bo2=(e2-e3)/sqrt(2).
```

Set `e=(1,-1)`, `E=diag(e)`, `c=k2/k3`,

```text
r=2 k2^2 (k3^2-k2^2)/k3^4,
v=(U1^2,U2^2).
```

For INF,

```text
d_j=-2 c |W_j|/(R-1),
W_j=Wraw_j/(2 sqrt(ID IN)).
```

The exact matrices certified here are

```text
Kp_odd=diag(d)+2 k2^2 diag(U) [E GD E-c^2 GN] diag(U),

Ko=diag(d)+2 r (E v)(E v)^T
   +2 k2^2 diag(U) [GtN-c^2 E GtD E] diag(U).
```

`Kp_odd` is `E Ke E`, where `Ke` is raw `K` in `(be1,be2)`. Hence this
conjugation changes off-diagonal signs but not the determinant. `Ko` is raw
`K` in `(bo1,bo2)`. No non-orthonormal row or column scaling is used.

## The overloaded upstream scalar

The distinct upstream seed-consistency candidate is renamed

```text
Chi_up(u)=1+B(u)K(u)/2+3 pi/(2K(u))-K(u)^2/12.
```

It is not `Cbr(u)`. The statement `Chi_up=0` and the branch fact
`Cbr(u)>0` are logically unrelated and are evaluated separately.

## Scope exclusions

No statement in this package applies to M1, M2, SUP, `n>=3`, general
`(G1')`, global reflection symmetry, a different singular chart, or a branch
outside the locally unique finite-interior INF germ.
