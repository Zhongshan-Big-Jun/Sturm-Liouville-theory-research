NUMERICAL_EVIDENCE

# MIN-REFL-C protocol addendum v2

The initial smoke replay exposed two coverage defects in the frozen base
protocol; this addendum is frozen before the full run and explicitly
supersedes only the affected sampling clauses.

1. The complete-root contrast list is the union of the registered 29-point
   geometric `delta_R` grid and

   ```text
   delta_R in {1e-4,1e-2,1e-1,1,9,99,9999,999999}.
   ```

   This preserves the original domain and adds exact anchors shared with the
   fixed-`mu` layer.

2. A coarse fixed-`mu` bracket can straddle an event-count transition even
   when a strict `2n`-event root lies just inside one adjacent chamber.  The
   full run therefore refines every finite sign-changing bracket, records
   whether its endpoint event counts agree, and retains the result only if
   the independently recomputed root passes all strict physical gates.  A
   discontinuous/wrong-chamber Brent output remains rejected evidence.

3. For each strict complete root found in layer 1, the full run adds one
   fixed-`mu` common-terminal task at its exact binary64 `(R,mu)`.  This is a
   held-in consistency/adversarial check of equal-norm multiplicity,
   reflection pairing, `h(h(q))=q`, and order preservation; it is not an
   independent validation sample and is labeled `complete_root_anchor`.

The base tolerances, validity predicates, seeds, epistemic limits, and proof
or certification bridges are unchanged.

