RIGOROUS_PARTIAL_RESULT

# Result

## Exact theorem proved

For the literal discrete-time switch-walk-switch chain in the frozen task, with both initial
lamp configurations all zero and bases at zero and two, respectively, the following holds for
every integer `t>=2`.  With `H_N=sum_{k=1}^N 1/k`,

```text
1/(4 sqrt(t))
<= ||P_t^(0,0)-P_t^(0,2)||_TV
<= 1/sqrt(floor(t/2)+1)
   + 2 H_(floor(t/2)+1)/sqrt(ceil(t/2)+1)
<= sqrt(2)[3+2 log(t+1)]/sqrt(t).
```

The lower bound has the requested fixed `t^{-1/2}` scale.  The proved upper bound has an
extra logarithmic factor.  Therefore the frozen target is not completed.

## Proof summary

1. Conditional on any positive-length base path, every visited site has a distinct last
   independent fair resampling bit, while every unvisited lamp remains at its forced initial
   zero.  The visited set is the interval between the walk's extrema.
2. Spatial translation by two sends the law from `(0,0)` to the law from `(0,2)` and preserves
   the common endpoint parity.
3. Projection to the endpoint reduces the lower bound to TV between a binomial mass function
   and its unit shift.  Unimodal telescoping and a self-contained Markov/Chebyshev bound give
   `1/(4sqrt(t))` for all `t>=1`.
4. Reflect the two base walks about site one until they meet, then coalesce them.  If the common
   tail covers both pre-meeting extremes, their endpoint/range triples agree and their final
   lamps can be coupled identically.  Reflection gives the tail survival estimate; the exact
   pre-meeting depth law `Pr(D>=d)=1/(d+1)` produces the harmonic factor in the displayed upper
   bound.
5. Exact normalized-range counts yield formula (6.2).  The simple unimodality route to the
   fixed-constant estimate is false: at `t=10,r=4,j=2` the accessible slice is `(26,16,26)`.

The full argument is in `candidate_proof.md`.

## Verification performed

- Route A and C artifacts matched their reported sha256 hashes before ingestion.
- Route B produced no file and contributed no claim.
- The candidate proof received a line-by-line adversarial coordinator audit covering the
  definition, logic, boundary cases, constants, parity, and conditional-lamp interface.
- Exact computation reproduced the Route C V-shaped counterexample and `t=1` full-state TV
  `3/4`, and enumerated full states through `t=12`.
- A fresh-context check rebuilt the state from files only and found structural convergence but
  a quantitative stall at `O3`.
- No independent-agent audit or formal proof is claimed.

## Remaining gaps

The first unresolved load-bearing obligation is `O3`: prove an explicit fixed-constant
`C/sqrt(t)` upper bound for the full state law.  One sufficient exact obligation is

```text
sum_{r=0}^t sum_{j=0}^r sum_{a in Z}
  |h_t^r(a,j)-h_t^r(a+2,j)|
<= 2 C_* 2^t/sqrt(t)
```

for fixed explicit `C_*` and all sufficiently large integer `t`.  No written artifact proves
this.  A direct full-state comparison could instead bypass the sufficient range-triple bound.

## Failed and blocked routes

- The reflected/coalescing route is PARTIAL.  Route A proves that this coupling's mismatch
  itself has order at least `log(t)/sqrt(t)` along its explicit bound, so constant optimization
  of the same mechanism cannot close `O3`.  This is not a TV lower bound.
- Naive parity-class unimodality of normalized range counts is REFUTED by `(26,16,26)`.
- Route B is an INCOMPLETE_RETURN: no artifact exists, it was not retried, and its analytic
  mechanism is neither accepted nor refuted.

## Novelty status

`UNKNOWN`.  This was a blind, internet-free run.  No literature, openness, or novelty claim is
made, and no external theorem is used as a premise.

## Human, model, and tool contributions

- Human: frozen task, blind restrictions, and stopping-boundary instructions.
- Coordinator: contract, reductions, lower bound, visible-hull lemma, synthesis, audit, and
  final stopping package.
- Route A worker: reflected coupling theorem and coupling-specific harmonic obstruction.
- Route C worker: exact state/range formulas, alternative logarithmic estimate, and the
  V-shaped counterexample.
- Route B worker: incomplete return; no ingested mathematics.
- Tools: exact integer Python enumeration and sha256 verification; no network or randomness.

## Reproducibility manifest

See `repro_manifest.md` and `artifact_hashes.sha256`.  Primary replay commands:

```text
python3 reproducibility/verify_route_claims.py
python3 reproducibility/exact_small_cases.py --triple-max 80 --full-max 12
```

## Confidence by axis

- **Semantic fidelity:** high; literal chain, all-zero starts, parity, and `t=0` were audited.
- **Mathematical correctness of partial theorem:** high under the coordinator audit; not
  independently or formally verified.
- **Completeness for frozen target:** low/absent; `O3` is explicitly open.
- **Novelty:** unknown by blind restriction.
- **Reproducibility:** high for hashes and finite checks; paper proof remains informal.

## Transaction and research status

- `research_status: partial_progress`.
- `transaction_status: local stopping package written`; no canonical knowledge base or merge
  transaction exists.
