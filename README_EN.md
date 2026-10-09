# Sturm-Liouville Theory Research

[中文](README.md) | [Read by problem](docs/research-guide.md) | [Problems and remaining gaps](research_map.md) | [Resume research](state/RESUME.md)

This repository preserves proofs, counterexamples, unsuccessful routes, computational tools and partial Lean formalizations from human-agent research on Sturm-Liouville theory. Contributions include prior literature, collaborators' work and project derivations; attribution and evidence belong to the original sources and research packages. The project uses the [mathematics research plugin](https://github.com/xsoc1/rigorous-open-math-research) for continuity and verification.

## Two research lines

- **Left-definite spaces and orthogonal systems.** Operator power domains, completeness of the original sparse polynomial family, deletion closures, finite constraints and stable replacement systems in the Krein model. Algebraic polynomial transport, abstract completion and genuine self-adjoint domains have distinct roles.
- **Eigenvalue ratios and gaps.** Adjacent ratios and gaps for the Dirichlet problem $-y''=\lambda\rho y$, including switching structure, symmetry and uniqueness. Each proof retains its own density class and parameter range.

## Selected results and scope

| Problem | Existing result | Recommended proof |
| --- | --- | --- |
| All-index adjacent ratios B1/B2 | Supremum formula in the stated density classes; infimum 1, not attained | [Supremum](docs/SL_ratio_proof.tex), [infimum](docs/SL_inf_ratio_proof.tex) |
| Fixed-index candidates B3 | Complete 2n simple-root count, strict decrease and limit of the balanced candidate ratios; equality with the global optimum remains open | [Candidate spectrum](docs/SL_fixed_n_supremum.tex) |
| n=1 gaps B4 | SUP/INF proof chains for all $R>1$ in the normalized box class $1\le\rho\le R$ | [Proof chain and prerequisites](docs/research-guide.md#n1-谱隙) |
| n>=2 gaps B4 | Finite-block/exact-switch structure and small-contrast local uniqueness; G2 gives uniform positive block widths for all exact zeros on $1\le R\le R_{max}$ | [Local proof](docs/SL_gap_nge2_symmetry_local_proof.tex), [complete G2 supplement](docs/SL_G2_compactness_proof.md) |
| Original family and deletions A1/A11/A12 | Fixed $c>0$, genuine complex $\mathcal H_c^s$, $0\le s<7/2$: full-family density, a density criterion for arbitrary retention, exact omitted-trace closure when both parity reciprocal sums diverge, infinite codimension when either converges | [Member window](docs/SL_fractional_left_definite.tex), [full-window deletions](docs/SL_full_window_deletions_and_finite_constraints.md) |
| Finite constraints A3-KREIN-FINITE | In the same model/window, individual-member filtering is complete precisely for intersections of subsets of the continuous central trace coordinate kernels | [Complete proof, section 7](docs/SL_full_window_deletions_and_finite_constraints.md#7-任意有限个连续约束下的逐项筛选分类) |
| Integer-order replacements A10 | Hermite-Legendre Riesz replacement bases for every fixed $c>0$ and nonnegative integer order; degree-independent bounds, with rates requiring weighted coefficients | [Complete integer-order proof](docs/SL_integer_left_definite_riesz_systems.md) |
| Bounded-direction spectral tails B11 | Parseval residuals and two-sided tails for positive bounded densities and real $L^\infty$ directions; sign certification requires reliable finite input enclosures | [Complete tail proof](docs/SL_bounded_direction_spectral_tail.md) |

G2 does not prove ND/G1 or unconditional global uniqueness. Riesz results concern the replacement systems and preserve the original-family nonbasis conclusion. The tail theorem does not cover delta/delta-prime interface directions. The [map](research_map.md) retains stable IDs and dependencies; the [guide](docs/research-guide.md) explains prerequisites and historical replacements.

## Main open questions

- Fixed-n global ratio optimality O1/O2; ND/G1, unconditional global uniqueness and optimal values for n>=2 gaps.
- Complete element descriptions on the summable deletion side, general non-diagonal A3/A4, infinite constraints, noninteger stable replacements and uniformity as $c\downarrow0$.
- Nonhomogeneous source control and broader recurrence families. Scoped M3/KP-DET chart results and remaining global questions are separated in the [guide](docs/research-guide.md#局部-chart-与外部结果).

## Reading and handoff

| Need | Entry |
| --- | --- |
| Mathematical intuition, failed routes and human annotations | [Project understanding](docs/PROJECT_UNDERSTANDING.md) |
| Current numerical interfaces, exact certificates and historical implementations | [Script guide](scripts/README.md) |
| Cards, retrieval gates and version evidence | [Tool entry](tools/README.md) |
| Directory roles, source/PDF correspondence and reproduction | [Repository guide](docs/repository-guide.md) |
| Working rules and this maintenance task | [AGENTS.md](AGENTS.md) |
| Completed work, unresolved items and publication evidence | [RESUME](state/RESUME.md) |

Proof, independent review, software tests, library reception, Blueprint reception, Lean and publication are separate states. [Lean status](lean-proof/STATUS.md) and the exact declarations/code/logs delimit formalization. Reports for [R14](reports/proof-audit-round14-20261004/REPORT.md), [R15](reports/proof-audit-round15-20261005/REPORT.md) and [R16](reports/proof-audit-round16-20261006/REPORT.md) preserve scoped outcomes and failed reviews. Pre-organization entries remain in the [snapshot manifest](docs/history/entry-snapshots-20261008.json), and full conversations in the [session log](state/AGENTS_SESSION_LOG.md). Most detailed research notes are in Chinese or mixed Chinese and English.


## Recent Lean and research reuse increment

Scoped complex interval L2/Krein/weighted-DD formalization and three exact roots are paired with task-focused retrieval, bounded knowledge and route comparison. [Lean evidence and lossless restoration](research/artifacts/lean-development-20261008/PUBLICATION.md) and [actual five-case integration](research/artifacts/manage-context-20261009/README.md) preserve scope and open bridges.
