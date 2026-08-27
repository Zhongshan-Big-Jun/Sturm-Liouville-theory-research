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

The root first stopped at the service-enforced five-hour limit after 1311.844
active seconds. It then resumed in the same session and completed a bounded
stopping-only continuation in 569.206 seconds. Total root active wall was
1881.050 seconds. Route A and Route C returned complete partial artifacts and
matched their reported hashes. Route B did not write an artifact and was not
retried. The root wrote a final response, coordinator audit, files-only
convergence check, and hash-bound final package.

Primary status: `COMPLETED_WITH_AUDITED_PARTIAL_RESULT`.

Solver label for the retained mathematics: `RIGOROUS_PARTIAL_RESULT`.

Both post-hoc neutral audits are independent and excluded from scored metrics.
The first audit checked the retained first-segment theorems; the final audit
checked candidate SHA256
`40359f326aec9c01ecc0fa73c43bac72ffca74b1bea2e847f0bed1a601b812e9`
and returned `PASS` for `O1`, `O1b`, `O2`, `O3p`, and `O5`. They do not
convert the open frozen target into a completed theorem.

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
| Root active wall | 1881.050 s |
| Aggregate agent time | 4395.626 s |
| Sessions | 4 |
| Child sessions | 3 |
| Model responses | 72 |
| Tool calls | 58 |
| Input tokens | 3,625,852 |
| Cached input tokens | 3,287,040 |
| Uncached input tokens | 338,812 |
| Output tokens | 125,692 |
| Reasoning output tokens | 83,477 |
| Cost proxy | USD 5.183904 |

One incomplete Route B return is fully charged to these totals. The two
neutral audits and repository-side exact replay are excluded. The continuation
alone used 569.206 seconds, 16 responses, 14 tool calls, 126,992 uncached input
tokens, 23,752 output tokens, and 8,840 reasoning tokens.

## Protocol compliance

The coordinator completed a direct attempt and exact falsification probe before
delegation and required hash-bound route packets. The three-route first batch
met the preregistered cap, but was more aggressive than the closure-first
smallest-batch recommendation. The continuation corrected this by launching no
new child session or research wave and stopping at the first exact gap. This is
a scheduling observation, not a frozen protocol violation.

## Reproducibility

Run the strict route-interface replay:

```text
py -3 reproducibility/verify_route_claims.py
```

The older exact finite-domain replay remains available as
`reproducibility/audit_exact_claims.py`. Finite replays are `EVIDENCE` only;
the theorem proof is in `candidate_proof.md`. Session-level metric definitions
and totals are in `session_metrics.json`.
