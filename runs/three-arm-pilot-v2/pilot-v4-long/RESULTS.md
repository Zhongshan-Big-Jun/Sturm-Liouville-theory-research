# Pilot v4 long-run results

Launch: 2026-08-25 20:08
Recovery restart: 2026-08-25 20:30 (after transient DeepSeek 402)
Run ended: all v4 processes stopped/terminated by 2026-08-25 21:05; watchdog/collector background jobs were interrupted before writing markers, so collection was done manually.
Tasks: U1 Batchelor-scale liminf, U2 TV asymptotics, U3 LICT_Z over Z.
Backend: DeepSeek `deepseek-chat` via Codex; five arms.

| Arm | U1 Batchelor | U2 TV asymptotics | U3 LICT_Z |
|---|---|---|---|
| A 本插件 | NO_ARTIFACT (0) | NO_ARTIFACT (0) | REPAIRABLE_GAP (78) |
| B 空白 | NO_ARTIFACT (2) | NO_ARTIFACT (0) | PASS (86) |
| C Rethlas | PARTIAL_NOT_COMPLETE (38) | WRONG_PROBLEM (29) | PASS (92) |
| D Danus | NO_ARTIFACT (0) | NO_ARTIFACT (0) | PASS (93) |
| E MMAT | PARTIAL_NOT_COMPLETE (36) | PARTIAL_NOT_COMPLETE (34) | NO_ARTIFACT (0) |

## Highlights

- U3 is where the five-arm comparison is meaningful: B/C/D all produced proofs that PASS independent blind review; A produced a strong REPAIRABLE_GAP proof with a repairable vanishing-cycle/base-change gap.
- U2 exposed a serious ambiguity/reading issue: the strongest candidate (C/U2) solved the non-canonical interpretation `(base 0, lamp at site 2 lit)` and is judged WRONG_PROBLEM. E/U2 produced only an unproven lemma roadmap.
- U1 had no completed proof in any arm. C/U1 had the best partial literature strategy; E/U1 had an honest route map; A/B/D produced no usable U1 artifact.
- A/U3, B/U3, C/U3, D/U3 were all restart-affected? A/U3 continued from first launch; B/U3 finished before outage; C/U3 and D/U3 restarted after API recovery.
- API billing event affected A/U1, A/U2, C/U1, C/U2, D/U1 high, D/U3, E/U1-U3. Recovery documented in `RECOVERY.md`.

## Independent reviews

Full details: `INDEPENDENT_REVIEWS.md`.

## Acceptance summary

- Accepted (score >= 70, correctness >= 32/40, no fatal flaw): B/U3 (86), C/U3 (92), D/U3 (93).
- Repairable but not accepted as submitted: A/U3 (78).
- Not accepted: all other candidates (wrong problem, partial, or no artifact).
