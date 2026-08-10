# Obligation graph

Run: R-20260806T011500Z-keylemma-E58FB1
Status label: RIGOROUS_PARTIAL_RESULT (see status_and_literature.md, candidate_proof.md)
Legend: DONE = proven analytically; VERIFIED = verified numerically (evidence, not proof);
OPEN = unresolved; SUPERSEDED = attempted and replaced; PARTIAL = reduced.

## Contract-level obligations

- C0  Normalize the exact statement of the KEY LEMMA (log form and F-prime form) and audit the source.  [DONE: problem_contract.md, finding C1]
- C1  Prove the log form: (d/dc)log(M1/M2) < 0 on (1,inf)x(0,1/2), i.e. G2 - G1 > 0.  [PARTIAL: reduced to R1, R2, L4box + bases]
- C2  Prove the F-prime form: F~(c) = M~1 G1 - M~2 G2 < 0 on (1,inf)x(0,1/2).  [PARTIAL: reduced to R1, R2, L5box + bases]
- C3  Audit every premise against the source.  [DONE: P1-P10, verify_premises.py]
- C4  Adversarial audit of the candidate proof.  [DONE: audit_report.md, verdict REPAIRABLE_GAP]

## Premise obligations (source Section 2, rechecked)

- P1  Even and odd secular equations, corrected odd form.  [DONE: P1]
- P2  Ranges and ordering: a1 in (0,pi/2), a2 in (0,pi), corners alpha0.  [DONE: P2]
- P3  Normalization identity u_k^2 = tan^2(a_k)/(1/2 + w tan^2 a_k).  [DONE: P3]
- P4  f_sym = (2/u^2)(T1 - T2).  [DONE: P4]
- P5  D'(c) = (8/q^2)(c+q) F(c).  [DONE: P5]
- P6  G is the log-derivative of M~ along either curve.  [DONE: P6]
- P7  f_sym = 2(c+q) F/(q u^2 (q^2-1)).  [DONE: P7]
- P8  (d/dc)log(M1/M2) = G1 - G2.  [DONE: P8]
- P9a F~' = M~1 G1 - M~2 G2.  [DONE: P9a; one finite-difference tolerance flag at (10, 0.05), artifact]
- P10 Positive margins of both target forms on samples.  [DONE: P10]

## Proof obligations

### Proved analytically
- L1  G1 < 0 on (1,inf)x(0,1/2).  [DONE: candidate_proof.md 2.1]
- L2  If G2 >= 0 then both C1 and C2 hold.  [DONE: candidate_proof.md 2.2]
- B1  q=1 base: J1(1,c) >= 0 on (0,1/2).  [DONE: N1(u) > 0 on (pi/3, pi/2)]
- B2  q=1 base: J2(1,c) <= 0 on [0.4,0.5].  [DONE: N2(w) < 0 on [2pi/3, 5pi/7]]
- B3  q=1 base: H'(1,c) < 0 on (0,1/2).  [DONE: T decreasing on (0,pi)]
- B4  F~(q,1/2) < 0 for all q > 1.  [DONE: exact closed form, P(x) > 0]
- B5  H(q,1/2) = 2 pi q (q+1)/(2q+1)^(3/2) > 0, increasing in q.  [DONE: exact]
- B7  G2(c;1) > 0 for c in (0,0.4].  [DONE: W(5 pi/7) < 0]

### Verified numerically (evidence, proof open)
- R1  G2 >= 0 for q >= 2, c in (0,1/2).  [VERIFIED: min 0.069181 at (2, 1/2); OPEN]
- R2  G2 >= 0 for q > 1, c in (0,0.4].  [VERIFIED: min 0.415004 at (1+, 0.4); OPEN]
- L4box  H' < 0 on (1,2]x[0.4,0.5].  [VERIFIED: max -7.7317; OPEN]
- L5box  F~'' = M~1 J1 - M~2 J2 > 0 on (1,2]x[0.4,0.5].  [VERIFIED: min 14.167; OPEN]
- B6  G2(c;2) >= 0 on (0,1/2).  [VERIFIED: min 0.069181 at c=1/2; OPEN; auxiliary]
- Q1  dG2/dq >= 0 on (1,inf)x(0,1/2).  [VERIFIED: min ~5e-4 (decays to 0); OPEN; linchpin for R1/R2]

### Superseded
- R3  G2(q,c) >= G2(q,1/2) monotonicity: SUPERSEDED (numerically false for large q; C4).
- R4  dJ1/dq >= 0 on (1,2]x[0.4,0.5]: SUPERSEDED by L5box (direct box check; margins verified 4.87 but not needed).
- R5  dJ2/dq <= 0 on (1,2]x[0.4,0.5]: SUPERSEDED by L5box.
- R6  dH'/dq <= 0 on (1,2]x[0.4,0.5]: SUPERSEDED by L4box.

## Dependency structure

- C1 (LOG)  <=  [Region A via L1,L2]  +  [Region B: L4box, R1, R2, B5].
- C2 (FP)   <=  [Region A via L1,L2]  +  [Region B: L5box, R1, R2, B4].
- Region B contained in (1,2)x(0.4,0.5)  <=  R1, R2.
- R2 <= Q1 + B7.   R1 <= Q1 + B6 (future route; B7 proved, B6 verified).
- T4 (source) <= C2 (FP);  the source's "equivalence" between (LOG) and (FP) is false
  (C1) but T4 only needs (FP), which is proved by the same chain.

## Verified numerical evidence (not proofs)

- H >= 2.4184 on the whole domain; min at the corner (q->1+, c->1/2-).
- -F~' >= 0.4253 on the bounded sampled range (q <= 100); min near (q~3.12, c~0.5).  For large q, -F~' shrinks toward 0 (M~ -> 0); the proof there uses R1 + L1 + L2 (region A), not the margin.
- Region B margins: |G1|/|G2| >= 7.42, M~2/M~1 <= 6.94, |G1|-|G2| >= 2.418,
  F~'' >= 14.7, H' <= -7.1.
- Corner asymptotics: G2(1/2;q) ~ (pi/sqrt 2) sqrt q -> +inf; G2(c;q) -> 4 pi/sin(2 pi c)
  for fixed c < 1/2 as q -> inf.
