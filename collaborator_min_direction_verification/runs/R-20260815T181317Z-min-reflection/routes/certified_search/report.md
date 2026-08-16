NUMERICAL_EVIDENCE

# MIN-REFL-C bounded counterexample and singular-root search

## Result

The final v2 run found no premise-complete asymmetric minimum-side point and
no floating singular-root candidate.  This is bounded numerical evidence,
not a proof of global reflection symmetry.

The complete-root layer used 1,584 deterministic starts at 33 contrasts with
`delta_R=R-1` between `1e-6` and `1e8`.  It retained 31 strict binary64 root
records.  At `R=1001`, `3163.2776601683795`, `10000`, and `10001`, poor
conditioning made one root appear as several nearby binary records.  All 12
records in those four apparent-multiplicity cases were refined at 100 decimal
digits and collapsed to one root per contrast.  Thus the sampled contrasts
contain 23 reconciled roots, with zero unresolved binary multiple-root cases.

Every retained complete record passed:

- the `n`th and `(n+1)`st terminal zero indices and equal terminal time;
- exactly `2n` strict events;
- the alternating minimum law, starting with material `R`;
- positivity, cell-separation, switch-residual, and transversality gates;
- terminal position, energy, endpoint-energy, and capped/uncapped evaluator
  checks;
- the equal-norm residual.

No retained complete record met the asymmetric-witness predicate.  The
smallest absolute normalized complete-root Jacobian determinant on the
sampled roots was `1.8628467253614767e-4`.

The direct three-equation singular scout used 160 deterministic starts in

```text
log(R-1) in [log(1e-5),log(1e7)],
a in [-10,10],
log(q-1) in [log(1e-7),log(1e5)].
```

It retained zero candidates.  Its closest optimizer output was not a root:

```text
R = 11605.09535619743,
mu = 1.0075243989488771,
q = 1.0009520760696344,
(A,C,normalized_det) =
  (1.736965981696814e-5,
  -1.7644175044516367e-5,
  -4.6374417243092407e-4).
```

This is far outside the registered root and singularity thresholds and lies
near the negative `a` boundary; it is only a near miss.

## Fixed-frequency reflection and order audit

The `n=2` fixed-`mu` layer evaluated 127 problems.  It attempted 38,100 base
samples, of which 24,639 returned finite indexed residuals, and retained 39
strict common-terminal roots after 77 even-contact trials:

- 8 roots came from the preregistered `mu` fractions;
- 31 came from exact complete-root anchor slices and were equal-norm roots at
  tolerance `5e-8`.

Every fixed `(R,n,mu)` problem contained at most one retained `q` root.  Hence
there was no same-parameter pair of distinct equal-norm roots, no observed
violation of order preservation, and no nontrivial `q <-> q_sharp` pair.  All
39 roots matched themselves under the independently evaluated reflection
map.

The held-out expansion used 64 problems for `n in {3,4}` and
`R in {1.01,2,100,1e4}`.  Of 11,520 attempted base samples, 5,438 were finite;
11 strict common-terminal roots were retained (`5` for `n=3`, `6` for
`n=4`).  Again, every problem had at most one root and every retained root was
reflection fixed to the recorded precision.

## Reflection involution diagnostics

Across all binary64 retained records, the worst diagnostics were

```text
relative |q_sharp-q|                         1.1248172239424525e-10
normalized self-switch reflection defect     1.0237370506871457e-8
|h(h(q))-q|                                  5.594102958639269e-10
partner mirror defect                        1.0194720452272321e-6
```

The largest binary partner defect occurred in the ill-conditioned
high-contrast cluster.  The 100-digit replay of all 12 conditioning-trigger
records gave the stronger maxima

```text
complete terminal-gap residual               2.4903213232130518e-84
complete log-norm residual                    5.096041703378822e-82
|q_sharp-q|                                  1.5002841908785776e-69
|q_sharp-h(q)|                               2.8574684782056875e-101
|h(h(q))-q|                                  7.895826336244900e-69
normalized self-switch reflection defect     2.3185797973613931e-67
normalized partner mirror defect             2.3090297524335162e-65
partner terminal-gap residual                2.4736323379422836e-69
partner log-norm residual                     2.4232815947992902e-67
```

These are mpmath decimal calculations, not outward-rounded interval
certificates.

## Smoke run versus final v2 run

The initial smoke protocol used 84 complete-root starts at 7 contrasts, 16
singular starts, and 15 fixed-`mu` problems.  It retained 5 complete roots,
no singular candidate, and no common-terminal root.  Inspection showed that
the last zero was a sampling defect: a coarse sign bracket can cross an
event-count transition while a strict physical root lies inside the adjacent
chamber.  That smoke output was deliberately overwritten and is not a frozen
evidence artifact.

`computation_contract_addendum_v2.md` froze the correction before the final
run.  Cross-event-count brackets were allowed only for refinement; every
output still had to pass all root-level physical predicates.  The final v2
run described above is the immutable evidential result.

## Exact audit observation from existing code

At a common terminal point, the endpoint energy identity gives

```text
p^2-r^2=1-q^2,
q_sharp=|r/p|=sqrt(1+(q^2-1)/p^2)=h(q).
```

Reflection equivariance then makes a non-fixed reflected pair a two-cycle of
`h`.  If `h` were proved order preserving on the premise-complete equal-norm
root set, a nontrivial two-cycle would be impossible.  The search explicitly
tested this bridge but did not prove the missing order theorem.  Details and
the audit of earlier nonphysical relaxed witnesses are in
`source_inspection.md`.

## Blind spots and calibrated conclusion

The search did not retain a root at `R=1.000001` or at sampled contrasts
`R>=31623.7766`; this is a coordinate/conditioning and finite-multistart blind
spot, not evidence of nonexistence.  The finite grids can also miss
disconnected or narrow chambers, roots outside the coordinate boxes,
tangencies above the contact threshold, and near-grazing event words.  The
imported evaluators can share an implementation defect.

Accordingly, this route stops with `NUMERICAL_EVIDENCE`.  Refutation still
requires an outward-rounded interval enclosure of one asymmetric root and
all its premises.  Proof still requires an exact order/invariant theorem or
a complete interval subdivision.

Exact domains, seeds, tolerances, versions, root records, rejected near
misses, and high-precision replay data are in `results.json`.  Final hashes
are in `artifact_manifest.json`; `audit.json` checks the frozen result.

