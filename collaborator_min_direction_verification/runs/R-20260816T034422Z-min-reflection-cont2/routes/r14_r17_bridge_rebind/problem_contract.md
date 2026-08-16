CANDIDATE_COMPLETE_PROOF

# MIN-REFL-C2-J contract: rebind the general-mu n=2 coefficient bridge

## Snapshot and trusted inputs

- Context: `CTX-DEFAULT`.
- Blueprint SHA-256:
  `b93b42029f95d55489c71e344af329220c3182ff07c2d0b57b9e170b7d4f7056`.
- Inventory SHA-256:
  `b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
- Trusted claims, used only in their accepted scopes:

```text
CLM-NGE2-MPO3A-FULL-RELAY
  semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46
CLM-NGE2-MPO3A-INTERNAL-PHASE-R8
  semantic-sha256:43f3bbdfa4b51c4504501ea9d5d68bf05ec1ca5b844da5dcf271da1f640d6702
CLM-NGE2-MPO3A-PHYSICAL-CONTINUANT-R7
  semantic-sha256:5a4e8e40668e50766f7594724eb357bddcf7b94139b86e8fdbf14582e39088ee
CLM-NGE2-MPO3A-MIN-DETERMINANT-PARITY-R35
  semantic-sha256:bccb84587f0fb907314362677afbcc473037f8f1f26ef1aaa0d2368acf911014
CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
  semantic-sha256:7b14d27f0e1a8dc6f97b2fa60a448497f072490eace29dee2de6785373924c89
```

The corresponding accepted proof-package contracts have been read at their
canonical bound paths and hashes.  Historical R11/R14/R17 formulas are
untrusted targets for local rederivation, not premises.

## Target implication

For every finite `R>1`, every `mu>1`, and every arbitrary possibly
asymmetric premise-complete transverse common-terminal minimum-law root with
`n=2`, prove the following conditional bridge:

```text
all four stable coefficient gaps G_i>0 on the full retained physical cube
 => each physical interface split Phi>0
 => left and time-reversed right gaps E_L,E_R>0
 => scalar H>0
 => det(L_-)>0
 => partial_q A_2<0
 => fixed-mu global root order and reflection fixing.
```

The coefficient-cover premise is not assumed true here.  It must be supplied
by a separately frozen complete C2-I certificate covering the whole strict
physical cube, with no unresolved boxes.

This status refers only to the conditional implication just displayed.  The
unconditional general-`mu` theorem remains a blocked reduction until C2-I is
complete, reviewed, and hash-bound.

## Required audits

- Reconstruct both momentum equations, Cramer solution, normalized `Phi`,
  the `g>=1` analytic half, the `g<1` quartic Bernstein reduction, and the
  stable `G_i` scaling exactly.
- Prove the phase coordinate map `(mu,alpha,beta)<->(k,t,y)` is bijective
  between the strict physical chamber and `(0,1)^3`.
- List every denominator and show it is nonzero on the retained physical
  subset.
- Keep cube closure distinct from the physical open cube.
- Audit the q-Jacobi singular case through the canonical continuant identity,
  not by matrix inversion.
- Treat left and right interfaces independently; no reflection premise.

## Completion and non-completion

- Complete route: a self-contained hash-bound conditional proof with the
  C2-I full coefficient cover as its only open input.
- Blocked route: freeze the first failed formula, phase-map gap, denominator,
  or global-order premise.
- This route never declares the general-mu theorem established before a
  complete C2-I cover is independently reviewed and bound.
- Lean formalization is off.  Canonical files, submissions, reviews, and
  integration are out of scope.
