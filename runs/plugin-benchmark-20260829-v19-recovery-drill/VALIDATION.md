# Validation record

## Drill-local checks

- Segment 00 checkpoint replay: `READY`, 10 checked artifacts.
- Segment 01 checkpoint replay: `READY`, 13 checked artifacts.
- Artifact manifest: `PASS`, 11 checked files.
- `git diff --check`: `PASS`.
- Historical benchmark files changed: none.

## Generic project validator

The `manage-math-research-program` generic validator returned `INVALID`.
The failure is not caused by this drill. Direct `git cat-file` checks against
the unmodified `HEAD` commit confirm that these required files were already
absent:

- `knowledge/.blueprint/config.json`.
- `knowledge/blueprint.json`.
- `knowledge/evidence_inventory.csv`.
- `knowledge/blueprint_update_requests.jsonl`.

The validator also reports historical protected artifacts outside its expected
registered upstream-run area. A representative reported artifact,
`runs/three-arm-pilot-v2/pilot-v5-codex-u2/v17-regression/arm-a-plugin-v17/candidate_proof.md`,
is already tracked at `HEAD`.

No Blueprint initialization or repository-wide artifact migration was
attempted. Either operation would exceed the preregistered files-only recovery
drill and could change historical research packages.

## Scope conclusion

The v1.9 recovery chain passes all drill-local integrity checks. The generic
project-validator failure remains an independently visible repository
maintenance issue and is not hidden or counted as a recovery-protocol failure.
