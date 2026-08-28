# Pilot v6 Arm B stage report

## Outcome

- Arm: task-only blank control.
- Model: `gpt-5.6-sol`, `xhigh`.
- Skills, plugins, memories, subagents, apps, browser, computer use, and network: disabled.
- Solver structure: one response, no tools, no child session.
- Posthoc anonymous blind audit: `REPAIRABLE_GAP`, accepted at 94/100.
- Hidden gold: not inspected.

The response independently reached all three required mathematical conclusions. Under the
abstract polynomial reading,

```text
Q_n^(s) in D(K_c^(s/2)) if and only if n in {0,1}.
```

It correctly distinguished the abstract polynomial completion from the concrete operator domain,
and correctly rejected the literal polynomial system as an operator-domain basis. It also
distinguished the genuine spectral inverse, whose images are dense but generally non-polynomial.

The first load-bearing support gap is equation (2): the exact power-domain characterization is
attributed to spectral calculus and one-dimensional regularity without stating the regularity
hypotheses or carrying out the domain induction. The anonymous reviewer supplied a local repair,
but that repair is posthoc and is not credited to the scored arm. The exact bonus degree spectrum
is correct but also unproved in the scored response.

## Scored resource data

| Metric | Value |
|---|---:|
| Root active wall | 602.092 s |
| Aggregate agent time | 602.092 s |
| Sessions | 1 |
| Turns | 1 |
| Model responses | 1 |
| Tool calls | 0 |
| Input tokens | 9910 |
| Cached input tokens | 8960 |
| Uncached input tokens | 950 |
| Output tokens | 25020 |
| Reasoning output tokens | 22272 |
| API-equivalent normalized estimate | USD 0.507784 |
| Artifact bytes, excluding `events.jsonl` | 8698 |

The normalized estimate uses
`uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`. It is a cross-arm proxy,
not an actual ChatGPT bill. The external audit is excluded from scored usage.

## Quota and isolation

- First exposed record: primary 3 percent, secondary 16 percent.
- Final record: primary 3 percent, secondary 16 percent.
- The isolated work root contained only `TASK.md` and its hash at launch.
- `CODEX_HOME` contained only the auth link and a strict disabling configuration.
- Frozen task SHA256: `359d335803eae43f45120e3ca3995b8f12ec2f98b357e2b10116eafe2d8c6332`.
- CLI SHA256: `1c8b7f5221f6779c1e689b00bfa2dd95503f2aa595b9e6c752550ddd8ddf26b6`.
- The session made zero tool calls, so it did not read outside the prompt.

## Audit bindings

- Final response SHA256: `874b0bde9dfaf194e8279519c2c70d739a8e4125094aa5495884fffa5c78ee58`.
- External review SHA256: `486ce4ffac8544990ba6450363f738e1cba631e98ce0c8f820dd434a5e33c4be`.
- External verdict SHA256: `d9f3f3e9c39fc2151899fa13cc398040797263c5907e8d5520bb8ed66e47fc7f`.

The 94/100 score uses the preregistered axes. It satisfies the acceptance threshold, but the arm
retains the `REPAIRABLE_GAP` verdict because explicit support gaps prevent `PASS`.
