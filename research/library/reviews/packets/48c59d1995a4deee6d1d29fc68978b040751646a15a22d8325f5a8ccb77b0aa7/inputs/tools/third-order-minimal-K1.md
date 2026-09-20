---
title: Even minimal-solution anchor K(1)=e/4
tags: [mathtool, self-developed, recurrence, minimal-solution, strict]
source: Self-developed proof run R-20260824T184147Z-k1-e4-ab
status: STRICT for the c=1 even anchor; general K(c) remains OPEN
created: 2026-08-25
---

# Even minimal-solution anchor K(1)=e/4

## Analytic statement

For the even third-order recurrence at c=1, let `mu_j` be the positive minimal
solution normalized by `mu_0=1`. The exact finite backward solution and its
limit are

```text
mu_j^(N) = (2j)!/(2N+2) * sum_{r=j+2}^N (r-j-1)/(2r-1)!,
mu_j^* = 2e (2j)! * sum_{r=j+2}^infinity (r-j-1)/(2r-1)!,
lim_{j -> infinity} j^3 mu_j^* = e/4.
```

The proof uses the scaled second difference `d_j` and the exact factorization
`d_j = d_{j-1}/(2(j-1)(2j-1))`. A finite terminal condition gives the
backward formula; positivity and the fixed-index limit identify the minimal
solution. The factorial-tail expansion then gives the constant `e/4`.

2026-09-20 round 2 correction: the terminal value is
`d_N = v_(N-2) = N/((N+1)(2N)!) > 0`, not zero. The old extra divisor
`(1/4)^j/(j!)^2` in this card's limit was incompatible with the displayed
factorial series and has been removed. The normalized sequence in this card
is precisely the sequence defined above, with no further rescaling.
Current correction evidence is in `reports/proof-audit-round2-20260920/REPORT.md`.

## Scope and status

- `STRICT`: the theorem above is proved for the even c=1 anchor, including the
  endpoint normalization and uniqueness of the minimal branch.
- `EVIDENCE`: the historical high-precision table in
  `docs/SL_third_order_recurrence_theory.tex` is retained only as numerical
  evidence and is not used as proof.
- `OPEN`: the corresponding closed form and constant `K(c)` for general c,
  source-term control in the box induction, and classification of all general
  coefficient families remain unresolved.

## Verification and artifacts

- Proof source: `docs/SL_third_order_K1_proof.tex`.
- Rendered proof: `docs/SL_third_order_K1_proof.pdf`.
- Full handoff run: `runs/rigorous-open-math-research/R-20260824T184147Z-k1-e4-ab/`.
- Historical independent blind audit: `audit_report.md` in that run. Its
  acceptance concerns that frozen version and is not a new approval of this
  corrected card. The round 2 report records the current verification scope.
- The Blueprint arm's deterministic proposal/review/integration helper failed
  before process creation with `helper_unknown_error`; this is a workflow caveat,
  not a mathematical gap in the frozen proof. The bare Codex arm independently
  obtained the same theorem.

## Applicability

Use this tool when the even c=1 recurrence is present and a rigorous anchor for
the minimal-solution asymptotic is needed. Do not extrapolate the constant to
general c without a new proof.
