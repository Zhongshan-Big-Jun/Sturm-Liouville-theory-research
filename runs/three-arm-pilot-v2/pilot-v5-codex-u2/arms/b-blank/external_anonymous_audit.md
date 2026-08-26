# Verdict

FATAL_GAP

# Certified scope

The argument is correct through equation (4). In particular:

- The switch-walk-switch definition is represented exactly. For every `t>=1`, every visited site is resampled, and its final value is its last independent fair resampling bit. Conditional on `(minimum,maximum,endpoint)=(l,r,z)`, the lamp kernel in (1) is therefore uniform on all configurations supported in `[l,r]`, with base endpoint `z`.
- The initial all-zero lamps at `0` and `2` are overwritten at the first switch. The candidate correctly interprets `y=(0,2)` as all lamps off with base position `2`.
- The common-kernel factorization and total-variation contraction in (2) are valid.
- The change of variables leading to (4), including the parity convention and zero extension in `i`, is valid.
- The lower bound is certified: projection to the endpoint gives (17), the total variation between a binomial mass function and its one-step translate is exactly its largest atom as in (18), and the Chebyshev counting argument gives `beta_t>=1/(4 sqrt(t))` for every `t>=1`.
- The parity discussion and the direct `t=1` calculation are correct. In particular, the common mass is `1/4`, so the total variation at time `1` is `3/4`.

Thus the submission rigorously proves

`||P_t^x-P_t^y||_TV >= 1/(4 sqrt(t))` for every integer `t>=1`,

but it does not prove the asserted upper bound.

# First error localization

The first false load-bearing statement is the assertion attached to equation (5): for fixed `w,e`, the parity-restricted sequence `i -> A_t^w(i,e)` is claimed to have at most one change of monotonicity.

An exact counterexample is

`t=48`, `w=8`, `e=4`, and `i=0,2,4,6,8`,

for which direct integer path counting gives

```text
A_48^8(0,4) = 1000894788882
A_48^8(2,4) = 1029170933020
A_48^8(4,4) = 1017584921004
A_48^8(6,4) = 1029170933020
A_48^8(8,4) = 1000894788882
```

The consecutive difference signs are `+,-,+,-`, so the sequence has three changes of monotonicity. These counts are reproducible by the finite exact recurrence that propagates integer path counts on states `(position,visited_0,visited_8)` for 48 nearest-neighbour steps and reads the terminal state `(4,true,true)`.

Error layer: proof. The statement of the target and the earlier chain reduction are not the source of this failure.

# Audit of equations (3)-(12)

- Equation (7) is the standard finite repeated-reflection formula for the killed walk on `{0,...,w}` and has the correct boundary displacement `w+2`.
- Equation (8) is correct inclusion-exclusion, including boundary cases when invalid-width or invalid-index terms are declared zero. Avoiding `0` gives the shifted interval `{1,...,w}`; avoiding `w` gives `{0,...,w-1}`; avoiding both gives `{1,...,w-1}`. For `w=0` or `w=1`, the same statement remains correct under the stated zero convention.
- Equation (9) correctly expresses the ratio of adjacent same-parity binomial coefficients, and equation (10) is the usual telescoping first-crossing count.
- Nevertheless, (5) does not follow from (7)-(10). Unimodality of the individual binomial image terms does not imply a one-turn property for their alternating reflected-image sum. The explicit counterexample disproves the claimed conclusion.
- Equation (6) is also only asserted. The phrases "pairing consecutive reflected images" and "the two unpaired image families" do not supply an indexed identity controlling every positive excess, its sign, or its boundary multiplicity. The counterexample above does not by itself disprove the global inequality (6), so (6) may still be true, but it is not proved by the submitted text.
- Equation (11) is valid under its stated one-turn hypothesis, but that hypothesis is unavailable because (5) is false. Hence applying (11) to all the span-count sequences is invalid.
- The endpoint summation estimate (12) is consistent with the unique decomposition of a nonnegative path by its maximum and endpoint, and the right-end estimate follows by reflection. This does not repair the missing control of the interior oscillations.
- Consequently, the span estimate (3) may still be true, but it is unproved here. Equations (13)-(16), and therefore the claimed `12/sqrt(t)` upper bound, depend entirely on (3) and are not certified.

# Why the gap is fatal for this submission

The false one-turn assertion is the mechanism that converts the three-parameter span-count sum in (4) into the endpoint and maximum bounds (6), (11), and (12). Repair requires a new global variation estimate for the oscillatory sequences, or a different coupling or analytic argument. This is not a local correction of notation, parity, or a boundary term. Since the contract requires both explicit bounds, the certified lower bound alone is incomplete.

# Audit conditions

This was a fresh label-blind audit using only the frozen problem contract and candidate proof as mathematical inputs. No network source, repository state, prior solution, or benchmark output was used. Scratch computation was exact integer enumeration and was used only to falsify the universal assertion at (5).
