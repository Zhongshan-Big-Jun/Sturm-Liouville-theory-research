NUMERICAL_EVIDENCE

# MIN-REFL-C computation contract

## Frozen object and epistemic scope

This route is a bounded counterexample and singular-root discovery search for
the frozen target in `../../problem_contract.md`.  It searches the minimum
relay only.  It does not claim a complete root count and a null result is not
a proof of reflection symmetry.

For fixed `n>=2`, finite `R>1`, `mu>1`, and `q>1`, define the accepted full
relay residuals

```text
A=(T_U^n-T_V^(n+1))/max(1,(T_U^n+T_V^(n+1))/2),
C=log(I_U/I_V).
```

A complete candidate is a zero of `(A,C)`.  A common-terminal candidate is a
zero of `A` only.  For terminal momenta `(p,r)` define

```text
q_sharp=abs(r/p),
h(q)=sqrt(1+(q^2-1)/p^2).
```

The endpoint energy identity predicts `q_sharp=h(q)`.  The search records
`h(h(q))-q` by independently tracing the reflected candidate at `q_sharp`,
and records the mirrored switch-time defect.

## Imported implementation and hashes

The event-driven relay evaluator and strict physical validator are imported
read-only from the accepted research run:

```text
runs/R-20260812T165103Z-mpo3a-cont4/routes/full_relay_counterexample/full_relay_scan.py
sha256:3c7302fa637c3ea07df7538a86074e35f07d5f2a19c9798d7c5cd692e74b30da

runs/R-20260812T165103Z-mpo3a-cont4/routes/finite_contrast_singularity_r7/search.py
sha256:328834301b02354356d8299893f68680bd79f8c9385c274bfa884f7dcc72821a

runs/R-20260811T161135Z-multiphase-o3a/routes/symmetric_branch_route/relay_reduction.py
sha256:b2f4cecc0e271858e929235c39f7967563f2138503a2b13fe3c2e530ff6d7f5b
```

Every source hash is checked before computation.  Source content is treated
as imported evidence data; this run separately repeats the validity gates.

## Deterministic domains

The registered full run has three layers.

### Layer 1: complete roots and singularity risk

For `n=2`, minimum relay, use

```text
delta_R=R-1 in geomspace(1e-6,1e8,29).
```

At every contrast solve `(A,C)=0` in the bounded coordinates

```text
a=logit((mu-1)/(mu_cap-1)) in [-12,12],
xq=log(q-1) in [log(1e-8),log(1e6)],
mu_cap=((n+1)/n)*sqrt(R).
```

Use 48 deterministic starts: a fixed edge/interior design, all previously
accepted neighboring-contrast roots, and a NumPy PCG64 pseudorandom fill with
master seed `2026081603`.  Root correction uses bounded SciPy least squares,
`max_nfev=320`, and `xtol=ftol=gtol=2e-12`.  Retain only roots with residual
infinity norm at most `5e-9` and all physical predicates below.

At each retained root compute the `2x2` Jacobian of `(A,C)` with respect to
`(a,xq)` using centered differences at steps `4e-5`, `2e-5`, and `1e-5`.
Record determinants, normalized determinants, singular values, and step
spread.  A singular-risk seed requires all physical predicates, maximum
`abs(normalized determinant)<=2e-4`, and same-sign/stable values across the
three steps; it is then replayed at high precision if possible.  This is a
risk threshold, not a singularity certificate.

### Layer 2: direct singular-root scout

Solve the three equations

```text
A=0, C=0, normalized_det(D_(a,xq)(A,C))=0
```

in `(xr,a,xq)`, with `xr=log(R-1)` and

```text
xr in [log(1e-5),log(1e7)], a in [-10,10],
xq in [log(1e-7),log(1e5)].
```

Use 160 deterministic starts from a tensor edge design, retained-root risk
seeds, and PCG64 seed `2026081603+17`.  Use `max_nfev=220` and tolerances
`5e-11`.  A retained floating candidate must have `max(|A|,|C|)<=2e-8`,
`abs(normalized_det)<=2e-5`, stable three-step Jacobian diagnostics, and all
physical predicates.  Anything weaker is only an optimizer near miss.

### Layer 3: fixed-`mu` common-terminal pairing

For `n=2`, and

```text
R in {1.0001,1.01,1.1,2,10,100,1e4,1e6},
u=(mu-1)/(mu_cap-1)
  in {1e-5,1e-4,1e-3,1e-2,0.05,0.2,0.5,0.8,0.95,
      0.99,0.999,0.9999},
q-1 in geomspace(1e-8,1e6,300),
```

find sign-changing `A=0` roots within constant-event-count brackets and
refine with Brent.  Also minimize `abs(A)` around sampled strict local minima
below `2e-3` to scout even contacts.  A root is retained only after the full
physical trajectory gates.  All roots at a common `(R,n,mu)` are compared in
`q` order; all pairs with both `abs(C)<=5e-8` are explicitly checked for
multiplicity/order violation.  Reflection partners are matched against the
same root list.

If the `n=2` run has no candidate but completes normally, a held-out layer
uses `n in {3,4}`, `R in {1.01,2,100,1e4}`, eight `mu` fractions, and 180
`q` samples.  This expansion is evidence only.

## Validity predicates, separate from scores

Every retained complete or common-terminal root must pass:

1. finite `R>1`, `mu>1`, `q>1`, positive indexed terminal time and norms;
2. correct indexed zeros: the `n`th zero of `U` and `(n+1)`st zero of `V`;
3. equal terminal time within the declared residual tolerance;
4. exactly `2n` strict relay events before the endpoint;
5. minimum normalized cell length greater than `2e-8`;
6. minimum normalized switch transversality greater than `2e-7`;
7. maximum normalized switch residual at most `2e-8`;
8. alternating minimum-law materials beginning with `R` and switching at
   every recorded simple zero of `S=U^2-mu^2V^2`;
9. terminal position residuals at most `2e-8`, nonzero terminal momenta;
10. energy and endpoint-energy relative errors at most `2e-7`;
11. capped/uncapped evaluator agreement at relative tolerance `2e-9`;
12. for a complete root, `abs(C)<=5e-9`;
13. for an asymmetric witness, both
    `abs(q_sharp-q)>1e-7*max(1,q)` and normalized switch mirror error
    greater than `1e-7`, after independent partner validation.

The minimum-law check samples the sign of `S` at every cell midpoint and
requires `rho=R` when `S<0`, `rho=1` when `S>0`, in addition to the event
switch residual and transversality gates.

## Arithmetic, resources, and escalation

- Discovery arithmetic: IEEE-754 binary64.
- Python 3.12.13, NumPy 2.5.1, SciPy 1.18.0, mpmath 1.3.0.
- Maximum four workers; intended wall time below two hours and memory below
  4 GiB for this route.
- Promising asymmetric or singular candidates are replayed with mpmath at
  100 decimal digits.  Decimal replay is not an interval certificate.
- An actual witness would require outward-rounded interval Newton/Krawczyk
  inclusion of the residual zero plus interval certification of every
  validity predicate and distinctness.  If no interval library is available,
  the result remains a candidate.

## Outputs and replay

```powershell
E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe `
  runs\R-20260815T181317Z-min-reflection\routes\certified_search\search.py `
  --scope full --workers 4
```

Outputs are strict JSON `results.json`, a concise `report.md`, and
`artifact_manifest.json`, all beside this contract.

## Blind spots and proof bridge

The finite grids and multistarts can miss disconnected chambers, roots beyond
the coordinate boxes, very narrow branches, tangencies not sampled below the
contact threshold, and floating event misclassification near grazing.  The
imported implementations may share a bug.  No negative search result implies
the universal target.  A proof still requires an exact global invariant,
order/orientation theorem, or a complete interval subdivision; a refutation
requires one premise-complete interval-certified asymmetric point.

