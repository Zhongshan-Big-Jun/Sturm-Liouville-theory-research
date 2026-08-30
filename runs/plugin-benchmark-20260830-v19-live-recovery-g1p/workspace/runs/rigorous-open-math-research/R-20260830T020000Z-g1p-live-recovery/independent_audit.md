PASS

# Fresh independent adversarial audit

## Audit identity and decision

- Run: `R-20260830T020000Z-g1p-live-recovery`.
- Role: fresh independent auditor. I did not author either route or the candidate synthesis.
- Protocol: `rigorous-open-math-research` v1.9.0, Phase 7-8 synthesis and adversarial audit, with the dual-track audit rules.
- Authorized project read set: exactly the eight artifacts listed in the canonical resume receipt.
- Candidate SHA256: `4e688ad5d7c0e3f4869e4aa43cad823549fc66db76bcd9293341eb85b0d8e556`.
- Verdict: `PASS`.
- Project-ingestion decision: the strict partial claims P1-P3 are mathematically acceptable for ingestion as `RIGOROUS_PARTIAL_RESULT` claims. They do not complete `KP-DET`, `KO-DET`, or the full negative-definiteness target.

`PASS` here means that every mathematical claim actually promoted by the partial package survived the independent audit. It does not mean that the open determinant theorem is complete.

## Definition audit: PASS

1. The package keeps the exact conditional scope: one prescribed finite-interior, symmetric, `n=2`, INF branch with finite `R>1`. It does not silently add branch existence, branch uniqueness, SUP, nonsymmetric sectors, `n>=3`, boundary collapse, or global `G1'`.
2. `Kp_odd` and `Ko` remain distinct. The odd-sector calculation uses

```text
H=E G_D(lambda_3) E-c^2 G_N(lambda_2),
E=diag(1,-1),
```

and the candidate never substitutes the raw `Ko` formula for `Kp_odd`.
3. The half/full normalization is consistent. With `v=sqrt(2)u_2` and `w=sqrt(2)u_3`, the half residual is exactly the full residual divided by `lambda_3`, and the factor `lambda_2 diag(v)Hdiag(v)` becomes `2lambda_2 diag(u)Hdiag(u)`.
4. The `U^2` congruence is correct:

```text
(2lambda_2)^(-1)U^(-2)Kp_odd U^(-2)
= [[a-gamma_1,b],[b,b-gamma_2]],

gamma_j=-d_j/(2lambda_2u_j^4)>0.
```

The fourth power in `gamma_j` is required and is present.
5. The local use of `tau` in the W1 normalization and `tau=R-1` in W2 is confined to separate route derivations and does not enter a mixed formula. It is a notation reuse, not a mathematical ambiguity in the synthesis.

## Logic audit: PASS

### Inertia and first-zero reduction

For a continuous path of real symmetric matrices starting negative definite, a positive determinant prevents a zero eigenvalue and hence preserves inertia. Therefore the trace inequalities are not independent once both determinant inequalities are proved. At a first determinant zero, the relevant sector is negative semidefinite. This validates P1 conditional on the strict near-one anchor declared in the contract.

### Semiseparable Green reduction

For `i<=j`, the one-dimensional Green factorization and the band identity give

```text
H_ij
=epsilon_i epsilon_j C_D w(x_i)r_D(x_j)
 -c^2 C_N v(x_i)r_N(x_j)
=v(x_i)h_j.
```

Symmetry then forces the normalized matrix to be `[[a,b],[b,b]]`. This is an exact identity, not a truncation or fit.

On the final density-`R` layer, the unique zero of the second Dirichlet-Neumann mode lies before `x_2`. Hence

```text
0<theta_3<pi/2,
0<theta_2=c theta_3<pi/2.
```

The Green diagonal formulas consequently have signs

```text
G_D(x_2,x_2;lambda_3)>0,
G_N(x_2,x_2;lambda_2)<0,
```

so `b>0`. The sign is compatible with the stated resolvent convention.

### Equality and singular cases

At a first loss, the congruent matrix `M` is negative semidefinite and singular. Since `b>0`, it cannot be the zero matrix, both diagonal entries are strictly negative, and its kernel is one dimensional with same-sign nonzero components. Its singularity is exactly

```text
gamma_2>b,
gamma_1-a=b^2/(gamma_2-b).
```

The abstract assignment in W1 gives a valid algebraic equality witness and is correctly labeled as not being a branch counterexample. It proves only that the structural signs alone do not close `KP-DET`.

### Jacobi equations and moving-level conditions

The INF jump signs and transverse switch velocities give

```text
dot(rho)=(R-1)[y_1 delta_a+y_2 delta_b]
```

on the left half, with a reflection-odd full perturbation. Squared base eigenfunctions are reflection-even, so both eigenvalue derivatives and `dot(c)` vanish. The parity-crossed endpoint conditions are correct: `phi'(L)=0` and `psi(L)=0`. Strict Dirichlet-Neumann interlacing puts each cross problem off its spectrum.

The Wronskian sign used in the quotient calculation is valid. Indeed,

```text
W_h'=(lambda_2-lambda_3)rho v w.
```

It decreases from zero while `w>0`, then increases after the unique zero of `w`, and its endpoint value `-w(L)v'(L)` is still strictly negative. Thus `W_h<0` throughout the open half interval. Differentiating the residual, including switch motion, yields exactly

```text
dot(F)=-tau Kp_odd y.
```

Differentiating `Q=w/v=e_jc` yields the displayed two moving-level conditions. The factor relating this level residual to `F_j` is nonzero at a band point, so the claimed equivalence with `Kp_odd y=0` is exact.

### Off-diagonal sign

For the impulse `y=(0,1)`, Sturm comparison places the first zero of the right-Neumann solution at `lambda_2` strictly to the left of the zero of `w`, so `r_N(b)>0`. Wronskian matching gives the left coefficient `A<0`. Sturm separation for the right-Dirichlet solution at `lambda_3` gives `r_D(b)>0`, and the second matching coefficient satisfies `B>0`. Therefore

```text
dot(F_1)=c^2v(a)^2(A-B)<0,
```

and `dot(F_1)=-tau(Kp_odd)_12` proves `(Kp_odd)_12>0`. This independently confirms the double-zero exclusion.

### Transfer and branch-chart identities

In transverse coordinates, `y=E(p,q)`. Reflection makes the antisymmetric residual derivative equal to the left residual derivative, so

```text
D_(p,q)A=-tau Kp_odd E.
```

Since `det(E)=-1`, the determinant identity is correctly

```text
det D_(p,q)A=-tau^2 det Kp_odd.
```

For symmetric switch motion, the sector decomposition of `J=diag(s)K` gives

```text
D_(a,b)S=-tau E Ko.
```

Thus the implicit-function chart uses only `Ko^(-1)` and is valid precisely when `Ko` is nonsingular. It does not invert `Kp_odd` or the singular full Jacobian. The package correctly leaves the simultaneous-singularity case outside this chart.

## Boundary audit: PASS

- `R=1` and `R=infinity` are used only as strict anchoring regimes and are not included in the target quantifier.
- Finite-interior assumptions ensure nonzero switch values, positive `gamma_j`, strict angle inequalities, and valid diagonal congruences.
- Switch collision and boundary-collapse charts are explicitly outside the contract.
- The zero matrix, corank-one, equality, higher-order crossing, and simultaneous sector-singularity cases are all distinguished.
- The one-sided Taylor sign is correct: if the first nonzero derivative is order `m`, negativity on the smaller-`R` side requires `(-1)^m kappa^(m)(R_*)<0`.

## Adversarial audit: PASS

- No numerical evidence or finite scan is used.
- No external citation carries a load-bearing step.
- The remaining scalar equality is not disguised as a proof of `KP-DET`.
- The crossing-form discussion is explicitly a certificate template and does not claim an unproved sign.
- The `Ko`-regular chart is conditional and does not hide the simultaneous-singularity exception.
- The untouched even-sector problem is not inferred from the odd-sector work.
- The central missing lemma is not merely restated under a new name: the package records both its scalar W1 form and its Jacobi W2 form, while honestly leaving its exclusion open.

## Exact residual open obligations

1. `KP-DET` remains open at the corank-one first-loss alternative. One must exclude

```text
gamma_2>b,
gamma_1-a=b^2/(gamma_2-b),
```

equivalently exclude the same-sign one-dimensional Jacobi kernel or prove the forbidden crossing sign.
2. The W2 analytic branch chart does not cover a point where both `Kp_odd` and `Ko` are singular. This is a genuine method boundary, but it is not an independent third root theorem: it is nested inside the unresolved `KP-DET` analysis and would also disappear after a proof of `KO-DET`.
3. `KO-DET` remains entirely open on the all-finite-`R` branch. Once `KP-DET` and `KO-DET` are proved, the trace claims follow from P1 and require no separate global estimate.

Global branch construction, SUP, nonsymmetric branches, boundary collision, `n>=3`, and global `G1'` remain outside the contract rather than residual defects of this package.

## Dual-track status and residual risk

The present verdict is the independent informal audit layer. No Lean scaffold, Lean full verification, or paper-level assembly was in the authorized minimal read set, so those layers were not checked. Under the dual-track protocol, any canonical gate that separately requires a Tier 0 or Tier 1 scaffold must verify that artifact before final promotion. This does not change the mathematical `PASS` for the strict partial claims audited here.

## Hash-bound read set

| Artifact | SHA256 |
|---|---|
| `problem_contract.md` | `38bcbaccfa6f00209b9cfe2796950318b961728ac99e2a493bcec76c696e2043` |
| `whiteboard-01.md` | `37d3977f9e99ddd3804970e388ace546c0e79ba3d88c5c32e9894d0e079fd23b` |
| `closure_gate-01.md` | `71261e957d6d900509d570976a7c919f58824f79e332d9a50fa7fb1de79091f3` |
| `candidate_proof.md` | `4e688ad5d7c0e3f4869e4aa43cad823549fc66db76bcd9293341eb85b0d8e556` |
| `route-01-spectral-coercivity/route_report.md` | `1acb935d917daf26bec63f45673402d51c6fa3559faac3c7333070a4e6371681` |
| `route-01-spectral-coercivity/derivation.md` | `6beedc48be799450d8e8430dcfd39787af801d281afb066896f5054dda084416` |
| `route-02-firstzero-jacobi/route_report.md` | `6e951602458330c22f90e52e45997c3a582297c0b80a34bc1cef2916ee1f0f68` |
| `route-02-firstzero-jacobi/derivation.md` | `ce72a80d18a5d94abdc0cb5627db11b6cebe950fe48438c79d6513cc4db69542` |
