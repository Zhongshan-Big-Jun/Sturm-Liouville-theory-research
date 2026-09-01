PARTIAL

# Exact exclusion of the simultaneous near-one left-collision face

## Input audit

All packet-bound hashes were verified before the argument.

```text
problem_contract.md                                           67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
route-01-transfer-schur/derivation.md                         a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
route-03-phi-exact/worker_result.md                           6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3
route-04-mass-g-wave/accepted_package.md                     cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192
route-04-mass-g-wave/repair/near_one_repair.md                8defee6c05565313b5d9f2e4365d102349c32e8cf9ef04bde6f288ace6c30314
route-04-mass-g-wave/repair/reaudit.json                      3f88a6ed8cf6da7f7adc41a195776fbfa9f00c8cec97153156a98f773a0c573d
```

## Exact finding

There is no sequence of complete admissible tuples satisfying

```text
m_j->1+,
alpha_j->0.
```

Equivalently, there exist `epsilon_0>0` and `delta_0>0` such that the
complete admissible phase system has no tuple in

```text
1<m<1+epsilon_0,
0<alpha<delta_0.
```

This is a strict sequential obstruction. It uses the full exact mass
equation and no numerical or formal-series premise.

## Proof

Assume for contradiction that complete admissible tuples indexed by `j`
obey `m_j->1+` and `alpha_j->0`. The exact modal inequality gives
`0<beta_j<3pi/2`. After passage to a subsequence, all phase variables have
limits in their compact closures.

The switch-uniform min-max argument in the bound near-one package applies
without a fixed-switch assumption. Hence

```text
c_j->c_0=2/3,
alpha_j+m_j beta_j+theta_j->3pi/2.
```

It follows that

```text
beta_j+theta_j->3pi/2.                              (1)
```

The apparent singularities in the norm formulas are removable even though
`alpha_j->0`. The two spectral equations give

```text
X_j=Z_j tan(alpha_j),
Y_j=-T_j tan(c_j alpha_j).                          (2)
```

Therefore the left-layer norm terms can be written as

```text
m_j^2 Z_j^2 Js(alpha_j)/cos(alpha_j)^2,
m_j^2 T_j^2 Js(c_j alpha_j)/cos(c_j alpha_j)^2,
```

and both tend to zero. Using `(1)` in the remaining middle and right terms
gives the exact limits

```text
I3hat_j->Jc(3pi/2)=3pi/4,
I2hat_j->Js(pi)=pi/2.                               (3)
```

Let `theta_j->theta_0`, and put

```text
C_0=cos(theta_0),
s_0=sin(2theta_0/3).
```

Passing the full exact mass equation

```text
C_j^2 I2hat_j=c_j^3 s_j^2 I3hat_j
```

to the limit and using `(3)` yields

```text
C_0^2=(4/9)s_0^2.                                  (4)
```

Both quantities are nonnegative on the closed phase interval, so `(4)`
implies

```text
C_0=(2/3)s_0.                                      (5)
```

Neither endpoint is possible. At `theta_0=0`, equation `(5)` would read
`1=0`; at `theta_0=pi/2`, it would read
`0=(2/3)sin(pi/3)`. Thus `C_0>0`, `s_0>0`, and

```text
s_0/C_0=3/2.                                       (6)
```

On the other hand, the transfer quantities in `(2)` have the limits

```text
Z_j->sin(beta_0+theta_0)=-1,
T_j->cos(c_0(beta_0+theta_0))=-1.
```

Since `alpha_j>0`, division by `alpha_j` in `(2)` is legitimate and gives

```text
X_j/alpha_j->-1,
Y_j/alpha_j->2/3.                                  (7)
```

Finally divide the exact band equation

```text
Y_j=-s_j X_j/C_j
```

by `alpha_j` and pass to the limit. Equations `(6)` and `(7)` give the
contradiction

```text
2/3=s_0/C_0=3/2.
```

This proves the sequential exclusion. If no uniform `epsilon_0,delta_0`
existed, choosing a tuple with `m<1+1/j` and `alpha<1/j` would produce the
excluded sequence, proving the equivalent uniform wedge statement.

## Admissibility and denominator audit

- Every tuple in the contradiction hypothesis satisfies the full spectral,
  band, mass, modal-index, and strict interior reconstruction constraints.
- Compactness of `beta` follows from the exact one-zero modal inequality,
  not from a branch ansatz.
- The norm limits use the spectral equations to remove both `0/0` forms.
- Division by `alpha_j` is valid because every reconstructed switch is
  strictly interior, so `alpha_j>0`.
- Division by `C_j` is used only after the mass equation proves that its
  limiting value is strictly positive.
- No division by `X`, `Y`, `sin(beta)`, or `sin(c beta)` is made.
- No complete branch existence is assumed or proved. The theorem says that
  any complete branch approaching `m=1` cannot enter the left-collision
  wedge.

## Remainder gap and effect on PHI-SIGN

There is no asymptotic remainder gap in the exclusion theorem. In
particular, no complete scaling family can have `alpha/(m-1)` bounded, let
alone tending to zero, while `m->1+`; if such complete tuples exist
arbitrarily near `m=1`, the uniform wedge instead forces
`alpha/(m-1)->+infinity`.

The obstruction supplies neither `G<=0` nor `Xi<=0`. It shows that the
previously unresolved simultaneous face contains no complete admissible
tuple and therefore cannot falsify `G>=0` or `PHI-SIGN`. The exact remaining
gap is the sign of `G`, `Xi`, and `Phi` on complete tuples outside this
excluded wedge, together with existence and global continuation of those
tuples.

decision_delta: The full mass equation is incompatible with the spectral and band limits on `m->1+`, `alpha->0`; this simultaneous face is exactly excluded, but no sign claim for `G`, `Xi`, or `Phi` away from the excluded wedge is added.
