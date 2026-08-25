# Blocker: GPT-5.6 model proxy unavailable

Date: 2026-08-25
Calibration runs A/B/C were prepared and launched under
`F:\benchmark\PILOT-V2-20260825\calibration`, but the configured model proxy
`http://172.22.112.1:7898` is closed. Codex events show repeated
`Reconnecting... request timed out`; no solver output was produced.
Runs were stopped and remain ready to relaunch when the proxy is restored.

## What is ready

- Adapted plan: `PLAN.md`
- Calibration run roots and scripts:
  `F:\benchmark\PILOT-V2-20260825\calibration\run-{a,b,c}.sh`
- QED safe adapter and config reused from existing harness.
- Main blind task: `blind-main/task.md`
- Gold/audit remain outside solver access.

## Next step after proxy restore

1. Relaunch calibration A/B/C.
2. Confirmation run if successful.
3. Then run the 9 main-task repeats according to Latin square.
