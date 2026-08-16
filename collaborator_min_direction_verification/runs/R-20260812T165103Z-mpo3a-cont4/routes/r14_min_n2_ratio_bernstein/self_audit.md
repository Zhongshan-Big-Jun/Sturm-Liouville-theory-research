# Self-audit: R14 phase-ratio and Bernstein frontier

## Verdict

`PASS_FOR_PARTIAL_RESULT`.

The route proves several new exact lemmas and one half-domain closure, but
does not prove the full general-`mu` interface theorem.  The unresolved
mathematics is isolated as four displayed Bernstein coefficient signs.

## Contract and provenance

- Canonical Blueprint hash was recomputed from `statistics/blueprint.json`:
  `0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799`.
- Inventory hash was recomputed from `statistics/evidence_inventory.csv`:
  `b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`.
- The accepted algebraic starting point is the frozen R11 route.
- No canonical file, evidence inventory, proposal, or sibling route was
  edited.

## Line-by-line sign audit

1. In the `r_A` identity, both denominators are positive on the positive
   phase and `1+cos((mu+1)alpha)>0`; the inequality is strict.
2. In the plus-only lemma, every cancelled factor is positive:
   `A in (0,pi/2)`, `B in (0,A)`, and `k in (0,1)`.
3. The equivalence `g>=1 iff F_+F_->=1` uses the already established
   strict ordering `F_+>F_->0`.
4. In the phase-ratio proof, `V>0`, `zeta>1`, and `V'>0` were checked
   explicitly.  The split `zeta<=mu` / `zeta>mu` is exhaustive.
5. The bound `0<V<Ahat+Bhat` uses strict inequalities
   `|cot theta|<csc theta` and
   `|mu cot(mu theta)|<mu csc(mu theta)`; it remains valid when either
   cotangent is negative.
6. The implication from `g<1` and decreasing `p/x^2` to
   `lambda x_+<x_-` preserves strictness because all factors are positive.
7. The endpoint relation `w_B=r_Bx_-/lambda` is exactly the equality case
   of the physical `B0` constraint.  Since `r_B>1`, it gives `w_B>x_+`.
8. The bridge `J>0` is proved independently of any numerical sample.
9. The implication `D>0 => Enew>0` uses `J>0` and positive
   `delta,p_+,u,w`.  At `r=1`, `delta=0` and `Enew=gKnew w>0`
   directly.
10. The Bernstein product factors and binomial weights were independently
    reconstructed in `exact_checker.py`.

## Counterexample and relaxation audit

- The discarded strengthening
  `g kappa_+ w-delta p_+u^2[x_++(1-g)w]>0` is not used.  It has a strict
  physical counterexample in the thin layer next to `r_B`.
- The cross-only relaxation is not used.  The exact rational no-go in
  `../r13_min_n2_cross_relaxation_no_go/` shows that it admits negative
  `E` and `Enew` values.
- The rational tangent envelope `k<T0<2k/(1-k^2)` is proved, but it is not
  used to assert any of the four open coefficient signs.

## Numerical non-propagation

Discovery searches found positive values for the four coefficient
candidates over large physical samples.  Those searches are omitted from
the proof chain.  They justify only the choice of frontier, not any theorem
statement.

## Exact remaining obligations

The only proposed completion step is to prove

```text
B_1>0, B_2>0, B_3>0, B_4>0
```

as displayed in equation (8.2) of `derivation.md`, on the true common-angle
domain or on a separately proved semialgebraic superdomain containing it.
Until then the route status must remain `RIGOROUS_PARTIAL_RESULT`.

