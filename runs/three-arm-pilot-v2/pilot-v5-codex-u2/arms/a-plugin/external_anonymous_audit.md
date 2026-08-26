# Fresh label-blind adversarial review

## Verdict

`PASS`

This verdict applies to the claimed partial theorem only. It does not certify the original constant-over-`sqrt(t)` upper bound, and it does not close `O3`.

## Audit scope and bindings

The review used only the following three mathematical inputs. No parent-directory material, repository state, prior conversation, memory, or network source was inspected.

- `problem_contract.md`: SHA256 `98d6ea8d4da0a5f121c36d7c0b2cc895ec81d7b30f6e9b2d079f212825f667f5`
- `candidate.md`: SHA256 `c76537d71604f3f5402d520423bcb045b8e203b4fc967c6fb8d1ebbf8abf043b`
- `dependency.md`: SHA256 `70315032fdc32eb1c171089ebcb9a08eb04dc9cf7e8127cb5cace9f77feee80c`

The audited claims are:

1. For `t>=1`, conditional on a deterministic base path, the terminal lamps on its visited interval are independent fair bits and all other lamps are zero.
2. For every integer `t>=1`, the full-state total variation is at least `1/(4 sqrt(t))`.
3. For every integer `t>=16`, the displayed reflection-then-synchronization coupling gives the rigorous partial upper bound `(2 log(t)+15)/sqrt(t)`.
4. Within the precisely stated class using the fixed reflection/synchronous paired-base-path law and preserving the correct lamp marginal conditional on each revealed path pair, the optimal conditional lamp repair has mismatch `F_t` with a genuine logarithmic loss.
5. The translated range-triple identity is an exact reduction of one sufficient route to the still-open upper-bound obligation.

## First-error localization

`first_error: none`

No erroneous or unsupported load-bearing step was found in the claimed partial result.

## Definition audit

The candidate uses the frozen chain exactly as stated. Both initial lamp configurations are all zero, the base starts are 0 and 2, and each switch is a resampling by a fresh fair bit. It does not interpret `(0,2)` as a lit lamp and does not replace resampling by an unproved alternative convention.

For a fixed path with `t>=1`, every visited site has at least one resampling. The terminal value at each visited site is its last resampling coin. Last coins for distinct sites are distinct members of the independent coin family, proving both fairness and mutual independence. A nearest-neighbour integer path visits the whole interval between its minimum and maximum. Thus the interval lamp kernel is exact, including repeated visits and the initially forced zeros. Since this conditional kernel depends only on `(L,U,Z)`, the common-kernel factorization and total-variation contraction are valid.

The maximal-overlap formula for interval lamp kernels is also exact. Common configurations must vanish outside the intersection, their count is `2^|I intersect J|`, and the smaller point mass is `2^(-max(|I|,|J|))`. This yields overlap `2^(-max(|I\J|,|J\I|))`. The mixture decomposition in `dependency.md` gives both exact marginals and attainment of this overlap.

## Logic and constant audit

For the lower bound, projection to the endpoint can only decrease total variation. At even `t`, the difference on `{z<=0}` is exactly `P(S_t=0)`. At odd `t`, the difference on `{z<=1}` is exactly `P(S_t=1)`. These are the parity-correct modal atoms. Chebyshev gives at least `3/4` of the mass in `(-2 sqrt(t),2 sqrt(t))`; that interval contains at most `2 sqrt(t)+1<=3 sqrt(t)` reachable atoms. Hence the modal atom is at least `1/(4 sqrt(t))`. The argument is valid for every integer `t>=1`, including `t=1`.

For the partial upper bound, the reflected bases meet at site 1 at the stopping time `tau=T_1`, necessarily at odd parity. Before meeting, each coordinate has a fresh fair increment; after meeting, the common continuation uses fresh independent fair increments. Therefore each base marginal is exactly the required simple random walk. The pre-meeting depth satisfies

`P(D>=k)=1/k` and `P(D=k)=1/[k(k+1)]`.

The fresh post-meeting walk is independent of the stopped pre-meeting data. On `{tau<=floor(t/2)}`, it has at least `ceil(t/2)` steps. Hitting both `D` and `-D` makes the two visited intervals equal, after which the conditional maximal lamp coupling agrees surely. The reflection identity

`P(T_k>n)=P(-k<=S_n<k)`

retains parity and contains exactly `k` reachable atoms. Together with the proved modal estimate `p_n^*<=sqrt(2/n)`, it gives each missing-level probability at most `min(1,2D/sqrt(t))`. The bound `P(tau>floor(t/2))<=3/sqrt(t)` is valid for `t>=16`. Finally,

`E[min(1,2D/sqrt(t))] <= (log(t)+6)/sqrt(t)`

follows from the exact depth law with `J=floor(sqrt(t)/2)`. Combining the terms gives exactly `(2 log(t)+15)/sqrt(t)`. The constants are conservative but correct.

The translated path-counting identity is also correct. For a physical triple `(l,u,z)`, the zero-start coordinates are `A=-l`, `R=u-l`, and `e=z-l`; translating a path started at 2 down by 2 replaces `A` by `A+2` while preserving `R,e`. Summing the absolute count difference therefore gives twice the triple-law total variation with the stated `2^(-t)` factor.

## Stopping-time and marginal audit

There is no optional-stopping misuse. Gambler's ruin is applied on finite intervals, and almost-sure finiteness of `tau` follows by the stated limiting argument. The post-meeting increments are explicitly fresh, so conditioning on `tau` and `D` does not bias the continuation. The estimates use only monotonicity of the available continuation length and an independent hitting event.

The terminal lamp coupling preserves each chain's exact conditional marginal for every revealed pair of base paths. The construction does not require coordinatewise matching of switch coins. The last-coin realization described in `dependency.md` shows that, within either chain, one can recover a family of independent fair switch coins conditional on its path. Thus no hidden path-dependent lamp bias is introduced.

## Boundary audit

- At `t=0`, neither lamp configuration is resampled and the endpoints are distinct, so the full-state total variation is 1. No claimed estimate improperly uses the `t>=1` kernel at time zero.
- At `t=1`, the lower-bound event and modal-atom estimate remain valid.
- The upper bound is claimed only for `t>=16`, exactly where its floor estimates and displayed constants are used.
- The obstruction lower bound is claimed only for `t>=ceil(exp(198))`; that threshold is sufficient because `log(t)>=198` dominates the explicit negative constants.
- Endpoint parity is preserved throughout. The meeting site and hitting identities use the reachable parity class rather than a parity-smoothed approximation.
- Empty, repeated-visit, and singleton-range cases do not create an exception. For `t>=1`, the actual visited set is a nonempty integer interval and every site in it is resampled.

## Adversarial audit of the route obstruction

For the fixed reflected/synchronous base coupling, the two terminal visited intervals relative to the meeting point are

`I_X=[min(-D,m),M]` and `I_Y=[m,max(D,M)]`.

Their exclusive-site counts are exactly `(D+m)_+` and `(D-M)_+`. If the fresh continuation has not hit `D`, at least one exclusive site remains, forcing conditional mismatch at least `1/2` even under maximal lamp coupling. Restricting to `D<=floor(t^(1/4))`, the parity-correct central atom lower bound yields a hitting-tail probability at least `D/(8 sqrt(t))`. Averaging against `P(D=k)=1/[k(k+1)]` produces the harmonic sum and hence the displayed lower bound of order `log(t)/sqrt(t)`. The subtraction of `P(tau>floor(t/2))` and the threshold `exp(198)` are numerically sufficient.

This proves only that the mismatch probability of this fixed coupling class is not `O(t^(-1/2))`. The packet explicitly preserves that scope and does not infer that `O3` itself is false.

## Status calibration

The status is correctly calibrated as `RIGOROUS_PARTIAL_RESULT`. The packet proves `O1`, proves `O2` with an explicit constant, proves a weaker logarithmic-loss upper bound, and rigorously falsifies one natural coupling route in its stated conditional-marginal class. It expressly leaves the required constant-over-`sqrt(t)` upper bound open. Therefore the original two-sided target is not claimed as solved.

Novelty and literature status remain `UNKNOWN` under the blind-review restriction.

## Structured verification record

```json
{
	"verdict": "PASS",
	"critical_errors": [],
	"gaps": [],
	"repair_hints": "",
	"first_error": null,
	"certified_scope": "The claimed rigorous partial theorem only; O3 and the original constant-over-sqrt(t) upper bound remain open."
}
```

