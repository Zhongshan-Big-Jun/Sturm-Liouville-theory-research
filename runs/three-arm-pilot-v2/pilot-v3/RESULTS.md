# Pilot v3 execution results (30-minute cap)

Launch: 2026-08-25 19:18
Backend: DeepSeek `deepseek-chat` / `high` via Codex CLI.
Cap: all runs stopped at 19:48 (30 min).

| Arm | T1 Bessel | T2 exponential mixing | T3 Lamplighter |
|---|---|---|---|
| A 本插件 | no final proof | candidate proof (No) | no final proof |
| B 空白 | no final proof | complete proof (No) | incomplete (terminal only) |
| C Rethlas | no blueprint | blueprint (unverified) | blueprint (unverified) |
| D Danus | 2 verified facts (partial) | 4 verified facts incl main theorem (No) | no facts |
| E MMAT | no final proof | no final proof | no final proof |

## Highlights

- A/T2: `CANDIDATE_COMPLETE_PROOF`, self-contained elementary proof of exponential-decay impossibility.
- B/T2: complete proof via BV high-frequency lemma and polynomial lower bound.
- C/T2 and C/T3: Rethlas produced `blueprint.md` but no `blueprint_verified.md`.
- D/T2: Danus fact graph includes the main no-go theorem plus supporting lemmas, all verifier-gated.
- D/T1: partial lemmas/facts only.
- E: MMAT reached orchestration/sketcher stages but no final proof within cap.

## Artifacts

- Tasks: `tasks/T1,T2,T3`
- A/B run dirs: `arms/A, arms/B`
- C blueprints: `F:\tools\rethlas-deepseek\agents\generation\results\pilot-T{2,3}\problem\blueprint.md`
- D fact graphs: `F:\tools\danus-deepseek\runtime\projects\pilotT{1,2}\fact_graph\facts\`
- E workspaces: `F:\tools\mmat-deepseek\data\workspace\pilot-T{1,2,3}\`

## Independent review for T2

| Candidate | Verdict |
|---|---|
| A (plugin) | PASS |
| B (blank) | REPAIRABLE_GAP |
| C (Rethlas) | REPAIRABLE_GAP |
| D (Danus) | PASS |

See `independent_review_t2.md`.

## Note

This is a 30-minute pilot with many incomplete runs. T1 and T3 did not produce enough completed proofs for scoring; T2 has four candidates, two of which passed independent review as submitted.
