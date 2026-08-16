RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-H problem contract: general-mu full three-cell interface

## Snapshot and target

- Context: `CTX-DEFAULT`.
- Blueprint SHA-256: `358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0`.
- Inventory SHA-256: `b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
- Target: the `n=2` minimum-side FULL THREE-CELL INTERFACE LEMMA from the
  historical R9 route: for every `mu>1`, common negative energy, two
  independent momentum matches at each interface, the strict R8
  first-crossing branches, and positive-negative-positive phase order imply
  the scalar Schur complement `H>0`.
- Mode: prove-or-refute; Lean formalization is off.

The accepted `mu=2` theorem is a trusted special case.  Historical R11,
R12, R14, and R17 artifacts may be rederived locally but are not silently
promoted to canonical premises.

## Quantifiers and local reduction

Fix `mu>1` and phases

```text
0<alpha<pi/(mu+1)<beta<pi/mu.
```

Let the exact common-angle one-cell quantities be `x_+,x_-,p_+,p_-,
kappa_+,kappa_-,rho_+,rho_-,e_+,e_-,U_+,U_-` as redefined in the route
report.  Put

```text
lambda=U_+/U_-, d=rho_+-rho_-, eta=-e_-,
w=(e_+-r eta/lambda)/d, u=x_++w, delta=r^2-1,
A0=1-x_+u.
```

The physical branch requires `r>1`, `w>0`, `A0>0`, and
`lambda*w/r-x_->0`.  The exact split target is

```text
Phi=(lambda^2 w^2+r^2 kappa_-+p_-)
       (A0+delta p_+u^2)-delta p_-w u^3 >0.
```

The full three-cell scalar follows if this same local statement is applied
at the left interface and, after time reversal, at the right interface.

## Required boundaries and forbidden substitutes

Audit `n=2`, `mu->1+`, `mu->infinity`, `R->1+`, left/right asymmetry, phase
thresholds, amplitude-boundary limits, and the empty physical branch.
Finite or floating-point scans are discovery/falsification only.  A relaxed
tuple off the common-angle manifold is not a physical counterexample.
No unbounded Arb subdivision is permitted.  A partial result must identify
an exact strict analytic subdomain or freeze the first still-unsiged factor
after all physical equations are imposed.

## Completion conditions

- Complete route: prove `Phi>0` for the full physical domain for every
  `mu>1`, and chain it to asymmetric left/right three-cell `H>0`.
- Material partial completion: prove a strict, nonempty, explicitly stated
  analytic subdomain for general `mu`, or a nontrivial open `mu` interval.
- Refutation: an exact physical common-angle witness satisfying every
  branch and matching premise with `Phi<=0`.
- Blocked: freeze one exact remaining factor/inequality plus restart
  condition; never claim a local nonphysical witness as a refutation.

