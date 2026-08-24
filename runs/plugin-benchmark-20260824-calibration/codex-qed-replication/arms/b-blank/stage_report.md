# Arm B stage report

## Configuration

- System: plain Codex.
- Model: `gpt-5.6-sol`.
- Reasoning effort: `xhigh`.
- Codex CLI: `0.149.0-alpha.4.3`.
- Model-visible task context: the frozen task only, plus the unavoidable Codex sandbox environment layer.
- Skills, plugins, memories, project instructions, MCP servers, web search, and subagents: disabled.
- Network: disabled for the solver.
- Repository, git, parent directory, prior solution, and external memory access: forbidden.

The scored sample is thread `01a0343d-f05c-70f1-b1c5-9fd07c2614e0`. The preflight `prompt_input_probe.json` contains zero occurrences of AGENTS instructions, available skills, the research skill, plugin instructions, or multi-agent instructions.

## Mathematical result

Status: `STRICT` after external review.

The blank control independently derived the same exact Chebyshev reduction:

```text
G_{n,s}(y) = sin(y) [U_n(z) + s^(-1) U_{n-1}(z)],
z = 1-kappa sin^2(y),
kappa = (s+1)^2/(2s).
```

It used the zeros of `U_n` as an alternating sign mesh, obtained all `n` simple scalar roots in `(-1,1)`, lifted them to exactly `2n` simple roots of the even polynomial, and checked all required boundary cases.

## Audit

- External anonymous first-time audit: `PASS`.
- First erroneous or unsupported step: none.
- Complete gap list: empty.
- Leakage audit: the solver made no tool calls, so it had no opportunity to read outside the prompt or use the network.
- Nonfatal runtime warning: the background model-list refresh timed out after the main response had already proceeded. This did not affect the solver result or usage record.

## Scored resource data

| Metric | Value |
|---|---:|
| Wall time | 253.951 s |
| Model responses | 1 |
| Tool calls | 0 |
| Subagents | 0 |
| Input tokens | 9,397 |
| Cached input tokens | 0 |
| Uncached input tokens | 9,397 |
| Output tokens | 10,279 |
| Reasoning output tokens, subset reported separately | 8,127 |
| API-equivalent normalized estimate | USD 0.2432 |

The runtime reported weekly use increasing from `57%` to `59%`, leaving `41%` until the reset at `2026-08-31 17:16:52 +08:00`.

Relative to Arm A, Arm B used `95.8%` fewer uncached input tokens, no cached input, `86.1%` fewer output tokens, no tools or subagents, and `77.6%` less wall time. Both arms passed the same external mathematical audit. Arm A additionally produced an independent Sturm proof, internal adversarial audit, convergence reconstruction, and a much larger persistent research package.

## Artifact bindings

- Frozen task SHA256: `1FA717B9A5F195C42ECCA97D51E20327CB4EB2C316C936C054F55F7DD7416F16`.
- Candidate proof SHA256: `8AA2733A96E2E470462FC74D3BF168DED152CDEAE8BA3CFD1A0F6462271F142C`.
- Root event log SHA256: `D59199286C8E50FE24F6AF02B1D70DD6E151E8C393ADD9924A209A50EDF30C65`.
- Prompt-input probe SHA256: `FBDDB0C95E521E6E5BBA2F837BF9242DFE7F49D8507E5D1DCA419CAA80E7DFD7`.
- Config SHA256: `3491369F5D610C2D066D99F560EE298A836FB9ACA69E5532F3E8D603A71D5995`.
- Runner SHA256: `039F549D5458CA786C1C2F17B90A53830A2FA31FEA2970A8D6E9D04EA98E2EFD`.

This result duplicates previously known project mathematics and is not claimed as novel.
