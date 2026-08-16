RIGOROUS_PARTIAL_RESULT

# Existing-solver and exact-obstruction inspection

## Exact reflection endpoint identity

The imported full-relay evaluator stores the terminal state as `(0,p,0,r)`
and defines the reflected shooting slope by

```text
q_sharp=|r/p|.
```

The independently evaluated endpoint-energy identity is

```text
p^2-r^2=1-q^2.
```

Therefore, whenever `p!=0`,

```text
q_sharp^2=r^2/p^2=1+(q^2-1)/p^2,
q_sharp=h(q):=sqrt(1+(q^2-1)/p^2).
```

This is exact algebra, not a numerical inference.  Applying reflection twice
gives `h(h(q))=q` on any premise-complete reflected pair.  Consequently, if
the restriction of `h` to equal-norm roots at fixed `(R,n,mu)` is strictly
increasing, no nontrivial reflected two-cycle can exist: if `q<q_sharp`, then
increasing order would give `h(q)<h(q_sharp)`, i.e. `q_sharp<q`, a
contradiction.  This isolates an exact sufficient order lemma; it does not
prove that lemma.

## Earlier numerical artifacts

The accepted-run files inspected were:

- `full_relay_counterexample/full_relay_scan.py`;
- `full_relay_counterexample/common_terminal_branch_scan.py`;
- `asymmetric_common_terminal_scout/scan.py`;
- `finite_contrast_singularity_r7/search.py`;
- `r8_certified_search/search.py` and its audited outputs.

They contain no premise-complete asymmetric or singular minimum candidate.
Earlier fixed-`mu` common-terminal roots were already numerically fixed by
reflection, but their scans did not separately report `h(q)` and the
two-application involution defect.  The present route adds those checks and
separates self-symmetry error from original/partner mirror error.

## Exact relaxed witnesses are not physical candidates

`r11_min_n2_general_mu/derivation.md` contains exact rational tuples with a
wrong split-gap sign on relaxed independent half-angle variables.  Both
tuples fail the same-`mu` common-angle equations

```text
atan(T)=mu atan(t),  atan(S)=mu atan(s).
```

They refute only relaxed algebraic proof strategies and cannot refute the
minimum reflection theorem.  The exact reduction identifies the remaining
physical obstruction as one subtraction in the common-angle quantity
`Phi`; no overlooked physical witness is present.

`r17_min_n2_inner_box_arb_certificate` rigorously signs the four relevant
coefficients only on the compact box `(k,t,y) in [1/64,63/64]^3`.  Its six
boundary collars and their intersections remain open.  This is a genuine
restart region for future certified search, but it does not supply a current
counterexample or a global proof.

## Calibrated status

The endpoint identity and the order-two-cycle reduction are exact.  The
claim that `h` is order preserving on all equal-norm roots remains open and
is comparable to the missing global-order mechanism.  No exact physical
obstruction or candidate counterexample was found in the inspected code.

