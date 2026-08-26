RIGOROUS_PARTIAL_RESULT

# Result

## Exact theorem proved

For the frozen switch-walk-switch chain started at `x=(0,0)` and `y=(0,2)`,

`||P_t^x-P_t^y||_TV >= 1/(4 sqrt(t))` for every integer `t>=1`,

and

`||P_t^x-P_t^y||_TV <= (2 log(t)+15)/sqrt(t)` for every integer `t>=16`.

Here `log` is natural. At `t=0`, the total variation is exactly 1 because the deterministic base positions differ. Both initial lamp configurations are all zero; no lamp at 2 is interpreted as lit.

Two additional exact partial results are proved:

1. Conditional on a length-`t` base path (`t>=1`) with minimum `L`, maximum `U`, and endpoint `Z`, the final lamps on `[L,U]` are iid fair bits and every lamp outside is zero. Thus the state law is a common Markov-kernel image of the range triple `(L,U,Z)`.
2. The translated `(L,Z)` and `(U,Z)` marginal TVs are each at most `12/sqrt(t)` for every `t>=1`.

The requested fixed-constant upper `C/sqrt(t)` is **not proved**, so this is not a complete solution of the frozen task.

## Proof summary

The lower bound projects to the endpoint. The endpoint laws are `S_t` and `S_t+2`; the parity-correct threshold event has difference equal to the central atom `2^{-t} binom(t,floor(t/2))`. Chebyshev, parity spacing two, and binomial unimodality give the explicit lower `1/(4sqrt(t))`.

For the upper partial theorem, reflect-couple the bases from 0 and 2 until they meet at 1, then synchronize. If `D` is the pre-meeting depth relative to 1, gambler's ruin gives `P(D>=k)=1/k`. Conditional on paths, fair interval-lamp laws have exact overlap `2^{-max(|I\J|,|J\I|)}`. A common continuation that reaches both old extreme depths erases the interval difference. The exact hitting identity `P(T_k>n)=P(-k<=S_n<k)` and an elementary central-binomial upper bound yield the displayed logarithmic estimate after summing the harmonic depth law.

The exact remaining reduction is

`2 TV(Q_t^0,Q_t^2) = 2^{-t} sum_{R,K,A}|h_t(R,K,A)-h_t(R,K,A+2)|`,

where `h_t` counts zero-start paths by range width `R`, endpoint above the minimum `K`, and origin height above the minimum `A`. The terminal coarea route proves this variation equals twice the aggregate number of parity-superlevel components and also expresses it through mixed differences of periodized binomial coefficients.

## First unresolved obligation

Prove a numerical `C_0<infinity`, independent of `t`, such that

`sum_{R,K,A}|h_t(R,K,A)-h_t(R,K,A+2)|`

` <= C_0 binom(t,floor(t/2))`                               `(O3*)`

for every integer `t>=1`. By the audited central-atom bound and the common lamp kernel, `(O3*)` immediately gives the required `C/sqrt(t)` upper. Equivalently, close the aggregate superlevel-component or explicit periodized-binomial variation bound in `subagents/aggregate_coarea.md`.

## Failed and blocked routes

- Reflection until meeting followed by synchronization has an intrinsic `log(t)/sqrt(t)` mismatch even with optimal conditional lamp coupling; the old pre-meeting lamps and harmonic depth law cause it.
- Fiberwise unimodality is false: at `(t,R,K)=(6,4,2)`, the compatible `A`-fiber is `[1,0,1]`.
- Taking absolute values separately in the four killed kernels or in each reflection image destroys the cancellation needed for `(O3*)`.
- A generic inequality bounding joint TV by the sum of its two marginal TVs is false; the computation-supported simple-walk version remains unproved.

## Verification performed

- Fresh independent global audit: `PASS` with zero errors/gaps for the claimed partial theorem, bound to candidate SHA-256 `c76537d71604f3f5402d520423bcb045b8e203b4fc967c6fb8d1ebbf8abf043b`.
- Independent module validation found and localized one non-load-bearing erroneous recurrence display; the correct recurrence is implemented in the exact scripts.
- Exact integer enumeration checked all small-time numerators and probed `(O3*)` and the mixed marginal comparison through `t=100` in the coordinator replay; larger subagent probes are recorded only as finite evidence.
- No internet, external theorem premise, or read outside the current directory was used.

## Novelty status

`UNKNOWN` under the mandated blind restriction. No novelty or literature-status claim is made.

## Human/model/tool contributions

- Human: supplied the frozen task, blind restrictions, and continuation wall cap; no mathematical hint or selection was supplied.
- Coordinator: contract, synthesis, lower bound, partial upper integration, exact scripts, obligation tracking, and terminal calibration.
- Research subagents: direct coupling obstruction and lamp overlap; range/one-sided reflection estimates; aggregate killed-kernel/coarea reduction; independent module and global audits.
- Tools: local exact-integer Python computation and SHA-256 hashing only; computation was used for falsification, not general proof.

## Reproducibility

See `repro_manifest.md` and `reproducibility/`. Primary replay:

`python3 reproducibility/audit_exact.py 100`

Expected output:

`PASS exact finite identities and conjecture probes for 0<=t<=100`

## Confidence by axis

- Semantic fidelity: high; fresh audit PASS.
- Mathematical correctness of stated partial theorem: high; fresh audit PASS with no gaps.
- Completeness for frozen target: incomplete; `O3*` is open.
- Novelty: unknown by blind design.
- Reproducibility: high for all finite checks and hash-bound text artifacts; no formal proof assistant was available.
