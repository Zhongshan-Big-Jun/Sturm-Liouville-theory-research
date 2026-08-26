# Arm B stage report

## Configuration

- System: plain Codex blank control.
- Model: `gpt-5.6-sol`.
- Reasoning effort: `xhigh`.
- Codex CLI: `0.149.0-alpha.4.3`.
- Model-visible task context: the frozen task plus the unavoidable Codex sandbox layer.
- Project documents, skills, plugins, memories, apps, network tools, and subagents: disabled.
- Solver network: disabled.
- Workspace: content-only, with no repository, git state, prior answer, or external memory.

The prompt-input probe passed with zero occurrences of project instructions, available skills,
research skills, plugin instructions, multi-agent instructions, and recommended plugins. The
session metadata reports `memory_mode=disabled` and `multi_agent_version=disabled`.

## Mathematical result

Status: `FATAL_GAP` after fresh label-blind external review.

The solver claimed the complete estimate with `c=1/4`, `C=12`, and `t_0=1`. The audit certifies
only the following strict partial claim:

```text
TV(P_t^x,P_t^y) >= 1/(4 sqrt(t)), t>=1.
```

It also certifies the exact conditional fair-lamp kernel, contraction to the range triple,
the path-count change of variables through equation (4), parity, and the direct `t=1` value
`TV=3/4`.

The claimed upper bound depends on a false one-turn assertion for the fiber
`i -> A_t^w(i,e)`. Exact integer dynamic programming gives the counterexample

```text
t=48, w=8, e=4, i=0,2,4,6,8,
A=[1000894788882,1029170933020,1017584921004,1029170933020,1000894788882],
successive signs=[+,-,+,-].
```

Therefore equations (3) and (6), including the global constant-order upper bound, remain
unproved. Repair requires a new global variation estimate or a different coupling and is not a
local edit.

## Audit

- External label-blind review: `FATAL_GAP`.
- First error: equation (5), the false one-turn fiber claim.
- Inclusion-exclusion equation (8), the lower bound, and the stated boundary cases: certified.
- Exact counterexample replay: `PASS` using integer recurrence, not floating-point evidence.
- Review usage: post-hoc and excluded from scored Arm B metrics.

## Scored resource data

| Metric | Value |
|---|---:|
| Wall time | 1254.674 s |
| Sessions | 1 |
| Turns | 1 |
| Model responses | 17 |
| Tool calls | 16 |
| Subagents | 0 |
| Input tokens | 543007 |
| Cached input tokens | 486400 |
| Uncached input tokens | 56607 |
| Output tokens | 40387 |
| Reasoning output tokens | 31935 |
| API-equivalent normalized estimate | USD 1.228728 |
| Candidate artifact bytes | 8559 |

The primary five-hour use was `4 percent` before launch, `5 percent` at the first scored model
record, and `18 percent` after completion. The secondary window was `41 percent` at the first
record and `43 percent` after completion. The normalized estimate uses
`uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`; it is a common comparison
proxy, not an actual ChatGPT bill.

## Artifact bindings

- Frozen task SHA256: `6859E0AF922BA8454758E2195FCEFCFE8FA164A40E2C23022EC7EBB2DA228943`.
- Prompt-input probe SHA256: `AE4423D80788F124E0AFB1102F0E447A030A71114FDA34F351D54F449A6F2336`.
- Candidate SHA256: `3B50DCBFD96EA8F0BF746F419E8D4E4AC43F8BAED76EE66A66F6399BEF8AA761`.
- Root event log SHA256: `F973DDDC86B6F8020B8F9981861B96F93FA1293DE4B1BF1FA91E9D7C965AEF4F`.
- External review SHA256: `85BB4A94C4E834C39AD136C614858C2EC366E14F93040A13E24A261FA4319BCA`.

See `final_response.md`, `external_anonymous_audit.md`, and
`reproducibility/audit_false_one_turn.py`.
