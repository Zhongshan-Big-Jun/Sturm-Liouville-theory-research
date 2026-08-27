# Resume protocol and completion record

The scored v1.7 root session is
`01a041fc-0f14-79b3-86b3-aef3d4aa1b8a` in the frozen external `CODEX_HOME` at
`F:\benchmark\PILOT-V5-V17-U2-20260827\codex-home`.

The regression was resumed on 2026-08-27 under the following frozen rules:

1. Use the same root session, work directory, model, reasoning effort, proxy,
   and plugin installation.
2. Do not copy this repository result or the post-hoc neutral audit into the
   scored work directory before the solver stops.
3. Do not start a new research wave. Route A and Route C have returned; Route B
   is an incomplete return and must be recorded as such.
4. Ask the root only to ingest its existing artifacts, run its stopping-boundary
   convergence check, and write an honest final partial report.
5. Preserve the original 75-minute active-wall cap. The first segment used
   1311.844 seconds. Preserve the preregistered efficiency target by stopping
   the scored root after at most 1727 additional active seconds.
6. Add the continuation usage to `session_metrics.json`; do not overwrite the
   first-segment measurements.

The same root completed the stopping package in 569.206 additional active
seconds, for 1881.050 total root seconds. It launched no new child session,
did not retry Route B, and did not start a new mathematical route. Final scored
status: `COMPLETED_WITH_AUDITED_PARTIAL_RESULT`. The fixed-constant upper bound
remains open at `O3`.

All external neutral audits are post-hoc and remain excluded from scored
usage. No further scored resume is authorized for this regression run.

The continuation was preflighted at `2026-08-27T12:31:29Z`. It uses the exact
first-segment CLI `0.149.0-alpha.4.3`, pinned by SHA256 in
`CONTINUATION_PREFLIGHT.md`, rather than the newer WSL default CLI. The frozen
launcher is `harness/resume-v17-a-wsl.sh`.
