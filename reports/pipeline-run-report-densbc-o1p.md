# Pipeline run report: DensBC O1' via /math-research-workflow

- Report date: 2026-08-16
- Run ID: R-20260816T210000Z-densbc-o1p
- Task packet: Q-20260816-densbc-o1p-F6E7D8A9
- Status: RIGOROUS_PARTIAL_RESULT (O1' closed on a structured subclass; general O1' remains open)

## 1. Problem chosen and why

Chosen from the Sturm-Liouville-theory-research repo: the DensBC O1' reduced core
(effective open problem), defined in
`runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/candidate_proof.md`
section 7. O1' asks whether some free run-base degree admits a nonzero `w in H`
whose moments satisfy the kept recursions and membership `<w,v_j>=0`. This is a
moment-representability + membership problem; it is the honest remaining core of
the boundary-constrained polynomial-density question. It was already audited as
POTENTIALLY_NEW / OPEN, so it is a legitimate research target.

## 2. What happened, step by step

### Stage A (manage)

1. Read project state: RESUME/current open problems; read the upstream DensBC O1
   candidate_proof and status_and_literature to extract O1'.
2. Ran a web sweep ("polynomial density constrained subspace kernel intersection
   moment representability criterion") and found only whole-space RKHS /
   moment-problem literature, no constrained-subspace kernel-intersection
   criterion. Recorded openness = OPEN.
3. Created task packet
   `agenda/task-packets/Q-20260816-densbc-o1p-F6E7D8A9.md` with a Novelty
   preflight (B0) section.
4. Initialized project `research_map.md` (research-map feature) and recorded the
   O1' context, a human contribution, and avoid notes via
   `update_research_map.py`.
5. Created the run directory and a whiteboard skeleton.

### Gate check (Stage A gate)

6. Ran `scripts/validate_pipeline.py --project .`. It reported hard FAILs:
   - the new task packet was missing required fields/sections (Project ID, Task
     state, Upstream invocation, Source bundle, Required run location);
   - the new whiteboard was missing the required bold `**Run ID:**` /
     `**Task packet ID:**` fields;
   - `_xsoc1_work/.../pipeline-handoff-bad/...` (nested plugin repo fixtures)
     was being scanned and failing intentionally.

### Bug fixes

7. Fixed the task packet to conform to the required format.
8. Fixed the whiteboard to use the required bold fields.
9. Fixed a real plugin bug in `validate_pipeline.py`: nested git repositories
   (e.g. `_xsoc1_work/`) inside the project were being validated as project
   content. Added `is_in_nested_repo()` and filtered handoff / whiteboard /
   evidence scans; added `tests/smoke_nested_repo.py` to prevent regression.
   Re-ran gate: 0 problems (only advisory warnings).

### Stage B (research)

10. Dispatched an independent solver subagent for O1' with a self-contained
    prompt (write artifacts under the run dir; STRICT/EVIDENCE discipline; no
    completion claims).
11. Monitored progress by polling agent status and reading the growing run-dir
    artifacts (problem_contract, whiteboard, candidate_proof).
12. The solver chose a concrete structured subclass: H_beta (diagonal weighted
    sequence space) with finite-degree polynomial Riesz representers (finite
    moment constraints). Rationale: simplest non-coordinate case with finite
    representer moments and cofinite kept set.
13. Solver produced STRICT results:
    - Theorem 1: kept set cofinite, finite run system and finite free-base set.
    - Theorem 2: moment parameterization V cap Q_sp^\perp <-> (finite membership
      matrix equation Tt=0 + weighted summability).
    - Lemma 3: infinite run admissible iff beta > 3/2.
    - Theorem 4 (main): density iff ker(T|_{B_adm}) = {0}; decision is finite
      linear algebra on the subclass.
    - Theorem 6: coordinate case recovers upstream Theorem E exactly.
    - Example 7: non-coordinate polynomial representer v_1 = x^4 + alpha x^6
      gives a finite free-base obstruction for every beta (density fails).
14. The solver ran its own independent adversarial audit (fresh subagent), which
    returned REPAIRABLE_GAP with 5 localized issues (conjugation convention,
    alpha convention, N index-set ambiguity, injectivity / 0-inf convention,
    r=0 notation). All 5 were repaired in candidate_proof.md.
15. A second, separately dispatched adversarial audit subagent was started for
    cross-check (see section 6 for its outcome).

### After Stage B

16. Research map updated with the selected route, the intermediate result, the
    rejected single-column route and an avoid instruction.
17. Solver wrote all standard artifacts (problem_contract, whiteboard,
    research_ledger, approach_registry, candidate_proof, audit_report,
    run-manifest.json with `formalization: scaffold`).

## 3. Other actions / monitoring

- Used `list_agents` to watch solver + audit subagents (status transitions:
  running -> ready).
- Read run-dir files at several points to observe intermediate content
  (problem_contract and candidate_proof were finalized mid-run).

## 4. Bugs encountered and fixed

| # | Bug / issue | Where | Fix |
| --- | --- | --- | --- |
| 1 | Task packet missing required fields/sections | our packet | rewrote to required template |
| 2 | Whiteboard missing bold required fields | our whiteboard | added `**Run ID:**`, `**Task packet ID:**` |
| 3 | Gate validated nested plugin repo `_xsoc1_work` fixtures as project content | validate_pipeline.py | added `is_in_nested_repo()` filter + smoke test |
| 4 | Candidate proof: audit round 1 found 5 localized issues | candidate_proof.md (solver) | repaired by solver (audit loop) |
| 4b | Candidate proof: audit round 2 found 1 wording gap in Theorem 6 | candidate_proof.md (solver) | repaired by orchestrator (finite-component wording + explicit r finite) |
| 5 | (shell quirk) empty `--failure ""` arg dropped by PowerShell when calling update_research_map.py | tooling | omitted empty flags; not a script bug |

## 5. Unexpected behaviors and quality judgments

### Positive (exceeded expectations)

- The solver independently ran its own adversarial audit and repaired findings
  before reporting (not required by the prompt) - good autonomous rigor.
- The solver correctly rejected the "single zero column is the whole answer"
  route as insufficient (non-coordinate constraints couple free bases) and used
  the full kernel criterion - good mathematical judgment.
- Honest labeling: status is RIGOROUS_PARTIAL_RESULT, subclass closed, general
  O1' explicitly left open - exactly the calibration the workflow requires.
- STRICT/EVIDENCE discipline held; no numerical evidence was used as proof.
- Regression checks (r=0, coordinate R, Example 7 consistency) were included.

### Issues / room for improvement

- Our own Stage A bookkeeping initially did not satisfy the gate (packet and
  whiteboard) - a process slip on the orchestrator side, caught by the gate;
  fixed. This validates the gate.
- The gate did not ignore nested repositories - a plugin bug; fixed with a
  regression test. (This is a genuine "plugin did not run as expected" finding.)
- Shell quoting with the research-map helper is finicky; CLI could later accept
  repeated flags or a JSON payload (nice-to-have).

## 6. Audit outcome (second independent cross-check)

A separate adversarial audit subagent (fresh context, no conversation history)
reviewed candidate_proof.md and returned:

- **Verdict:** REPAIRABLE_GAP
- **Critical errors:** 0
- **Gaps:** 1 (minor, localized: Theorem 6 finite-component wording)
- **Overall:** the core proof correctly closes O1' on the structured H_beta
  subclass; only a one-line clarification was needed.

The gap: the literal sentence "every finite component contains at least one
constrained degree" is false for pinned singleton components `{0}`, `{1}` when
unconstrained (they carry no free parameter). Repaired in candidate_proof.md:
now "every finite component that contains a free base contains at least one
constrained degree"; also added the explicit standing hypothesis `r` finite in
Section 0. The independent auditor's per-obligation notes confirmed Theorem 2,
Lemma 3, Theorem 4, Example 7, the cofinite kept-set, and the algorithmic
content all PASS.

## 7. Result

- O1' CLOSED (STRICT) on the subclass: H_beta, beta >= 0, with finite-degree
  polynomial Riesz representers / finite moment constraints.
- Exact criterion: closure(span Q_sp) = V  <=>  ker(T|_{B_adm}) = {0} (columns
  A m_b for admissible free bases independent); admissible = finite run, or
  infinite run with beta > 3/2.
- Coordinate Theorem E recovered; non-coordinate Example 7 exhibits density
  failure.
- General O1' (arbitrary H, infinite-band representer data) remains OPEN.
