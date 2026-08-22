# Obligation graph

Run: R-20260823T000000Z-o1p-baseline

## Root

- O1'-GENERAL: decide closure(span Q_sp)=V for general non-diagonal H.
  Status: OPEN. Exact remaining gap: moment-representability/membership in
  arbitrary H.

## New theorem dependencies

| ID | Statement | Status | Proved by |
| --- | --- | --- | --- |
| N1 | H_shift(m,lambda) satisfies (H1),(H2), J is bounded invertible. | PROVED | Lemma 0.1 |
| N2 | For finite polynomial representers, kept set N is cofinite. | PROVED | Theorem 1.1 |
| N3 | In H_shift, infinite-run moment vectors are not l^2. | PROVED | inside Theorem 2.1 |
| N4 | V cap Q_sp^perp is isomorphic to ker(T|B_fin). | PROVED | Theorem 2.1 |
| N5 | m=1 regression to H_lambda. | PROVED | Theorem 3.1 |
| N6 | lambda=0 regression to H_0. | PROVED | Theorem 3.2 |
| N7 | v_1=x^4 in bandwidth-2 stable family: not dense. | PROVED | Theorem 4.1 |
| N8 | Bandwidth >=2 non-diagonal family criterion. | PROVED | Theorem 2.1 + Theorem 4.1 |
| N9 | Banded-shift family finite-rank decidable. | PROVED | Theorem 2.1 Corollary (Remark 2.2) |
| N10 | Abstract band-invertible structure theorem. | PROVED | Theorem 2.3 |

## Upstream dependencies reused

| ID | Statement | Status | Source |
| --- | --- | --- | --- |
| U1 | closure(span Q_sp)=V iff V cap Q_sp^perp={0}. | PROVED | Theorem A (R-20260814T070000Z) |
| U2 | Run lemma: within a run M_k = (floor(k/2)/floor(b/2)) M_b. | PROVED | R-20260816T000000Z Theorem 3 |
| U3 | H_lambda finite-rank criterion. | PROVED | R-20260816T220000Z |
| U4 | H_beta finite polynomial criterion. | PROVED | R-20260816T210000Z |

## Open/blocked obligations

| ID | Description | Status |
| --- | --- | --- |
| O-B1 | Arbitrary banded Gram, no invertible moment map. | BLOCKED |
| O-B2 | Weighted L^2 / non-Toeplitz H. | OPEN |
| O-B3 | Infinite-degree or non-polynomial representers. | OPEN |
| O-G | Full general O1' moment-problem core. | OPEN |

## Graph edges

- O1'-GENERAL --reduces_to--> O-G --is_special_case--> O-B1/O-B2/O-B3
- O1'-GENERAL --treats subclass--> N4
- N4 depends on N1,N2,N3,U1,U2
- N5 depends on N4,U3
- N6 depends on N4,U4
- N7 depends on N1,U1,N2 (and direct elementary computation)
- N9 depends on N4,N2,N1
