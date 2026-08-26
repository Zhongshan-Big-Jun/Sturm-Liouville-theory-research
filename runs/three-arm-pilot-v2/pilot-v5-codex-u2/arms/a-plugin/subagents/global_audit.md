RIGOROUS_PARTIAL_RESULT

# Fresh adversarial global audit

## Frozen package and verdict

- `problem_contract.md`: SHA-256 `98d6ea8d4da0a5f121c36d7c0b2cc895ec81d7b30f6e9b2d079f212825f667f5`.
- `candidate_proof.md`: SHA-256 `c76537d71604f3f5402d520423bcb045b8e203b4fc967c6fb8d1ebbf8abf043b`.
- `subagents/direct_coupling.md`: SHA-256 `70315032fdc32eb1c171089ebcb9a08eb04dc9cf7e8127cb5cace9f77feee80c`.
- `subagents/partial_validator.md`: SHA-256 `82f3f1b8261ea9c6d75af2d01cc25c6ab758713581771eab1c361006fa797542`.
- The contract agrees with the frozen statement in `PROMPT.md`, whose local SHA-256 is `0ab0af8e6936c0597626493029004dc4f8851bf79e5f6ae4076ccc2605d012a7`.

Verdict: `PASS` for the explicitly claimed partial theorem. This is not a pass for the frozen two-sided target: the constant-order upper obligation `O3` remains openly and accurately unproved.

## Definition and marginal audit

Lemma 1 is exact for every `t>=1`. Conditional on a deterministic admissible base path, independence of switch coins from moves leaves all departure and arrival coins independent fair bits. Every visited site is resampled: the start by the first departure switch and any later first-visited site by its arrival switch. Distinct sites select distinct chronological last coins, so their terminal bits are mutually independent; repeated visits do not change this. The nearest-neighbour visited set is exactly `[L,U]`, while all unvisited lamps retain their forced initial zero. This treats both starts correctly: `(0,2)` has no lit lamp, and its initially zero lamp at 2 is resampled at time zero when `t>=1`.

Consequently `P_t^(0,a)=Q_t^a K` uses the same Markov kernel for `a=0,2`. The contraction argument has the correct total-variation normalization. At `t=0` no switch occurs and the two deterministic states have different base coordinates, hence total variation is exactly 1; Lemma 1 deliberately has domain `t>=1`.

## Lower-bound audit (`O2`)

Projection to the base cannot increase total variation. The projected laws are `S_t` and `S_t+2`. For even `t`, the probability difference on `{z<=0}` is exactly `P(S_t=0)`; for odd `t`, the difference on `{z<=1}` is exactly `P(S_t=1)`. These are the parity-correct modal atoms

`p_t=2^(-t) binom(t,floor(t/2))`.

Chebyshev gives `P(|S_t|<2 sqrt(t))>=3/4`. The open interval contains at most `2 sqrt(t)+1<=3 sqrt(t)` points of the one reachable parity lattice for `t>=1`. Unimodality therefore gives `p_t>=1/(4 sqrt(t))`. Thus

`||P_t^x-P_t^y||_TV >= 1/(4 sqrt(t))`

with the stated exact constant for every integer `t>=1`.

## Reflection coupling, conditional lamps, and hitting identities

Before meeting, `Y_n=2-X_n`; afterward both coordinates use the same fresh increment. Each coordinate's next increment is fair conditional on the joint past, so both base marginals are exact simple random walks. Equal parity is retained, and the meeting is at site 1 at an odd time. The included dependency proves `tau<infinity` almost surely by finite gambler's ruin followed by a limit, so the depth variable is legitimate. For `D=1-min_{j<=tau}X_j`, gambler's ruin on `[1-k,1]` gives

`P(D>=k)=1/k`, `P(D=k)=1/[k(k+1)]`, `k>=1`.

For interval lamp laws `mu_I,mu_J`, the overlap coefficient is exactly

`2^(|I intersect J|-max(|I|,|J|)) = 2^(-max(|I\J|,|J\I|))`.

The explicit common-part/residual decomposition in `subagents/direct_coupling.md` attains this overlap, including `I=J`, and gives the correct conditional marginal to each chain for every revealed path pair. Integrating those conditional marginals preserves each terminal chain law. Thus revealing both paths and then maximally coupling lamps introduces no path-dependent marginal bias.

Reflection at the first visit to `k` gives the exact identity

`P(T_k>n)=P(-k<=S_n<k)`.

The half-open interval contains exactly `k` reachable parity atoms. The central-binomial induction proves `p_n^*<=sqrt(2/n)` for every `n>=1`, so `P(T_k>n)<=min(1,k sqrt(2/n))`; at `k=1` the survival probability is the single modal atom. All uses of the fresh post-meeting continuation condition on the stopping history and then use increments independent of that history, so the conditioning steps are valid.

## Logarithmic upper-bound audit

Let `n=floor(t/2)`. On `{tau<=n}`, at least `ceil(t/2)` fresh common steps remain. If that continuation hits both `-D` and `D` relative to the meeting site, the two total visited intervals and endpoints coincide, and the conditional lamp coupling agrees surely. The two one-sided hitting failures have union-bound probability at most

`2 min(1,2D/sqrt(t))`.

Also `P(tau>n)<=sqrt(2/n)<=3/sqrt(t)` for `t>=16`. With `J=floor(sqrt(t)/2)` and the exact depth law,

`E[min(1,2D/sqrt(t))]`

`<= (2/sqrt(t)) sum_(k=1)^J 1/(k+1) + P(D>J)`

`<= (log(t)+6)/sqrt(t)`.

The constants and directions are correct, yielding for every integer `t>=16`

`||P_t^x-P_t^y||_TV <= (2 log(t)+15)/sqrt(t)`.

For the small positive times `1<=t<=15`, O1 and the lower bound still apply. The displayed logarithmic expression is in fact larger than 1 there (`2 log(t)+15>=15` and `sqrt(t)<4`), so total variation at most 1 also gives that inequality if one elects to extend it; the candidate only claims it from 16. Time zero was handled separately above.

## Range-triple identity and completion-status audit

The counting identity (12) has the correct factor `2^(-t)` for `2 TV`, the translation sends `A` to `A+2` while preserving `R,e`, and extending `H` by zero retains support and parity. It is only a reduction: no order-`2^t/sqrt(t)` diagonal-variation bound is supplied.

There is no complete `C/sqrt(t)` upper claim anywhere in the candidate. Lines 3 and 77--79 call the result partial, lines 148--173 explicitly leave `O3` unresolved, and the referenced coupling obstruction is carefully restricted to the fixed reflection/synchronous base-path pairing. The logarithmic lower bound for that particular coupling does not assert that the target itself is false. Thus the first unresolved frozen-target obligation is exactly the advertised constant-order upper bound, but it is not a gap in the correctness of the explicitly claimed partial theorem.

## Structured verification result

```json
{
  "verdict": "PASS",
  "critical_errors": [],
  "gaps": [],
  "repair_hints": "No repair is required for the claimed partial theorem. To complete the frozen task, prove an explicit order-2^t/sqrt(t) bound for the sum in candidate equation (12), or construct a different exact-marginal full-state coupling with mismatch C/sqrt(t).",
  "covered_scope": "Contract fidelity; O1 for all t>=1; forced zeros and repeated visits; t=0; O2 with constant 1/4 for all t>=1 and exact parity; reflection/synchronous base marginals; almost-sure meeting and depth law; maximal conditional interval-lamp coupling; hitting/reflection identities; every conditioning interface in the logarithmic coupling; upper bound (2 log t+15)/sqrt(t) for all integers t>=16; small positive times; exact range-triple translation identity; and calibration of the non-completion claim.",
  "residual_risk": "The frozen target remains incomplete because no constant C proves O3. No external literature or formal proof assistant was used; the audit is a self-contained first-time mathematical check of the frozen local package."
}
```
