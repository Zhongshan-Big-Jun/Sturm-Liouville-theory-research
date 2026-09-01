REPAIRABLE_GAP

# Independent audit of W4 and W5

Audit ID: `AUDIT-W4-W5-MASS-G-01`.

## Hash verification

All six bound inputs were hashed before review and matched the packet.

| Path | Verified SHA256 |
|---|---|
| `problem_contract.md` | `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d` |
| `route-01-transfer-schur/derivation.md` | `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3` |
| `route-03-phi-exact/worker_result.md` | `6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3` |
| `route-03-phi-exact/audit/independent_audit.json` | `3bace4993b5a14c55950043322dd410e65f7f0135df5e03c95dde18a5ad6b3dd` |
| `route-04-mass-g-wave/prover_result.md` | `d55114570d516c69e446f2c228a76fb8827335e596df6c62e3d355a5232f9ffa` |
| `route-04-mass-g-wave/falsifier_result.md` | `03a06fbe30ae7acea06a7da21d694f3d07bb3140458c93ce78b16b911fefb9e9` |

## W4 audit

### Independent derivation of the phase quadratics

On `F3=0`, the transfer identities give

```text
partial_beta X=-m Z,
partial_beta Z=X/m,
partial_theta X=-D,
D Z+X partial_theta Z=1,
cos(alpha)=Z sin(alpha)/X.
```

Therefore

```text
E3(F3)/sin(alpha)
=-[alpha(X^2+Z^2)+beta(m Z^2+X^2/m)+theta]/X
=-Q3/X.
```

For the lower residual, with arguments `(A0,B0,H0)`, one similarly has

```text
partial_B0 Y=m T,
partial_B0 T=-Y/m,
partial_H0 Y=N,
N T-Y partial_H0 T=1,
cos(A0)=-T sin(A0)/Y.
```

It follows that, at `(A0,B0,H0)=(c alpha,c beta,c theta)`,

```text
E2(F2)/sin(c alpha)
=-c[alpha(Y^2+T^2)+beta(m T^2+Y^2/m)+theta]/Y
=-c Q2/Y.
```

Substitution in the audited mass-slope equation, followed by the reversible
use of `Y=-sX/C`, gives

```text
C^2 Q2=c^2 s^2 Q3.                                    (1)
```

Expanding by the positive phase weights gives

```text
alpha A+beta B+theta H=0.                              (2)
```

No sign is taken while multiplying by the negative factor `sX/c`, so the
equivalence is lossless.

### Coefficient formulas, signs, and equality cases

The spectral and band equations imply

```text
Z=X cot(alpha),
T=-Y cot(c alpha),
C^2 Y^2=s^2 X^2.
```

Hence

```text
A=s^2 X^2[csc(c alpha)^2-c^2 csc(alpha)^2]
 =s^2 X^2 Lalpha,                                      (4)

B-mA=-mu C^2Y^2+mu c^2s^2X^2
    =-mu(1-c^2)s^2X^2,

B=s^2X^2[m Lalpha-mu(1-c^2)].                          (5)
```

Substituting these identities into `(2)` and dividing only by the positive
quantity `s^2X^2` yields

```text
(alpha+m beta)Lalpha+theta H/(s^2X^2)
=beta mu(1-c^2)>0.                                     (3)
```

All powers of `c` and all signs in `(1)-(5)` are correct. From `(3)`,

```text
H<=0  implies
Lalpha>=beta mu(1-c^2)/(alpha+m beta)>0,

Lalpha<=0 implies
H>=s^2X^2 beta mu(1-c^2)/theta>0.
```

Equality in the first lower bound occurs exactly at `H=0`; equality in the
second occurs exactly at `Lalpha=0`. Equation `(2)` has strictly positive
weights. It excludes an all-nonnegative or all-nonpositive coefficient
triple, because equality would force `A=0`, whereas `(5)` would then give
`B=-mu(1-c^2)s^2X^2<0`. Thus the strict mixed-sign conclusion is valid.

The statement `(SC)` is clearly labeled as an unproved sufficient
implication. It is neither asserted as necessary nor as equivalent to
`G>=0`. W4 is accepted as a rigorous partial result.

## W5 audit

### Exact witness and modal checks

At

```text
m=sqrt(5), c=4/5, alpha=theta=pi/4, beta=pi,
s=sin(pi/5), q=cos(pi/5)=(1+sqrt(5))/4,
```

direct transfer substitution gives

```text
X=Z=D=-1/sqrt(2),
Y=s,
T=-q,
N=(1-3sqrt(5))/4.
```

Consequently

```text
F3=(-1/sqrt(2))cos(pi/4)-(-1/sqrt(2))sin(pi/4)=0,
F2=s q-q s=0,
Y=-sX/C=s.
```

The identity `tan(pi/5)tan(2pi/5)=sqrt(5)` verifies the displayed exact
family relation. The modal bounds are also strict:

```text
delta_3=atan(1/sqrt(5))<pi<delta_3+pi,
s/(m q)=tan(pi/10),
delta_2=9pi/10,
c beta=4pi/5<delta_2.
```

The reconstruction gives

```text
p=pi(1+2sqrt(5)),
a=alpha/p>0,
b=(alpha+m beta)/p<1/2.
```

Thus the tuple is exactly spectral, band-consistent, modal, and strictly
interior.

### Sign certificate and mass defect

Using only the packet's rational input bounds, rational interval propagation
gives the following enclosing intervals. The printed endpoints below are
rounded outward.

| Quantity | Recomputed enclosure |
|---|---|
| `Ttheta` | `(0.8804223283, 0.8804230931)` |
| `Dtheta` | `(1.7459566607, 1.7459601926)` |
| `U` | `(0.2418849936, 0.2418882780)` |
| `K` | `(-0.0714927785, -0.0714911626)` |
| `G` | `(-0.6738999447, -0.6738906765)` |
| `Xi` | `(-0.1809243829, -0.1809159067)` |

Each enclosure lies strictly inside the wider interval printed in W5. The
input bounds are themselves outward: their endpoint squares bracket `5` and
`2`, while `s^2=(5-sqrt(5))/8` gives the stated bracket for `s`. The strict
signs of `G` and `Xi` therefore follow from exact rational interval
arithmetic, not from an unvalidated floating-point sample.

Independent expansion of the two norm formulas gives exactly

```text
Delta_M
=(-625sqrt(10+2sqrt(5))
  +125sqrt(50+10sqrt(5))
  +250sqrt(50-10sqrt(5))
  +320sqrt(5)pi+3456pi)/3200.
```

This is positive because the sole negative radical is greater than `-2500`,
the term `3456pi` is greater than `10368`, and all other terms are positive.
Hence the tuple fails `E_mass` exactly. W5 explicitly identifies that defect
and does not claim a counterexample to `G>=0`, `PHI-SIGN`, or `KP-DET` on the
complete system. The exact witness portion is accepted.

### First load-bearing gap in the near-one theorem

Section 3 asserts that "standard Sturm continuity and the fixed mode indices"
give the phase and norm limits uniformly while the switch positions are
allowed to vary with `m`. The stated hypotheses only bound `alpha` away from
its endpoints. The proof does not supply the required compactness and
uniform-continuity chain:

1. It does not show uniform spectral convergence for the moving
   three-layer densities, or derive `c->2/3` and the two total-phase limits
   independently of the moving switches.
2. It does not first use the modal bounds to obtain compactness of `beta`,
   extract all possible phase cluster points, and pass the exact norm
   formulas to `I3hat->3pi/4` and `I2hat->pi/2` uniformly.
3. It uses endpoint separation of `theta` and boundedness of
   `X Ttheta^2/C^2` before proving that every cluster point satisfies
   `cos(theta)=(2/3)sin(2theta/3)` and that compactness upgrades exclusion of
   `theta=0,pi/2` to a uniform separation.

These omissions are repairable and the proposed limit calculation is
consistent: after the missing compactness step, the mass identity gives
`C=(2/3)s`, then `c s/C=1`,

```text
U->cos((2/3)alpha)-cos(alpha)>0
```

uniformly on `[eta,pi-eta]`, while `Dtheta` grows like a positive multiple of
`m^2/(m^2-1)`. However, under the packet's first-time audit standard, this
repair cannot be supplied silently. The restricted near-one statement is
therefore downgraded from an accepted theorem to a plausible conditional
claim pending the explicit uniform compactness proof.

## Joint boundary and decision

All divisions used in W4 and in the exact W5 witness have strictly nonzero
denominators on the stated open domain. Excluded switch-collision and
mode-index faces are not imported as equality cases. Exact identities are
kept separate from the rational interval sign certificate. The accepted W4
and exact-witness statements do not prove or refute `PHI-SIGN` or `KP-DET`.
Those obligations remain open.

The overall verdict is `REPAIRABLE_GAP` solely because W5 presents the
restricted near-one statement as a theorem without the load-bearing uniform
compactness and branch-continuity argument required by its moving-switch
hypotheses.
