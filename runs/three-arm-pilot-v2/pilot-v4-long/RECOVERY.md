# Pilot v4 API billing recovery note

- First launch: 2026-08-25 20:08, 15 runs.
- Around 20:20, multiple A/C/D/E runs reported DeepSeek `402 Payment Required: Insufficient Balance`.
- Affected: A/U1, A/U2, C/U1, C/U2 (before verification), D/U1 high, D/U3 (both workers), E/U1-U3.
- B/U1 and B/U3 finished before the outage; B/U3 produced a solution draft.
- At 20:29-20:30 API balance/endpoints rechecked: `deepseek-chat`, `/chat/completions` and `/responses` both work; balance ~46-48 CNY.
- Failed artifacts were backed up to `F:\benchmark\PILOT-V4-LONG-20260825\failed-snapshots\`.
- At 20:30 the 9 affected runs were restarted clean; watchdog cap reset to 20:30 + 2h.
- Final results must note this recovery and that some runs have different wall-clock start times.

See `F:\benchmark\PILOT-V4-LONG-20260825\STATUS.md` and `PROGRESS_LOG.md` for live status.
