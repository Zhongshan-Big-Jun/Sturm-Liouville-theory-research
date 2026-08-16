CANDIDATE_COMPLETE_PROOF

# R11 problem contract: conditional relay order and min `n=2`, `mu=2` closure

## Frozen statement

At canonical snapshot

- blueprint `sha256:7eb6256786ff20ce8dcf5bb1b8ce669337eb216a38e4e274c8292f1ef6456242`,
- inventory `sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`,

prove the following unconditional restricted theorem:

> For every finite `R>1`, let the min relay at `mu=2` start from the positive normalization `(U,U_t,V,V_t)(0)=(0,1,0,q)`, `q>1`, with material `rho=R` on the initial punctured interval where `S=U^2-4V^2<0`. Let `T_U^2(q)` and `T_V^3(q)` be the second and third positive scalar zeros of the unique global relay trajectory and define `A_2(2,q)=T_U^2(q)-T_V^3(q)`. Then `A_2(2,.)` is continuous on `(1,infinity)`, has at most one zero, and every zero is premise-complete, transverse, has exactly four active relay events, and is fixed by reflection after positive reorientation.

The theorem is conditional only in the sense that it does not assert a zero exists. It does not cover `mu!=2`, `n>2`, the global min problem at arbitrary frequency, equal-norm existence or orientation as `mu` varies, min O3a, or universal O3a.

As a reusable intermediate result, isolate the sign-independent statement for either relay orientation.  With `rho_-` denoting the coefficient on `S<0` (`rho_-=1` for max and `rho_-=R` for min), prove for each fixed finite `R>1`, `n>=2`, and `mu>1` that a uniform strict sign `sigma partial_q A_n^c>0` at every premise-complete common-terminal root implies global continuity, at-most-one, and reflection fixing.  This is a conditional implication only: do not claim its local-sign hypothesis for general `n,mu`.

## Trusted inputs

- `HYP-NGE2-DOMAIN`.
- `CLM-NGE2-ZERO-BOUND`.
- `CLM-NGE2-MPO3A-FULL-RELAY`.
- `CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10`, semantic `semantic-sha256:157a7bf928676b7565e5e08e965909ab0657e48888d37095c43352a228bbbd21`.
- `DEF-NGE2-MPO3A-SELFCONSISTENCY`.

The frozen max R9 proof package may be used as a checked derivational template, but the max theorem is not a premise. Every relay-sign-sensitive step must be rewritten for the min law.

## Required sign and boundary changes

1. Initially and at every joint contact `S<0` on both punctured sides, so the common proof uses `rho_-`; the min specialization has `rho_-=R`, not `1`.
2. The accepted local derivative is `partial_q A_2<0`; the oriented-zero argument must use negative, not positive, orientation.
3. The terminal common zero lies in the closure of a negative-sign cell.  Terminal event-pair softness must be proved uniformly with coefficient `rho_-`, then specialized to `rho_-=R` for min.
4. No reflection symmetry may be assumed before at-most-one is proved.
5. Joint zeros, nonzero grazing, finite Zeno accumulation, changes of material word, and terminal pair birth/death must be handled rather than excluded by a fixed-chamber definition.

## Completion condition

Freeze a content-hashed derivation and a separate self-audit passing definition, logic, boundary, and adversarial audits, with `unresolved_obligations: []` for exactly the restricted theorem. Do not submit or edit canonical files in this task.
