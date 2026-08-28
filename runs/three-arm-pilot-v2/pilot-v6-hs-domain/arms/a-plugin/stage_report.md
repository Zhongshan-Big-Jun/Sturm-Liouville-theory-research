# Pilot v6 Arm A stage report

## Outcome

- Arm: optimized `rigorous-open-math-research` v1.7.0 with bounded research children.
- Model: `gpt-5.6-sol`, `xhigh`.
- Solver label: `INDEPENDENTLY_AUDITED_PROOF`.
- Internal independent audit: `PASS`, with no mathematical gap.
- Posthoc anonymous blind audit: `PASS`, 99/100 under its audit rubric, with no repair required.
- Hidden gold: not inspected.

For every real `c>0`, every integer `s>=4`, and every `n>=0`, the exact result under the
abstract polynomial reading is

```text
Q_n^(s) in D(K_c^(s/2)) if and only if n in {0,1}.
```

The abstract polynomial completion is not canonically equal to the operator domain under the
identity on polynomial representatives. It is naturally unitarily equivalent through a
boundary-correcting map. The literal full polynomial span is not contained in the operator
domain, and its individually admissible named members span only `span{1,x}`.

Under the genuine spectral inverse reading, every transported member lies in the required
operator domain and the transported span is dense, but those functions are generally not
polynomials.

There is no remaining mathematical obligation inside the frozen contract. The first optional
upgrade is proof-assistant formalization. Literature and novelty status remain `UNKNOWN` because
network and source access were forbidden.

## Scored resource data

| Metric | Value |
|---|---:|
| Root active wall | 1514.327 s |
| Aggregate agent time | 1984.341 s |
| Sessions | 3 |
| Turns | 4 |
| Model responses | 82 |
| Tool calls | 62 |
| Input tokens | 4866982 |
| Cached input tokens | 4651520 |
| Uncached input tokens | 215462 |
| Output tokens | 74357 |
| Reasoning output tokens | 33449 |
| API-equivalent normalized estimate | USD 4.209596 |
| Artifact bytes, excluding `events.jsonl` | 76549 |

`Model responses` counts exposed `token_count` records. `Tool calls` counts raw
`custom_tool_call` records. The normalized estimate is
`uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`; it is a cross-arm proxy,
not an actual ChatGPT bill. The posthoc anonymous audit is excluded from all scored resource data.

## Quota data

- First exposed root record: primary 18 percent, secondary 3 percent.
- Final root record: primary 75 percent, secondary 12 percent.
- The user reported both windows reset before launch. The difference between reset and first
  exposure includes coordinator and preflight usage outside the scored arm.

## Audit and reproducibility bindings

- Frozen task SHA256: `359d335803eae43f45120e3ca3995b8f12ec2f98b357e2b10116eafe2d8c6332`.
- Candidate proof SHA256: `0e36b83891a4b5a509174eb7e367365652c0637267b5d4610f5e01a7c42ec080`.
- Internal audit SHA256: `046e7db41ea7f1043b85a172b65e5c535b457cc9d46c61b77a25b4f6edf00c3b`.
- External review SHA256: `86d6e02c79dd436014896b92a39425eec28f136aac9f52d1a19d32599b19de8d`.
- External verdict SHA256: `b75787758bde1b9dd6ad778b7449942911de1d05764a537fba79e8365a4e52b5`.

The exact symbolic replay terminates with `ALL_EXACT_CHECKS_PASS`. It is a deterministic finite
check and `EVIDENCE`, not a substitute for the strict proof in `candidate_proof.md`.

The anonymous score uses the auditor's five-axis review rubric and is not yet the final
preregistered cross-arm score. The preregistered score and hidden-gold comparison are computed
only after A, B, and C are all frozen.
