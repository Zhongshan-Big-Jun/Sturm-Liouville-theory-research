# Adversarial audit report

## Package identity

- Frozen contract: `problem_contract.md`, sha256
  `976cffb63e8e20d1395f0abff0f3735b7ba538b188b420772c22df80df46ed23`.
- Integrated partial proof: `candidate_proof.md`, sha256
  `40359f326aec9c01ecc0fa73c43bac72ffca74b1bea2e847f0bed1a601b812e9`.
- Obligation graph at audit: `obligation_graph.md`, sha256
  `e4fb3e040a2d9dbf02e72cec560b288f916938e39cd5ca3ae6cb2d28446afc5e`.
- Route A input: sha256
  `6ce207738f66fcd3b0b5b2c39175cf068be15f8b8532b76593e11b5cd386b647`.
- Route C input: sha256
  `f260fe18d316ad8d58294700ad4bb3cd40514537728a7ac67ae576c19ca7bbf2`.
- Audit role: fresh adversarial coordinator pass.  It is not an independent-agent audit; the
  continuation instruction prohibited a new subagent.

## Verdicts

- **Frozen-target completion verdict:** `FATAL_GAP`.
- **Partial theorem (7.1) module verdict:** `PASS`.
- **Definition audit:** `PASS` for the partial theorem.
- **Logic audit:** `PASS` for `O1`, `O1b`, `O2`, `O3p`, and `O5`; `FAIL` for completion at open
  `O3`.
- **Boundary audit:** `PASS` for the scope actually claimed (`t>=2` in (7.1)).
- **Adversarial audit:** `PASS` for the partial modules; the naive unimodality route is
  concretely refuted and the reflected-coupling lower bound is correctly classified as
  coupling-specific, not a TV lower bound.

The `FATAL_GAP` label is relative to the frozen completion contract.  It does not say that a
proved line of (7.1) is false; it says the required fixed-constant upper-bound module is absent
and is not a local cosmetic repair.

## Definition and semantic-fidelity audit

- `(0,2)` is used throughout as all lamps zero with base at two.  No lit initial lamp is
  introduced.
- For `t>=1`, the last-resampling proof makes the lamps i.i.d. fair exactly on the visited
  interval; outside lamps retain the forced initial zero.  The proof explicitly excludes
  `t=0`, when no switch occurs.
- Translation acts on both lamp locations and the base.  Both starts are even, so endpoint
  parity agrees at every time.
- The chain is not lazified or replaced by another switch convention.
- Formula (3.1) correctly includes every enclosing exact range and the weight
  `2^{-(u-l+1)}`.  The visible-hull fibers are finite and both likelihoods are constant on a
  fiber, validating the exact TV identity (3.2).

## Logic and constant audit

- Endpoint projection gives a lower bound, not an upper bound.  The shifted binomial masses
  are `p_k` and `p_{k-1}`; unimodal telescoping yields their TV as `max p_k`.
- The Markov/Chebyshev calculation in Section 4 is self-contained and gives
  `max p_k>=1/(4sqrt(t))` for every `t>=1`.
- The one-sided reflection identity (5.3) has the correct half-open endpoints and parity count.
  The central-atom induction proves the precise bound used in (5.4).
- In the reflected coupling, each `Y` increment is a past-measurable sign times a fresh fair
  sign, so the `Y` marginal is a simple symmetric walk from two.  Both paths meet at site one.
- The pre-meeting intervals are exactly `[-D,1]` and `[1,D+2]`.  Requiring the common tail to
  visit both extremes is sufficient for equal triples and hence for a valid shared conditional
  lamp coupling.
- The gambler-depth law `Pr(D>=d)=1/(d+1)` and truncated expectation bound
  `E[(D+1)1_{tau<=n}]<=H_(n+1)` have correct indices.
- With `n=floor(t/2)`, the remaining tail has at least `t-n=ceil(t/2)` steps.  The union bound
  gives exactly (5.1), and the harmonic integral plus denominator inequalities give (5.2).
- Formula (6.2) has the correct normalized translation `a -> a+2` and factor `2^{-t-1}`.
  Inequality (6.3) is sufficient, not claimed necessary.

## Boundary and computation audit

- `t=0`: TV is one; no conditional-fair-lamp assertion is applied.
- `t=1`: exact replay confirms full-state TV `3/4`; this illustrates that triple TV can be a
  strict upper bound.
- `t>=2`: all denominators and walk lengths in (5.1) are positive; this is the exact threshold
  of the combined partial theorem.
- `python3 reproducibility/verify_route_claims.py` passed and exactly reproduced the killed
  counts and V-shaped slice `(26,16,26)`.
- `python3 reproducibility/exact_small_cases.py --triple-max 20 --full-max 12` replayed without
  discrepancy.  These finite checks are used only for interfaces and counterexamples, never
  as the asymptotic proof.

## First unresolved obligation

`O3`: find fixed numerical `C,t_0` with full-state TV at most `C/sqrt(t)` for every
`t>=t_0`.  One exact sufficient version is `O3c`, inequality (6.3).  The written artifacts do
not prove it.  The reflected coupling cannot close it by constant optimization because Route A
proves that coupling's own mismatch has a harmonic logarithmic loss.

## Structured verification output

```json
{
  "verdict": "FATAL_GAP",
  "critical_errors": [],
  "gaps": [
    {
      "location": "candidate_proof.md Section 7 / obligation O3",
      "issue": "The frozen target requires a fixed C/sqrt(t) upper bound, but the strongest proved upper bound contains H_floor(t/2)+1 and is O(log(t)/sqrt(t))."
    },
    {
      "location": "obligation O4",
      "issue": "No independent-agent completion audit or formal verification is available; the target is incomplete before this gate in any event."
    }
  ],
  "repair_hints": "Prove the fixed-constant normalized-range inequality O3c, or construct a direct full-state cancellation/coupling that avoids linear charging of the pre-meeting depth; then obtain an independent audit.",
  "covered_scope": "Literal switch-walk-switch definition; all-zero starts at bases 0 and 2; t=0 exception; t=1 exact check; all integers t>=2 for partial theorem (7.1); translation; parity; conditional lamps; endpoint lower bound; reflected logarithmic upper bound; normalized-range identity and V-shaped counterexample.",
  "residual_risk": "No Lean/formal proof, independent verifier, or literature check was available. Route B returned no artifact. The fixed-constant upper bound is mathematically open within this package."
}
```

## Verification matrix

| Item | Adversarial coordinator audit | Independent audit | Formal verification | Paper re-read |
|---|---|---|---|---|
| `O1` conditional lamps | PASS | unavailable | not run | PASS |
| `O1b` visible hull | PASS | unavailable | not run | PASS |
| `O2` explicit lower bound | PASS | unavailable | not run | PASS |
| `O3p` logarithmic upper | PASS | unavailable | not run | PASS |
| `O3` fixed-constant upper | FATAL_GAP | unavailable | not run | FAIL |
| `O5` partial theorem | PASS | unavailable | not run | PASS |

No `INDEPENDENTLY_AUDITED_PROOF` or `FORMALLY_VERIFIED_PROOF` label is warranted.
