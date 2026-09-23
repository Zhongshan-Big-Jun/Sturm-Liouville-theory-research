# L10: boundary-extension expansions and the moving-density bridge

Author proposal, 2026-09-23. Independent acceptance review is pending. All project conclusions below are this author's adaptations, not claims that the paper proves the project's optimization problem.

## Source identity and actual reading

Y. Latushkin and S. Sukhtaiev, *Resolvent expansions for self-adjoint operators via boundary triplets*, Bulletin of the London Mathematical Society 54(6) (2022), 2469-2491, [DOI](https://doi.org/10.1112/blms.12706). Formula locators here refer specifically to [arXiv:2110.07434v1](https://arxiv.org/pdf/2110.07434v1), 18 PDF pages, not to journal pagination. DOI registration confirms online publication 2022-07-12 and print issue 2022-12. Direct Wiley requests returned 403; they were not full-text reads. The arXiv PDF returned 200. Raw responses, UTC times, hashes and extraction identities are in `../source-manifest.json`.

Read PDF pp.1-9, 12-13 and 16, plus the Remark 2.14 continuation at the start of p.17. Inspected original rendered pp.4,5,13,16 for formulas and operator spaces. Theorem 2.9's proof continuation on pp.10-11 and Theorem 2.11's proof on pp.14-15 were not read. This is a hypothesis/result adaptation, not an audit of every proof in the paper.

## Source contract, in compressed form

Hypotheses 2.1-2.2 (pp.3-4) use one densely defined closed symmetric operator A in one Hilbert space, equal deficiency indices, and a fixed bounded surjective trace T on dom(A*) with its graph norm and Green identity. Extensions have domains T^{-1}(ran Q_t); the Lagrangian orthogonal projections Q_t have an operator-norm second-order Taylor expansion. Hypothesis 2.6 (p.7) requires an isolated eigenvalue of finite multiplicity.

Theorem 2.5 (pp.5-7, (2.7)-(2.11)) obtains a first-order resolvent expansion into the graph space and second order in the original Hilbert space. Proposition 2.8, Theorems 2.9-2.10 (pp.8-9,12; (2.20),(2.24),(2.44)-(2.45)) transport projections and the finite spectral cluster and select eigenvalue expansions. Theorem 2.11 (p.13,(2.48)) additionally uses Z_t=[X_t,Y_t], X_tY_t*=Y_tX_t*, invertible X_tX_t*+Y_tY_t*, and a norm expansion. Corollary 2.12 (p.16,(2.65)) specializes to self-adjoint Robin data. Remark 2.14 (pp.16-17) adds bounded self-adjoint perturbations with norm expansions.

## Project mapping and an explicit obstruction

The project model is `-u''=lambda rho_a u`, Dirichlet on [0,1], fixed positive block values c_j and ordered interfaces a_j. At one configuration it is self-adjoint in H_a=L2(rho_a dx), with simple isolated eigenvalues and normalization integral rho_a u_k^2=1. Those facts supply the spectral isolation part only.

Let ell_j(t)=a_j(t)-a_{j-1}(t)>0. An explicit unitary map to the fixed space direct-sum_j L2(0,1) is

`(U_t u)_j(xi)=sqrt(c_j ell_j(t)) u(a_{j-1}(t)+ell_j(t) xi)`.

The transformed expression on the interior of block j is

`-(c_j ell_j(t)^2)^(-1) d^2/dxi^2`.

Continuity of physical value and slope gives the matching conditions

`v_j(1)/sqrt(c_j ell_j)=v_{j+1}(0)/sqrt(c_{j+1} ell_{j+1})`,

`v_j'(1)/(ell_j sqrt(c_j ell_j))=v_{j+1}'(0)/(ell_{j+1} sqrt(c_{j+1} ell_{j+1}))`.

These equations exhibit both a changing differential expression and changing matching data. A compactly supported smooth test function in a changing block belongs to every natural minimal domain, yet the actions on it differ when ell_j changes. Thus this natural pullback does **not** produce extensions of one fixed minimal differential operator. A fixed boundary coordinate space, or smooth finite matching matrices, does not repair that missing hypothesis. The coefficient difference multiplying d²/dxi² is unbounded on L2, so Remark 2.14's bounded-additive extension does not supply the repair either. This rules out the naive application, not every possible alternative realization.

Multiplication by sqrt(rho_a) to move H_a to L2(dx) is another incomplete shortcut: a genuinely displaced nonzero jump is not continuous in the L-infinity multiplier norm. A norm-C2 boundary path cannot be inferred from that operation.

| Needed before using L10 as a proof dependency | Current status in this packet |
| --- | --- |
| A common fixed-Hilbert-space symmetric operator and fixed adjoint expression | Natural affine pullback above fails this requirement |
| One graph-norm bounded surjective trace satisfying the appropriate Green identity | Ordinary interval traces exist at a fixed configuration; compatibility with a common A* is unproved |
| Self-adjoint domains described by a norm-C2 Lagrangian projection | Finite matching equations are explicit; the required fixed symplectic realization has not been constructed |
| Identification of transported spectral projections, reduced resolvent and normalization | Must be checked under any new realization; not implied by a matrix Hessian resemblance |
| Applicability of an unbounded principal-coefficient/form extension, if used | Requires a different theorem and its own hypotheses; not supplied here |

## Allowed use in P3

L10 supplies a disciplined separation of domain velocity, domain acceleration, spectral projection and reduced resolvent. It does not authorize inserting distributional density derivatives into its boundary formula. Our [bounded interface theorem](../derivations/P3-interface-chain-rule.md) instead proves the needed local differentiability directly from finitely many transfer matrices. It recovers the weighted normalization component and finite interface acceleration without invoking an unproved L10 bridge.

For nonlinear interface coordinates, the second derivative contains a gradient-times-coordinate-acceleration term; a Hessian alone is coordinate-independent along a path only after accounting for that term. This also applies before stationarity. No conclusion about global inertia, G1', reflection symmetry or uniqueness follows from L10 or this packet.

Current project evidence read: round9 `analytic-repair.md` V1-V4; `tools/second-variation-weighted-eigenvalues.md`; `tools/transfer-matrix-secular.md`; `scripts/gap_lib.py`; `scripts/_gapn2_jacobian_spectral.py`; the relevant portions of `scripts/_gapn2_jacobian_analytic.py`, `scripts/_gapn2_second_variation_probe.py` and `docs/SL_gap_nge2_symmetry_local_proof.tex`. Exact paths, ranges and hashes are recorded in the manifest. Historical numerical labels in those sources were not treated as fresh execution evidence.
