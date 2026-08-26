# Usage amendment

Date: `2026-08-26`.

The user explicitly removed the emergency-reserve requirement after the primary five-hour
window reset. This amendment supersedes only the reserve and early-stop percentages in
`PLAN.md`. It does not change the frozen mathematical task, arm definitions, isolation rules,
model settings, scoring, or audit requirements.

- Primary window at amendment: `3` percent used of `300` minutes.
- Secondary window at amendment: `9` percent used of `10080` minutes.
- Primary reset observed: `2026-08-26 13:53:49 +08:00`.
- New policy: no planned emergency reserve.
- Run order: Arm A, blind audit and repair, Arm B, Arm C, final blind audit and integration.
- Stop only when all planned stages complete, the actual rate limit prevents continuation, or
  a mathematical or infrastructure stop condition from the frozen protocol is reached.
- If a limit interrupts an arm, retain and report the partial artifact but do not score it as a
  completed arm.
