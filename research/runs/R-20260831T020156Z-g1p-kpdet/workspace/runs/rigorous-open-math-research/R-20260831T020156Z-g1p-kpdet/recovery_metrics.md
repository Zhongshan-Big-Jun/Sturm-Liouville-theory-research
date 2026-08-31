# Recovery and run metrics

## Interruption safety

- Research workers dispatched: 2.
- Worker restarts: 0.
- Duplicate worker dispatches: 0.
- Transcript replays: 0.
- Worker reconciliation records: 2, both `INGESTED` exactly once.
- Sealed checkpoints through the final validation boundary: 4, sequences 00-03.
- Verified resume receipts through the final validation boundary: 4, sequences 00-03.
- Lost worker artifacts: 0.
- Recovery protocol model calls: 0.
- Recovery protocol network calls: 0.
- Deterministic sequence-03 schema-repair model calls: 0.
- Final scoped workflow gate: 0 hard problems, 1 expected partial-status warning.

## Review and integration

- Fresh mathematics audit agents: 1, verdict `PASS`.
- Fresh Blueprint review agents: 1, verdict `approve`.
- Blueprint validation attempts with a valid submission path: 1, passed.
- Blueprint deterministic integrations: 1, merged.
- Canonical post-integration validations: 1, passed.

## Formalization

- Lean target: one Tier 0 scaffold.
- Final `lake env lean` exit code: 0.
- Expected scaffold holes: 1, exactly `PHI-SIGN`.
- Duplicate Lean process detected and stopped: 1.
- Pre-pass repairs: tab characters replaced because Lean forbids them; two real-division definitions marked `noncomputable`.

## Usage limits

Per-agent tokens, cache tokens, response counts, and monetary cost are not
available from this local task interface and are therefore recorded as
`unknown`. No values are estimated or invented.
