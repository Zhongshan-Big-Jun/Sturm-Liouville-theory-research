# Problem contract

## Objects and definitions

- The state space is the set of pairs `(eta,z)` with `z in Z` and finitely supported
  `eta: Z -> Z_2`.  The symbol `0` means the all-zero configuration.
- One switch-walk-switch step independently replaces the current-site lamp by a fair bit,
  makes one simple-symmetric nearest-neighbour base move, and independently replaces the
  arrival-site lamp by a fair bit.
- `P_t^x` and `P_t^y` are the laws after the integer number `t>=0` of steps from
  `x=(0,0)` and `y=(0,2)` respectively.
- Total variation is `sup_A |mu(A)-nu(A)| = (1/2) sum_s |mu(s)-nu(s)|`.

## Hypotheses

No asymptotic modification, lazification, continuous-time replacement, or alternative lamp
convention is permitted.  All resampling bits and base increments in the definition are
independent.  Both initial lamp configurations are all zero.

## Target conclusion

Exhibit numerical constants `0<c<=C<infinity` and an integer `t_0`, and prove for every
integer `t>=t_0` that

`c/sqrt(t) <= ||P_t^x-P_t^y||_TV <= C/sqrt(t)`.

## Quantifiers and dependency of constants

The same displayed numerical `c,C,t_0` must work simultaneously for all integer `t>=t_0`.
They may not depend on `t`, a trajectory, an endpoint, a range, or a lamp configuration.

## Equivalent formulations that are actually proved equivalent

Spatial translation by two sends the law from `x` to the law from `y`.  Hence the target is
equivalently a two-site translation estimate for the single law `P_t^x`.  This equivalence
uses the given chain, not a change of lamp convention.

## Boundary and degenerate cases

- At time `t`, both base positions have parity `t (mod 2)` because both starts are even;
  parity therefore does not itself separate the two laws.
- At `t=0`, the laws are point masses at distinct states and their TV distance is one.
- A site visited at least once, including the initial base site, is resampled; an unvisited
  site's initially zero lamp stays zero.
- Repeated switches at one site do not create dependence in the final lamps: the last switch
  at each visited site is an independent fair bit.
- `(0,2)` means base position two with the all-zero lamp configuration; it never means a lit
  lamp at site two.

## Permitted outcomes

- A complete proof with explicit constants and threshold.
- A rigorous partial theorem or exact reduction with the first unresolved obligation, if the
  completion gate cannot be passed.
- A counterexample only if it literally contradicts the frozen target.

## Completion criteria

Both inequalities, the numerical constants, and the uniform integer threshold are proved.
Every external theorem is stated in the exact form used and all hypotheses are checked.
The conditional-lamp law, translation, parity, initial zeros, and all coupling/conditioning
interfaces pass independent adversarial audit.

## Answer space

The result must decide whether the requested two-sided `t^{-1/2}` estimate holds under the
literal frozen switch-walk-switch chain and, if yes, provide a reproducible proof.

## Acceptance criteria per subproblem

- `O1`: derive the exact conditional final-lamp law from the stated resampling variables.
- `O2`: prove an explicit `c/sqrt(t)` lower bound for all stated times.
- `O3`: prove an explicit `C/sqrt(t)` upper bound for the full lamplighter state law, not only
  its base projection.
- `O4`: audit parity, time threshold, constants, conditioning, translations, and initial zeros.

## Results that do not count as completion

A base-walk-only upper bound; a finite computation; a non-explicit big-O statement; an
uncited or unstated heat-kernel theorem; a coupling that equalizes only endpoints or ranges
but not full states; or a proof for a different switching rule.

## Forbidden moves

No internet; no task-source lookup outside the current run; no silent theorem recall as a
premise; no numerical-to-universal leap; no interpretation of `(0,2)` as a lamp bit; no
discarding parity or small-time exceptions.

## Tool, citation, and search constraints

Blind autonomous run.  Internet and literature lookup are forbidden.  Exact local programs
may be used only for discovery/falsification and must be accompanied by a proof bridge.

## Ambiguities or competing interpretations

None after applying the literal state notation and transition rule in the frozen task.

## Contract audit

Coordinator comparison against the frozen statement: all objects, quantifiers, conventions,
and completion requirements are preserved.  Independent audit remains obligation `O4`.
