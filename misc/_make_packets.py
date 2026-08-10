# -*- coding: utf-8 -*-
import hashlib, json, io, os

ROOT = r"F:\LaTeX\BVE research"

def h6(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:6].upper()

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", os.path.relpath(path, ROOT))

t1_hash = h6("gap-n1 KEY LEMMA closure delegation 2026-08-06")
t1_task = "Q-20260806-keylemma-" + t1_hash
t1_run  = "R-20260806T011500Z-keylemma-" + t1_hash
t2_hash = h6("gap-n1 O3a branch lemmas A-C delegation 2026-08-06")
t2_task = "Q-20260806-o3a-branch-" + t2_hash
t2_run  = "R-20260806T011500Z-o3abranch-" + t2_hash

packet1 = """# Research task packet

- **Task ID**: @@TASK@@
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
- Environment: Python 3.10 at C:\\Users\\HuangZY\\AppData\\Local\\Programs\\Python\\Python310\\python.exe
  (numpy 2.2.6, scipy 1.15.3); xelatex at D:\\texlive\\2024\\bin\\windows\\xelatex.exe;
  PhaseSolver and gap_lib.py available under the run roots and scripts/.
- If the KEY LEMMA is proved, the final proof document goes to docs/SL_gap_n1_proof.tex
  (manager compiles); the solver run must produce candidate_proof.md and audit_report.md.

## Required run location

runs/rigorous-open-math-research/@@RUN@@/

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
"""

packet2 = """# Research task packet

- **Task ID**: @@TASK@@
- **Project ID**: MRP-20260731-BVE-SL
- **Created**: 2026-08-06T01:15:00Z
- **Task type**: solve
- **Portfolio problem ID**: O-2026-SL-GAP-3B7A2C
- **Task state**: DRAFT

## Project reason for this task

For the n=1 adjacent-gap extremal theorem, the 2-parameter extremum step (obligation O3a:
any sign-consistent interior critical point of D over the barrier family satisfies b = 1 - a)
was reduced by a prior run to three explicit branch lemmas (A/B/C) via proven theorems
T1-T4 (fixed-point reformulation, sigma-equivariance, exact identity dR1/db = -dR2/da).
Closing Lemmas A-C proves uniqueness up to reflection, hence the symmetric configuration is
the unique extremizer. This is the second critical-path item and is independent of the
KEY LEMMA delegation running in parallel.

## Authoritative problem source

The exact statements to prove are Lemma A, Lemma B, Lemma C in:
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md,
  Section 4 (exact remaining gap), with the supporting theory T1-T4 in Sections 1-3.
Summary of the three lemmas (recheck against the source before use):

- Lemma A: on the common a-range where both good branches Gamma_1, Gamma_2 exist, the branch
  functions g1, g2 are C^1 with g1'(a) > g2'(a) > 0, with an R-uniform positive lower bound
  on g1' - g2'. Numerics: min(g1'-g2') = 42.78 (R=1.05) down to 0.287 (R=100); margin shrinks
  with R, so a proof must give an explicit R-uniform bound.
- Lemma B: endpoint signs of h = g1 - g2: h < 0 at the left end and h > 0 at the right end of
  the common range; endpoints originate from the R->1 limiting zero positions arccos(1/4)/pi
  and arccos(-1/4)/pi.
- Lemma C: coverage: every sign-consistent fixed point lies on both good branches.

Given Lemmas A-C, T4 yields at most one fixed point; combined with the existence of the
symmetric fixed point it is exactly one and symmetric (b = 1 - a) by T2.

## Source bundle

| Item | Version | Path | Role | Verification note |
|---|---|---|---|---|
| Agent B report (O3a) | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md | authoritative reduction T1-T4 + Lemma A/B/C statements | recheck all formulas and numerics |
| Solver library | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentB_lib.py | reproducible numerics (fixed points, branches, h') | floating point; evidence only |
| Trace scripts | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentB_goodbranch*.py, agentB_scan*.py | branch tracing | evidence only |
| O3b report | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentC_O3b_boundary.md | boundary-case context | context only |
| Obligation graph | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/obligation_graph.md | O3a dependencies | recheck |
| Primary literature | cited | papers/ (Mahar-Willner 1976, AEH arXiv:2407.02459, Cheng-Kung-Law-Lian 2010) | background | recheck against original sources |

## Related paper analyses

No independent structured analysis exists beyond the prior run reports listed above.

## Relevant tool-library leads

- tools/residual-exactness.md (T3 identity and second-order sensitivity attempts)
- tools/gap-n1-reduction.md (why O3a matters)
Leads only; do not treat as verified premises.

## Known ambiguities and bibliographic risks

- Agent B's earlier attack on Lemma A via second-order sensitivity (closed-form spectral sums
  of eigenfunction products) produced no clean formula; the route is recorded as failed.
- T is NOT a global contraction (R=100 fixed point is a repeller with spectral radius 1.642
  and a genuine 2-cycle); contraction-type arguments are refuted.
- fptable rows for R=50/100 (a~0.002, b~0.997) are spurious non-sign-consistent residual
  roots and must be excluded.
- The claim has not been refuted at any R in {1.02, 1.05, 1.2, 1.5, 2, 3, 4, 5, 10, 20, 50,
  100, 1000}: exactly one good root each, a+b-1 ~ 1e-14.

## User constraints and available resources

- Chinese final reporting; ASCII punctuation in all files; citations with clickable links.
- At least 8 hours of effective research time before concluding; failure routes and lessons
  must be recorded in the research ledger.
- Environment: Python 3.10 at C:\\Users\\HuangZY\\AppData\\Local\\Programs\\Python\\Python310\\python.exe
  (numpy 2.2.6, scipy 1.15.3); xelatex at D:\\texlive\\2024\\bin\\windows\\xelatex.exe;
  solver/zero library agentB_lib.py under the prior run root.
- If Lemmas A-C are proved, the integrated proof document goes to docs/SL_gap_n1_proof.tex
  (manager compiles); the solver run must produce candidate_proof.md and audit_report.md.

## Required run location

runs/rigorous-open-math-research/@@RUN@@/

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
"""

p1 = packet1.replace("@@TASK@@", t1_task).replace("@@RUN@@", t1_run)
p2 = packet2.replace("@@TASK@@", t2_task).replace("@@RUN@@", t2_run)
write_utf8(os.path.join(ROOT, "agenda", "task-packets", t1_task + ".md"), p1)
write_utf8(os.path.join(ROOT, "agenda", "task-packets", t2_task + ".md"), p2)

p = os.path.join(ROOT, "index", "task-packets.json")
with io.open(p, "r", encoding="utf-8-sig") as f:
    tp = json.load(f)
tp["items"].extend([
    {"task_id": t1_task, "path": "agenda/task-packets/" + t1_task + ".md",
     "problem_id": "O-2026-SL-GAP-3B7A2C", "state": "READY",
     "run_id": t1_run, "dispatched_at": "2026-08-06T01:15:00Z"},
    {"task_id": t2_task, "path": "agenda/task-packets/" + t2_task + ".md",
     "problem_id": "O-2026-SL-GAP-3B7A2C", "state": "READY",
     "run_id": t2_run, "dispatched_at": "2026-08-06T01:15:00Z"},
])
tp["updated_at"] = "2026-08-06T01:15:00Z"
write_utf8(p, json.dumps(tp, ensure_ascii=False, indent=2) + "\n")

for run_id, task_id in [(t1_run, t1_task), (t2_run, t2_task)]:
    rr = os.path.join(ROOT, "runs", "rigorous-open-math-research", run_id)
    os.makedirs(rr, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "project_id": "MRP-20260731-BVE-SL",
        "task_id": task_id,
        "upstream_skill": "$rigorous-open-math-research",
        "upstream_skill_version_or_hash": "v2026-08-05 (changelog)",
        "started_at": "2026-08-06T01:15:00Z",
        "completed_at": None,
        "run_root": "runs/rigorous-open-math-research/" + run_id,
        "task_packet_path": "agenda/task-packets/" + task_id + ".md",
        "task_packet_sha256": None,
        "upstream_status_verbatim": None,
        "artifacts": [],
        "environment": {
            "model": None,
            "tools": ["Python 3.10 (numpy 2.2.6, scipy 1.15.3)", "xelatex (TeX Live 2024)"],
            "formal_systems": [],
            "unknown_fields": ["model"]
        },
        "manager_ingestion_state": "DISPATCHED",
        "missing_or_unavailable_artifacts": [],
        "notes": ["manager-created run root; upstream writes problem-level artifacts"]
    }
    write_utf8(os.path.join(rr, "run-manifest.json"), json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    write_utf8(os.path.join(rr, "task-packet-link.txt"), "task packet: agenda/task-packets/" + task_id + ".md\n")

print("T1:", t1_task, t1_run)
print("T2:", t2_task, t2_run)