# Approach registry

## Route A — algebraic/Chebyshev reduction

- Route key: `trace-det-chebyshev`
- Family: algebraic encoding.
- Core mechanism: compute `det C_s`, `tr C_s`, apply the `2x2` Cayley-Hamilton recurrence, and reduce the problem to a one-variable polynomial.
- Target obligation: `O1`, then `O2`.
- Why easier: replaces a matrix power by one scalar polynomial family.
- First deliverable: exact formula and degree.
- Fast falsification tests: `n=1,2`; `y=0,pi/2`; `s=1`.
- Expected bottleneck: prove all scalar roots lie in the needed interval and are simple.
- Cost tier: 1, escalating to 2 because the user explicitly requested independent research agents.
- Minimal first step: determinant and trace.
- Escalation criterion: exact scalar family identified.
- Status: PROVED and final audit PASS.
- Exact gap: no route-local gap.
- Owner: coordinator and `SUB-ALG`.

## Route B — oscillation/phase counting

- Route key: `trig-phase-bracketing`
- Family: analytic oscillation.
- Core mechanism: parameterize scalar roots by `z=cos(theta)` and bracket sign changes at an exact mesh.
- Target obligation: `O2`.
- Why easier: reduces location/simplicity to exact signs and a degree count.
- First deliverable: disjoint intervals containing one root each.
- Fast falsification tests: endpoint signs, `n=1`, parameter extremes `s down to 1` and `s to infinity`.
- Expected bottleneck: endpoint interval and proof that no repeated roots remain.
- Cost tier: 2.
- Minimal first step: compare values at `theta=j*pi/n` or interlacing nodes.
- Escalation criterion: a uniform sign pattern.
- Status: PROVED independently in `subagents/SUB-OSC.md`.
- Exact gap: no route-local gap; this route does not itself supply the required polynomial extension.
- Owner: `SUB-OSC`.

## Route C — disproof/boundary audit

- Route key: `counterexample-boundary-symbolic`
- Family: adversarial counterexample search.
- Core mechanism: attack exact formulas, named edge cases, multiplicity failures, and the limits `s=1`, `s to infinity`.
- Target obligation: falsify `T0` or expose a gap in `O1`-`O4`.
- First deliverable: exact counterexample or bounded no-counterexample report with symbolic checks.
- Fast falsification tests: `n=1`; `x=0`; endpoints; repeated-root equations.
- Expected bottleneck: converting absence of examples into no claim.
- Cost tier: 2.
- Minimal first step: exact low-degree computation.
- Escalation criterion: suspicious factor or vanishing discriminant.
- Status: PARTIAL / NONE_FOUND.
- Exact gap: no counterexample in the exact mechanisms attacked; the later integrated-proof audit `O5` passed.
- Owner: `SUB-ADV`.

## Route D — frozen first-time proof audit

- Route key: `hash-bound-independent-verifier`.
- Family: adversarial verification.
- Core mechanism: recompute every load-bearing step from only the frozen contract and candidate.
- Target obligation: `O5`.
- First deliverable: structured verdict with first error and gap list.
- Cost tier: 3, triggered by completion gate.
- Status: PROVED / PASS.
- Exact gap: none; critical errors and gaps are empty.
- Artifact: `subagents/SUB-AUDIT.md`, sha256 `4c8831a11edbdcb70c4599ef818e96633c507d2feef58a91659953b000f1c92f`.
