# Arm C source and protocol manifest

## Frozen source

- Upstream repository: `https://github.com/proofQED/QED.git`.
- Pinned commit: `121900964e6572aaf094412d434b5ac2a792a65f`.
- Commit tree: `e39b6d85f1c8bc2e011cbadfc38cc5f851202a64`.
- Pinned checkout status before export: clean.
- Content-only source export SHA256, provenance-only because the archive is not retained here: `1A0C202A3CD2FE9C7E83FC1E00F4546C25C86135AE035952B57AFE5AE34417CA`.
- Content-only source export size: `819200` bytes.
- The source archive itself is not duplicated here. The immutable commit and archive hash bind the executed source.

## Frozen task

- Task SHA256: `1FA717B9A5F195C42ECCA97D51E20327CB4EB2C316C936C054F55F7DD7416F16`.
- Problem source commit: `613cf5f1e103c99563987d01d5d2a43adca93746`.
- Hidden historical gold commit: `e6cf00fe87df93a7c0bc63de840b4aa7cdc2708f`.

## Runtime

- Model: `gpt-5.6-sol`.
- Reasoning effort: `xhigh`.
- Codex CLI: `0.149.1`.
- QED retry bounds: one proof attempt, one revision, and one decomposition.
- Actual path: Stage 0 classified the task as Easy and short-circuited before all decomposition and verification roles.

## Safe adapter

The upstream launcher hardcodes `--search` and `--dangerously-bypass-approvals-and-sandbox`. The external adapter removed exactly these flags and invoked Codex with:

- `workspace-write` sandboxing.
- Approval policy `never`.
- Child shell network disabled.
- Native Codex subagents disabled.
- Fresh isolated Codex home with memories disabled and no prior session history.
- No project repository or `.git` directory in the solver workspace.

QED was invoked directly through `code/pipeline.py`. The upstream `run.sh` and `smoke_test.py` were not used. The adapter files, dry-run invocation log, and static forwarded-argument test are retained in `harness/`.

Offline execution is a fidelity limitation because QED's Stage 0 prompt is designed to perform a web literature survey. This benchmark tests the pinned orchestration code under the common no-network rule, not its full online literature-search behavior.

QED's own `token_usage.json` reports the correct per-provider Codex call but retains an incorrect top-level Claude model label and omits cached input, reasoning output, and tool counts. Scored metrics use the raw Codex session counters. The raw session is not committed because it contains encrypted model internals. `sanitized_events.jsonl` retains the exposed counters and exact tool invocations, and `harness/sanitize_session.py` records the filtering rule.

## Bindings

- Candidate proof SHA256: `6C204AF0D690C4ADED05810B22E076AE8A22F451D4520C29314D764E47C44896`.
- Final label-blind external audit SHA256: `94D17F1D5D2F0A74DE8BA831947A25D9D3F1354729000B2425C9C837EC031990`.
- Sanitized event log SHA256: `176BBABBE666403E25D0BEEE3619D9E8E012AFC8355FD8F7C3C079B54892D901`.
- Session sanitizer SHA256: `FAC131F0B854B4019437581B9DFAE2CB9D50C9EAB6FE383254AE836E751BBDE9`.
- Timing sidecar SHA256: `4F606E18468F9A40B589A7641E42511D186421984586B25FB933AEC311449A9E`.
- Adapter static test SHA256: `A487A08F10808F6EE1F13336BB1CC4963C2356BAF8B7BB2348AFBF1258CDB1DB`.
- Pipeline log SHA256: `52569D7AD9E6AF534F43008016C8AD65BB17B28D6799DD9BC0C2DF2DAD0D3042`.
- Wrapper log SHA256: `C34F42EB8FF41799B53FD96C5468091509FD4986258CF203DC443FE30EA48454`.
- Prompt-input probe SHA256: `14734512CB9CA254EFB5BA6C59C9FC812B249969A2EBD4B0754D3E54B67D17B1`.
- Codex config SHA256: `8215E6E3DF057747FB2B817B0BD11E79A63146FE5CA44D022D822C4AA782D461`.
- Executed QED safe config SHA256 in the CRLF Windows worktree: `4E135D6108037DC03CA2CE84CE15FB4A30FFB6F15786634D259FB6245DB3754A`.
- Retained QED safe config SHA256 after Git's canonical LF normalization: `F999508AC0690C4FCA40A4234AF39DCBA5A17C59A939CE47AD08AE0A6B5A9171`.
- Runner SHA256: `AC5B75C028A1A1456272888A0C5D28ADA0CA39C20E03F3C74EFE7EAD1F6EC5F8`.
- Safe adapter SHA256: `E2EE93A5A21F4867243FB1A776EABA2EF14545A7D49F1A44D36E6FAD6D922C9A`.
- QED token log SHA256: `739323499E220F6AD6D2F3000C0CF689362AD1CC273BE39135B634B0EB16E576`.
