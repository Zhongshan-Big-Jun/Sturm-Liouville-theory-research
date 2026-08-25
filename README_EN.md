# Sturm-Liouville Boundary Value Problems Research (BVE research)

中文版: [README.md](README.md)

A frontier mathematics research project on Sturm-Liouville (SL) boundary value problems, along two main lines:

1. **Completeness of eigenfunction/polynomial systems**: In which Hilbert space (left-definite space) is the solution set of an SL boundary value problem equivalent to all orthonormal function systems in that space? Baseline paper: Littlejohn-Quintero-Roba, *Krein-Sobolev Orthogonal Polynomials* (Springer 2025, DOI 10.1007/978-3-031-90135-5_7).
2. **Optimal bounds for eigenvalue gaps and ratios**: For the weighted Dirichlet problem $-y'' = \lambda \rho y$, $0 < a \le \rho \le A$ (measurable box class), optimize the adjacent spectral gap $D_n = \lambda_{n+1} - \lambda_n$ and the ratio $\lambda_{n+1}/\lambda_n$.

Strictness convention: rigorous proofs and numerical evidence are explicitly distinguished; assertions without a rigorous proof are never labeled "solved".

## Main results

### Rigorously proved (see docs/ for details)

| Result | Source | Status |
| --- | --- | --- |
| Closed form $\sup_{n,\rho} \lambda_{n+1}/\lambda_n = \nu(R)$ (balanced-phase method) | `docs/SL_ratio_proof.tex` | Proved |
| $\inf_{n,\rho} \lambda_{n+1}/\lambda_n = 1$ (Weyl asymptotics; infimum not attained) | `docs/SL_inf_ratio_proof.tex` | Proved |
| Independent reproof of Mahar-Willner Lemmas 1-2 (periodic extension + zero truncation) | `docs/SL_mw_lemma_reproof.tex` | Proved |
| Structural stability of the degenerate limit $c \to 0$ of the shifted Krein operator | `docs/SL_krein_c0_limit.tex` | Proved |
| $\{p_n\}$ analytically complete in $H^2$ (moment-jump criterion + growth lemma) | `docs/SL_h2_completeness_proof.tex` | Proved |
| $\{p_n\}$ complete in every integer left-definite space $H^s$ ($s \ge 1$) | `docs/SL_h3_completeness_proof.tex` | Proved |
| $n=1$ gap extremals: SUP/INF attained by $[1,R,1]$ / $[R,1,R]$ | `docs/SL_gap_n1_proof.tex` et al. | Proved |
| $n \ge 2$ gaps: finite-block reduction (at most $2n+1$ blocks) + exact $2n$-switch theorem | `docs/SL_gap_nge2_finite_reduction_proof.tex`, `SL_gap_nge2_exact_2n_switches_proof.tex` | Proved |
| Even minimal-solution anchor $K(1)=e/4$ | `docs/SL_third_order_K1_proof.tex` | Proved (STRICT for the even c=1 anchor; general $K(c)$ open) |
| $n \ge 2$ gaps (local): reflection symmetry at $R=1$ + local uniqueness as $R \to 1$; global uniqueness depends on $(G1')/(G2)$ (open) | `docs/SL_gap_nge2_symmetry_local_proof.tex` | Proved (local) |

### Partial proofs / strong numerical conjectures / open problems

- Fixed-$n$ supremum: symmetric phase structure proved, closed forms for $n=1,2$; global extremality and the $2n$-root count remain open (`docs/SL_fixed_n_supremum.tex`).
- Global symmetry and minimal block count for $n \ge 2$ gap extremals: local theorems at $R=1$ and as $R \to 1$ are proved; global uniqueness depends on the open conditions $(G1')/(G2)$; the rest is strong numerical conjecture (`docs/SL_gap_nge2_symmetry_local_proof.tex`).
- Authoritative open-problem list: `docs/SL_spectral_topics_summary.tex`, Section 5.
- Literature: no published result directly equivalent to the $n \ge 2$ theorems was found; the project does not claim priority, and early literature such as Willner-Mahar 1979 remains an overlap risk.

## Current open problems

Authoritative list: `docs/SL_spectral_topics_summary.tex` §5 (per-problem progress and failed routes).

1. **Structure closure for gap extremals** ($n\ge2$): closed forms for switch positions/block lengths, reflection symmetry and uniqueness (reduced to proving (G1$'$) $\det K>0$), closed form or sharp bounds for $\max/\min D_n$, formalization of the $n=1$ certificate replay kernel. Progress (2026-08-14 session 105): the M3 piece of (G1') (n=2 INF large-R asymptotics) has its level-cascade STRICT structure confirmed by an independent adversarial audit (INDEPENDENTLY_AUDITED_PROOF, R-210/R-211/R-212) plus a decisive negative result (no K0~3.46 zero of the truncated integer-power system through u^7); the corrected-branch seed root and closed observables remain open; next (P1): joint {K0,K1,C0,C1} solve or a log-correction ansatz.
2. **General boundary/potential classes**: Neumann case (Li-Ao line), nonnegative potential $q\ge0$ (Gan-Zheng-Li-Shao line), and sign-changing weights - optimal constants and extremal structure for eigenvalue ratios.
3. **Unified MDE extremal-measure theory**: extremal measures for Neumann gaps and maximal gaps, unified with nodal bounds (Chu-Guo-Meng-Zhang).
4. **General denseness criterion in left-definite spaces**: necessary and sufficient conditions for polynomial density in Hilbert spaces with general boundary constraints. Progress (2026-08-14 session 106, run R-20260814T070000Z-densbc): STRICT theorems A-H (master criterion V ∩ Q^\perp = {0}; constrained moment characterizations; corrected constraints-restore-density; complete diagonal classification: the sparse family is dense in a coordinate-constrained subspace iff beta <= 3/2 AND R has no finite run; first-moment/jump criteria on V); two packet conjectures falsified (V = span{x^2,x^3}^\perp is NOT dense for all beta - free parameters relocate to M_4/M_5; the criterion "beta <= 3/2 OR constraints kill M_2 = M_3" is false - R = {4} creates a finite singleton run); open core O1-O3 (exact criterion for general non-diagonal H / general L_j expansions / fractional window).
5. **Nonlinear generalizations (p-Laplacian etc.)**: scope of the Wen-Zhou singular-measure technique.
6. **General moment-representability criterion**: closed-form criterion in general Hilbert spaces.
7. **Threshold-line classification for jump stability**: coefficient families on the threshold line ($\sum\sim\log m$) not fully classified; higher-order moment-jump replacement mechanism (S3) for variable-coefficient operators.
8. **Third-order recurrence theory**: general $K(c)$ closed form, source-term control and exclusion of degenerate configurations in box induction, and classification of product solutions for general coefficient families remain open. The even c=1 anchor $K(1)=e/4$ is proved in `docs/SL_third_order_K1_proof.tex`.
9. **Fixed-$n$ supremum closure**: global extremality (Keller reduction), $2n$-root count, monotone convergence $\Lambda_n^{\sup}(R)\downarrow c_\infty(R)$.
## Lean 4 formal verification (lean-proof/)

A machine-checkable proof project (Lean 4.31.0 + mathlib v4.31.0). Authoritative status: `lean-proof/STATUS.md` (status matrix) + `lean-proof/audit_report.md`/`verification.json` (obligation-level audit, O1-O24). Current machine check: 26 `SL/*.lean` files, 0 `sorry/admit/axiom` hits, `lake build` exit 0, 8584 jobs.

**Done (by proof line)**

- Completeness lines: $H^2$ full chain (StabilityGrowth/MomentRecurrence/MomentBound/Completeness), $H^3$ algebraic core (H3Completeness/H3MomentBound/H1Isometry), $H^s$ transfer reduction (TransferOperator/HsOrthogonalSystems), density moment characterization (DensenessCriteria).
- Ratio line: balanced-phase closed form (BalancedPhase), three-block transfer matrices/secular equations (TransferMatrix), reflection symmetry of the fixed-$n$ alternating configuration (ReflectionSymmetry).
- Other lines: stability-threshold core (Stability), third-order recurrence line (ThirdOrder/ThirdOrderClosedForms/ThirdOrderClassification/ThirdOrderMinimal), Krein $c\to0$ polynomial level (KreinDegenerateLimit/KreinHighGrowth), $n=1$ gap symmetry-line algebraic core (SymlineTensionRatio, including the $\gamma_0^*$ threshold and Lemma ys2, certificate-free; SymlineKeyLemma adds the P1/P2 log-derivative bounds and the W0 lemma; SymlineUniqueZero adds the KEY-LEMMA assembly core of section 4.4 (unique zero + sign conclusions, with endpoint signs/phase-branch/derivative-identity kept as analytic hooks)).

**Not yet formalized (by gap type, consistent with STATUS.md)**

- Spectral/functional-analysis dependencies: isometries $K_c\colon H^2\to L^2$ (O16) and $H^3\to H^1$, $H^s$ operator-level isometry and completeness, density finish ($w=0$), Krein quotient level ($H^1/W \cong L^2_0$), Weyl asymptotics (inf-ratio line), MW lemma reproof, transfer-matrix-to-eigenvalue spectral connection.
- Proved but not started: $n=1$ gap line (gap_n1_proof/well_rigidity/O3a/inf_limit; the symline algebraic core is partly formalized, see SymlineKeyLemma/SymlineUniqueZero) and $n\ge2$ switch/reduction documents, fractional $H^s$ sparse-basis completeness.
- Numerical/non-rigorous in source (not formalized): global extremality for $n\ge2$ gaps, $2n$-root count for the fixed-$n$ supremum, nonzero Casoratian of the three third-order solutions.
- Hypothesized inputs: the classical Legendre/Krein-Sobolev orthogonality facts in HsOrthogonalSystems (literature facts, not formalized).

## Directory layout

| Directory | Contents |
| --- | --- |
| `docs/` | Research documents and full proofs (tex/pdf) |
| `lean-proof/` | Lean 4 formalization project (status matrix/audit/machine check) |
| `scripts/` | Numerical audit and reproduction scripts (Python, EVIDENCE level, not proofs) |
| `tools/` | Mathematical tool library (Obsidian-compatible Markdown) |
| `papers/` | Reference full texts (copyrighted items for personal research only) |
| `research_cache/`, `images/`, `misc/` | Search caches, scanned pages, failed/test artifacts |
| `runs/` | rigorous-open-math-research run directories (contracts/ledgers/audits) |
| `state/`, `index/`, `agenda/`, `knowledge/`, `literature/`, `reports/`, `archive/` | Project management (manage-math-research-program) |
| `AGENTS.md`, `PROJECT.md` | Project rules + session log; MRP project entry |

## Build and reproduction

```text
# Lean formalization (lean-proof/)
lake build                                     # build the whole package (mathlib compiled on first run)
lake env lean SL/<File>.lean                   # check a single file
python <lean-verify>/scripts/verify_lean_project.py --project lean-proof --build
                                               # sorry/axiom scan + build (refreshes run-manifest.json)

# Documents (docs/, requires xelatex)
xelatex SL_<name>.tex

# Numerical scripts (scripts/, Python 3.10+, numpy/scipy)
python scripts/<name>.py                       # each script header states purpose and precision
```

## Repository structure

- Parent repository: `Zhongshan-Big-Jun/Sturm-Liouville-theory-research` (public)
- Personal fork: `xsoc1/Sturm-Liouville-theory-research` (public)
- Sync: after pushing content to the parent, the fork is synced to the same commit (the project `project.json` sets `git_sync.push_order = ["origin", "fork"]`, executed by `sync_remotes.py` from the manage skill).

## Working methods

- Read `AGENTS.md` first when entering the project (code rules, strictness labeling, session log).
- Mathematics research: `$rigorous-open-math-research`; project management: `$manage-math-research-program`; Lean verification: `$lean-verify`; end-to-end orchestration: `$math-research-workflow` plugin.
- Answer questions honestly; numerical evidence must never be presented as results; assertions without a rigorous proof must never be called "solved".
