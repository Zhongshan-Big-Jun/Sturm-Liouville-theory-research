# Sturm-Liouville Boundary Value Problems Research (BVE research)

中文版: [README.md](README.md)

A frontier mathematics research project on Sturm-Liouville (SL) boundary value problems, along two main lines:

1. **Completeness of eigenfunction/polynomial systems**: In which Hilbert space (left-definite space) is the solution set of an SL boundary value problem equivalent to all orthonormal function systems in that space? Baseline paper: Littlejohn-Quintero-Roba, *Krein-Sobolev Orthogonal Polynomials* (Springer 2025, DOI 10.1007/978-3-031-90135-5_7).
2. **Optimal bounds for eigenvalue gaps and ratios**: For the weighted Dirichlet problem
   $$
   -y'' = \lambda \rho y, \qquad 0 < a \le \rho \le A \ \text{(measurable box class)},
   $$
   optimize the adjacent spectral gap $D_n = \lambda_{n+1} - \lambda_n$ and the ratio $\lambda_{n+1}/\lambda_n$.

Every conclusion follows a strictness convention: rigorous proofs and numerical evidence are explicitly distinguished, and assertions without a rigorous proof are never labeled "solved".

## Main results

### Rigorously proved (see docs/ for details)

| Result | Source | Status |
| --- | --- | --- |
| Closed form $\sup_{n,\rho} \lambda_{n+1}/\lambda_n = \nu(R)$ (balanced-phase method, three-step proof) | `docs/SL_ratio_proof.tex` | Proved |
| $\inf_{n,\rho} \lambda_{n+1}/\lambda_n = 1$ (Weyl asymptotics; infimum not attained) | `docs/SL_inf_ratio_proof.tex` | Proved |
| Independent reproof of Mahar-Willner Lemmas 1-2 (periodic extension + zero truncation) | `docs/SL_mw_lemma_reproof.tex` | Proved |
| Structural stability of the degenerate limit $c \to 0$ of the shifted Krein operator | `docs/SL_krein_c0_limit.tex` | Proved |
| $\{p_n\}$ is analytically complete in the second left-definite space $H^2$ (moment-jump criterion + growth lemma) | `docs/SL_h2_completeness_proof.tex` | Proved |
| $\{p_n\}$ is complete in every integer left-definite space $H^s$ ($s \ge 1$) | `docs/SL_h3_completeness_proof.tex` | Proved |
| $n=1$ gap extremals: SUP/INF attained by $[1,R,1]$ / $[R,1,R]$ (phase-ratio rigidity; obligations O1/O2/O3a/O3b closed) | `docs/SL_gap_n1_proof.tex` et al. | Proved |
| $n \ge 2$ gaps: finite-block reduction (extremal bang-bang, at most $2n+1$ blocks) + exact $2n$-switch theorem (exactly $2n$ effective interior switches after merging adjacent equal-value blocks) | `docs/SL_gap_nge2_finite_reduction_proof.tex`, `SL_gap_nge2_exact_2n_switches_proof.tex` | Proved |
| $n \ge 2$ gaps (local): reflection symmetry of the extremizer at $R=1$ for general $n$ (direct Wronskian formula, $2n$ simple zeros) + local uniqueness and symmetry as $R \to 1$; global uniqueness depends on the topological-degree conditions $(G1')/(G2)$ (open) | `docs/SL_gap_nge2_symmetry_local_proof.tex` | Proved (local) |

### Partial proofs / strong numerical conjectures / open problems (honest labeling)

- Fixed-$n$ supremum: symmetric phase structure of the alternating configuration proved, closed forms for $n=1,2$; global extremality and the $2n$-root count remain open (`docs/SL_fixed_n_supremum.tex`; numerics: `docs/SL_ratio_summary.tex`).
- Global symmetry and minimal block count for $n \ge 2$ gap extremals: the local theorems at $R=1$ and as $R \to 1$ are rigorously proved (see table above); global uniqueness depends on the open conditions $(G1')/(G2)$ (`docs/SL_gap_nge2_symmetry_local_proof.tex`, Section 5); the rest is strong numerical conjecture.
- Authoritative list of open problems: `docs/SL_spectral_topics_summary.tex`, Section 5.
- Literature search: no published result directly equivalent to the $n \ge 2$ theorems was found; the project does not claim priority, and early literature such as Willner-Mahar 1979 remains an overlap risk (verification records are kept in the proof documents).

## Lean 4 formal verification (lean-proof/)

A formal verification project for the research results (Lean 4.31.0 + mathlib v4.31.0) serving as machine-checkable evidence of correctness:

- **Status matrix**: `lean-proof/STATUS.md` (proved result -> formalization status for each result, with incomplete parts honestly marked).
- **Machine check**: `lean-proof/run-manifest.json` (12 .lean files under SL/ scanned, 0 sorry/admit/axiom hits, `lake build` exit 0, 8572 jobs).
- **Obligation-level audit**: `lean-proof/audit_report.md` + `verification.json` (24 obligations O1-O24, verdict FORMALLY_VERIFIED).
- **Done**:
  - $H^2$ completeness line complete: StabilityGrowth / MomentRecurrence / MomentBound / Completeness (growth lemma, moment recurrence/scaling, $L^2$ moment bound, annihilation + Weierstrass finish).
  - $H^3$ line: H3Completeness (moment-jump/scaling/growth/annihilation algebraic core) + H3MomentBound (analytic $H^1$ moment bound, Cauchy-Schwarz, wired into hbdE/hbdO to close all moments to zero).
  - First step of the $H^s$ line: TransferOperator (closed form of the transfer operator $K_c^{-r} x^k$ + bijectivity of $K_c$).
  - Stability-threshold core: Stability (Thm 2.2 functional core + Thm 2.3 sharpness series).
  - Core trigonometric closed form of the ratio-supremum line: BalancedPhase.
  - Third-order recurrence line: ThirdOrder (fixed-point equivalence + exact order reduction) + ThirdOrderClosedForms (even/odd closed forms verified + fixed-point trajectories + ratio identities $1/(2n+7)$, $3/(2n+9)$).
- **Not yet formalized (registered)**: the $H^3$ isometry $K_c\colon H^3 \to H^1$ and the $\Delta w = \int w\,dx$ (FTC) gluing; explicit complete orthonormal polynomial system in $H^s$; reproof of the MW lemmas; the gap lines ($n=1$ theorem family, $n \ge 2$ switches/reduction); third-order recurrence classification direction; Krein $c \to 0$ limit; fractional $H^s$ and density criteria.

## Directory layout

| Directory | Contents |
| --- | --- |
| `docs/` | Research documents and full proofs (tex/pdf, including proof packages, research summaries and surveys) |
| `lean-proof/` | Lean 4 formal verification project (status matrix/audit/machine check) |
| `scripts/` | Numerical audit, reproduction and exploration scripts (Python, EVIDENCE level, not proofs) |
| `tools/` | Mathematical tool library (Obsidian-compatible Markdown: analysis/applicability/verification status) |
| `papers/` | Full texts of references (copyrighted items for personal research use only) |
| `research_cache/` | Literature search caches and metadata |
| `images/` | Scanned pages and test images |
| `misc/` | Failed/test artifacts, debugging artifacts and archived data |
| `runs/` | rigorous-open-math-research run directories (contracts/ledgers/audits, per RUN_ID) |
| `state/`, `index/`, `agenda/`, `knowledge/`, `literature/`, `reports/`, `archive/` | Project management (manage-math-research-program): state/index/agenda/knowledge/literature/reports/archive |
| `AGENTS.md` | Project rules + per-session work log (read first) |
| `PROJECT.md` | MRP project entry (ownership and recovery guide) |

## Build and reproduction

```text
# Lean formalization (lean-proof/)
lake build                                     # build the whole package (mathlib compiled on first run)
lake env lean SL/<File>.lean                   # check a single file
python <lean-verify>/scripts/verify_lean_project.py --project lean-proof --build
                                               # sorry/axiom scan + build (refreshes run-manifest.json)

# Documents (docs/, requires xelatex)
xelatex SL_<name>.tex                          # compile each tex document

# Numerical scripts (scripts/, Python 3.10+, numpy/scipy)
python scripts/<name>.py                       # each script header states purpose and precision
```

## Repository structure

- Parent repository: `Zhongshan-Big-Jun/Sturm-Liouville-theory-research` (organization, public)
- Personal fork: `xsoc1/Sturm-Liouville-theory-research` (personal profile, public)
- Sync direction: after content is pushed to the parent, GitHub's Sync fork brings the fork to the same commit.

## Working methods

- Read `AGENTS.md` first when entering the project (code rules, strictness labeling rules, session log).
- Mathematics research via `$rigorous-open-math-research`; project management via `$manage-math-research-program`; Lean formal verification via `$lean-verify`; end-to-end orchestration (manage-research-verify) via the `$math-research-workflow` plugin.
- Answer questions honestly; numerical evidence must never be presented as results; assertions without a rigorous proof must never be called "solved".
