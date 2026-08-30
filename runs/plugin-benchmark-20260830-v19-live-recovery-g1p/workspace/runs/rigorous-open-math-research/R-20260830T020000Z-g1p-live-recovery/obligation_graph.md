# Obligation graph

## Shortest dependency chain

```text
A-NEAR + A-CONT + KP-DET + KO-DET
	=> KP-NEG + KO-NEG
	=> KP-TRACE + KP-DET + KO-TRACE + KO-DET
	=> ROOT.
```

The first open load-bearing claim is `KP-DET`. The trace claims are not independent load-bearing nodes after the inertia bridge.

## Nodes

### ROOT

- Statement: For every finite `R>1` on the prescribed `n=2` symmetric INF branch, `Kp_odd(R)` and `Ko(R)` are negative definite.
- Quantifiers: Every finite `R>1` on that branch.
- Depends on: `KP-NEG`, `KO-NEG`.
- Evidence/status: `OPEN`.
- Proof or citation: None.
- Known edge cases: Strict near-one and sufficiently large finite `R` are closed.
- Verifier notes: Does not imply global `G1'`.

### A-CONT

- Statement: The prescribed finite-interior sector matrices form continuous real symmetric paths in `R` on the branch.
- Quantifiers: Every finite-interior branch chart in the target.
- Depends on: Exact transfer-matrix and simple-spectrum construction.
- Evidence/status: `PROVED` within the branch contract.
- Proof or citation: Frozen local proof and exact half-problem construction.
- Known edge cases: Branch collision or chart termination is outside the sign contract.
- Verifier notes: Global branch existence is a contract input, not re-proved here.

### A-NEAR

- Statement: There is `delta>0` such that both sector matrices are negative definite for `1<R<1+delta`.
- Quantifiers: The prescribed INF branch.
- Depends on: Constant-string zero simplicity and rescaled matrix limit.
- Evidence/status: `PROVED`.
- Proof or citation: Frozen addendum `2026-08-13e`, Section 2.
- Known edge cases: `R=1` itself is excluded.
- Verifier notes: Exact strict anchor.

### A-LARGE

- Statement: There is finite `R_infty` such that both sector matrices are negative definite for `R>R_infty` on the accepted large-`R` INF chart.
- Quantifiers: Sufficiently large finite `R`.
- Depends on: Accepted exact asymptotics.
- Evidence/status: `PROVED`.
- Proof or citation: `observable_determinant_refutation.md`.
- Known edge cases: It does not bridge the middle regime.
- Verifier notes: For `Kp_odd`, the first and second diagonal entries are negative to leading order and the determinant is positive. For `Ko`, the leading trace is negative and the determinant is positive.

### KP-DET

- Statement: `det Kp_odd(R)>0` for every finite `R>1` on the branch.
- Quantifiers: Every finite `R>1`.
- Depends on: `A-CONT`, `A-NEAR`, `A-LARGE`, and exclusion of `KP-FIRSTZERO`.
- Evidence/status: `OPEN`.
- Proof or citation: Endpoint anchors only.
- Known edge cases: Any failure lies in a compact middle interval.
- Verifier notes: Earliest open load-bearing claim.

### KP-FIRSTZERO

- Statement: No compact-middle first-loss point `R_*` admits `det Kp_odd(R_*)=0` with `Kp_odd(R)` negative definite immediately to its left.
- Quantifiers: Every candidate first-loss point.
- Depends on: Exclusion of the exact Green-kernel null-vector equation in `direct_attempt.md`, including the possible double-zero case.
- Evidence/status: `OPEN`.
- Proof or citation: Exact reduction in this run.
- Known edge cases: A corank-one kernel and the exceptional zero-matrix case must both be treated.
- Verifier notes: Numerical survival is irrelevant to this node.

### KO-DET

- Statement: `det Ko(R)>0` for every finite `R>1` on the branch.
- Quantifiers: Every finite `R>1`.
- Depends on: The analogous first-zero exclusion for `Ko`.
- Evidence/status: `OPEN`.
- Proof or citation: Endpoint anchors only.
- Known edge cases: Any failure lies in a compact middle interval.
- Verifier notes: It is second in the closure order after `KP-DET`.

### KP-NEG

- Statement: `Kp_odd(R)` is negative definite for every finite `R>1`.
- Quantifiers: Every finite `R>1`.
- Depends on: `A-CONT`, `A-NEAR`, `KP-DET`, `INERTIA`.
- Evidence/status: `BLOCKED` by `KP-DET`.
- Proof or citation: Inertia bridge in `direct_attempt.md`.
- Known edge cases: None within the branch contract.
- Verifier notes: Once `KP-DET` closes, `trace Kp_odd<0` follows.

### KO-NEG

- Statement: `Ko(R)` is negative definite for every finite `R>1`.
- Quantifiers: Every finite `R>1`.
- Depends on: `A-CONT`, `A-NEAR`, `KO-DET`, `INERTIA`.
- Evidence/status: `BLOCKED` by `KO-DET`.
- Proof or citation: Inertia bridge in `direct_attempt.md`.
- Known edge cases: None within the branch contract.
- Verifier notes: Once `KO-DET` closes, `trace Ko<0` follows.

### INERTIA

- Statement: A continuous symmetric matrix path that starts negative definite and never has zero determinant remains negative definite.
- Quantifiers: Any connected parameter interval.
- Depends on: Continuity of ordered eigenvalues.
- Evidence/status: `PROVED`.
- Proof or citation: `direct_attempt.md`.
- Known edge cases: The determinant must be strictly positive, not merely nonnegative.
- Verifier notes: This closes both trace nodes once the determinants close.
