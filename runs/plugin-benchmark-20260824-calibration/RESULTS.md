# B3 O3 five-arm calibration benchmark — results

Date: 2026-08-24
Benchmark: `B3-O3-CAL-20260824`
Task: prove or disprove that `G_{n,s}` has exactly `2n` simple zeros in `(0, pi)` for every `n >= 1`, `R > 1`.
Status: **calibration / contaminated regression benchmark**, not out-of-distribution evidence.

## Summary

All five arms returned an affirmative proof of the frozen claim, based on the same exact Chebyshev reduction. Four arms passed the independent neutral mathematical review as submitted. The MMAT arm had one non-fatal repairable gap in an auxiliary leading-coefficient formula; that formula has been corrected in its `result.md`, and the theorem conclusion is unchanged.

## Main comparison table

| Arm | Setup | Self-reported outcome | Independent review | Wall (s) | Steps | Tool calls | Input tok | Cache-read tok | Output tok | Artifact (excl task) |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A — our-plugin v1.6.0 | DSH subagent + `rigorous-open-math-research` v1.6.0 | `CANDIDATE_COMPLETE_PROOF` | PASS (HIGH) | 552.9 | 38 | 38 | 51,807 | 2,172,160 | 57,055 | 16,418 B |
| B — blank control | Plain prompt, no skills/plugins/memory/subagents | Complete STRICT proof | PASS (HIGH) | 273.0 | 15 | 14 | 33,686 | 539,776 | 29,944 | 9,615 B |
| C — Rethlas emulation | Rethlas-style memory/branch/counterexample workflow | CORRECT / strict proof | PASS (HIGH) | 387.3 | 23 | 22 | 49,281 | 1,062,656 | 40,752 | 12,943 B |
| D — Danus emulation | Danus-style orchestrator/worker/verifier fact graph | Complete STRICT proof, 11 facts | PASS (HIGH) | 461.3 | 33 | 33 | 45,086 | 1,769,600 | 49,113 | 27,132 B |
| E — MMAT emulation | MMAT-style obligation graph / nl-prover roles | Complete STRICT proof | REPAIRABLE_GAP → fixed (non-fatal) | 361.0 | 25 | 24 | 39,152 | 1,139,584 | 38,817 | 14,705 B |

Token numbers are as recorded by the runtime (`inputTokens`, `cacheReadTokens`, `outputTokens`). `Artifact (excl task)` excludes the common `task.md`.

## Independent neutral review

Review files: `/tmp/bench-review/candidate1_result.md` … `candidate5_result.md` with mapping 1=A, 2=B, 3=C, 4=D, 5=E.

- Candidate 1 (A): PASS — proof faithful, root-count lemma rigorous, audits complete. HIGH confidence.
- Candidate 2 (B): PASS — monotone-phase argument valid, polynomial extension and simplicity correct. HIGH confidence.
- Candidate 3 (C): PASS — sign-alternation lemma valid, hyperbolic exclusion correct, transfers correct. HIGH confidence.
- Candidate 4 (D): PASS — factorization, hyperbolic/elliptic split, and simplicity transfer correct; optional non-binding note to expand `Q_n(delta) != 0`. HIGH confidence.
- Candidate 5 (E): REPAIRABLE_GAP — the claimed leading coefficient `alpha^n(2^n + 2^{n-1} s^{-1})` is wrong; the correct value is `2^n alpha^n`. This is not load-bearing: the polynomial still has exact degree `2n`, and the proof conclusion remains true. The submitted `result.md` has been corrected.

## Protocol and caveats

1. **Contamination**: B3 O3 and the Chebyshev reduction were previously used in this project. Plugin v1.6.0 was developed with knowledge of that history. Results are calibration/regression, not OOD evidence.
2. **Actual model deviation**: pre-registration specified `gpt-5.6-sol` with `xhigh`; all five sessions actually ran `deepseek-v4-flash-vision-exp` with `high` reasoning.
3. **External arms are emulations**: Rethlas, Danus, and MMAT/MMAT were not executed as their complete upstream systems; each was a single-session prompt-level emulation inside an isolated arm directory.
4. **No nested subagents**: none of the five arms spawned subagents (`subagent_calls = 0`). Arm A was permitted up to 3 but did not use them; the isolation rule prevented nested fresh agents.
5. **Minor isolation footnotes**: blank, Danus, and MMAT started with a `pwd`/`ls` at the repository root before changing into their arm roots; no forbidden prior-solution/git/network material was read. Blank also initially created two scratch files outside its arm root and then moved them into the arm root.
6. **Not novelty**: all five reproduce known mathematics for this project. The benchmark records reproduction quality and resource usage, not new mathematical theorems.

## Artifacts

- `frozen_task.md` — frozen task
- `source_manifest.json` — frozen sources and five-arm config
- `metrics.json` — raw session metrics
- `arms/<arm>/result.md` and `arms/<arm>/report.md` — each arm's submitted output
- `RESULTS.md` — this table
