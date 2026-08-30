# Plugin performance report: v1.11 scoped pipeline validation

Date: 2026-08-30

Status: ENGINEERING_VALIDATED. This round produced no new mathematical claim.

## Outcome

Released workflow v1.11.0 with a deterministic scoped validation mode for a
self-contained logical project nested inside a legacy repository. The mode
allows a new experiment to certify its own pipeline state without claiming
that unrelated historical migration debt has been repaired.

Published revisions:

- Codex parent and fork: `2c61581a22392bf89cc99c71d03ca0b1fe9a80b5`.
- DSH adapter: `eae522a8f1896b10196efabe57550c8a7563a757`.
- Local Codex install: `math-research-workflow@math-research` v1.11.0.

## New gate contract

`validate_pipeline.py` now accepts:

```text
--project <physical-repository-root> --scope <relative-logical-project-root>
```

The scoped root is treated as a complete logical project. It must contain
`project.json` or `blueprint-project.json`. Task packets, runs, Lean artifacts,
quota checkpoints, completion certificates, source hashes, formalization paths,
and optional git cleanliness are evaluated relative to and confined within that
root.

The following conditions fail before or during validation:

- absolute or project-escaping scope paths;
- scope roots inside nested git repositories;
- scope roots without a project marker;
- source or formalization bindings that escape the validation root.

Every scoped result explicitly says that artifacts outside the scope were not
assessed and that the verdict is not a whole-project PASS.

## Real-artifact drill

Target:
`runs/plugin-benchmark-20260830-v19-live-recovery-g1p/workspace`.

| Invocation | Result | Meaning |
| --- | --- | --- |
| Direct logical root as `--project` | 0 problems, 2 warnings | Reference result |
| BVE root plus `--scope` | 0 problems, 2 warnings | Exact hard-verdict equivalence |
| BVE root plus `--scope --check-git` | 0 problems, 2 warnings, scoped git clean | Unrelated dirty files do not contaminate the scope |
| BVE root without `--scope` | 67 problems, 20 warnings | Historical whole-project debt remains visible |

The source and installed validator hashes both equal
`A1356606F06580E9D9A695579E4AFD417421583EC2964974FF2218139EA992B7`.

No model call, research child, transcript replay, or mathematical recomputation
was used in this drill.

## Validation

Parent plugin repository:

- `validate_all.py`: 81/81.
- Smoke tests: 12/12.
- Workflow plugin validator: PASS.
- Workflow skill validator: PASS.
- Python compile and `git diff --check`: PASS.

DSH adapter:

- `validate_all.py`: 51/51.
- Smoke tests: 16/16.
- Bundle check, Node syntax check, sync-check, Python compile, and diff check:
  PASS.
- Upstream lock: 107 files at parent commit `2c61581`.

The DSH sync layer was also generalized for independent plugin semantic
versions. It now consumes the upstream workflow version even when rigorous and
workflow versions differ.

## Static context cost

The always-loaded workflow SKILL entry grew from 31,701 bytes in v1.10.0 to
31,931 bytes in v1.11.0, an increase of 230 bytes, or about 0.73 percent. It
remains below the 32,768-byte gate with 837 bytes of headroom. Full scope
semantics live in on-demand documentation rather than the entrypoint.

## Blueprint v2.2 gateway assessment

The current installed Codex skills and plugin caches contain no
`runtime/blueprintctl.py`. Under the project's Blueprint v2.2 highest-precedence
layout rule, no project-local `knowledge/tools/*.py` or legacy Blueprint tool
was run or copied. The Blueprint gateway and artifact-root migration therefore
remain OPEN until an active plugin supplies the required runtime gateway.

This limitation does not affect the scoped pipeline validator, but it prevents
this round from honestly claiming that the separate Blueprint artifact-root
issue is fixed.

## Next bounded optimization candidates

1. Add or adopt the authoritative Blueprint v2.2 runtime gateway, then test
   `ensure` and artifact-root resolution without project-local tools.
2. Define a formalization handoff contract across isolated logical project
   roots, including hash-bound source and destination roots.
3. Reduce workflow entrypoint size before adding another always-loaded rule.

