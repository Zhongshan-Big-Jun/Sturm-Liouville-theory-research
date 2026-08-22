# Escalation ladder

Run: R-20260822T220000Z-b3-baseline

## Cost tiers

- Tier 0: read/reuse existing artifacts, no heavy computation.
- Tier 1: local analytic derivation + light numerical cross-checks (single scripts).
- Tier 2: moderate symbolic/computational exploration, background jobs.
- Tier 3: heavy full-scale global search or formalization effort.

## Log

| Time | Tier | Route | Trigger | Result | Next |
|---|---|---|---|---|---|
| 2026-08-22T22:20Z | 0 | all | Read project context | Existing partial results registered | Start R1 at Tier 1 |
| 2026-08-22T22:25Z | 1 | R1 | Goal: prove ratio bang-bang reduction | In progress | Formalize lemmas |
| 2026-08-22T22:35Z | 1 | R1 | Derived ratio energy invariant | STRICT structural theorem: exact 2n switches + [1,R,...,1] pattern | Escalate to R2/R3 |
| 2026-08-22T23:00Z | 2 | R2 | Found transfer-matrix recurrence + Chebyshev/Jacobi identification | O3 STRICT PROVED: exactly 2n roots in (0,pi) | Use in R3/O2 |
