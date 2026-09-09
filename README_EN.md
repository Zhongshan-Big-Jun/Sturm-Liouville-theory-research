# Sturm-Liouville Theory Research

[中文](README.md) | [Research guide](docs/research-guide.md) | [Project understanding](docs/PROJECT_UNDERSTANDING.md) | [Tool library](tools/README.md) | [Lean status](lean-proof/STATUS.md)

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

The entries below summarize existing proofs and audited packages, checked against repository records on 2026-09-09. `STRICT` applies to the stated theorem and assumptions; it does not certify the entire project or imply complete formalization.

| Research line | Existing result | Scope and evidence |
| --- | --- | --- |
| Adjacent ratios over all indices | Balanced-phase supremum formula; infimum 1, not attained | [Supremum](docs/SL_ratio_proof.tex), [infimum](docs/SL_inf_ratio_proof.tex); retain the density class of each source |
| n=1 adjacent gaps | Reduction, rigidity, symmetric-line analysis, and extremal proof chain | [Proof guide](docs/research-guide.md); all R>1 in the normalized box class |
| n>=2 gap structure | Finite-block reduction and exactly 2n switches | [Reduction](docs/SL_gap_nge2_finite_reduction_proof.tex), [switch theorem](docs/SL_gap_nge2_exact_2n_switches_proof.tex); global uniqueness remains open |
| Left-definite spaces and domains | Moment-based completeness proofs and an obstruction for algebraically transported polynomials | [H2 proof](docs/SL_h2_completeness_proof.tex), [exact power-domain statement](tools/krein-power-domain-polynomial-obstruction.md) |
| B4/P1 M3 | STRICT asymptotics and signs of two sector determinants | [Tool and proof chain](tools/m3-largeR-closure.md); n=2 symmetric INF, large R, finite nonzero interior chart |
| KP-DET | Complete-constraint branch closed for 0<c<=2/3; exact quadrature reduction P20-P21 | [Sequence 26][kp-whiteboard]; audited partial results, with Q9 still OPEN in the local main run |

The plugin repository separately contains [three complete Q9 benchmark proofs and anonymous PASS audits][q9]. They have not been integrated into this repository's canonical graph or formalized in Lean. They do not establish closure of global G1', KO-DET, or the full n>=2 extremal problem.

## Open directions

- Global nondegeneracy, symmetry, uniqueness, and optimal values for n>=2 gap extremals.
- Fixed-n ratio optima and remaining monotonicity questions. Later STRICT results already cover the 2n root count; see the [guide](docs/research-guide.md).
- General non-diagonal density criteria O1'/O1'LD, the remaining fractional window, and threshold classification.
- General K(c), source-term control, and broader coefficient families in the third-order recurrence. [K(1)=e/4](docs/SL_third_order_K1_proof.tex) is a proved specific anchor.

The research map and early survey contain records from different dates. Follow the precise theorem, audit, scope, and relevant latest run when resuming. The guide identifies historical G2 status differences that still need statement-level reconciliation.

## Formalization status

[lean-proof/](lean-proof/) pins Lean/mathlib v4.31.0. It contains machine-checked lemmas and proof components, as well as research scaffolds with `sorry` and conditional analytical interfaces. Historical successful builds apply only to their recorded files and versions.

Consult the [status matrix](lean-proof/STATUS.md), [obligation audit](lean-proof/audit_report.md), and [scaffold register](lean-proof/formalization_progress.md), then inspect the exact root theorem and its dependencies. The repository does not claim that all mathematical results have been verified in Lean.

## Collaboration and maintenance

Read [AGENTS.md](AGENTS.md) before maintenance. Human ideas and agent annotations can be recorded in [project understanding](docs/PROJECT_UNDERSTANDING.md) or relevant tool cards with their evidence status.

The [primary repository](https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research) and [fork](https://github.com/xsoc1/Sturm-Liouville-theory-research) follow the project's synchronization rules. The [cleanup report](reports/repository-cleanup-20260909/REPORT.md) records removals and evidence preservation; historical homepages remain accessible through the research guide.

[kp-whiteboard]: research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/whiteboard-26.md
[q9]: https://github.com/xsoc1/rigorous-open-math-research/blob/f95627ca1b44aeb75692a5814e20050b0e6a40cb/benchmarks/codex-20260908-q9/CONCLUSIONS.md
