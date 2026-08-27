# Arm C stage report

## Configuration

- System: QED at commit `121900964e6572aaf094412d434b5ac2a792a65f`.
- Model for every QED role: `gpt-5.6-sol`.
- Reasoning effort: `xhigh`.
- Codex CLI: `0.149.1`.
- QED mode: decomposition, one decomposition, one revision, and one proof attempt.
- Model-side tools, network, skills, plugins, memories, and subagents: disabled.
- QED Stage 0: pre-seeded with a neutral `Hard` classification and a no-literature statement,
  so the frozen no-network protocol could enter QED's decomposition core.

The prompt-input probe passed with zero project-document, skill, plugin, memory, or multi-agent
leakage markers. Its SHA256 is
`6DB0A0B35F9BB0BC63E4F03095506A6386FE90FA11E648B008BDBF2866642738`.

## Offline adapter disclosure

QED normally gives Codex roles file paths and expects tool-based reads and writes. With all model
tools disabled, the adapter appended the exact contents of existing, explicitly named files under
the isolated output root to each prompt. It supplied no mathematical route or prior solution.
Every original and adapted prompt hash is retained in `wrapper.log`.

The decomposer returned valid YAML directly, but QED's fallback parser selected the first nested
Markdown fence in the exact GOAL text and saved a 55-byte YAML scalar. The scalar is retained as
`decomposition.parser-bug.yaml`. The unchanged model response was copied to `decomposition.yaml`,
then parsed as a mapping with 10 steps and key step `STEP6`. This was a format-only normalization;
no mathematical text was edited and the decomposer was not rerun.

The post-pipeline `proof_effort_summary.md` is non-authoritative. Its prompt did not receive the
required referenced files and it incorrectly says `PASS`. Scoring uses the proof, QED structural
review, regulator decision, and fresh external audit instead. The generated failure analysis also
miscounts retry-state indices; its mathematical description of the open STEP6 is consistent, but
its run counts are not used.

## Mathematical result

Primary label: `PARTIAL_NOT_COMPLETE`.

The QED solver honestly declined to assert its unproved constant-order plan step. A fresh
label-blind independent audit certifies

```text
1/(2 sqrt(t)) <= ||P_t^x-P_t^y||_TV
               <= (5+3 log(t))/sqrt(t),                t>=1.
```

It also certifies:

- the exact conditional fair-lamp kernel on the visited interval;
- contraction to the `(L,U,Z)` range-endpoint triple;
- the exact diagonal-variation and killed-walk image formulas;
- the explicit parity-lattice binomial estimates;
- the reflection coupling and exact pre-meeting depth tail `P(K>=k)=1/k`;
- `TV(P_0^x,P_0^y)=1` and `TV(P_1^x,P_1^y)=3/4`.

The lower constant `1/2` improves the previously retained project lower constant `1/4`.

The original target is not complete. The first unresolved obligation is an explicit constant
`C` such that

```text
TV(Q_t^0,Q_t^2) <= C/sqrt(t),
```

or a direct full-lamplighter argument of the same order. The current pathwise range-equality
coupling has a harmonic tail and yields the logarithmic loss.

## QED internal review

- Structural verification: `FAIL` for the original complete task.
- Structural verdict: `CONTINUE`.
- Regulator: `REVISE_PROOF`.
- The one-proof preregistration cap then stopped revision and produced final state `FAILED`.
- Detailed verification was not run because structural verification failed.
- Fresh external label-blind audit: `PARTIAL_NOT_COMPLETE`, with all explicitly proved partial
  claims accepted.

## Scored resource data

| Metric | Value |
|---|---:|
| End-to-end wall | 2198.87 s |
| QED role sessions | 7 |
| Model responses | 7 |
| Model tool calls | 0 |
| Input tokens | 139453 |
| Cached input tokens | 7936 |
| Uncached input tokens | 131517 |
| Output tokens | 67782 |
| Reasoning output tokens | 48563 |
| API-equivalent normalized estimate | USD 1.8848824 |
| Candidate proof bytes | 25810 |

The seven roles were decomposer, prover, structural verifier, structural verdict, regulator
decision, final failure analysis, and proof-effort summary. `Model responses` counts exposed
`token_count` records. The normalized estimate uses
`uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M` and is not an actual bill.

The first scored rate-limit record, after the decomposer, showed primary `6%` and secondary
`56%`. Completion showed primary `35%` and secondary `61%`. The user requested no emergency
reserve. External audit usage is post-hoc and excluded.

## Artifact bindings

- Frozen task SHA256:
  `6859E0AF922BA8454758E2195FCEFCFE8FA164A40E2C23022EC7EBB2DA228943`.
- Candidate proof SHA256:
  `A528FECC631800697BC35A626BA7B562F145D254DD1DFAA99D313A6557000AAC`.
- Decomposition SHA256:
  `87E171BAAECDE98C729F43BF28D365C8C84112921680E19480FF13D971E7B17B`.
- QED structural review SHA256:
  `14F799EC69BCA42AAA3AA9FA95542B88E299FAD648AE473A84D4C846113E7E7A`.
- External review SHA256:
  `7392A6DFDB2C6CB7BE5E89439E3954FC9F567DD9136B7B86D3AD4CCE39B29081`.
- Offline wrapper SHA256:
  `54E987AFF2E18849F072AFFB937CCEE08FF9237A971E720F723F817498A61826`.
- Inline adapter SHA256:
  `AD7E8B6986C611819F2C73FF3D2EF122ECED928273D571CAE5CF0918D8EA9D79`.

Raw sessions remain in the external benchmark workspace because they contain encrypted model
internals. Seven sanitized logs retain session metadata, exposed usage counters, rate limits,
and task completion records.
