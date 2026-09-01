PASS

# Independent audit of W8 and W9

## Audit binding

- Audit ID: `AUDIT-W8-W9-ALPHA-PI-01`.
- Review mode: fresh first-time joint audit.
- Authorship separation: the reviewer authored neither endpoint result.
- Every frozen SHA256 in `audit_packet.md` was recomputed and matched.

| Artifact | Verified SHA256 |
| --- | --- |
| `problem_contract.md` | `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d` |
| `route-01-transfer-schur/derivation.md` | `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3` |
| `route-04-mass-g-wave/repair/near_one_repair.md` | `8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314` |
| `route-05-alpha-collision/accepted_package.md` | `49d1691a384a6b7d550d8b547dfc25de5daf14fd575d6018462417b04e7257ba` |
| `route-06-alpha-pi/prover_result.md` | `b0f66b3090280f946d2ec4d49df54eed942ae56913aa77d286e1ce8e028881cb` |
| `route-06-alpha-pi/falsifier_result.md` | `ece86c1ff05afa17a3fdb6f9bab94e31b69cbdf38190e2a6c1d1b77a10e5b514` |

## Independent algebra

### 1. Switch-uniform spectral and total-phase limits

The density satisfies `1<=rho_m<=m^2` independently of the switch positions. For each fixed boundary condition and eigenvalue index, min-max gives

```text
lambda_k(1)/m^2<=lambda_k(rho_m)<=lambda_k(1).
```

The frozen labels are DD index 1 and DN index 2 on `L=1/2`, so their uniform limits are `4pi^2` and `9pi^2`. Hence `c->2/3`. From the phase definitions,

```text
alpha+m beta+theta=pL=m sqrt(lambda_3)L,
c(alpha+m beta+theta)=cpL=m sqrt(lambda_2)L.
```

The modal inequality gives `0<beta<3pi/2`, so `(m-1)beta->0`. Therefore both total-phase limits are uniform and may equivalently be written

```text
alpha+beta+theta->3pi/2,
c(alpha+beta+theta)->pi.
```

Under `alpha->pi`, this gives `beta+theta->pi/2`.

### 2. Transfer limits and the undivided band equation

All six transfer expansions are exact:

```text
X=cos(beta+theta)-(m-1)S sin(beta),
Z=sin(beta+theta)+(1/m-1)C sin(beta),
Y=sin(c(beta+theta))+(m-1)Cc sin(c beta),
T=cos(c(beta+theta))+(1-1/m)s sin(c beta),
D=sin(beta+theta)+(m-1)C sin(beta),
N=cos(c(beta+theta))-(m-1)s sin(c beta).
```

Thus any endpoint subsequence has

```text
(X,Z,Y,T,D,N)->(0,1,sqrt(3)/2,1/2,1,1/2).
```

The band equation must be used as `CY=-sX`, without division by `C`. Passing to the limit gives `C_0 sqrt(3)/2=0`, hence `theta->pi/2`. The total phase then gives `beta->0`. This conclusion holds for the whole sequence because every convergent subsequence has the same limit.

### 3. First-order scales

Set `d=pi-alpha`. The DN equation gives

```text
X=Z tan(alpha)=-Z tan(d),
```

so `X/d->-1`. Dividing `CY=-sX` by `d`, while `Y,s->sqrt(3)/2`, gives `C/d->1`. With `e=pi/2-theta` and `C=sin(e)`, this is also `e/d->1`.

W8's optional beta scale is correct. Rearranging the exact formula for `X` gives

```text
mS sin(beta)=C cos(beta)-X.
```

After division by `d`, the right side tends to `1-(-1)=2`, while `mS->1`. Hence `sin(beta)/d->2`; since `beta->0`, it follows that `beta/d->2`.

### 4. Independent removal of both norm singularities

Before taking limits, the DN spectral equation gives the exact identity

```text
X^2/sin(alpha)^2=Z^2/cos(alpha)^2.
```

The new denominator tends to `1`, and the middle interval has length `beta->0`. Therefore

```text
I3hat->Js(pi)+Jc(pi/2)=pi/2+pi/4=3pi/4.
```

Separately, the DD equation gives

```text
Y^2/sin(c alpha)^2=T^2/cos(c alpha)^2.
```

Here `cos(c alpha)->-1/2`, so this removal is nonsingular and independent of the DN removal. The middle interval has length `c beta->0`, and

```text
I2hat->Js(2pi/3)+Js(pi/3)
      =(pi/3+sqrt(3)/8)+(pi/6-sqrt(3)/8)
      =pi/2.
```

### 5. Mass residual and uniform wedge

For

```text
Delta_M=C^2 I2hat-c^3 s^2 I3hat,
```

the first term tends to zero, while

```text
c^3 s^2 I3hat
->(2/3)^3 (3/4) (3pi/4)
=pi/6.
```

Hence `Delta_M->-pi/6`. The claimed uniform strengthening `Delta_M<-pi/12` follows by sequential negation. If no endpoint neighborhood had this property, choosing widths `1/j` would produce a spectral-band-modal sequence with `m_j->1+`, `alpha_j->pi`, and `Delta_M>=-pi/12`, contradicting the limit. Complete tuples satisfy `Delta_M=0`, so the complete endpoint wedge is empty.

### 6. Sequential-to-uniform and combined quantifiers

The absence of every complete sequence with `m_j->1+` and `alpha_j->pi` is equivalent, in this finite-dimensional phase domain, to the existence of one pair `epsilon_pi,delta_pi>0` giving an empty wedge. The stated upgrade is therefore valid.

For the combined near-one claim, shrink the accepted endpoint widths if needed and choose

```text
eta=min(delta_0,delta_pi,pi/4)/2,
epsilon_*=min(epsilon_0,epsilon_pi,epsilon_eta).
```

If `1<m<1+epsilon_*`, then `alpha<eta` is excluded by the alpha-zero wedge, `alpha>pi-eta` is excluded by the alpha-pi wedge, and every remaining alpha lies in the single fixed strip `eta<=alpha<=pi-eta`, where the accepted theorem gives `G>0`. Thus one common epsilon covers all alpha values.

Moreover, the frozen formulas give the direct identity

```text
Phi=X G-Dtheta Dalpha.
```

Since `X<0`, `G>0`, `Dtheta>0`, and `Dalpha>0`, the surviving strip has `Phi<0`. No endpoint sign is needed because both endpoint wedges are empty.

## Four-part audit

- Definition audit: phase conventions, mode labels, and the middle-layer factor `m` are consistent with the frozen derivation. No limit point is treated as an admissible interior tuple.
- Logic audit: the spectral-band subsystem forces the endpoint scales before the mass equation is used. The mass equation supplies the contradiction and is not used circularly.
- Boundary audit: all divisions occur only after the corresponding exact spectral identity has removed the vanishing factor. The strict members satisfy `C>0`; the proof uses the undivided band equation when `C->0`.
- Adversarial audit: an alternative scale `C/d->k` is impossible because the band equation forces `k=1`. The compatible modal scale `beta/d->2` does not itself contradict admissibility, so the proof correctly locates the first contradiction in the mass residual.

## Verdict and remaining scope

`PASS`. Both W8 and W9 establish the same exact endpoint exclusion. W8's stronger first-order and uniform residual claims are correct. There are no critical errors and no repairable gaps in the bound claims.

This audit does not promote any arbitrary finite-`R` statement. Global `G`, global `Xi`, global `PHI-SIGN`, and `KP-DET` remain open, as do branch existence and all excluded sectors from the problem contract.

decision_delta: The alpha-pi endpoint exclusion, its forced first-order scales, its exact norm and mass limits, and the common-epsilon near-one assembly all pass independent audit; only the near-one neighborhood is closed, while arbitrary finite-R G, Xi, PHI-SIGN, and KP-DET remain open.
