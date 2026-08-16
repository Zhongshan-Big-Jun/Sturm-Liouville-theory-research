# Research Ledger — R-20260816T120000Z-leftdef-density

Chronological record of work.

## Entry 1 (struct facts, EVIDENCE exact)
Ran reproducibility/ld_struct_facts.py.  Confirmed:
- H^1 moment matrix <x^i,x^k>_1 NON-diagonal (F1).
- All p_n (n in D) satisfy Krein BC => in H^2 (F2).
- x^2, x^3 do NOT satisfy Krein BC => not in H^2 (F3).


## Entry 2 (stronger structural fact)
Checked which monomials are in H^2 via Krein BC: ONLY x^0=1 and x^1=x pass;
x^k for ALL k>=2 fail.  So H^2 ∩ C[x] = span{p_n} (sparse family), and the only
monomials in H^2 are 1, x.  This sharpens the packet's "x^2,x^3 absent" to
"all x^k (k>=2) absent."  (EVIDENCE exact; higher s by H^s ⊂ H^2.)

## Entry 3 (counterexample, exact)
Ran reproducibility/ld_counterexample.py.  For V = ker(Delta) in H^2:
- Q_sp = {p_0} ∪ {even p_{2n}} (even sparse family only).
- q = p_5 - 2 p_7 = -2x^7+4x^5-2x^3 is odd, in V (Delta q = 0), nonzero, in H^2,
  and orthogonal (exact) to every kept even p_n.
- Hence q in V ∩ Q_sp^perp, q != 0 => closure(span Q_sp) != V (DensBC Theorem A).
Decision: first concrete left-definite STRICT non-density instance (Theorem L5).

## Entry 4 (transfer descent)
Formalized Theorem L3: K_c isometry H^t -> H^{t-2} maps constrained density
problem down to H^{s'} (s' in {0,1}); correct moment base is the second-order
jump (free params N_2, N_3), not the DensBC first-order run recursion.
STRICT (proof in candidate_proof.md).

## Entry 5 (whole-space recovery, Q2/Q3)
Theorem L1: V = H^s => density holds for all integer s >= 1; no first
obstruction survives (s=1: M_2,M_3 killed by growth; s>=2: M_2,M_3 undefined).
STRICT.

## Entry 6 (literature sweep)
4 web queries (2026-08-16).  No external exact constrained-density criterion
surfaced; closest: Krein-Sobolev (Axioms 2025), exceptional OPS completeness,
moment-problem char.  Novelty: POTENTIALLY_NEW (not claimed open as a fact).


