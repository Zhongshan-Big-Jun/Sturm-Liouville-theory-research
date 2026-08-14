# Obligation Graph

Run: R-20260814T070000Z-densbc-3F8A2C

Claims and proof obligations for the candidate proof.

## Dependencies (leaf -> root)

M0 (Hilbert facts) -- Hahn-Banach / orthogonal complement, Weierstrass density
   of Pi in H, Cauchy-Schwarz moment bound.  [assumed standard]

M1 (Theorem A master) = M0.  status: PROVED (textbook; verified).

M2 (Theorem B monomial characterization) = M0 + Theorem A.  status: STRICT/trivial.

M3 (Theorem C sparse characterization) = M0 + Theorem A.  status: STRICT/trivial.

M4 (Theorem D corrected mechanism) = M0 + M1 + recursion arithmetic for the
   sparse family {p_n} (support {n,n-2} for n>=4).  status: STRICT (needs the
   support computation verified -- done in evidence scripts).

M5 (Theorem E diagonal classification) = M0 + M1 + diagonal recursion-graph
   decomposition (Lemma 4.1) + series convergence/divergence analysis. 
   status: STRICT, evidence-backed (scripts v1,v2,v3,v4,v5).

M6 (Theorem F first-moment on V) = M0 + M1 + Cauchy-Schwarz growth argument.
   status: STRICT (statement; proof complete in candidate_proof.md).

M7 (Theorem G jump on V) = M0 + M1 + project growth-lemma (cited as a theorem,
   re-derived in the project tool; treated as accepted premise here).
   status: STRICT conditional on the growth lemma.

M8 (Theorem H boundary-functional interpretation) = Theorem A + D.  status: STRICT.

## Refuted claims (recorded)

F1 (packet: span{x^2,x^3}^\perp dense for every beta) -- REFUTED for beta>3/2.
   Counterexample: nonzero w with free M_4, M_5, orthogonal to all kept p_n.
F2 (proposed criterion beta<=3/2 OR constraints force M2=M3=0) -- REFUTED.
   Free params relocate to M_4,M_5; finite runs destroy density at beta<=3/2.

## Open obligations (open core)
O1 general non-diagonal H: exact finite-low-moment survival criterion (no
   closed form beyond diagonal).
O2 general L_j expansion criterion for density for all beta in non-coordinate H.
O3 fractional left-definite window, inherited.

## Verification status
- Theorem E is the crown result; its two non-density directions and one density
  direction are each stated and proven in candidate_proof.md and numerically
  corroborated.  Independent adversarial audit dispatched.
