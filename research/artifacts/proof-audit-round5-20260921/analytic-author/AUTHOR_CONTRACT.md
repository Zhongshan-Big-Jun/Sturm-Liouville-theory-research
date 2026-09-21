# Round 5 analytic author contract

Role: mathematical proof author only. This submission will require a separate fresh independent review. No review or approval is asserted here.

User task: start from c0b36b90004cffb0552c9fa9f229e1f7cec8a706, verify the supplied fifth-round audit and replacement proof as claims, and write a standalone Chinese ctexart proof with English punctuation for fixed c > 0 on the complex second left-definite space H_c^2 = D(K_c), with Krein boundary conditions.

Authorized writes are limited to the new repository file `/mnt/f/LaTeX/BVE research/docs/SL_cofinite_left_definite.tex` and this external directory. Existing project documents, cards, indexes, AGENTS, canonical content, history, and Git are not author edit targets. No agents are spawned. The specific user scope overrides the generic AGENTS maintenance rule. Six read inputs are frozen with byte counts and SHA256 in `source_manifest.json`.

Required mathematical contract:

1. Distinguish D(K_c) from ordinary Sobolev H^2 and from s = 3 or general O1'LD. All spans and subspaces are over C; L^2 inner products are linear in their first argument.
2. Prove energy positivity, equivalence of the left-definite and Sobolev norms on D(K_c), and an isometric surjection onto L^2. The intended surjectivity proof solves the inhomogeneous ODE and explicitly inverts a two by two endpoint matrix.
3. Verify the two explicit Green representers, including endpoint cancellation, one-sided interface data, and conjugation. Give M_0 = 1/c as an all-index counterexample to original Claim 4. Identify original Claim 4, Theorem 5, and Corollary 6 as REFUTED candidates, without reclassifying accepted H2/H3 results.
4. Prove the cofinite closure theorem for every cofinite subset of the admissible indices. Its proof must include tail polynomial equality, local zero-trace cutoff estimates, Sobolev polynomial approximation, and endpoint residual correction. Finite computations are supplementary only.
5. Classify closed subspaces with an actual cofinite retained family via S in C^2, and state the exact density condition. Include the noncoordinate line f(0) = f'(0).
6. Repair finite deletion of monomials by multiplying the annihilator by x^M; derive the odd change-of-variable norm factor 1.
7. User steering during authoring: explicitly prove that both sufficiently high parity recurrences characterize exactly span{g_0,c, g_1,c}, verify the first-linear normalizations <g_0,c,1> = <g_1,c,x> = 1/c with zero cross moments, and derive g = c M_0 g_0,c + c M_1 g_1,c. Adding M_0 = M_1 = 0 then recovers rigidity. Keep this within s = 2 and the tail/cofinite setting.

Nonclaims: independent acceptance, general O1'LD, s = 3 classification, c = 0 or uniform c -> 0 bounds, a full repository audit, historical certificate reruns, and full real-analysis Lean verification.

Author workflow: reason from source statements, build a complete analytic proof, use separately implemented algebraic/numerical probes on fragile identities and estimates, compile only an external source copy if a suitable engine is available, then freeze the source hash and report actual checks and unresolved scope. Stop after author submission.
