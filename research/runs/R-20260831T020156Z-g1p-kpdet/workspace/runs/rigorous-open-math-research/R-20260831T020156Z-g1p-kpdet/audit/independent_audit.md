PASS

# Fresh independent adversarial audit

## Bound package

- Run: `R-20260831T020156Z-g1p-kpdet`.
- Auditor role: fresh independent verifier. The auditor did not author the candidate or either route.
- `problem_contract.md`: SHA256 `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `candidate_proof.md`: SHA256 `e9305a8795b31cd528555108c5268b92664e63f48ab728592f2947336a050188`.
- `direct_attempt.md`: SHA256 `c6f8343eede001af58b50bb4b229cfd381e06323ada14c1cfe381fc3dbe4ed58`.
- `route-01-transfer-schur/derivation.md`: SHA256 `a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3`.
- `route-02-jacobi-falsifier/derivation.md`: SHA256 `1e664a7742ea6a9e5674cc2499e7a47c6c4955309ed14d0b9e1e0b164f851f5d`.

All five hashes were recomputed before the audit and matched the frozen values.

## Obligation findings

### P1. Strict lower-right pivot: PASS

On the final layer, direct differentiation of

```text
Q=(A/B)cos(k_3t)/sin(k_2t),
A/B=-c sin(theta_2)/cos(theta_3)
```

gives

```text
Q'(b)=-c[k_3 tan(theta_3)+k_2 cot(theta_2)].
```

The Dirichlet cross Green kernel has value
`sin(theta_3)cos(theta_3)/k_3`, while the Neumann cross Green kernel has
value `-sin(theta_2)cos(theta_2)/k_2`. The derivative-jump convention for
`-d^2/dx^2-lambda rho` gives these signs. Since `v=sqrt(2)u_2` on the
half-string, the whole-string Wronskian is `W=v^2Q'/2`, so the penalty
coefficient has the stated factor `2`.

The modal domain gives `0<theta_3<pi/2` and
`theta_2=c theta_3 in (0,pi/2)`. Therefore both

```text
tan(t)-sin(t)cos(t)=sin(t)^3/cos(t)
cot(t)-sin(t)cos(t)=cos(t)^3/sin(t)
```

are strictly positive, and `R/(R-1)>1`. Hence
`gamma_2-b_0>0` with no endpoint or equality exception in the contracted
finite-interior domain. The conclusion `(Kp_odd)22<0` follows through the
positive congruence factor.

### P2. Schur equivalence: PASS

Writing `delta=gamma_2-b_0>0`, the normalized matrix is

```text
M=[[a_0-gamma_1,b_0],[b_0,-delta]].
```

Its determinant is exactly

```text
det M=-delta[a_0-gamma_1+b_0^2/delta]
     =(b_0-gamma_2)S_KP.
```

The normalization from `Kp_odd` to `M` is a positive scalar and diagonal
congruence, so it preserves the determinant sign. Thus
`det Kp_odd>0` if and only if `S_KP<0` on the whole contracted branch.

### P3. Five-phase reduction and reconstruction: PASS

The right-to-left transfer formulas were re-derived on all three density
layers. They give the two spectral equations exactly, including the signs of
`Z` and `T`. The modal inequalities imply `X<0` and `Y>0`, and the two band
conditions reduce without sign loss to

```text
A/Bv=-c s/C,
Y=-sX/C.
```

The weighted half-masses satisfy

```text
I3=I3hat/p,
I2=I2hat/(c p).
```

Consequently normalization at the right switch is exactly equivalent to
`C^2 I2hat=c^3 s^2 I3hat`. No sign is lost when the squared mass identity is
used, because the normalized amplitude ratio and `-c s/C` are both strictly
negative.

Conversely, an admissible tuple reconstructs

```text
p=(alpha+m beta+theta)/L,
a=alpha/p,
b=(alpha+m beta)/p,
lambda_3=p^2/R,
lambda_2=c^2p^2/R.
```

The strict phase constraints give `0<a<b<L`, the positive first
Dirichlet-Dirichlet mode, and the one-zero Dirichlet-Neumann mode. The
spectral, band, and mass equations then recover both normalized switch
relations. Thus the stated admissible phase system neither adds nor removes
branch points.

The left Green values, the left penalty, and the right pivot reduce to

```text
S_KP=K0[Aalpha/Y^2+Ttheta^2/(s^2Dtheta)].
```

Here `K0`, `Y^2`, `s^2`, `C^2`, and `Dtheta` are strictly positive. Using
`Y=-sX/C` therefore proves, without losing equality cases,
`S_KP<0` if and only if `Phi<0`, and `S_KP=0` if and only if `Phi=0`.

### P4. Jacobi flux and locking geometry: PASS

For each Jacobi equation, differentiating the projective Wronskian gives the
stated source jump. At a switch,
`lambda_3w(x_j)^2=lambda_2v(x_j)^2`, so the two projective fluxes have equal
jumps and equal zero initial values. This proves the common piecewise-constant
flux law.

The moving-level conditions give
`delta(a)=-y_1Q'(a)/c>0` and
`delta(b)=-y_2Q'(b)/c>0`. On `(a,b)`, strict decrease of `Q` from `c` to
`-c`, with `0<c<1`, gives `|w|<v`. Since the common flux is negative,
`delta'<0` on both sides of the unique zero `z` of `w`. The identity
`P=-psi(z)w'(z)`, together with `P<0` and `w'(z)<0`, gives `psi(z)<0`.
This yields exactly one simple downward locking point in `(a,z)` and the
integral identity `(P4a)`. Its right side increases continuously from zero
to infinity because `1/w^2` has a nonintegrable second-order pole at the
simple zero `z`.

The final-layer boundary representations give the displayed formulas for
`alpha(b)` and `beta(b)`. Substitution of the final flux and the second
moving-level condition yields

```text
y_1v(a)^2/[y_2v(b)^2]
=R/(R-1)[tan(theta_3)+c cot(theta_2)]/Ttheta-1
=(gamma_2-b_0)/b_0>0.
```

Thus `(P4b)` has the correct sign and factors. The package correctly uses
the locking theorem only to close this quotient-only route, not to assert
existence of a Jacobi kernel.

## Definition, logic, boundary, and adversarial audits

- Definition audit: PASS. The parity fields, Wronskians, density phases,
  weighted normalization, Green boundary conditions, and matrix convention
  agree across the four bound artifacts.
- Logic audit: PASS. P1-P4 are reductions and necessary geometry only. No
  implication is reversed, and the unresolved phase inequality is not used as
  a premise.
- Boundary audit: PASS for the contracted scope. All denominators are
  protected by the strict finite-interior and modal-domain inequalities. The
  excluded switch-collision and mode-boundary faces are not silently included.
- Adversarial audit: PASS. Independent sign and factor derivations were made
  for both outer switches, the mass normalization, the determinant factor,
  the flux jumps, and the endpoint ratio. No finite or numerical experiment is
  used.

## Status boundary

The audited result is a `RIGOROUS_PARTIAL_RESULT`. The package does not prove
`Phi<0`, does not construct an admissible tuple with `Phi=0`, and therefore
does not prove or refute `KP-DET`. `KO-DET`, simultaneous sector singularity,
and global G1 prime remain outside the package. The explicit remaining
obligation is exactly the sign of `Phi` on the complete admissible phase
system.

There are no critical errors and no repairable gaps in P1-P4.
