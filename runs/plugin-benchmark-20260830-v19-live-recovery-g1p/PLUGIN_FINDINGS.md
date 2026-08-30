# v1.9 plugin findings

## Validated behavior

1. Unresolved live work forces `RECONCILE_INFLIGHT` as the unique resume action.
2. Exact worker and session IDs survive sealing and receipt creation.
3. Completed and replaced actions must enter `do_not_repeat`.
4. Open obligations cannot silently disappear across checkpoint lineage.
5. The mathematical status remains unchanged unless an explicit audited status
   transition is supplied.
6. Checkpoint operations are sub-second after valid inputs are prepared.

## Candidate v1.10 improvements

### P0. Version bound mutable artifacts automatically

The first post-resume merge accidentally edited `whiteboard.md` and
`closure_gate.md`, which were bound by segment 00. Verification correctly made
the checkpoint stale. The files were restored byte-for-byte and progression
moved to `whiteboard-01.md` and `closure_gate-01.md`.

Add a deterministic `advance` helper that copies bound mutable artifacts to the
next sequence, refuses in-place edits, and returns their new bindings. This is
the highest-value usability fix.

### P1. Normalize CLI paths and timestamps

- Accept project-relative paths without joining an already project-prefixed
  path twice, or fail with the exact accepted path form before validation.
- Accept valid ISO-8601 timestamps with seven fractional digits, or expose a
  canonical timestamp generator in the CLI.

### P1. Add explicit obligation supersession

The lineage guard correctly rejected a renamed open obligation. Add a typed
`supersedes` or `refines` record so a strictly smaller gap can retain ancestry
without manual ID preservation and do-not-repeat repair.

### P1. Add a scoped pipeline gate

The parent repository has 66 legacy migration problems and 19 warnings. The
new run itself passes. A `--scope`, `--since`, or registered-subproject mode
would distinguish new-run validity from historical migration debt without a
7,000-line nested scaffold project.

### P2. Honor Blueprint artifact roots

`blueprint_query.py` emitted broken artifact locator warnings because it did not
resolve paths through the configured parent artifact root. The actual artifacts
and hashes were valid.

### P2. Formalization handoff across isolated workspaces

The scoped workspace needed a duplicate Lean scaffold while the canonical Lean
project lives at the parent root. Add a hash-bound external formalization
handoff or a first-class parent-project scaffold pointer.

## Release recommendation

Do not call these mathematical-performance regressions. v1.9 passed its core
safety contract. Implement P0 and the two P1 CLI or lineage improvements as a
small v1.10 usability release, then rerun only this recovery drill and the
static test suite. No three-arm mathematics benchmark is needed for those
deterministic changes.
