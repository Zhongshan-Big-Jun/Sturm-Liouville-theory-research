# Pilot v5 v1.7 closure-first regression preregistration

- Registered: `2026-08-27T06:30:25Z`.
- Run ID: `R-20260827T063025Z-u2-v17-regression`.
- Purpose: matched scheduling regression against scored pilot v5 Arm A.
- Scored system: `gpt-5.6-sol`, `xhigh`, rigorous plugin v1.7.0, research
  sub-agents enabled, at most 3 concurrent sub-agents.
- Plugin commit: `957d80b7f1c58b60972a4ece87945cd93c0a1476`.
- Codex CLI: `0.149.0-alpha.4.3`.
- Prompt SHA-256:
  `0AB0AF8E6936C0597626493029004DC4F8851BF79E5F6AE4076CCC2605D012A7`.
- Prompt equality rule: `PROMPT.md` must be byte-identical to the scored v1.6
  Arm A prompt.
- Isolation: fresh `CODEX_HOME`, no memory, `--ignore-rules`, isolated work
  directory, no repository reads, no internet, workspace-write sandbox.
- Wall cap: 75 minutes. No emergency quota reserve.
- WSL transport proxy: `http://172.22.112.1:7898`, preflight returned HTTP
  401 from the unauthenticated `/v1/models` probe; port 7897 timed out.
- Controls: reuse frozen v1.6 Arm A, blank Arm B, and QED Arm C metrics; do not
  rerun controls.

## Quality gate

The run passes the quality gate only when an independent external audit finds
no false completion claim and accepts every theorem-strength claim retained in
the final comparison. A partial result may pass quality while the original
target remains incomplete.

## Efficiency targets

- root wall at most 3039 s;
- model responses at most 184;
- tool calls at most 151;
- child sessions at most 4;
- uncached input at most 609,441;
- output at most 234,234;
- cost proxy at most USD 13.0252915.

Missing any target is reported as a regression or unconfirmed optimization,
not explained away post hoc.

## Contamination limitation

U2 is reused from pilot v5 to isolate the scheduling change. The solver does
not receive prior outputs, but this is not an OOD test and cannot establish
general mathematical quality. A later matched run on a new problem class is
required before a general performance claim.
