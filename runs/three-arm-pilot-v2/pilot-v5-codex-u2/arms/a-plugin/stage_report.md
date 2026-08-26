# Arm A stage report

## Configuration

- System: `rigorous-open-math-research` v1.6.0.
- Model: `gpt-5.6-sol`.
- Reasoning effort: `xhigh`.
- Root research agent: 1.
- Unique child sessions: 7.
- Network: disabled inside the scored solver sandbox.
- Blind workspace: content-only, with no project repository, prior answer, or external memory.
- Scored thread: `01a03b91-c0d3-7792-ab90-c80bb7b40e46`.

Two infrastructure-only preflights are excluded. The scored run used two active segments of the
same thread because the first segment reached the service-enforced five-hour limit. The two root
segments used `2764 s` and `1288 s`, preserving the preregistered `4800 s` active wall cap.

## Scored outcome

Primary label: `PARTIAL_NOT_COMPLETE`.

Solver label: `RIGOROUS_PARTIAL_RESULT`.

The frozen constant-order upper bound was not proved. The strongest independently audited
partial theorem is

```text
1/(4 sqrt(t)) <= ||P_t^x-P_t^y||_TV
               <= (2 log(t)+15)/sqrt(t),
```

where the lower bound holds for every integer `t>=1` and the upper bound holds for every integer
`t>=16`. At `t=0`, the total variation is exactly 1.

Additional strict results are:

- the exact conditional fair-lamp kernel on the visited interval;
- `12/sqrt(t)` upper bounds for each of the translated `(L,Z)` and `(U,Z)` marginal TVs;
- a `Theta(log(t)/sqrt(t))` obstruction for reflection-then-synchronization even with optimal
  conditional lamp coupling;
- exact killed-kernel, periodized-binomial, and discrete-coarea reductions of the remaining joint
  range-triple variation.

The first unresolved obligation is to prove a constant `C_0`, independent of `t`, such that

```text
sum_(R,K,A) |h_t(R,K,A)-h_t(R,K,A+2)|
<= C_0 binom(t,floor(t/2)).
```

## Audits

- Module validator: `REPAIRABLE_GAP`. It found one false non-load-bearing recurrence display and
  one compressed reflection derivation. The integrated report uses the correct forward recurrence
  and the two-half-line subtraction.
- Fresh global adversarial audit: `PASS` for the explicitly claimed partial theorem, with the
  original constant-order target explicitly left open.
- Exact integer replay: `PASS` through `t=100`. This is `EVIDENCE` for conjectural comparisons and
  a deterministic check for displayed finite identities, not a proof of the open bound.
- External anonymous audit: pending at the time of this stage-file creation. Its usage is post-hoc
  and excluded from scored metrics.

## Scored resource data

| Metric | Value |
|---|---:|
| Root active wall | 4052 s |
| Aggregate agent time | 13806 s |
| Unique sessions | 8 |
| Turns | 10 |
| Model responses | 307 |
| Tool calls | 216 |
| Input tokens | 24779882 |
| Cached input tokens | 23671808 |
| Uncached input tokens | 1108074 |
| Output tokens | 390390 |
| Reasoning output tokens | 250595 |
| API-equivalent normalized estimate | USD 21.7088192 |
| Artifact bytes, excluding `events.jsonl` | 267779 |

`Model responses` counts exposed `token_count` records. `Tool calls` counts raw
`custom_tool_call` records. Totals sum the root and child session counters. The normalized estimate
uses `uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`; it is only a cross-arm
proxy and is not an actual ChatGPT bill.

One MC continuation child consumed resources but terminated with the root before returning its
promised artifact. Its usage is included. No mathematical claim depends on that missing return.

## Quota data

- Scored segment 1: primary approximately `6% -> 100%`; secondary approximately `9% -> 22%`.
- Scored segment 2: first observed primary `3%`, final primary `62%`; secondary approximately
  `24% -> 34%`.
- The user explicitly removed the emergency reserve before the scored launch.

## Artifact bindings

- Frozen prompt SHA256: `0AB0AF8E6936C0597626493029004DC4F8851BF79E5F6AE4076CCC2605D012A7`.
- Candidate proof SHA256: `C76537D71604F3F5402D520423BCB045B8E203B4FC967C6FB8D1EBBF8ABF043B`.
- Direct coupling SHA256: `70315032FDC32EB1C171089EBCB9A08EB04DC9CF7E8127CB5CACE9F77FEEE80C`.
- Range translation SHA256: `07F2C63D3A0670FFF434B78778C355DDFECC1FFDB41DC8C7C1B3FA70B9890D5E7`.
- Aggregate coarea SHA256: `537B367FB01BD1175781DAA3E543273E0912A9A2D3C266B359D0FF8D03E22FFF`.
- Fresh global audit SHA256: `BA55AD7ED8A2F05A458B45F9ADA841AA8FE228AD92FBD3C0040A6A82BACE2D82A`.

See `final_report.md`, `candidate_proof.md`, `audit_report.md`, `subagents/`, and
`reproducibility/` for the full hash-bound package.
