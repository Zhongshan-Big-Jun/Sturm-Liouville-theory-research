# Pilot v6 Arm C stage report

## Outcome

- Arm: real QED decomposition pipeline at commit `121900964e6572aaf094412d434b5ac2a792a65f`.
- Model for every active role: `gpt-5.6-sol`, `xhigh`.
- QED internal status: `FAILED`.
- External anonymous mathematical audit: `PASS`, 97/100, no load-bearing error.
- Hidden gold: not inspected.

QED produced a complete eight-step proof of all three frozen claims. It also proved that
`C[x] intersect D(K_c^(s/2))` is a graph core, while distinguishing this from the non-density of
the individually admissible named members.

The internal structural verifier passed statement fidelity, completeness, originality,
decomposition adherence, and every key-step structural check. It failed only because the offline
status citation pointed to `related_info/related_work.md`, which the verifier prompt adapter did not
inline. The regulator classified this as a documentation issue, requested a revision, and then hit
the frozen one-revision limit. No mathematical counterexample was reported.

The external first-time audit independently checked the proof before reading QED's reports. It
returned `PASS`. Benchmark reporting retains both facts: the QED system did not self-certify its
run, while the frozen proof artifact is an independently audited proof.

## Mathematical result

For every real `c>0`, integer `s>=4`, and `n>=0`, under the algebraic polynomial reading,

```text
Q_n^(s) in D(K_c^(s/2)) if and only if n in {0,1}.
```

The abstract polynomial completion is not equal to the operator domain under the identity on
polynomial representatives. The boundary-correcting map `K_c^(-m)L^m` gives a unitary equivalence
in the energy norms. The literal full polynomial span is not contained in the operator domain,
and its individually admissible named members span only `span{1,x}`. The different intersection
`C[x] intersect D(K_c^(s/2))` is graph-norm dense.

No mathematical gap remains inside the frozen contract.

## Scored resource data

| Metric | Value |
|---|---:|
| Pipeline wall | 1438.3 s |
| Aggregate model active time | 1373.396 s |
| QED model calls | 7 |
| Sessions | 7 |
| Turns | 7 |
| Exposed model responses | 8 |
| Tool calls | 1 |
| Input tokens | 167013 |
| Cached input tokens | 18944 |
| Uncached input tokens | 148069 |
| Output tokens | 61896 |
| Reasoning output tokens | 40819 |
| API-equivalent normalized estimate | USD 1.8377736 |
| Artifact bytes, excluding QED source clone | 170999 |

The one tool call was a fail-closed code-mode attempt in the final proof-effort-summary stage. It
did not supply mathematical information. `QED model calls` follows QED's token tracker; `exposed
model responses` counts token records and is one larger because that final session responded again
after the failed tool attempt.

The normalized estimate uses
`uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`. It is a cross-arm proxy,
not an actual ChatGPT bill. The external audit is excluded from all scored usage.

## Quota data

- Latest account record before C: primary 3 percent, secondary 16 percent.
- First C call final record: primary 33 percent, secondary 21 percent.
- Final C record: primary 67 percent, secondary 26 percent.

## Infrastructure replacement

The initial launch exited before any model process because QED unconditionally required a command
named `claude`, although all frozen active roles used Codex. It produced no wrapper log, Codex
session, or mathematics and is excluded as `INFRA_INVALID`.

The permitted replacement used fresh roots and a fail-closed `claude` shim. The shim would exit 70
if invoked. It was never invoked. No provider, model, prompt, QED commit, budget, or scoring rule
changed.

## Bindings

- Frozen task SHA256: `359d335803eae43f45120e3ca3995b8f12ec2f98b357e2b10116eafe2d8c6332`.
- QED proof SHA256: `daf055b84e09024f6a653b57adb771e50b268e1cf9692dab97c6ab59a7bd9987`.
- Structural report SHA256: `916ea1907955a99c17ab70e9198d25b692e29d8b34a82634a381231a79b117e4`.
- External review SHA256: `763acdd921d14153edf21653ddc934864c218f8ae72a693a634518ffc7e44e9c`.
- External verdict SHA256: `950ef474acc837946de7675a2fbc37f6e92c0499212128f00f3a190d723d54a3`.
