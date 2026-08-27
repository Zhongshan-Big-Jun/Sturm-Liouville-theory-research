RIGOROUS_PARTIAL_RESULT

# Post-scoring independent adversarial audit

## Status and verdict separation

This review is posthoc and is excluded from the scored arm metrics. I did not author the
reviewed package, and I did not modify any file in the scored arm.

- Overall package-audit verdict: `PASS`.
- Retained partial theorem `O5`: `PASS`.
- Frozen target completion verdict: `FAIL`.
- Frozen target truth status: `OPEN_IN_THIS_PACKAGE`, not refuted.

The completion verdict is `FAIL` only because the package does not prove the required fixed
`C/sqrt(t)` full-state upper bound. It is not a finding that the target theorem is false. The
package states this limitation consistently and does not promote its logarithmic upper bound
to the frozen target.

## Hash binding

Before reading the mathematical proof, I verified that `candidate_proof.md` has exactly the
required SHA256:

`40359f326aec9c01ecc0fa73c43bac72ffca74b1bea2e847f0bed1a601b812e9`.

The complete reviewed-file binding is:

| Reviewed file | SHA256 |
|---|---|
| `problem_contract.md` | `976cffb63e8e20d1395f0abff0f3735b7ba538b188b420772c22df80df46ed23` |
| `candidate_proof.md` | `40359f326aec9c01ecc0fa73c43bac72ffca74b1bea2e847f0bed1a601b812e9` |
| `final_report.md` | `0c3d848d65ff4637192a086fed8ba4a92e85ce62f7aba9afff82d9626e24d17d` |
| `audit_report.md` | `be9cabc4b2a82eac0db979c847a62ba3a240d061147707a213949a92415a1209` |
| `convergence_check.md` | `4cb871fe661375175c27f540065ea16814e2331b59a86d572042115da1bdafae` |
| `obligation_graph.md` | `e4fb3e040a2d9dbf02e72cec560b288f916938e39cd5ca3ae6cb2d28446afc5e` |
| `subagents/route_a.md` | `6ce207738f66fcd3b0b5b2c39175cf068be15f8b8532b76593e11b5cd386b647` |
| `subagents/route_c.md` | `f260fe18d316ad8d58294700ad4bb3cd40514537728a7ac67ae576c19ca7bbf2` |
| `reproducibility/verify_route_claims.py` | `3e381b7db80c16474b429df2a656081560436c95530b4d067f209f2610924216` |

For an additional compact binding, concatenate the nine lines
`relative_path`, one ASCII space, `sha256`, and LF, in the table order. The SHA256 of those
UTF-8 bytes is:

`4aeb57d35f3fa881ac3468ba1d5501a44c35c5be82ee9e4ba6280205b15c81c8`.

Only the nine listed frozen inputs and fresh local calculations were used. No internet,
literature, prior answer, or unlisted project artifact was used as mathematical evidence.

## Independent obligation audit

### `O1`: conditional lamp law

Verdict: `PASS`.

For every base path of length `t>=1`, the initial vertex is resampled by the departure switch
of step one and every subsequently visited vertex is resampled on arrival. A nearest-neighbour
path visits exactly every integer between its minimum and maximum. Selecting the
chronologically last resampling variable at each visited site selects distinct variables from
the independent fair switch family. Therefore the final lamps are mutually independent fair
bits on `[L_t,U_t]` and are the forced initial zero outside it. Every path with the same
`(L_t,U_t,S_t)` induces the same lamp kernel, so the assertion remains valid after conditioning
only on that triple.

The proof correctly excludes `t=0`, when no resampling occurs.

### `O1b`: visible-hull TV equality

Verdict: `PASS`.

For `t>=1`, formula (3.1) correctly sums over every exact base range containing the start,
endpoint, and support of the final lamp configuration. A specified zero-one pattern on a
range `[l,u]` has conditional probability `2^{-(u-l+1)}`. Consequently, for each fixed start,
the point-mass function is constant on every fiber of

`V(eta,z)=(min(supp(eta) union {z}),max(supp(eta) union {z}),z)`.

Every such fiber is finite. If it has size `n_v` and the two constant likelihoods are
`a_v,b_v`, its full `l1` contribution `n_v|a_v-b_v|` equals the pushforward contribution
`|n_va_v-n_vb_v|`. Thus formula (3.2) is an equality, not merely a data-processing bound. Its
stated quantifier, every integer `t>=1` for the two specified starts, is correct.

### `O2`: explicit lower bound

Verdict: `PASS`.

At a common endpoint, the two endpoint masses are `p_k` and `p_(k-1)`, where
`p_k=2^{-t} binom(t,k)` and the sequence is extended by zero at both ends. The total discrete
variation of this unimodal sequence is exactly twice its maximum, including the two-point
plateau when `t` is odd. Hence endpoint TV is `max_k p_k`.

For `K` distributed as `Binomial(t,1/2)`, the written variance computation and Markov
inequality give probability at least `3/4` to `|K-t/2|<sqrt(t)`. That interval contains at
most `2sqrt(t)+1<=3sqrt(t)` integers for every `t>=1`. Therefore

`TV(P_t^(0,0),P_t^(0,2)) >= 1/(4sqrt(t))`

for every integer `t>=1`. The projection direction is correct and the numerical constant
`c=1/4` is uniform.

### `O3p`: explicit logarithmic-loss upper bound

Verdict: `PASS`.

The half-open reflection identity

`Pr(M_m<a)=Pr(-a<=R_m<a)`

has the correct endpoints and contains exactly `a` sites of the accessible parity. The
central-binomial induction gives the claimed atom upper bound `1/sqrt(m+1)`, and therefore the
one-sided survival bound `a/sqrt(m+1)`.

In the reflected/coalescing coupling, the second walk has independent fair increments because
each next increment is a past-measurable sign times a fresh fair sign. Before meeting at site
one, the two visited intervals are exactly `[-D,1]` and `[1,D+2]`. After meeting, a common tail
that visits both old extremes makes the endpoint-range triples equal, after which the common
conditional lamp kernel couples the complete states.

The exact gambler-depth law is `Pr(D>=d)=1/(d+1)`. On `tau<=N`, the truncation `D<=N` gives

`E[(D+1)1_(tau<=N)]<=H_(N+1)`.

With `n=floor(t/2)`, the remaining tail length satisfies `m>=t-n`. The two one-sided survival
bounds and a union bound therefore yield, for every integer `t>=2`,

`TV <= 1/sqrt(n+1)+2H_(n+1)/sqrt(t-n+1)`.

Since `t-n=ceil(t/2)`, this is exactly the denominator stated in the final report and `O5`.
The inequalities `H_N<=1+log N`, `n+1>=t/2`, `t-n+1>=t/2`, and `n+1<=t+1` give the displayed
`sqrt(2)[3+2log(t+1)]/sqrt(t)` bound with no hidden dependence in the constant.

The reflection and meeting times preserve endpoint parity because both starts are even and
both walks meet at the odd site one at an admissible odd time.

### `O5`: strongest retained partial theorem

Verdict: `PASS`.

Combining `O2` and `O3p` proves exactly, for every integer `t>=2`,

`1/(4sqrt(t)) <= TV <= 1/sqrt(floor(t/2)+1)`

`+ 2H_(floor(t/2)+1)/sqrt(ceil(t/2)+1)`.

All denominators are positive at the threshold, and the two modules have compatible chain
definitions, starts, parity conventions, and time quantifiers.

## Formula and route cross-checks

- The normalized-range definition in (6.1) correctly sends an actual interval `[l,u]` to
  `r=u-l`, start coordinate `a=-l`, and endpoint coordinate `j=z-l`.
- Translation of the start from zero to two changes only `a` to `a+2`. Therefore the factor
  and all three sums in (6.2) are correct: the triple TV is
  `2^{-t-1} sum|h(a,j)-h(a+2,j)|`.
- A common triple-to-lamp Markov kernel proves full-state TV is at most triple TV. This is
  correctly distinguished from the stronger visible-hull equality.
- Inequality (6.3) is sufficient for the fixed-constant upper bound but is not proved or
  claimed necessary.
- The killed-walk inclusion-exclusion gives exactly `(26,16,26)` for
  `(t,r,j)=(10,4,2)`. This refutes parity-class unimodality and only that shortcut.
- Route A's lower estimate for the reflected coupling mismatch is correctly restricted to
  that coupling. It is never asserted to be a lower bound for total variation.

## Reproducibility checks

The authorized replay command

`py -3 reproducibility/verify_route_claims.py`

returned:

- `PASS route-C V-slice: (26,16,26) with listed killed-count terms`;
- `PASS literal t=1 full-state TV: 3/4`.

Fresh exact dynamic programs, passed through standard input without writing author files,
also verified:

- visible-hull TV equals full-state TV for every `0<=t<=10`;
- endpoint TV equals the largest binomial atom and satisfies the squared exact form of the
  `1/(4sqrt(t))` lower bound for every `1<=t<=10`;
- formula (6.2) equals direct triple enumeration for every `0<=t<=10`; and
- the `O3p` upper bound is consistent with exact full-state TV for every `2<=t<=10`.

These bounded computations are `EVIDENCE`, not proof of the universal estimates. The
universal verdicts above rest on the written derivations.

The final report's historical statements about other commands and absent route returns were
not needed as mathematical premises. Under the read-only scope, this review does not
independently attest unlisted runtime history, but no contradiction appears among the nine
authorized files.

## Four mandatory audits

### Definition audit

`PASS`. The state, all-zero starts, resampling rather than toggling, translation, TV
normalization, range, endpoint, and visible-hull map are consistent across all retained
modules.

### Logic audit

`PASS` for `O1`, `O1b`, `O2`, `O3p`, and `O5`. The directions of projection,
data-processing, sufficient-statistic equality, and coupling inequalities are all correct.
No open fixed-constant estimate is used inside the retained theorem.

### Boundary audit

`PASS`. The package separates `t=0`, verifies the `t=1` convention, states `O1` and `O1b` for
`t>=1`, and states the combined partial theorem for `t>=2`. Empty lamp support, width-zero
ranges, accessible parity, odd-time meeting, and harmonic indices are handled.

### Adversarial audit

`PASS` for the retained modules. The first genuine completion obstruction is not hidden:
neither the reflected coupling nor the V-shaped normalized-range route supplies a fixed
`C/sqrt(t)` full-state upper bound.

## Exact defects and open frontier

No exact defect was found in `O1`, `O1b`, `O2`, `O3p`, or `O5`. Thus:

- `first_error`: none for the retained partial theorem;
- `critical_errors`: empty;
- `exact_defects`: empty;
- `repairable_gaps`: empty within the claims actually promoted as proved.

The following remain open and must not be committed as a solution of the frozen target:

1. `O3`, a uniform fixed-constant `C/sqrt(t)` upper bound for the full state law;
2. `O3c`, the sufficient normalized-range array inequality (6.3), or a direct substitute;
3. `O0`, the complete frozen two-sided target; and
4. target-level `O4`, which can only audit completion after `O3` is proved.

This posthoc review independently closes the audit of the retained partial theorem only. The
historical statement in the frozen files that no independent review was then available is not
a defect; it describes the state at the scoring boundary.

## Promotion labels

May be retained as `STRICT`:

- `O1`, `O1b`, `O2`, `O3p`, and `O5`;
- formulas (3.1), (3.2), (5.1)-(5.7), and (6.1)-(6.2) with their written quantifiers;
- the exact V-shaped counterexample; and
- Route A's coupling-specific logarithmic obstruction, with its restricted scope.

Must remain `EVIDENCE`:

- all bounded exact enumerations when separated from their paper proof bridges.

Must remain `OPEN`:

- `O3`, `O3c`, `O0`, and target-level `O4`.

## Confidence and novelty

- Semantic fidelity: high.
- Mathematical correctness of retained partial theorem: high, independently audited.
- Completeness for the frozen target: absent.
- Reproducibility of the authorized exact checks: high.
- Novelty: `UNKNOWN`, because internet and literature checks were forbidden.
