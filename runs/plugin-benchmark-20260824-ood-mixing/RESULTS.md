# OOD benchmark results: exponential mixing by bounded shear

Date: 2026-08-24
Problem: QED analysis-Apr-24 problem 3 (unpolluted, withheld correct proof)
Expected answer: **No** — exponential `dot H^{-1}` decay by a uniformly bounded `W^{1,1}` shear is impossible.

## Main results table

| Arm | Actual implementation | Outcome | Independent review | Wall | Steps / tool calls | Token proxy | Artifact |
|---|---|---|---|---:|---:|---:|---:|
| A | DSH subagent + `rigorous-open-math-research` v1.6.0 | Complete candidate proof: No (self-contained) | PASS | 502.3 s | 14 / 19 | in 65,963; cache 803,712; out 55,024 | 16,162 B |
| B | Blank control (plain prompt) | Partial: No, with key lemma sketched | PARTIAL_NOT_COMPLETE | 762.5 s | 11 / 10 | in 21,520; cache 703,744; out 84,502 | 9,247 B |
| C | Rethlas actual (Codex gen + verify service) | Complete blueprint: No; verification service 500, no `blueprint_verified.md` | PASS (blueprint) | 1,031 s | Codex iter 0–2 | codex tokens used ≈ 909,689 | blueprint 17,955 B + memory |
| D | Danus actual (codex branch, workers + verifier fact graph) | Verifier-gated fact graph: No; 3 verified facts | REPAIRABLE_GAP if only theorem fact; full fact graph supplies lemmas | ≈ 1,200 s | 2 workers, 2 rounds | captured codex tokens ≈ 286,649 | project 320,611 B |
| E | MMAT actual (NL-Prover Codex harness) | No final artifact; orchestration started, no proof files, reconnect/stopped | not applicable | attempted ≈ 780 s | no completed output | no token data | 0 files |

## Independent review summary

- Candidate 1 = A: PASS (HIGH). Self-contained; explicit solution, k=0 sector, W^{1,1} tail lemma, polynomial lower bound.
- Candidate 2 = B: PARTIAL_NOT_COMPLETE (HIGH). Central frequency-localization lemma only sketched.
- Candidate 3 = C: PASS (HIGH). Self-contained blueprint; literature remarks explicitly non-load-bearing.
- Candidate 4 = D: REPAIRABLE_GAP (HIGH) when judged as the single theorem fact; the missing decisive lemma exists as separately verified Danus facts `3d7f...` and `7cfe...`, so the full fact graph is complete.

## Caveats

1. **All actual external systems ran through Codex CLI backed by DeepSeek `deepseek-chat`**, not the upstream projects' default OpenAI/Claude models.
2. **Rethlas used MCP theorem search/downloads** despite the no-network instruction; protocol deviation noted. Its verification service returned HTTP 500 for all inputs, so no `blueprint_verified.md` was produced.
3. **MMAT did not complete** in the observed window. A read-only first attempt could not write files; a writable second attempt hit Codex reconnect errors and was stopped after ~13 minutes with only `problem.md` in the workspace.
4. **Danus captured token data is partial** (round-1 codex runs; some round-2 codex runs were cut off when workers were stopped).
5. This is still a single hard problem, not a full benchmark suite; no statistical generalization claim.

## Artifacts

- `frozen_task.md`
- `metrics.json`
- `independent_review.md`
- `arms/a-our-plugin/`, `arms/b-blank/`, `arms/c-rethlas/`, `arms/d-danus/`, `arms/e-mmat/`
- External deployment dirs:
  - `F:\tools\rethlas-clone\Rethlas`
  - `F:\tools\danus-clone\Danus` (codex branch)
  - `F:\tools\mmat-agent-team`
