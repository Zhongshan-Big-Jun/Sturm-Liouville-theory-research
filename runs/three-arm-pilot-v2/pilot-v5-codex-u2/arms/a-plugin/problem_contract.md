# Problem contract

- Contract ID: `U2-TV-2026-08-26-v1`
- Authoritative source: `PROMPT.md`, SHA-256 `0ab0af8e6936c0597626493029004dc4f8851bf79e5f6ae4076ccc2605d012a7`.
- Status: frozen blind task; no internet or external-file access permitted.

## Objects and definitions

The state space is the restricted wreath product written as pairs `(eta,z)`, where `z` is an integer and `eta: Z -> Z_2` has finite support. The symbol `0` in `(0,z)` is the all-zero configuration.

One discrete switch-walk-switch step independently replaces the lamp at the current base position by a fair bit, makes one nearest-neighbour simple-random-walk move, and independently replaces the lamp at the arrival position by a fair bit. `P_t^s` is the time-`t` law started from state `s`. Total variation is `sup_A |mu(A)-nu(A)| = (1/2) sum_w |mu(w)-nu(w)|`.

The two starts are exactly `x=(0,0)` and `y=(0,2)`: both lamp configurations are all zero; `(0,2)` does not mean that lamp 2 is lit.

## Hypotheses

Time `t` is an integer with `t >= 0`; all resampling coins and base moves are mutually independent and have the probabilities stated above.

## Target conclusion

Exhibit numerical constants `0<c<=C<infinity` and an integer `t_0`, and prove for every integer `t>=t_0` that

`c/sqrt(t) <= ||P_t^x-P_t^y||_TV <= C/sqrt(t)`.

## Quantifiers and dependency of constants

The same displayed numerical `c,C,t_0` must work simultaneously for every integer `t>=t_0`; they may not depend on `t`, a path, endpoint, range, or lamp realization.

## Equivalent formulations that are actually proved equivalent

For `t>=1`, conditional on a base path with minimum `L`, maximum `U`, and endpoint `Z`, the final lamps on the integer interval `[L,U]` are independent fair bits and all lamps outside are zero. Consequently the state law is obtained from the law of `(L,U,Z)` by a common Markov kernel. This statement must be proved, not assumed.

## Boundary and degenerate cases

- Audit `t=0` and all times below the selected `t_0`, without requiring the target estimate there.
- The two endpoints have the same parity because the starting positions differ by 2; parity cannot be discarded.
- The time-zero lamps at sites 0 and 2 are forced zero, but the initial switch at the respective starting site resamples them when `t>=1`.
- Repeated visits and the fact that every one-dimensional nearest-neighbour visited set is an interval must be checked.
- Every conditioning and coupling must preserve each chain's exact marginal law.

## Permitted outcomes

- affirmative proof with explicit constants;
- negative proof by a rigorous counterexample to the claimed asymptotic;
- strongest exact partial theorem plus the first unresolved obligation at the resource boundary.

## Completion criteria

Both bounds, all external results in the exact form used with hypotheses verified, explicit constants and time threshold, semantic fidelity to the stated chain, and an independent adversarial audit with no mathematical gap.

## Answer space

Decide whether the required uniform two-sided `t^{-1/2}` estimate is rigorously established for the frozen chain, and provide an auditable proof or calibrated partial result.

## Acceptance criteria per subproblem

- `O1` lamp-kernel reduction: prove exact conditional independence and handle the forced initial zeros.
- `O2` lower bound: derive an explicit central endpoint mass bound for all claimed times, including parity.
- `O3` upper bound: prove an explicit `O(t^{-1/2})` total-variation estimate, with every sum/coupling justified.
- `O4` synthesis: constants satisfy `0<c<=C<infinity` and the estimates hold simultaneously for every integer `t>=t_0`.

## Results that do not count as completion

Scaling heuristics, local-limit asymptotics without a uniform explicit inequality, finite computation, a bound for a different lamp convention, a coupling without verified marginals, or only one side of the target estimate.

## Forbidden moves

No internet; no read outside the current directory; no silent external theorem; no interpretation of `(0,2)` as a lit lamp; no change from resampling to a different switch convention unless their equality in law is explicitly proved; no completion claim with an open obligation.

## Tool, citation, and search constraints

Only files under the current directory and local shell computation may be used. The run is blind: literature/status claims are `UNKNOWN`, and the proof should be self-contained wherever possible. Up to three concurrent research subagents are authorized.

## Ambiguities or competing interpretations

None material after the prompt's explicit clarification of `0` and total variation. Addition/XOR by an independent fair bit is equal in law to resampling, but this equivalence requires a one-line verification before algebraic use.

## Contract audit

Coordinator comparison against `PROMPT.md`: all objects, starts, quantifiers, parity, lamp convention, total-variation normalization, explicit-constant demand, and blind restrictions are retained. A separate adversarial pass will re-audit fidelity.
