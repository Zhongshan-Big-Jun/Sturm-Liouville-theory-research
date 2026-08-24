# Arm C stage report

## Configuration

- System: QED at pinned commit `121900964e6572aaf094412d434b5ac2a792a65f`.
- Model: `gpt-5.6-sol`.
- Reasoning effort: `xhigh`.
- Codex CLI: `0.149.1`.
- QED bounds: one proof attempt, one revision, and one decomposition.
- Network: disabled for the solver.
- Project repository, git metadata, parent-directory contents, prior solution, and external memory: absent from the solver cwd and forbidden by the frozen task. The sandbox still exposed generic read-only root access, so this is protocol and workspace isolation rather than an OS-level guarantee that every outside path was unreadable.
- Native Codex subagents and web search: disabled.
- Runtime adapter: strips upstream search and dangerous bypass flags, then enforces workspace-write, approval never, and child shell network disabled.

The scored Codex session is thread `01a03458-94be-7933-a023-c74e457c32ba`. The prompt-input probe contains zero occurrences of AGENTS instructions, available skills, the research skill, plugin instructions, or multi-agent instructions.

## Actual QED path

QED's Literature Survey role initially wrote a Hard classification, then revised it to Easy in the same call after identifying a direct Sturm argument. QED consequently took its Easy short circuit:

- Literature Survey roles run: 1.
- Decomposer roles run: 0.
- Prover roles run: 0.
- Structural verifier roles run: 0.
- Detailed verifier roles run: 0.
- Verdict roles run: 0.

Therefore this sample does not exercise QED's multi-role proof and verification architecture. The candidate was accepted only after a separate anonymous reviewer audited it.

## Mathematical result

Status: `STRICT` after external review.

The candidate gives a direct regular Sturm-Liouville proof. It realizes

```text
M_{n,s}(y)=L(y)(H_s(y)L(y))^n
```

as the full transfer matrix and normalizes the Dirichlet shooting solution so that

```text
F(lambda)=u(1,lambda)=G_{n,s}(y)/sqrt(lambda),
y=sqrt(lambda)st.
```

At `y=pi`, every block transfer matrix is `-I`. The corresponding eigenfunction vanishes at exactly the `2n` internal interfaces and nowhere else in `(0,1)`. The regular Sturm oscillation theorem therefore identifies this as the `(2n+1)`-st Dirichlet eigenvalue, giving exactly `2n` lower eigenvalues and thus exactly `2n` zeros of `G` in `(0,pi)`.

A Lagrange-identity calculation proves analytic simplicity:

```text
u'(1,lambda_k)F'(lambda_k)=integral_0^1 rho u^2 dx > 0,
F'(lambda_k)=st G'(y_k)/(2 lambda_k).
```

The separate audits for `n=1`, `y=0`, `y=pi`, `y=pi/2`, and `R=1` all pass.

## Audit

- Final fresh-context, label-blind external audit: `PASS`.
- An earlier independent audit also returned `PASS`, but its source path exposed the arm label, so it is not counted as label-blind.
- First erroneous or unsupported step: none.
- Complete gap list: empty.
- Transfer order, eigenvalue indexing, zero-eigenvalue correspondence, Lagrange-identity sign, analytic simplicity, and all required boundary cases were independently recomputed.
- Leakage audit: the retained sanitized event log exposes all four exact tool invocations. Every path and working directory stays within the isolated content-only output workspace. No repository, git, network, prior-answer, memory, skill, plugin, or subagent access was observed.

## Scored resource data

| Metric | Value |
|---|---:|
| End-to-end pipeline wall time, externally measured | 283.717 s |
| QED role calls | 1 |
| Codex model responses | 5 |
| Tool calls | 4 |
| Subagents | 0 |
| Input tokens | 82,667 |
| Cached input tokens | 45,312 |
| Uncached input tokens | 37,355 |
| Output tokens | 11,583 |
| Reasoning output tokens, subset reported separately | 6,919 |
| API-equivalent normalized estimate | USD 0.3992 |
| QED output package bytes at completion, Windows worktree | 16,833 |

The normalized estimate uses `uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`. It is only a cross-arm accounting proxy and is not an actual ChatGPT bill.

The Codex response, tool, token, and final quota counters come from the raw Codex session and are preserved in `sanitized_events.jsonl`. Here `model responses` means the five per-turn `token_count` records. `Tool calls` means four top-level Codex `exec` events; one event may bundle multiple nested shell or patch operations. `QED role calls` and its `283.600 s` call elapsed time come from QED's tracker. The `283.717 s` end-to-end wall time is an external filesystem-timestamp measurement recorded as provenance-only in `timing.json`; retained QED logs independently support `284 s` after rounding. The starting quota is inferred from Arm B, output bytes are the retained Windows-worktree directory sum, and the audit status comes from the post-hoc reviewer.

QED's own tracker correctly records one per-provider Codex call and its total input and output, but its top-level model remains the unused Claude default and it omits cache, reasoning, and tool-call fields.

Arm B's immediately preceding final counter was `59%`; this is the inferred, not directly measured, Arm C starting point because the fresh C home logged `quota_used=-1` before its first call. Arm C's final counter directly reported `68%`, leaving `32%` until the reset at `2026-08-31 17:16:52 +08:00`.

Relative to Arm B, Arm C was `11.7%` slower, used `297.5%` more uncached input, emitted `12.7%` more output, and had a `64.2%` higher normalized estimate. Both passed the same external mathematical audit. Arm C produced an independent Sturm proof, but its QED verification chain was not exercised.

Relative to Arm A, Arm C used `75.0%` less wall time, `83.2%` less uncached input, `84.3%` less output, and `89.6%` less normalized cost. Arm A produced multiple independent routes, plugin-internal adversarial review, convergence reconstruction, and a substantially larger persistent research package.

## Protocol limitations

- The problem is historically contaminated and is only a regression calibration.
- QED Stage 0 is designed for online literature search, but the common benchmark rule disabled search and network access.
- The Easy short circuit means this run is not evidence about QED's decomposer or verifier quality.
- Arm C used Codex CLI `0.149.1`; Arms A and B used `0.149.0-alpha.4.3`. Model and reasoning effort were unchanged.
- QED's bundled token tracker is incomplete, so cross-arm counters were normalized from the underlying Codex session.
- This is one task and one sample, so no statistical ranking is claimed.

## Artifact bindings

- Frozen task SHA256: `1FA717B9A5F195C42ECCA97D51E20327CB4EB2C316C936C054F55F7DD7416F16`.
- Candidate proof SHA256: `6C204AF0D690C4ADED05810B22E076AE8A22F451D4520C29314D764E47C44896`.
- Final label-blind external audit SHA256: `94D17F1D5D2F0A74DE8BA831947A25D9D3F1354729000B2425C9C837EC031990`.
- Sanitized event log SHA256: `176BBABBE666403E25D0BEEE3619D9E8E012AFC8355FD8F7C3C079B54892D901`.
- Timing sidecar SHA256: `4F606E18468F9A40B589A7641E42511D186421984586B25FB933AEC311449A9E`.
- Pipeline log SHA256: `52569D7AD9E6AF534F43008016C8AD65BB17B28D6799DD9BC0C2DF2DAD0D3042`.
- Prompt-input probe SHA256: `14734512CB9CA254EFB5BA6C59C9FC812B249969A2EBD4B0754D3E54B67D17B1`.
- QED content export SHA256, provenance-only because the archive is not retained: `1A0C202A3CD2FE9C7E83FC1E00F4546C25C86135AE035952B57AFE5AE34417CA`.

The retained `qed_output/` directory contains the same 12 logical files. The executed Windows worktree measured `16,833` bytes; Git's canonical LF objects total `16,697` bytes because it normalizes line endings in several imported text files. Its `proof.md` and the top-level `candidate_proof.md` both have SHA256 `6C204AF0D690C4ADED05810B22E076AE8A22F451D4520C29314D764E47C44896` under either representation.

This result duplicates previously known project mathematics and is not claimed as novel.
