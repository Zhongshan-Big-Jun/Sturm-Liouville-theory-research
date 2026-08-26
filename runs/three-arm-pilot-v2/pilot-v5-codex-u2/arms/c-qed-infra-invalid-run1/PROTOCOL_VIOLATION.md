# Arm C run 1 protocol violation

Status: `INFRA_INVALID`. This run is excluded from scoring.

The frozen task forbids internet access. The adapter stripped QED's `--search` and
`--dangerously-bypass-approvals-and-sandbox` flags, set
`sandbox_workspace_write.network_access=false`, disabled configured web search, apps, browser,
plugins, and remote plugins, and passed the prompt-input leakage probe. Nevertheless, the Codex
`code_mode_host` meta-tool still exposed `web__run` as a nested callable tool.

The first QED literature-survey session made 46 meta-tool calls, 44 of which invoked
`tools.web__run` to search or open internet sources. The root monitor detected this from a
sanitized copy of the live session and immediately sent Ctrl-C. No decomposition, prover,
structural-verifier, or detailed-verifier session had started.

The only mathematical output was `difficulty_evaluation.md`, which classified the problem as
Hard. There is no proof artifact and no mathematical result from this invalid run.

## Bindings

- QED commit: `121900964e6572aaf094412d434b5ac2a792a65f`.
- Raw session SHA256:
  `EE1F5A850677D8D0311BD1A85C256F05A4E3E326E15A87271372A5E5293B9020`.
- Local sanitized session SHA256:
  `E4224775F3A5F3134BEF2243C3D33227FBC4D8D9FF673F79DE096C9F53E06742`.
- Prompt-input probe SHA256:
  `FBB7968316613306399BDA84C7F65F6CF106C75E30AF8ACD98C46E368E7FC186`.
- Frozen task SHA256:
  `6859E0AF922BA8454758E2195FCEFCFE8FA164A40E2C23022EC7EBB2DA228943`.
- Difficulty file SHA256:
  `FF8340C9CCE79EEA67AA7839312A66F8EDE1A2F892AD8347EDE73D0A89D42714`.

The full raw and sanitized sessions remain in the external benchmark workspace. They are not
copied into the repository because they contain network-retrieved material from an invalid run.

## Repair

The replacement adapter disables `features.code_mode_host`. A schema probe shows that
`functions.exec` remains named in the model schema but Code Mode reports fail-closed before any
nested tool can execute. QED's own response fallbacks allow its decomposition and verification
pipeline to continue without model-side tools. The replacement must use a fresh content-only
workspace and is scored independently.
