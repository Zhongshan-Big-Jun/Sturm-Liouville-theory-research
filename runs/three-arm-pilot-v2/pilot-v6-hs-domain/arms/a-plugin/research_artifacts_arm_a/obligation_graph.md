# Obligation graph

Status values: `ACCEPTED`, `OPEN`, `CLOSED`, `FALSIFIED`, `AUDIT_PENDING`.

| ID | Claim | Depends on | Status |
|---|---|---|---|
| O0 | Exact theorem contract and two readings are faithful to the frozen task | prompt | CLOSED (second-pass audit) |
| O1 | \(K_0\ge0\), form domain \(H^1\), and \(\ker K_0=\operatorname{span}\{1,x\}\) | direct form calculation | CLOSED |
| O2 | Polynomial power-domain criterion is the complete iterated Krein boundary criterion | self-adjoint power-domain recursion, O1 | CLOSED (coordinator proof) |
| O3E | For even \(s\), \(L_{\rm poly}^{-1}P_n\in D(K_c)\) iff \(n\le1\) | O1, orthogonality | CLOSED (coordinator proof) |
| O3O | For odd \(s\), \(L_{\rm poly}^{-1}R_n\in D(K_c)\) iff \(n\le1\) | O1, form orthogonality | CLOSED (coordinator proof) |
| O4 | Q1: \(Q_n^{(s)}\in D(K_c^{s/2})\iff n\in\{0,1\}\) on polynomial reading | O2, O3E/O3O | CLOSED (coordinator proof) |
| O5 | Abstract polynomial completion is not canonically equal to the operator domain; exact unitary relation identified | O4, completion maps | CLOSED (coordinator proof) |
| O6 | Literal polynomial span is not a subspace/dense operator-domain basis; genuine operator images are dense | O4, isometry+density theorem | CLOSED (coordinator proof) |
| O7 | Integrated proof passes independent adversarial audit | O1--O6 | CLOSED (independent PASS) |

Shortest completion chain: `O1 + O2 -> (O3E,O3O) -> O4 -> (O5,O6) -> O7`.

All mathematical and independent-audit obligations O0--O7 are closed.  No
formalization or novelty obligation is part of the frozen completion contract.
