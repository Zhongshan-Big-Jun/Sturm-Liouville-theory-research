# Pilot v4 review plan

## Scoring (100 pts) — same as pilot v3/two-arm plan

- Mathematical correctness/closure: 40
- Contract fidelity/completeness: 20
- Strict progress over blind start: 15
- Epistemological calibration: 10
- Citation/evidence fidelity: 10
- Reproducibility: 5

Accepted: score >= 70, correctness >= 32/40, no FATAL_GAP / WRONG_PROBLEM /
circular load-bearing citation, no numerical-evidence-as-proof.

## Review procedure

1. After the 2-hour cap / natural completion, freeze all arm outputs.
2. For each (arm, task), collect the candidate final artifact:
   - A/B: `arms/{A,B}/U*/final_response.md` plus any `final_report.md` / persistent artifacts in the arm sandbox.
   - C: `F:\tools\rethlas-deepseek\agents\generation\results\pilot-U*\problem\{blueprint.md,blueprint_verified.md}` and `logs/`.
   - D: `F:\tools\danus-deepseek\runtime\projects\pilotU*\fact_graph\facts\` and `workers/*/memory`.
   - E: `F:\tools\mmat-deepseek\data\workspace\pilot-U*\` (final proof artifacts, lemmas, presentation).
3. Blind independent reviews: separate subagents, no access to other arms' outputs or arm identities until verdicts recorded.
4. Verdicts: PASS / REPAIRABLE_GAP / PARTIAL_NOT_COMPLETE / FATAL_GAP / WRONG_PROBLEM.
5. Fill `RESULTS.md`: per-arm-per-task summary, highlights, independent review, score table, accepted count.
6. Copy results into `runs/three-arm-pilot-v2/pilot-v4-long/` and commit/push when network allows.
