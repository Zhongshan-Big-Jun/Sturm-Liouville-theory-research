# Pilot v4 long-run plan

- Launched: 2026-08-25 20:08
- Runtime root: `F:\benchmark\PILOT-V4-LONG-20260825`
- Cap: 2 hours (watchdog-managed)
- Backend: DeepSeek `deepseek-chat` / `high` via Codex CLI
- Five arms: A local plugin, B blank Codex, C Rethlas-DeepSeek, D Danus-DeepSeek, E MMAT-DeepSeek
- Three unpolluted hard tasks: U1 Batchelor-scale liminf, U2 TV asymptotics, U3 LICT_Z over Z

See `REVIEW_PLAN.md` for scoring/verdict rules. Results will be recorded in `RESULTS.md` after collection and independent review.

## Pollution caveat

U1 (Batchelor-scale liminf) was previously used in the one-off 31-minute Batchelor
test on 2026-08-25, so it is not strictly unpolluted for these arms. U2 and U3 are
new in this benchmark. The v4 round is therefore best read as: longer retry on U1,
plus first long-run test of U2/U3.
