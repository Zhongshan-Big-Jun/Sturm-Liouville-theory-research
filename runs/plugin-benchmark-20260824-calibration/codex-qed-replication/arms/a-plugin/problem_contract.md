# Problem contract

- Contract ID: `B3-O3-root-count-v1`
- Authoritative source: the frozen calibration task supplied on standard input on 2026-08-24.
- Research mode: blind discovery. No repository, Git history, internet source, memory, or prior solution to this exact task may be inspected.

## Objects and definitions

Let `n` be an integer with `n>=1`, let `R>1`, and put `s=sqrt(R)>1`. For real `y`, put `c=cos(y)` and `q=sin(y)` and define

`E(y)=[[c,q],[-q,c]]`,

`C_s(y)=[[c^2-s^(-1)q^2,(1+s^(-1))cq],[-(1+s)cq,c^2-sq^2]]`,

`M_{n,s}(y)=E(y)C_s(y)^n`, and `G_{n,s}(y)=(M_{n,s}(y))_{12}`.

For `x in (-1,1)`, define

`Q_{n,s}(x)=G_{n,s}(arccos x)/sqrt(1-x^2)`.

## Hypotheses

The main quantifiers are uniform: every integer `n>=1` and every real `s>1` (equivalently `R=s^2>1`).

## Target conclusion

Decide whether `G_{n,s}` has exactly `2n` zeros in the open interval `(0,pi)`, all simple. If the polynomial formulation is used, prove its equivalence, polynomial extension, exact degree, complete root location, and simplicity.

## Quantifiers and dependency of constants

There are no asymptotic or hidden constants. Every identity and root count must hold simultaneously for arbitrary fixed `n>=1` and `s>1`.

## Equivalent formulations that are actually proved equivalent

Open obligation `O1`: derive an exact factorization `G_{n,s}(y)=sin(y) Q_{n,s}(cos y)` with a genuine polynomial `Q_{n,s}` and show that zeros and multiplicities correspond on `(0,pi)`.

## Boundary and degenerate cases

Must be audited separately: `n=1`; `y=0`; `y=pi`; `y=pi/2`; and the excluded boundary `R=1` (`s=1`). Endpoint zeros must not be counted.

## Permitted outcomes

- affirmative uniform exact proof;
- exact counterexample or negative proof;
- strongest rigorously justified partial result with the first unresolved obligation.

## Completion criteria

1. Contract fidelity is independently audited.
2. An exact formula valid for all allowed parameters is proved.
3. Exactly `2n` interior zeros are located or counted without relying on numerics.
4. Every counted zero is proved simple.
5. All required boundary cases are checked.
6. An independent adversarial audit reports no mathematical gap in the final candidate.

## Answer space

The output must decide TRUE or FALSE for the frozen universal statement, or explicitly withhold that decision if a load-bearing obligation remains.

## Acceptance criteria per subproblem

- `O1` polynomial reduction: matrix identity plus reversible zero/multiplicity correspondence.
- `O2` scalar root theorem: all roots located in the needed interval, exact count, and simplicity.
- `O3` lifting: each scalar root yields exactly two interior roots and no extras.
- `O4` boundaries: explicit computations for every named case.
- `O5` audit: first-time verifier finds zero critical errors and zero gaps.

## Results that do not count as completion

Finite scans; numerical plots; finitely many `n` or `R`; merely pairing roots; a degree bound without location and simplicity; endpoint counting; or an unproved appeal to oscillation/interlacing.

## Forbidden moves

No inspection outside the current directory; no repository or Git-history inspection; no internet; no prior-solution lookup; no unverified recollection as a premise; no silent quantifier changes; no numerical evidence promoted to proof.

## Tool, citation, and search constraints

Local scratch symbolic computation is permitted only for falsification and identity checking. The final proof must be self-contained. No external citation will be used. Research subagents may use only the frozen statement and coordinator-created packet files.

## Ambiguities or competing interpretations

None material. `sqrt(R)` is the positive square root, and zeros are ordinary real zeros with simplicity meaning nonzero first derivative.

## Contract audit

Coordinator audit: all matrices, domains, quantifiers, named boundary cases, and non-completion conditions were transcribed from the frozen task. Independent audit is assigned as part of subtask `SUB-AUDIT` after a candidate proof exists.
