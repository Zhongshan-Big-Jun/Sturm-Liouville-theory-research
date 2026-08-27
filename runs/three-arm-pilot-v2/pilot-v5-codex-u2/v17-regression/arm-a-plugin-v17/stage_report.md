# v1.7 regression Arm A stage report

## Configuration

- Run ID: `R-20260827T063025Z-u2-v17-regression`.
- Model: `gpt-5.6-sol`, reasoning effort `xhigh`.
- Plugin: `rigorous-open-math-research` v1.7.0 at commit
  `957d80b7f1c58b60972a4ece87945cd93c0a1476`.
- Root coordinator: 1.
- Research child sessions: 3.
- Network: disabled.
- Prompt SHA256:
  `0AB0AF8E6936C0597626493029004DC4F8851BF79E5F6AE4076CCC2605D012A7`.

## Termination and scored status

The root stopped at the service-enforced five-hour limit after 1311.844 active
seconds. Route A and Route C returned complete partial artifacts. Route B did
not write an artifact before termination. The root wrote a live candidate
proof but no final response and no internal global audit.

Primary status: `PAUSED_QUOTA_WITH_AUDITED_PARTIAL_RESULT`.

Solver label for the retained mathematics: `RIGOROUS_PARTIAL_RESULT`.

The post-hoc neutral audit is independent and excluded from scored metrics. It
returned `PASS` for every retained partial theorem claim. It does not convert
the interrupted run into a completed end-to-end regression.

## Audited partial theorem

For every integer `t>=2`, put `n=floor(t/2)`. Then

```text
1/(4 sqrt(t)) <= ||P_t^(0,0)-P_t^(0,2)||_TV
               <= 1/sqrt(n+1)+2 H_(n+1)/sqrt(t-n+1)
               <= sqrt(2)[3+2 log(t+1)]/sqrt(t).
```

The lower bound already holds for every integer `t>=1`. The uniform
fixed-constant upper bound `C/sqrt(t)` remains `OPEN`.

The exact visible-hull TV equality is a reusable structural result. Route A's
coupling-specific lower obstruction rules out removal of the logarithm by
constant optimization of that coupling. Route C supplies exact state-mass and
triple formulas and falsifies the naive parity-class unimodality argument.

## Audit classification

- `STRICT`: all theorem claims listed in `external_neutral_audit.md` under
  Promotion decision.
- `EVIDENCE`: finite exact dynamic-program outputs and bounded replays.
- `OPEN`: O3, Route A's alternative mechanism, Route C inequality (17), and
  the complete frozen target.
- Novelty: `UNKNOWN`, because literature access was forbidden.

## Resource data

| Metric | Value |
| --- | ---: |
| Root active wall | 1311.844 s |
| Aggregate agent time | 3826.420 s |
| Sessions | 4 |
| Child sessions | 3 |
| Model responses | 56 |
| Tool calls | 44 |
| Input tokens | 1,914,732 |
| Cached input tokens | 1,702,912 |
| Uncached input tokens | 211,820 |
| Output tokens | 101,940 |
| Reasoning output tokens | 74,637 |
| Cost proxy | USD 3.5672448 |

One incomplete Route B return is fully charged to these totals. The neutral
audit and repository-side exact replay are excluded.

## Protocol compliance

The coordinator completed a direct attempt and exact falsification probe before
delegation and required hash-bound route packets. The three-route first batch
met the preregistered cap, but was more aggressive than the closure-first
smallest-batch recommendation. This is a scheduling observation, not a frozen
protocol violation.

## Reproducibility

Run:

```text
py -3 reproducibility/audit_exact_claims.py
```

The replay passes on its finite declared domains. It is `EVIDENCE` only.
Session-level metric definitions and totals are in `session_metrics.json`.
