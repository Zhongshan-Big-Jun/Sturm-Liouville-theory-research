# Plugin v1.14.0 Blueprint runtime gateway

## Outcome

Plugin v1.14.0 closes the active-runtime gap for Blueprint v2.2 projects. A
project with `blueprint-project.json` now binds one installed, plugin-owned
runtime through a single `ensure` operation. Canonical validation, retrieval,
proposal validation, and integration use that gateway. Project-local Python
tools are neither executed nor copied.

This release changes infrastructure only. It adds no mathematical claim,
changes no accepted theorem status, and does not promote any formalization
tier.

## Released components

| Component | Version | Release commit |
| --- | --- | --- |
| Parent marketplace | workflow 1.14.0, rigorous 1.11.0, manage 1.7.0 | `45abefa`, followed by DSH-layout fix `968a1cd` |
| DSH adaptation | 1.14.0 | `4ee31a2` |
| Local Codex CLI used for installation | 0.151.0-alpha.7.2 | installed marketplace snapshot |

The parent commits were pushed to `xsoc1/rigorous-open-math-research` and then
to `Zhongshan-Big-Jun/rigorous-open-math-research`. The DSH commit was pushed
to `xsoc1/math-research-dsh`.

## Runtime contract

- `runtime/blueprintctl.py` supports `version`, `ensure`, `validate`, `query`,
  `validate-submission`, and `integrate`.
- `ensure` validates `blueprint-project.json`, the configured Blueprint root,
  artifact root, work root, schema versions, and path containment.
- The disposable state binds the exact project root and ID, layout hash,
  config hash, runtime version, and combined runtime/tool hash.
- Configuration or runtime drift fails closed and requires a fresh `ensure`.
- Codex plugin layout and DSH flat skill layout resolve the same bundled tool
  set. There is no project-local fallback.
- Relative evidence locators resolve from the configured external artifact
  root. The receiver and query code use the same rule.

The standalone gateway file SHA-256 is
`DC5B680DFF646E45504A2F7D2974374EF46BD6E141E9C27E71314A8A8EA79156` in the
parent source, local Codex cache, and DSH bundle. The bound combined runtime
and tool hash is
`sha256:45b9caa919a472141b106a43d67de146aa372a42014a826592650f79264aad7f`.

## Release gates

| Target | Result |
| --- | --- |
| Parent repository validator | 81/81 PASS |
| Parent smoke suite | 14/14 PASS |
| Parent plugin and skill validators | PASS |
| DSH repository validator | 51/51 PASS |
| DSH smoke suite | 18/18 PASS |
| DSH bundle, Node syntax, and upstream sync checks | PASS |
| Gateway adversarial smoke | PASS in both Codex and DSH layouts |

The gateway smoke covers pre-ensure rejection, idempotent binding, a poisoned
project-local validator, external artifact roots, no-op proposal validation,
configuration drift, artifact-root mismatch, and path escape.

## Real BVE project activation

The installed Codex runtime was used on the real project root exactly once:

```text
operation: ensure
status: READY
wall: 0.363512 s
project_id: source_repo
```

It created only disposable operational directories and
`research/work/runtime/blueprint-gateway.json`. The canonical graph and
inventory were not rewritten. The initial bound snapshot was:

```text
blueprint_sha256: sha256:3b99f2090d73029fa77498a897979e614ddccbb205b613449fdd2181ce6ccc48
inventory_sha256: sha256:0c1e576e4902ffb8720e8a9b7c02a0df1c5425af805f1c9aba05b9968279ed5e
```

Post-ensure operations used only `validate` and `query`, without a second
`ensure`. Canonical validation reported:

- 9 nodes and 10 edges.
- Acyclic graph and valid typed dependencies.
- 3 evidence inventory rows with valid links.
- 1 mathematics context, 4 claims, 3 proved inferences, 0 open inferences,
  and no contradictions.

The cross-root artifact query for `CLM-R001-FINITE-R-BRANCH-V1` resolved to
`research/artifacts/blueprint-rigorous-math/R-20260825T100044Z-b4-m3-blueprint/round-001/route-001-finite-r-branch-certification/candidate_branch_proof.md`.
It exists, remains inside the configured artifact root, has size 12377 bytes,
and verified as
`sha256:0f609135b8d8bd2c9d830d0c9b86ef3b41454c217578a18992c76a9afad404d8`.

## Interpretation and limits

The previous blocker recorded in v1.11 through v1.13 is closed: there is now
an installed active Blueprint runtime, and the real canonical BVE graph can be
validated and queried without invoking legacy project-local Python tools.

This result certifies the canonical Blueprint graph and inventory through the
new gateway. It does not claim that every historical full-repository pipeline
artifact has been migrated, and it does not change any open Sturm-Liouville
research obligation.
