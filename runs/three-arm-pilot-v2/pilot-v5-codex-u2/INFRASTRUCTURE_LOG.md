# Infrastructure log

## Invalid Windows launch

- Started: `2026-08-25 23:33:20 +08:00`.
- Stopped: `2026-08-25 23:39:11 +08:00`.
- Wall time: `350.638` seconds.
- Quota checkpoint before launch: primary `23` percent, secondary `4` percent.
- Last observed quota before termination: primary `32` percent, secondary `5` percent.
- Classification: `INFRA_INVALID`, excluded from Arm A.
- Reason: the managed Windows permission profile exposed the arm and its spawned subagents as
  read-only. The solver could not read the copied v1.6.0 phase references through tools and
  could not create the required persistent research artifacts.
- Mathematical output: none retained and none scored.
- Termination: the exact `codex.exe` process at PID `49892` was verified by command line and
  stopped. The process returned exit code `-1`.

## WSL replacement preflight

- Runtime: Ubuntu WSL, `codex-cli 0.149.1`.
- Workspace: `F:\benchmark\PILOT-V5-CODEX-U2-20260825\arm-a-plugin-wsl-run1`.
- Plugin source: installed v1.6.0 cache, copied under the arm-local `.agents/skills` directory.
- Workspace read preflight: `PASS`.
- Workspace write preflight: `PASS`.
- Network policy inside the solver sandbox: disabled.
- Transport proxy outside the solver sandbox: Windows TCP forwarder
  `172.22.112.1:7898 -> 127.0.0.1:7897`, connectivity checked before launch.

## WSL quota-bound launch

- Started: approximately `2026-08-25 23:43:49 +08:00`.
- Stop checkpoint: `2026-08-25 23:44:49 +08:00`.
- Quota before launch: primary `32` percent, secondary `5` percent.
- Quota at hard stop: primary `46` percent, secondary `7` percent.
- Status: `PAUSED_QUOTA`, excluded from the scored Arm A result.
- Work completed: loaded the v1.6.0 static entry, phase references, delegation contract, and
  subtask template; confirmed content-only workspace and absence of a git repository.
- Mathematical output: none. No theorem contract, route result, proof, or audit artifact had
  been created when the stop line was reached.
- Termination: verified WSL process group for the exact pilot v5 work root received `SIGINT`.
- Resume rule: start a fresh scored Arm A directory only after the primary 300-minute window
  resets. Do not count either infrastructure attempt in Arm A metrics.
