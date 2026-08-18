# Research Ledger: R-20260816T220000Z-densbc-o1p2

Task: Q-20260816-densbc-o1p2-F1A2B3C4

## 2026-08-16 (session, run R-20260816T220000Z-densbc-o1p2)

1. Read upstream artifacts:
   - R-20260816T000000Z-densbc-o1/candidate_proof.md (O1 structure, reduced core O1').
   - R-20260816T210000Z-densbc-o1p/candidate_proof.md (diagonal H_beta + finite
     polynomial constraints closed).
   Decision: choose route (B)-style concrete non-diagonal example, but with a
   banded Gram and an exact finite-rank theorem for the example class.

2. Designed H_lambda:
   - l^2(N_0), x^k = e_k + lambda e_{k+1}, lambda in (-1,1).
   - Gram bandwidth 1; moment map J(w)_k = w_k + lambda w_{k+1}.
   - Verified J is bijective l^2 -> l^2 with inverse
     w_k = sum_{j>=0}(-lambda)^j M_{k+j}; this is strict and written in
     candidate_proof.md.

3. Derived general H_lambda criterion:
   - N is cofinite for finite polynomial representers (bandwidth accounted by
     threshold D = max d_j + 1).
   - Infinite run moment sequences grow linearly, hence are not l^2; finite run
     sequences are finite support and realizable.
   - Therefore V cap Q_sp^perp is isomorphic to ker(T|_{B_fin}).
   Result recorded as Theorem 2 in candidate_proof.md.

4. Worked the concrete representer v_1 = x^4:
   - Computed N exactly for lambda != 0 and lambda = 0.
   - Computed B_fin = {2,3,4,5} (lambda != 0) or {2,4} (lambda = 0).
   - T row on finite runs has a zero column at b = 2, so density fails.
   - Explicit obstruction: t_2 = 1 gives M = delta_2 and
     w = lambda^2 e_0 - lambda e_1 + e_2.
   Result recorded as Theorem 4 in candidate_proof.md.

5. Exploratory computation (EVIDENCE ONLY, not used in proof):
   - Ran a Python search over low-degree polynomial representers in H_lambda
     (lambda = 0.5) trying to find a single representer with at most one finite
     run and a nonzero T entry (which would give density in H_lambda).
   - The search found no candidate in the tried coefficient grids.
   - This is NOT a theorem; it is recorded to avoid repeating the search and to
     keep the failed route visible.

6. Wrote deliverables: problem_contract.md, candidate_proof.md, whiteboard.md,
   research_ledger.md, approach_registry.md, run-manifest.json.

7. Launched fresh-context adversarial audit of candidate_proof.md (subagent
   e15a1ac0-57c3-4133-81df-59ed1d09c1f8).  Audit returned REPAIRABLE_GAP
   (minor): the mathematical argument is sound; one arithmetic typo in the
   p_7 kept-set computation (coefficient 4/3 should be 3/2) and two optional
   explicitness notes.  The p_7 typo was fixed; real-coefficient convention and
   finite-run-below-tail sentence were added.  No change to conclusions.

8. Orchestrator-launched second independent audit (subagent
   c5c51550-d536-4cda-9ed1-dd7ec9b470ad).  Verdict REPAIRABLE_GAP, 0 fatal;
   1 concrete arithmetic error (p_7 coefficient) already fixed by the solver,
   plus 5 small omissions:
   (a) explicit pinned {0,1} handling in Theorem 2 converse;
   (b) injectivity of the obstruction <-> kernel-t map (via density of Pi);
   (c) explicit standing assumption r < infinity, d_j < infinity;
   (d) reword the {0,1} sentence in Theorem 1;
   (e) (p_7 typo, fixed).
   All five were repaired in candidate_proof.md.  Conclusions unchanged:
   H_lambda O1' reduces to ker(T|_{B_fin}) = {0}; v_1 = x^4 is non-dense for
   every lambda in (-1,1) with explicit obstruction
   w = lambda^2 e_0 - lambda e_1 + e_2.
