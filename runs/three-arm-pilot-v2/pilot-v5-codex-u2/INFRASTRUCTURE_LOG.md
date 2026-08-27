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

## Scored Arm A hard-limit continuation

- Scored workspace: `F:\benchmark\PILOT-V5-CODEX-U2-20260825\arm-a-plugin-wsl-run2`.
- Scored thread: `01a03b91-c0d3-7792-ab90-c80bb7b40e46`.
- First segment active wall: `2764` seconds.
- First segment stop: service-enforced five-hour usage limit at `100` percent.
- Preserved results: theorem contract, ledgers, exact enumeration, `direct_coupling.md`, and
  `range_translation.md`.
- Resume policy: same thread, model, reasoning effort, sandbox, prompt contract, and workspace.
  The continuation cap is `2036` seconds, preserving the preregistered `4800` second total active
  wall cap.
- User instruction after reset: continue with no emergency reserve.

## Arm C invalid run 1

- Classification: `INFRA_INVALID`, excluded.
- The initial wrapper stripped the CLI search flag and disabled sandbox network, but the Code Mode
  host still exposed nested `web__run` calls to the QED literature-survey role.
- The run was stopped after 44 nested Web calls among 46 model tool calls and before decomposition.
- Compact evidence is under `arms/c-qed-infra-invalid-run1`.

## Arm C invalid run 2

- Classification: `INFRA_INVALID`, excluded.
- Setting `features.code_mode_host=false` closed Web access but also disabled all model-side file
  reads and writes. QED roles received only paths and returned tool-access blockers.
- The run used six sessions and 242392 input tokens, but no role received the problem contents.
- Compact evidence is under `arms/c-qed-infra-invalid-run2`.

## Arm C scored run 3

- Workspace: `F:\benchmark\PILOT-V5-CODEX-U2-20260825\arm-c-qed-run3`.
- QED source: content-only export of commit `121900964e6572aaf094412d434b5ac2a792a65f`.
- Offline adaptation: append exact contents of existing files named in each prompt and confined to
  the output root; all model tools and network remain disabled.
- Preflight and prompt-input probe: `PASS`, with all context-leakage markers zero.
- Decomposer response: valid 10-step YAML. QED fallback selected an inner Markdown fence and saved
  a scalar; the unchanged response was restored as `decomposition.yaml` and parsed as a mapping.
- Scored event span: `2198.87` seconds across seven QED roles.
- Pipeline result: structural `FAIL`, regulator `REVISE_PROOF`, final QED state `FAILED` because the
  preregistered one-proof cap was exhausted.
- Fresh external audit: `PARTIAL_NOT_COMPLETE`, accepting the explicit lower bound and logarithmic
  upper bound while leaving the constant-order upper bound open.
