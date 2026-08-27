INDEPENDENTLY_AUDITED_PROOF

# Neutral mathematical audit

## Verdict

`PASS` for every theorem-strength claim retained by the frozen artifacts.

This is a pass of the partial package, not a proof of the frozen target. The lower bound is
closed, while the requested constant-over-`sqrt(t)` full-state upper bound remains open.

## Scope and provenance

The audit used only the five authorized frozen inputs and fresh local exact computations. No
internet, literature, prior benchmark answer, or unlisted project artifact was used. The
author files were not modified.

| Input | SHA256 |
|---|---|
| `problem_contract.md` | `15a22e80e231febc4527dcedf0475e68ee6bd83f4361ea6110a2ea20f2342eb8` |
| `candidate_proof.md` | `f1f2ca8e343ef5ac7056ea596e3db516cc705d14d9d106362722610383f4449c` |
| `subagents/route_a.md` | `6ce207738f66fcd3b0b5b2c39175cf068be15f8b8532b76593e11b5cd386b647` |
| `subagents/route_c.md` | `f260fe18d316ad8d58294700ad4bb3cd40514537728a7ac67ae576c19ca7bbf2` |
| `reproducibility/exact_small_cases.py` | `3ce81aff83e381a59a5a63e0d2605a4d056c2624fcb34b590881313f2042fbc2` |

## Claim-by-claim audit

### Definitions, conditional lamps, translation, and parity

- The state interpretation and switch-walk-switch transition agree with the frozen contract.
  In particular, `(0,2)` is the all-zero lamp configuration with base point `2`.
- For every `t>=1`, every visited site is resampled. The chronologically last switch variables
  selected at distinct visited sites are distinct independent fair bits. Hence, conditional on
  the base path, the lamps are i.i.d. fair on the visited interval and zero outside. Since this
  conditional law depends only on `(L_t,U_t)`, the same statement remains true after
  conditioning on `(L_t,U_t,S_t)`.
- Spatial translation by two maps the law from `(0,0)` to the law from `(0,2)`. Both endpoint
  supports have parity `t mod 2`; there is no parity singularity.
- The `t=0` exception is handled separately. No positive-time lamp statement is used there.

Verdict for these claims: `STRICT`.

### Visible-hull total-variation equality

For a fixed final state, summing over all compatible base ranges gives formula (3.1). A
compatible range must contain the start, endpoint, and every lit lamp, and its exact lamp
pattern has conditional probability `2^{-(u-l+1)}`. Thus each of the two point-mass functions
is constant on every fiber of

`V(eta,z)=(min(supp(eta) union {z}),max(supp(eta) union {z}),z)`.

Each fiber is finite. If its size is `n_v` and the two point masses are `a_v,b_v`, its full
`l1` contribution is `n_v|a_v-b_v|`, exactly the pushforward contribution
`|n_va_v-n_vb_v|`. Summation proves the equality of full-state and visible-hull TV for
`t>=1`. It also holds directly at `t=0`, when the two visible hulls are distinct.

Verdict for (3.1)-(3.2): `STRICT`.

### Explicit endpoint lower bound

At a common endpoint the two binomial masses are `p_k` and `p_{k-1}`. Extending the unimodal
sequence by zero at both ends makes its total discrete variation exactly twice its maximum,
so the endpoint TV is `max_k p_k`. Markov's inequality applied to
`(K-t/2)^2`, whose expectation is `t/4`, puts at least `3/4` of the mass in
`|K-t/2|<sqrt(t)`. This interval contains at most `2sqrt(t)+1<=3sqrt(t)` integers for
`t>=1`. Therefore

`TV(P_t^(0,0),P_t^(0,2)) >= 1/(4sqrt(t))`

for every integer `t>=1`.

The projection direction, quantifiers, plateau case for odd `t`, and constant `1/4` are all
correct.

Verdict for (4.1)-(4.2): `STRICT`.

### Route A

- The reflection identity
  `P(M_m<a)=P(-a<=R_m<a)` has the correct half-open endpoints and parity count. The elementary
  central-binomial upper bound gives `P(M_m<a)<=a/sqrt(m+1)`.
- The pre-meeting depth satisfies exactly `P(D>=d)=1/(d+1)`. Its truncated first moment is at
  most `H_{N+1}`.
- The reflected paths have pre-meeting ranges `[-D,1]` and `[1,D+2]`. After coalescence, triple
  equality occurs exactly when the common tail reaches both old extremes. Splitting at
  `n=floor(t/2)`, conditioning at the meeting time, and applying the one-sided estimate on
  both sides proves

  `TV <= 1/sqrt(n+1)+2H_(n+1)/sqrt(t-n+1)` for every `t>=2`.

  The simplified bound `sqrt(2)[3+2log(t+1)]/sqrt(t)` follows with the stated constants.
- Equal triples admit identical conditional fair lamps, so the same upper bounds hold for the
  literal full-state laws.
- The local lower survival estimate is valid under `m>=256` and
  `1<=a<=sqrt(m)/16`. Combining it with the exact depth distribution gives the stated
  coupling-mismatch lower bound (15) for every `t>=512`. Consequently, this particular
  reflected/coalescing coupling cannot have mismatch probability `C/sqrt(t)` for a fixed
  `C`. The artifact correctly does not promote this to a TV lower bound.

Verdict for Route A formulas (1), (2), and (15), including the full-state interface:
`STRICT`.

### Route C

- The path-count formula (1), boundary inclusion-exclusion (2), recurrence (3), and
  normalized masses (4)-(6) are exact. The forced zero lamps outside the range are included.
- Formula (7) counts the empty support separately and counts each nonempty support with given
  extrema using the correct multiplicity `kappa(p,q)`. The endpoint and lamp domains include
  exactly the union of the two reachable supports.
- Formula (9) is the exact translated triple TV. Its indices and the shift
  `h_t^r(a,j)-h_t^r(a+2,j)` are correct. Formula (10) has the correct data-processing
  direction. The `t=1` values, full-state TV `3/4` and triple TV `1`, are exact.
- The ordered two-extreme coverage argument has valid stopping-time independence. With the
  exact law `P(A=a)=1/((a+1)(a+2))`, it proves formula (16) for every integer `t>=31`, hence
  an explicit `O((1+log t)/sqrt(t))` full-state upper bound.
- The displayed killed-path table at `(t,r,j)=(10,4,2)` is exact. On the accessible parity
  class the array is `(26,16,26)`, which is a genuine counterexample to the proposed
  unimodality sign argument.

Verdict for Route C formulas (1)-(10), (16), and the counterexample: `STRICT`.

## Four mandatory audits

### Definition audit

`PASS`. The two starts, lamp resampling rule, finite support, endpoint, range, translations,
and TV normalization are used consistently. No argument substitutes toggling for resampling.

### Logic audit

`PASS`. Implication directions, conditioning, mixture arguments, stopping-time interfaces,
and the coupling inequality are correct. The Route A obstruction is explicitly limited to
one coupling and is not used to infer a lower bound on TV.

### Boundary audit

`PASS`. The artifacts correctly separate `t=0`, use lamp uniformity only for `t>=1`, retain
endpoint parity, and state thresholds `t>=2`, `t>=31`, and `t>=512` where needed. Empty lamp
support and degenerate range width zero are included in the finite formulas.

### Adversarial audit

`PASS`. The weakest interfaces were attacked directly: full state versus sufficient
statistic, triple versus lamp coupling, the heavy-tailed pre-meeting depth, parity-class
unimodality, and finite support multiplicities. No counterexample or unsupported inference
was found among the retained claims.

## Exact computational checks

The supplied script was run with:

`py -3 exact_small_cases.py --triple-max 40 --full-max 10`

It produced exact integer `l1` numerators and denominators. Fresh independent exact dynamic
programs additionally checked:

- full-state TV equals visible-hull TV for every `0<=t<=10`;
- Route C formula (7) equals direct full-state enumeration for every `1<=t<=6`;
- Route C formula (9) equals direct triple enumeration for every `1<=t<=6`;
- the Route C counterexample row values are exactly
  `(81,0,55,0,26)`, `(162,89,89,32,16)`, and `(81,55,0,0,26)` on the accessible rows.

These checks are `EVIDENCE` only. The universal classifications above rest on the written
proofs, not on finite computation.

## Promotion decision

May be committed as `STRICT`:

1. the conditional lamp law for `t>=1`;
2. translation and parity statements;
3. the exact visible-hull TV equality;
4. the exact endpoint TV identity and the uniform lower bound `1/(4sqrt(t))` for `t>=1`;
5. Route A's explicit logarithmic full-state upper bound;
6. Route A's coupling-specific logarithmic lower obstruction;
7. Route C's exact finite state and triple formulas;
8. Route C's explicit logarithmic full-state upper bound; and
9. Route C's exact counterexample to parity-class unimodality.

Must remain `EVIDENCE`:

- all finite outputs of `exact_small_cases.py` and the fresh bounded exact enumerations, when
  considered without their separate proof bridges.

Must remain `OPEN`:

- `O3`, the uniform full-state upper bound `C/sqrt(t)` with fixed numerical `C`;
- Route A's requested alternative coupling or signed cancellation without harmonic loss;
- Route C's normalized-range array inequality (17); and
- the frozen two-sided target as a complete theorem.

## First failing claim and gaps

There is no failing retained theorem claim. Accordingly:

- `first_error`: none;
- `critical_errors`: empty;
- `gaps`: empty for the retained partial theorems;
- global completion frontier: `O3`, as listed above.

## Novelty and confidence

Novelty is `UNKNOWN`, because internet and literature checks were forbidden. Semantic
fidelity, mathematical correctness of the retained claims, and reproducibility are high.
Completeness for the original target is explicitly false: the constant-order upper bound is
not proved.
