# Safe adapter static test

The safe adapter was invoked with `/bin/echo` substituted for the real Codex executable. The simulated upstream argument list included both `--search` and `--dangerously-bypass-approvals-and-sandbox`.

Observed forwarded arguments:

```text
-m gpt-5.6-sol -c model_reasoning_effort=xhigh exec --ignore-rules --skip-git-repo-check --strict-config --color never -s workspace-write -c approval_policy="never" -c sandbox_mode="workspace-write" -c sandbox_workspace_write.network_access=false -c agents.enabled=false --json -C /tmp TEST
```

Result: `PASS`. Both upstream unsafe flags are absent. Workspace-write, approval never, disabled child shell network, and disabled native subagents are present.
