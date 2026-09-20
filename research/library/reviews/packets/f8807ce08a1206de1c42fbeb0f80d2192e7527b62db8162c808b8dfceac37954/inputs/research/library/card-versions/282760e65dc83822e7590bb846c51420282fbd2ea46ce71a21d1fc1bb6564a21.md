---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0bfab-5af3-7352-a134-deabd755066c"], "created": "2026-08-25", "dependencies": [{"location": "tools/third-order-recurrence.md", "sha256": "9982e1b1af8f41e9763bcfadf96217a1818241ae155d1ac29feb4cc6a92608ae"}], "evidence_status": "SCOPED_STATUS_AND_DEPENDENCY_UPDATE", "source": "Self-developed proof run R-20260824T184147Z-k1-e4-ab", "sources": [{"locator": "Existing c=1 finite terminal convention and normalized limit", "path": "docs/SL_third_order_K1_proof.tex", "sha256": "e6d81354b9f73985d7d7f21c278ebf90a5ba90990379095c3b7d7bd5b8e0cbc5"}, {"locator": "Fourth-round explicit family general-c extension", "path": "docs/SL_third_order_recurrence_theory.tex", "sha256": "71f45bf0a48eb3b6b2007597e1209f7757b45bcbdccb770eaf39d5407887633e"}], "status": "STRICT even c=1 anchor; exact-family general-c extension linked separately", "tags": ["mathtool", "self-developed", "recurrence", "minimal-solution", "strict"], "title": "Even minimal-solution anchor K(1)=e/4", "tool_id": "third-order-minimal-K1"}
---

# Even minimal-solution anchor K(1)=e/4

## Analytic statement

For the even third-order recurrence at c=1, let `mu_j` be the positive minimal
solution normalized by `mu_0=1`. For an integer `N>=3`, the unnormalized finite
backward solution has terminal values `mu_(N+1)^(N)=1` and
`mu_N^(N)=mu_(N-1)^(N)=0`. Its finite formula and normalized limit are

```text
mu_j^(N) = (2j)!/(2N+2) * sum_{r=j+2}^N (r-j-1)/(2r-1)!,  0<=j<=N-1,
mu_k^* = lim_{N -> infinity} mu_k^(N)/mu_0^(N),  fixed integer k>=0,
mu_k^* = 2e (2k)! * sum_{r=k+2}^infinity (r-k-1)/(2r-1)!,
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
The finite sequence itself tends to zero at every fixed index; taking its
normalized ratio before the limit is essential. The finite sum is not the
formula for the separately prescribed terminal value at `N+1`.
Current correction evidence is in `reports/proof-audit-round2-20260920/REPORT.md`.

## Scope and status

- `STRICT`: the theorem above is proved for the even c=1 anchor, including the
  endpoint normalization and uniqueness of the minimal branch.
- `EVIDENCE`: the historical high-precision table in
  `docs/SL_third_order_recurrence_theory.tex` is retained only as numerical
  evidence and is not used as proof.
- For the same explicit even/odd coefficient family, the fourth-round proof now gives the normalized general-c positive-tail formula and constants. See `tools/third-order-recurrence.md` and `docs/SL_third_order_recurrence_theory.tex`. This card retains the original even c=1 terminal convention above; its finite unnormalized sequence must not be confused with the other convention.
- `OPEN`: source-term control in the box induction and classification of arbitrary coefficient families remain outside those exact-coefficient results.

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

2026-09-21 scope update: the c=1 proof and all displayed anchor formulas are unchanged. The new general-c proof specializes to the same e/4 constant; this status update and its exact dependency receive new independent review.
