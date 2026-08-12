# Research task packet

- **Task ID**: Q-20260806-keylemma-E58FB1
- **Project ID**: MRP-20260731-BVE-SL
- **Created**: 2026-08-06T01:15:00Z
- **Task type**: solve
- **Portfolio problem ID**: O-2026-SL-GAP-3B7A2C
- **Task state**: DRAFT

## Project reason for this task

The n=1 adjacent-gap extremal proof (SUP/INF of D=lambda_2-lambda_1 over the box class
1<=rho<=R, Dirichlet string) is reduced to a single unproven inequality, the KEY LEMMA
(obligation O2 in the run obligation graph). Proving it closes O2 completely: the symmetric
3-block barrier family then has a unique maximizer u*(R) with the predicted sign pattern, and
the well family follows identically. This is the highest-leverage step in the current program
and the template for n>=2.

## Authoritative problem source

The exact statement to prove is the KEY LEMMA in:
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentA_O2_single_crossing.md,
  Section 2.9 (statement and equivalent forms), with the full derivation in Sections 2.1-2.8.
Project-level restatement (docs/SL_gap_n1_research_summary.pdf, tools/key-lemma-decomposition.md):

For all q>1 and all c in (0,1/2):
  (d/dc) log( M1(c)/M2(c) ) < 0,
where M(alpha;c) = q(q^2-1) alpha^2 sin^2(alpha) / (q + c Phi(alpha)),
Phi(alpha) = cos^2(alpha) + q^2 sin^2(alpha), M_k(c) = M(alpha_k(c);c),
and alpha_1(c) in (0,pi/2), alpha_2(c) in (0,pi) are the intersections of beta = c*alpha
with the even/odd secular curves of the half-problem:
  even: tan(alpha_1) tan(alpha_1 q v/u) = 1/q,
  odd:  q tan(alpha_2) + tan(alpha_2 q v/u) = 0,  with v/u = c (i.e. u = q/(2(c+q))).
Equivalent forms established in the source: G(alpha_2(c);c) > G(alpha_1(c);c) and F'(c) < 0,
where F = M1 - M2 and G is the explicit log-derivative in the source.

If the KEY LEMMA holds, T4 in the source upgrades O2 to PROVED (F has exactly one zero on
(0,inf), f_sym one zero u* in (0,1/2) with the required sign pattern, D_sym increases then
decreases at u*). A proof of the equivalent continuation statement (every zero of f_sym(.;R)
is a simple - to + crossing) would also close O2; the source records it as comparable in
difficulty. Either route is acceptable; the upstream decides.

## Source bundle

| Item | Version | Path | Role | Verification note |
|---|---|---|---|---|
| Agent A report (O2) | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentA_O2_single_crossing.md | authoritative derivation and KEY LEMMA statement | recheck every formula; odd secular equation and normalization identities were corrected in this report and machine-verified |
| Phase solver | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentA_verify.py | reproducible numerics (alpha1/alpha2, M, G) | floating point; evidence only |
| KEY LEMMA decomposition tool | 2026-08-05 | tools/key-lemma-decomposition.md | untrusted context: G2-G1 = (A-C)+(B-D), exact corner limits, falsified B-D q-monotonicity | derived in this project; not a proof premise |
| Research summary | 2026-08-05 | docs/SL_gap_n1_research_summary.pdf | status and gap record | context only |
| Obligation graph | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/obligation_graph.md | O2 dependencies (T1-T4) | recheck |
| Primary literature | cited | papers/ (Keller 1976, Mahar-Willner 1976, AEH arXiv:2407.02459) | background theorems | recheck against original sources |

## Related paper analyses

No independent structured analysis of the KEY LEMMA exists. Prior run reports (Agent A-C)
are the closest context and are listed in the source bundle.

## Relevant tool-library leads

- tools/key-lemma-decomposition.md (decomposition identity + corner limit; not a proof)
- tools/gap-n1-reduction.md (why O2 matters)
- tools/two-block-gap-bounds.md (boundary case already proved)
Leads only; do not treat as verified premises.

## Known ambiguities and bibliographic risks

- The KEY LEMMA is project-derived (not from literature); novelty risk low but it must be
  proven from first principles.
- Correct odd secular equation is q*tan(s2u)+tan(s2qv)=0 (the task's older form with the
  product of tangents is FALSE; already corrected and machine-verified).
- Numerical margins of G(alpha2)-G(alpha1) are large (min 2.4481 at R=1.1, growing with R);
  this slack suggests a robust analytic route but is not itself a proof.
- Itemwise q-monotonicity of B-D is FALSE (counterexample c=0.01, q 5000->20000, B-D
  199.79->193.99); any route relying on it must be discarded. A-C q-monotonicity passes all
  sampled grids but is unproved.
- Exact corner limits (q->1+, c->1/2-): A-C -> 2.80613..., B-D -> -0.38773..., sum ->
  4*pi/(3*sqrt3) = 2.41840... (the coarse-grid values 2.8086/-0.3751/2.4258 in an earlier
  handoff are superseded by these exact limits).
- Boundary cases: c->0+ (alpha1->pi/2, alpha2->pi) and c->1/2- (alpha1 = pi - alpha2) are
  explicit; the estimates near these endpoints must be handled rigorously.

## User constraints and available resources

- Chinese final reporting; ASCII punctuation in all files; citations with clickable links;
  final section listing the mathematics involved when a document is produced.
- At least 8 hours of effective research time before concluding; failure routes and lessons
  must be recorded in the research ledger.
- Environment: Python 3.10 at C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  (numpy 2.2.6, scipy 1.15.3); xelatex at D:\texlive\2024\bin\windows\xelatex.exe;
  PhaseSolver and gap_lib.py available under the run roots and scripts/.
- If the KEY LEMMA is proved, the final proof document goes to docs/SL_gap_n1_proof.tex
  (manager compiles); the solver run must produce candidate_proof.md and audit_report.md.

## Required run location

runs/rigorous-open-math-research/R-20260806T011500Z-keylemma-E58FB1/

## Upstream invocation

Use $rigorous-open-math-research on the concrete problem in this task packet. Treat this
packet as project context, not as a verified theorem contract. Independently normalize and
audit the exact statement, and recheck every theorem used as a premise against its original
source and exact version. Follow the upstream skill's own problem-level workflow and output
protocol. Write all standard artifacts under RUN_ROOT. Return the upstream result status
verbatim together with the run root and artifact locations. Do not call
manage-math-research-program from inside the solver run.

## Manager ingestion checklist

- [ ] Preserve upstream status verbatim.
- [ ] Index the run root and artifact paths/hashes.
- [ ] Do not copy or replace upstream standard artifacts.
- [ ] Update the portfolio, maps, tool candidates, budget, checkpoint, and resume entry.
- [ ] Promote reusable knowledge only from exact source or audited artifact locations.
