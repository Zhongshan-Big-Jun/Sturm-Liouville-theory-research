# R13 certificate repair and proof boundary

The authoritative current calculation uses `misc/rigid1d.py` and `misc/e1_certgen.py`; the latter's source-bound `e1-exact-certificate/v2` ledger contains 57 complete obligations. The old input bundle and actual baseline replay remain separately stored. The unchanged mathematical definitions in `comps2` retain the original gamma interval [131/200,1309/1250] and m=791/2500.

The interval justification is in `interval-author/analytic_justification.md`. Taylor sin/cos point remainders follow the derivative bound 1 at any real center. Offset sin/cos ranges use monotonicity on [0,1], including cos(0)=1, and return [-1,1] for larger radii. Atan uses monotonic endpoints with finite point reductions; cross-1 is not an exceptional mathematical input. Square roots use integer square-root rational bounds; dual derivatives require a positive value interval. The actual E1 calls satisfy these domains. No numerical sampling establishes these lemmas.

Every point/Taylor contract specifies its exact domain, expression, derivative/value role, strictness and target. In particular the two range bounds compare against 27/10 and 19/10, and tau<13/10 uses strict lt. Taylor witnesses contain the entire cell, its center, center enclosure, derivative enclosure, rational M and radius M*w, final bound and target-subtracted margin. B1'<0 is checked as -3*cos(gamma)-(pi-gamma)*sin(gamma), with each factor positive. Eight exact cells cover h''<0 on [131/200,13/10]. The h endpoint facts and tau monotonicity on the checked tangent branch give all three concavity reductions. None is a hardcoded True.

For a rational x and decimal scale S=10^d, lower display uses floor(S*x)/S and upper uses ceil(S*x)/S, including negative x. These are integer divisions; they cannot turn a nondegenerate true interval into a false decimal singleton. M and M*w are displayed upward; certificate margins downward. Cell coordinates are exact terminating decimals (or rational fractions), so the printed domain is not silently enlarged. Exact ledger fractions, rather than a decimal center, remain authoritative.

Actual recomputation retained all 57 statements. Examples of conservative displayed bounds:

- B1(.85) in [0.009851718322,0.009851718323], still >=1/200.
- TA_B2>=27/10: smallest displayed lower margin 0.002392350303 across its four cells.
- TC>=19/10: smallest displayed lower margin 0.058681319813 across its four cells.
- h(.655)>=m: displayed lower margin 0.000025571653.

The generator writes RUNNING before work. A false/incomplete fact gives nonzero exit 1 and separate failed evidence; an exception gives exit 2. It preserves a previous accepted ledger's bytes but marks this attempted generation unsuccessful. Publication is allowed only for all 57 current contracts. The receiver requires PASS status, exact ledger hash, current engine/generator/contract hashes, complete named obligations, correct witness arithmetic and all predicates. It rejects failed/unknown/missing rows and inconsistent displays/radii/targets. This is finite witness validation, not independent reevaluation of the transcendental functions. The analytic lemmas and their independent review remain explicit dependencies.

Normal and -O negative tests inject one false fact, one exception and one unknown result into the real build/main path. Each generator invocation fails; both current consumers reject it and leave old publication bytes unchanged. The first test attempt had an incorrect six-digit formatting expectation for a twelve-digit point row. Its failure and source were retained in `certificate-attempt1`; the replacement checks enclosure of exact endpoints rather than an output spelling. No threshold or counterexample was relaxed.

The retired Decimal sources `rigid_dec.py`, `zz_verify_e1_dec.py`, their old ledger and `audit_o3a_cert_replay.py` retain their original bytes. Direct active-code searches found no repaired proof/Green/Jacobian caller depending on them. Current reuse was through the old engine card and true-curve/rational-certificate cards; those entries are corrected and the engine card remains withdrawn. Old PASS records and old random samples are historical observations, not reliable enclosures. No theorem is retracted merely because that superseded engine is defective.

Evidence levels: these are analytic enclosure arguments plus a finite exact-rational certificate calculation and software acceptance tests. Independent floating spectral comparisons are separate. No new Lean compilation or full theorem formalization is claimed. The rest of the O3a analytic proof, A1/A12, compatible Legendre systems, genuine stationary Jacobian and measurable-box existence retain their stated scope.
