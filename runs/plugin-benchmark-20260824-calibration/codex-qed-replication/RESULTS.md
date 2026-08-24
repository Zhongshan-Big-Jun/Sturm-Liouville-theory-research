# Codex and QED three-arm replication - results

Status: completed on 2026-08-24.

This is a single-sample contaminated regression calibration. The B3 O3 theorem and its Chebyshev reduction were already present in project history, and plugin v1.6.0 was developed with knowledge of that history. The table must not be interpreted as out-of-distribution evidence.

## Frozen comparison

All three arms used `gpt-5.6-sol` at `xhigh` reasoning, the same frozen task with SHA256 `1FA717B9A5F195C42ECCA97D51E20327CB4EB2C316C936C054F55F7DD7416F16`, no solver web access, and an independent anonymous mathematical audit outside scored usage.

| Metric | Arm A: plugin | Arm B: blank | Arm C: QED |
|---|---:|---:|---:|
| Final externally audited status | STRICT | STRICT | STRICT |
| External anonymous audit | PASS | PASS | PASS |
| Main execution path | Plugin research workflow | One plain Codex response | QED Easy short circuit |
| Wall time, s | 1,132.770 | 253.951 | 283.717 external |
| Model responses | 77 | 1 | 5 |
| QED role calls | N/A | N/A | 1 |
| Tool calls | 71 | 0 | 4 |
| Sessions | 5 | 1 | 1 |
| Fresh child agents | 4 | 0 | 0 |
| Input tokens | 3,895,349 | 9,397 | 82,667 |
| Cached input tokens | 3,672,576 | 0 | 45,312 |
| Uncached input tokens | 222,773 | 9,397 | 37,355 |
| Output tokens | 73,731 | 10,279 | 11,583 |
| Reasoning output tokens | 30,412 | 8,127 | 6,919 |
| Normalized estimate, USD | 3.8347 | 0.2432 | 0.3992 |
| Weekly quota, before to after | about 25% to 57% | 57% to 59% | about 59% inferred to 68% |

The normalized estimate is `uncached_input*USD 4/M + cached_input*USD 0.40/M + output*USD 20/M`. It is a common accounting proxy, not an actual ChatGPT bill. Post-hoc reviewer usage is excluded from every arm.

For every arm, `model responses` counts exposed per-turn token-counter records rather than independent pipeline roles or API launches. `Tool calls` counts top-level tool-call events; one event may bundle multiple nested operations. QED role calls are reported separately.

Arm C's Codex response, tool, token, and final quota counters come from its raw Codex session and are preserved in a retained sanitized event log. Its role count and `283.600 s` call elapsed time come from QED's tracker. The table's `283.717 s` end-to-end wall is an externally measured, provenance-only timestamp difference in `arms/c-qed/timing.json`; retained QED logs support `284 s` after rounding. The C starting quota is inferred from Arm B, output bytes are a retained directory sum, and audit status comes from the post-hoc reviewer.

QED's bundled tracker correctly records one per-provider Codex call and total input and output, but it leaves an unused Claude model at the top level and omits cache, reasoning, and tool-call counters.

## Mathematical outputs retained

All three arms proved the same uniform theorem: for every integer `n>=1` and every `R>1`, `G_{n,s}` has exactly `2n` simple zeros in `(0,pi)`.

- Arm A produced the Chebyshev reduction, an independent Sturm shooting and Pruefer route, internal adversarial review, a fresh-context convergence reconstruction, and the largest persistent research package.
- Arm B independently produced a complete Chebyshev proof without tools, skills, plugins, memory, project instructions, or subagents.
- Arm C produced a direct Sturm oscillation proof. At `y=pi`, the explicit eigenfunction has exactly the `2n` interfaces as its interior zeros, so it is the `(2n+1)`-st eigenfunction. A Lagrange identity transfers Dirichlet eigenvalue simplicity to analytic simplicity of `G`.

Every proof and external audit is retained in its arm directory. These are benchmark reproductions of known project mathematics, not novel theorem claims.

## What this sample shows

1. Correctness does not separate the systems on this task. Every arm received `PASS` with no mathematical gap.
2. Arm B is the efficiency winner for this sample. Relative to Arm A it used `95.8%` less uncached input, `86.1%` less output, `77.6%` less wall time, and a `93.7%` lower normalized estimate. Equivalently, Arm A's estimate was `15.8` times Arm B's.
3. Arm C did not improve correctness over Arm B. It was `11.7%` slower, used `297.5%` more uncached input, emitted `12.7%` more output, and had a `64.2%` higher normalized estimate.
4. Arm A paid substantial overhead for assurance and reusable artifacts. Its value on this run is the independent routes, adversarial review, convergence evidence, and durable package, not a higher final theorem score.
5. QED's Stage 0 role and Easy routing were tested, but its decomposition and verification chain was not exercised. Stage 0 changed the classification from Hard to Easy and skipped decomposition, proving, structural verification, detailed verification, verdict, and summary roles.

The defensible conclusion is narrow: on this contaminated B3 O3 regression task, the optimized plugin and pinned QED run did not beat a blank `gpt-5.6-sol` control on audited theorem correctness, while both incurred more resource cost. This does not establish that prompts are generally sufficient, that the plugin lacks value on open problems, or that QED's full verifier chain is ineffective.

## Protocol limitations

- Single task, one scored sample per arm, and no uncertainty interval.
- Historical contamination favors memorized or rediscovered known routes and invalidates OOD claims.
- Arm A is intentionally richer than the other arms and optimizes for research traceability, not minimum one-shot cost.
- QED's Stage 0 normally requests online literature search. The common no-network rule and safe adapter test an offline variant rather than full online fidelity.
- QED took an Easy short circuit, so the comparison is not a three-way multi-agent benchmark in realized execution.
- Arm C used Codex CLI `0.149.1`; Arms A and B used `0.149.0-alpha.4.3`. The model and reasoning effort were unchanged, but the CLI drift remains a protocol deviation.
- Weekly quota percentages are coarse runtime reports and should not be treated as a precise token-to-quota conversion.

## Recommended next benchmark

Use the separate OOD suite, freeze a single Codex CLI version, require tasks whose expected solution is absent from project history, and run at least three seeds per arm. For a genuine QED architecture comparison, select a task that reaches its Hard path and pre-register that an Easy short circuit is scored as a distinct one-role condition rather than as full QED.

## Artifact index

- Arm A: `arms/a-plugin/stage_report.md`, `arms/a-plugin/candidate_proof.md`, and `arms/a-plugin/external_audit.md`.
- Arm B: `arms/b-blank/stage_report.md`, `arms/b-blank/final_response.md`, and `arms/b-blank/external_audit.md`.
- Arm C: `arms/c-qed/stage_report.md`, `arms/c-qed/candidate_proof.md`, `arms/c-qed/external_audit.md`, and `arms/c-qed/source_manifest.md`.
