Use $rigorous-open-math-research. Solve the frozen task below autonomously under its blind
restrictions. Use research subagents for mechanism-distinct proof search and adversarial audit,
with at most 3 concurrent subagents. Write all skill-required persistent artifacts in the current
directory, including `problem_contract.md`, `obligation_graph.md`, `approach_registry.md`,
`research_ledger.md`, `candidate_proof.md`, `audit_report.md`, `repro_manifest.md`, and
`final_report.md`. Do not read outside the current directory. Do not use the internet. Do not ask
the user questions. At the resource boundary, preserve the strongest exact partial result and its
first unresolved obligation.

<FROZEN_TASK>

# U2 total-variation asymptotics

Let `Z_2 wr Z` be the lamplighter group. Write each state as `(eta,z)`, where
`eta: Z -> Z_2` has finite support and `z in Z` is the base position. Let `0` denote the
all-zero lamp configuration.

Consider the discrete-time switch-walk-switch chain. From `(eta,z)`, independently resample the
lamp at `z` from `Bernoulli(1/2)`, move the base to `z+1` or `z-1` with probability `1/2` each,
then independently resample the lamp at the arrival site from `Bernoulli(1/2)`. Let `P_t^x`
denote the law at integer time `t>=0` started from `x`.

Set `x=(0,0)` and `y=(0,2)`. Thus both initial lamp configurations are all zero, and the two
initial base positions are `0` and `2`.

Prove that there are explicit constants `0<c<=C<infinity` and an explicit integer `t_0` such
that, for every integer `t>=t_0`,

```text
c/sqrt(t) <= ||P_t^x-P_t^y||_TV <= C/sqrt(t).
```

Here total variation is `sup_A |P_t^x(A)-P_t^y(A)|`, equivalently one half of the `l^1`
distance on the countable state space.

State every external theorem in the exact form used and verify all hypotheses. Audit parity,
small times, the effect of the two forced initial zero lamps, and every conditioning or coupling
step. Do not replace the chain by a different lamp convention or interpret `(0,2)` as a lamp lit
at site `2`.

A complete result requires both bounds with explicit constants. If incomplete, return the
strongest exact partial result and the first unresolved obligation without claiming completion.

</FROZEN_TASK>
