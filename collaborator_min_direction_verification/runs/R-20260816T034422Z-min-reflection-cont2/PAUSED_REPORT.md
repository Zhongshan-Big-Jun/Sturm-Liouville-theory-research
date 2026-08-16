# Minimum-side global reflection: paused research report

Paused by explicit user instruction at `2026-08-16T14:59:44+08:00`, before
the continuation deadline.  All subagents and research computations were
stopped.  No H/J proposal was created after the pause request.

## 1. Current canonical state

Canonical Blueprint:

```text
sha256:b93b42029f95d55489c71e344af329220c3182ff07c2d0b57b9e170b7d4f7056
146 nodes, 324 edges
```

Evidence inventory:

```text
sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
```

Submission `SUB-20260816-1346-MINREFLECTION-C2AD-R2` was independently
reviewed and deterministically merged.  It added these trusted nodes:

```text
INF-NGE2-MPO3A-MIN-FOREST-CHARGE-R36
CLM-NGE2-MPO3A-MIN-FOREST-CHARGE-R36
INF-NGE2-MPO3A-MIN-DEFECT-TRANSLATION-R36
CLM-NGE2-MPO3A-MIN-DEFECT-TRANSLATION-R36
```

The first claim gives the all-dimensional path-forest/interval-charge
expansion of `det(H)`.  The second gives the exact positive-cell endpoint
defect decomposition and proves that common interface translation moves the
two adjacent eigenvalues at the same first-order speed.  Neither claim signs
`det(H)` or proves reflection.

The previously trusted `n=2, mu=2` global reflection theorem and compact
`mu=2` reflection/exclusion strips remain unchanged.

## 2. Independently pre-reviewed, proposal-worthy, but not canonical

### C2-H: arbitrary-`mu` local weak-contrast interface theorem

For every fixed finite `mu>1` and strict physical positive-negative phase
pair, an explicit phase-dependent `tau>0` is proved such that

```text
1<R<min(rB^2,1+tau)  =>  Phi>0.
```

Applying this separately to the actual left and time-reversed right phase
pairs of an asymmetric `n=2` word gives `H>0` when

```text
R-1<min(tau_L,tau_R).
```

There is no phase-uniform positive infimum and therefore no new global
weak-contrast reflection theorem.  The repaired proof and exact checker
passed independent pre-review.

### C2-J: complete conditional bridge to `n=2` global reflection

The physical/common-angle bridge was rederived without treating historical
R14/R17 artifacts as trusted premises.  The exact proved implication is:

```text
G_1,...,G_4>0 on every retained g<1,rB>1 point of (0,1)^3
  => B_i>0 => D(r)>0 => Phi>0
  => H>0 => det(L_-)>0 => partial_q A_2<0
  => at most one fixed-mu root and every root is reflection fixed.
```

The `g>=1` half-domain is analytic and needs no coefficient certificate.
Independent pre-review found exactly one open premise: complete retained-cube
coverage in the displayed antecedent.  The conditional theorem is
proposal-worthy; the unconditional theorem is not proved.  Proposal,
immutable review, and integration were deliberately not started after the
pause request.

## 3. Exact and certified coefficient progress, not canonical

Use `L=[0,1/64]`, `I=[1/64,63/64]`, and `H=[63/64,1]` in coordinate order
`(k,t,y)`.  Sixteen of twenty-seven complete dyadic cells now have exact or
directed-Arb conditional certificates:

```text
III,
LII, HII, IHI, IIL, IIH,
LIL, HIL, LHI, IHH,
HIH, HHL, HHI, HHH,
LHL, IHL.
```

The eleven remaining cells are

```text
LLL, LLI, LLH,
ILL, ILI, ILH,
HLL, HLI, HLH,
LIH, LHH.
```

The first nine are the entire low-`t` slab.  `LIH` is the remaining
upper-`y` annulus and `LHH` is the remaining mixed high-`t`/high-`y`
dependency region.

Additional exact progress:

- A complete original-coordinate collar `t>=1-2^-17` is certified.
- The 21 residual `IHL` boxes were closed by a targeted exact endpoint-order
  contractor: 2,319 visits, zero stack, zero atomic failures.
- On the full inner cube, the stronger bounds
  `Pplus*Nhat_i/(g*Knew*cp^4)<1/4` were certified for all four coefficients:
  5,848,407 directed-Arb boxes, zero singular/unresolved boxes, empty stack.
- On the complete physical retained `t=0` boundary, the three nonzero
  limiting ratios are also rigorously below `1/4`; the five complementary
  compact charts all terminate without unresolved boxes.  At `k=0`, the
  critical ratio reduces to
  `x^2(theta-x)/(2(theta+x))`, `x=-tan(theta)`, and has a direct analytic
  `<1/4` proof.

The last two quarter bounds provide substantial boundary margin, but an
effective positive-`t` collar connecting the exact `t=0` boundary to all
nine low-`t` cells has not yet been frozen.

## 4. General-`n` determinant progress and exact blockers

- The trusted forest formula reduces the first coupled case `n=3` to
  `q_1q_2+e(q_1+q_2)>0`, with `e>0`.
- Full shared-contrast and two-momentum elimination gives the loaded central
  matrix
  `[[F_2/v_1,s_2],[s_2,E_2/v_2]]` and
  `det=-D_mid/(v_1v_2)`.  Existing physical equations do not compare
  `gamma_3/v_1` with `-gamma_4/v_2`, so the sign remains open.
- The total forest charge is the unsigned difference
  `f^T P^(-1)f-gamma^T f`.
- Linear cross-root Green/Picone combinations cannot prove endpoint order:
  a full-rank elimination audit shows that an uncontrolled cross-mode skew
  polarization necessarily remains.
- The endpoint defect has no cellwise one-sided sign; strict physical local
  cells realize both drift signs.  No complete physical root counterexample
  was found.

## 5. Accurate final status

```text
n=2, mu=2 global minimum reflection: trusted from earlier work
n=2, arbitrary mu local weak-contrast H>0: proved and pre-reviewed, not submitted
n=2, arbitrary mu coefficient-cover => global reflection: proved conditional bridge, not submitted
n=2 full coefficient cube: open; 16/27 full dyadic cells effective
n>=3 determinant orientation det(H)>0: open
all-n minimum global reflection: open
physical asymmetric or determinant-sign counterexample: none found
```

## 6. Exact resume point

If research is resumed, the shortest faithful path is:

1. create one immutable proposal for C2-H and the C2-J conditional bridge,
   then obtain formal independent review and deterministic integration;
2. use the proved `<1/4` boundary margin to construct an effective low-`t`
   collar and close the nine low-`t` cells;
3. resolve `LIH` and `LHH` in stable coordinates;
4. only then invoke C2-J to obtain unconditional arbitrary-`mu`, `n=2`
   reflection;
5. treat `n>=3` separately at the loaded central-block sign, not by assuming
   the stronger matrix inequality `H>0`.

No further action was taken after the pause request beyond this status
organization.
