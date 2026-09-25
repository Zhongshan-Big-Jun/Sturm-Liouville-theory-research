# Sturm-Liouville Theory Research

2026-09-26: Round11 repairs the residual Jacobian CROSS blocks and finite differences whose coordinate conversion changed their direction. A separate analytic review accepts the fixed-c>0 cofinite closure classification throughout 0<=s<7/2, including the three critical orders and the original-family non-Schauder/Riesz conclusion under nonzero termwise scaling and reordering. See the [report](reports/proof-audit-round11-20260926/REPORT.md), [proof PDF](docs/SL_cofinite_all_orders.pdf), and [reusable card](tools/krein-cofinite-closure-all-orders.md). Numerical execution and local Lean evidence have separate scopes.

2026-09-25: Round10 repairs independently reviewed. Lifted-phase indexing replaces missed-root sign scans, and geometric reflection sectors are checked after coordinate conversion. Historical numerical output is revalidated only where actually rerun. See the [round10 report](reports/proof-audit-round10-20260925/REPORT.md).

[中文](README.md) | [Research guide](docs/research-guide.md) | [Project understanding](docs/PROJECT_UNDERSTANDING.md) | [Tool library](tools/README.md) | [Lean status](lean-proof/STATUS.md)

Literature absorption (2026-09-23): [13 source pointers and reading notes](literature/absorption-20260923/README.md) connect the domain dictionary, s=3 cofinite closure, fixed-c Legendre replacement systems, finite moving-interface derivatives and two infinite-deletion subclasses to the tool library. The [report](reports/literature-absorption-20260923/REPORT.md) separates independent analytic review, finite checks and remaining scope. L13 lacks its complete constraint definitions and is not a proof dependency.

Ninth-round repair (2026-09-23): block tangency now uses actual integrals, the normalized eigenfunction derivative includes its kernel component, and the false one-dimensional Green-diagonal divergence argument is withdrawn. Reflection preserves the normalized secular function; the physical function has a frequency factor. A Jacobi proof establishes strict decrease and the limit of the prescribed balanced candidate sequence, without identifying it with the global optimum. See the [ninth-round report](reports/proof-audit-round9-20260923/REPORT.md) for evidence and verification scope.

Eighth-round repair (2026-09-22): the symmetric-well INF limit now uses a continuous phase bound over the entire thin-layer region and elementary positive-margin comparison for large w. T1 no longer depends on the old grid or high-precision T3 values. For fixed interior u the leading correction is C(u)/R, and 0<=R*m_R-M=O(1/R). Four revised tool cards, exact rational certificates, scoped Lean and fresh independent reviews are recorded in the [eighth-round report](reports/proof-audit-round8-20260922/REPORT.md).

Seventh-round repair (2026-09-21): corrected constant-density formulas and supplied a uniform Volterra endpoint argument for the local symmetry theorem. For every fixed n>=1, the gap supremum tends to (n+1)^2*pi^2; 4*pi^2 is the n=1 special case. Five tool cards and ten diagnostic scripts address the directly propagated derivative, normalization, sign and matrix-product errors; scoped independent reviews and replays are recorded. See the [seventh-round report](reports/proof-audit-round7-20260921/REPORT.md) for the distinct analytic and local Lean scopes.

Sixth-round repair (2026-09-21): corrected sparse-projection, finite-moment and constraint-representer claims. The complete original sparse family is now proved dense for exactly the nonnegative range $0\le s<7/2$ in the specified genuine left-definite spaces. Analytic proofs and library propagation passed fresh independent reviews. Local Lean coverage is stated separately in the [sixth-round report](reports/proof-audit-round6-20260921/REPORT.md).

Fifth-round audit (2026-09-21): the old O1'LD tail-rigidity, unconditional cofinite-density and proper-subspace candidates are refuted. The monomial finite-deletion lemma retains its conclusion with a corrected proof. The two-trace classification at s=2 has passed independent review, and its revised tool card is available for reuse; see the [fifth-round report](reports/proof-audit-round5-20260921/REPORT.md).

The fourth revision on 2026-09-21 separates ordinary-function and quotient limits, repairs the third-order program, reduction assumptions and parameter table, and proves general-c minimal solutions for the specified even/odd coefficient family. See the [fourth-audit report](reports/proof-audit-round4-20260921/REPORT.md) for analytic, independent-review and local-Lean scopes.

The third audit on 2026-09-20 corrects the general recurrence versus product-model distinction, false basis-perturbation stability claims, and a quotient-completeness proof gap. Updated cards, programs, local Lean checks, independent reviews and their limits are documented in the [third-audit report](reports/proof-audit-round3-20260920/REPORT.md).

The 2026-09-20 second audit repairs spectral/domain claims, the first-pair global extremum argument and K1 terminal conditions, and connects external findings to versioned library corrections. See the [audit report](reports/proof-audit-round2-20260920/REPORT.md) for independent reviews, local Lean evidence and remaining gaps.

This is a research output repository using the [rigorous-open-math-research plugin](https://github.com/xsoc1/rigorous-open-math-research) for long-term mathematics research. It preserves proofs, counterexamples, successful and unsuccessful routes, reusable tools, and partial Lean formalizations from human-agent collaboration.

The mathematics includes prior literature, collaborators' contributions, and project derivations. The plugin supports retrieval, organization, research continuity, and verification work. Attribution and evidence belong to the original sources and individual research packages.

## Research questions

- **Orthogonal systems and left-definite spaces.** Completeness, constrained density, moment recurrences, and operator power domains. Algebraic polynomial inverses, abstract completions, and genuine self-adjoint operator inverses must be distinguished.
- **Eigenvalue ratios and gaps.** Extremal adjacent ratios and gaps for the Dirichlet problem $-y''=\lambda\rho y$, including switching structure, symmetry, and uniqueness. Each proof specifies its density class and parameter range.

## Start reading

| Interest | Entry point |
| --- | --- |
| Proofs and remaining gaps by problem | [Research guide](docs/research-guide.md) |
| Current mathematical understanding and human annotations | [Project understanding](docs/PROJECT_UNDERSTANDING.md) |
| Stable problem IDs and relationships | [Research map](research_map.md) |
| Literature methods, reusable tools, and route history | [Tool library](tools/README.md) |
| Layout, document builds, and reproduction | [Repository guide](docs/repository-guide.md) |

Most detailed research notes are currently in Chinese or mixed Chinese and English.

## Selected results and their scope

The overview retains the research lines compiled on 2026-09-09, with left-definite density updated in round6, gaps in rounds7-8, fixed-n balanced candidates in round9, and cofinite closure in round11. `STRICT` applies to the stated theorem and assumptions; it does not certify the entire project or imply complete formalization.

| Research line | Existing result | Scope and evidence |
| --- | --- | --- |
| Adjacent ratios over all indices | Balanced-phase supremum formula; infimum 1, not attained | [Supremum](docs/SL_ratio_proof.tex), [infimum](docs/SL_inf_ratio_proof.tex); retain the density class of each source |
| n=1 adjacent gaps | Reduction, rigidity, symmetric-line analysis, and extremal proof chain | [Proof guide](docs/research-guide.md); all R>1 in the normalized box class |
| Symmetric-well INF limit | R*m_R tends to M≈24.9438661384, with nonnegative O(1/R) error; near-minimizers converge when R*eta_R tends to zero | [Continuous proof](docs/SL_gap_n1_inf_limit_proof.tex); non-symmetric/all-box conclusions require their own evidence |
| Fixed-n balanced ratio candidates | Complete 2n simple-root count; c_n strictly decreases to ((pi-phi)/phi)^2 | [Current proof](docs/SL_fixed_n_supremum.tex); phi=arccos((sqrt(R)-1)/(sqrt(R)+1)), R>1; global optimality remains open |
| n>=2 gap structure | Finite-block structure, small-contrast local symmetry, and fixed-n>=1 gap supremum limit (n+1)^2*pi^2 | [Current proof](docs/SL_gap_nge2_symmetry_local_proof.tex); measurable box and finite-piecewise classes; finite-R global uniqueness remains open |
| Left-definite spaces and domains | Full-window cofinite closure from the retained continuous central traces, 0<=s<7/2; the original family remains non-Schauder/Riesz under nonzero scaling and reordering | [All-order proof](docs/SL_cofinite_all_orders.pdf), [tool card](tools/krein-cofinite-closure-all-orders.md), [power-domain obstruction](tools/krein-power-domain-polynomial-obstruction.md); fixed c>0, general infinite deletion remains separate |
| B4/P1 M3 | STRICT asymptotics and signs of two sector determinants | [Tool and proof chain](tools/m3-largeR-closure.md); n=2 symmetric INF, large R, finite nonzero interior chart |
| KP-DET | Complete-constraint branch closed for 0<c<=2/3; exact quadrature reduction P20-P21 | [Sequence 26][kp-whiteboard]; audited partial results, with Q9 still OPEN in the local main run |

The plugin repository separately contains [three complete Q9 benchmark proofs and anonymous PASS audits][q9]. They have not been integrated into this repository's canonical graph or formalized in Lean. They do not establish closure of global G1', KO-DET, or the full n>=2 extremal problem.

## Open directions

- Global nondegeneracy, symmetry, uniqueness, and optimal values for n>=2 gap extremals.
- Fixed-n global ratio optima and properties of the actual supremum sequence. Root count, monotonicity and the limit of the prescribed balanced candidates are proved; see the [guide](docs/research-guide.md).
- General non-diagonal density criteria O1'/O1'LD, general infinite deletion and constrained problems for other boundary conditions. The fixed-c>0 cofinite classification is now proved throughout 0<=s<7/2 in this model.
- Nonhomogeneous source-term control and broader coefficient families in the third-order recurrence. The [specified even/odd family](docs/SL_third_order_recurrence_theory.tex) now has minimal-solution constants for every c>0 and a rational-ratio classification. [K(1)=e/4](docs/SL_third_order_K1_proof.tex) remains the even-family anchor.

The research map and early survey contain records from different dates. Follow the precise theorem, audit, scope, and relevant latest run when resuming. The guide identifies historical G2 status differences that still need statement-level reconciliation.

## Formalization status

[lean-proof/](lean-proof/) pins Lean/mathlib v4.31.0. It contains machine-checked lemmas and proof components, as well as research scaffolds with `sorry` and conditional analytical interfaces. Historical successful builds apply only to their recorded files and versions.

Consult the [status matrix](lean-proof/STATUS.md), [obligation audit](lean-proof/audit_report.md), and [scaffold register](lean-proof/formalization_progress.md), then inspect the exact root theorem and its dependencies. The repository does not claim that all mathematical results have been verified in Lean.

## Collaboration and maintenance

Read [AGENTS.md](AGENTS.md) before maintenance. Human ideas and agent annotations can be recorded in [project understanding](docs/PROJECT_UNDERSTANDING.md) or relevant tool cards with their evidence status.

The [primary repository](https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research) and [fork](https://github.com/xsoc1/Sturm-Liouville-theory-research) follow the project's synchronization rules. The [cleanup report](reports/repository-cleanup-20260909/REPORT.md) records removals and evidence preservation; historical homepages remain accessible through the research guide.

[kp-whiteboard]: research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/whiteboard-26.md
[q9]: https://github.com/xsoc1/rigorous-open-math-research/blob/f95627ca1b44aeb75692a5814e20050b0e6a40cb/benchmarks/codex-20260908-q9/CONCLUSIONS.md
