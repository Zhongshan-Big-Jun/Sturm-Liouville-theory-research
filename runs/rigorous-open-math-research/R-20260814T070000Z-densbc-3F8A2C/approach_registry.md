# Approach Registry

Run: R-20260814T070000Z-densbc-3F8A2C

## Route portfolio

R1. V-generalized moment characterization (tautological master criterion +
    constrained moment form). State: open -> established as STRICT Theorem A/B.
    Owner: solver. Gap: none (it is a restatement + Hahn-Banach/Weierstrass).
    Status: DONE (Theorem A: monomial & sparse versions).

R2. Constraint-restores-density mechanism (packet's key claim).
    State: packet's specific example FALSIFIED (R-001, R-005a); the corrected
    mechanism (all p_n in V + x^2,x^3 in V^\perp) is STRICT (R-006, Theorem D).
    Owner: solver. Status: DONE (with correction).

R3. Diagonal-space complete classification (A5).
    State: packet's proposed criterion ("beta<=3/2 OR constraints force M2=M3=0")
    FALSIFIED via both (a) free params shift (beta>3/2) and (b) finite-run
    phenomenon (beta<=3/2). Corrected criterion established (R-005, Theorem E).
    Owner: solver. Status: DONE (STRICT classification + evidence).

R4. Sufficient criteria on V (first-moment beta<1; jump criterion).
    State: general form established as STRICT Theorem F/G with the finite-low-
    free-param caveat. Owner: solver. Status: DONE (statement-level; see proof).

R5. Boundary-functional side (constraint functionals L_j with expansions killing
    free params). State: reduced to Theorem D hypotheses; general version open.
    Owner: solver. Status: PARTIAL (open core item O1).

R6. Literature. State: deep-reads landed (R-004, R-008, R-009); entire constrained
    problem is open in the classical literature. Owner: lit subagents.
    Status: DONE.

## Corrected diagonal classification (crown result)

H_beta, V={w_i=0 for i in R}, kept sparse family. Dense in V  <->  beta<=3/2
AND R has no finite run.
- finite even run <-> exists constrained even 2q>=4 with 2q-2 not in R;
- finite odd run  <-> exists constrained odd 2q+1>=5 with 2q-1 not in R.

## Failed / superseded ideas
- Packet's claim that span{x^2,x^3}^\perp restores density for all beta:
  FALSE (R-001). The recursion M_{2m}=m M_2 breaks at p_4.
- Proposed criterion "beta<=3/2 OR constraints force M_2=M_3=0": FALSE.
  Free params relocate to M_4 (or the next free base), and finite runs linger.

## Remaining gaps (open core)
- O1 general (non-diagonal) H: the precise "which free low base moments are
  pinned" is governed by the moment-characterization's representability
  (analogue of project O2); no closed form beyond diagonal.
- O2 full constraint-functional expansion criterion (R5 general version).
