# Arm A stage report

## Configuration

- System: `rigorous-open-math-research` v1.6.0.
- Model: `gpt-5.6-sol`.
- Reasoning effort: `xhigh`.
- Root research agent: 1.
- Initial independent route agents: 3.
- Independent integrated-proof audit: the adversarial agent was reused with a new hash-bound packet.
- Fresh-context convergence agent: 1.
- Network: disabled for the solver and all subagents.
- Repository, git, parent directory, prior solution, and external memory access: forbidden.

The scored sample is thread `01a03419-1479-7092-8fd9-04184576ebb3`. Earlier failed harness preflights are excluded from the scored usage.

## Mathematical result

Status: `STRICT`.

For every integer `n>=1` and every `R>1`, with `s=sqrt(R)`, the entry `G_{n,s}` has exactly `2n` zeros in `(0,pi)`, and all are simple.

The main exact reduction is

```text
G_{n,s}(y) = sin(y) [U_n(z) + s^(-1) U_{n-1}(z)],
z = (1+a) cos^2(y) - a,
a = (s+s^(-1))/2.
```

Thus

```text
Q_{n,s}(x) = P_n((1+a)x^2-a),
P_n(z) = U_n(z) + s^(-1) U_{n-1}(z).
```

An exact sign mesh gives `n` distinct simple roots of `P_n` in `(-1,1)`. Each scalar root lifts to two distinct nonzero roots of `Q` in `(-1,1)`, and the cosine substitution preserves simplicity. The package also contains an independent Sturm shooting and Prüfer-angle proof.

The separate checks for `n=1`, `y=0`, `y=pi`, `y=pi/2`, and `R=1` all pass.

## Audits

- Plugin-internal first-time audit: `PASS`, zero critical errors, zero gaps.
- File-only convergence reconstruction: mathematical state converged; stale status metadata was found and repaired.
- External anonymous first-time audit: `PASS`, zero gaps.
- Exact symbolic replay: `PASS`. It verifies determinant, trace, the `(EC_s)12` entry, and recurrence identities for `n=1,...,6`. This replay is `EVIDENCE` only; the uniform theorem is established by the written proof.
- Leakage audit: no repository, git, network, prior-answer, or outside-workspace access was observed in the scored event log.

## Scored resource data

Wall time: `1132.770 s`, or `18 min 52.770 s`.

The totals below sum the root session and four child sessions. The root session's own token counter is not treated as an aggregate of child counters.

| Metric | Value |
|---|---:|
| Model responses | 77 |
| Tool calls | 71 |
| Input tokens | 3,895,349 |
| Cached input tokens | 3,672,576 |
| Uncached input tokens | 222,773 |
| Output tokens | 73,731 |
| Reasoning output tokens, subset reported separately | 30,412 |
| API-equivalent normalized estimate | USD 3.83 |
| Output package bytes | 252,207 |

The normalized estimate uses `uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`. It is only a cross-arm accounting proxy and is not an actual ChatGPT bill.

The runtime reported weekly use increasing from approximately `25%` to `57%`, leaving `43%` until the reset at `2026-08-31 17:16:52 +08:00`.

## Artifact bindings

- Frozen task SHA256: `1FA717B9A5F195C42ECCA97D51E20327CB4EB2C316C936C054F55F7DD7416F16`.
- Candidate proof SHA256: `59B46FA2EE1E2D6A38AD4D386C936405AD96F4861DB4509872C6160A0C6791B6`.
- Final report SHA256: `A6C5F4D937D89D27FA10F541D61E7B21C1CECAAE6EDD62858D483BB5F95063EA`.
- Internal audit summary SHA256: `928DC7E99974360F03FD257FC6BBE018F84B247ECFDD0032A9D2D3A13EA77D9A`.
- Root event log SHA256: `50AF2FB2D29346DB5BA16F5403E714ACA905637C5F42CAB44013FEDB36FF4F15`.

This result duplicates previously known project mathematics and is not claimed as novel.
