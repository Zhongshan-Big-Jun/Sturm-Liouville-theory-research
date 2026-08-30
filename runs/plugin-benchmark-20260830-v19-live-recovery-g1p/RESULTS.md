# v1.9 live in-flight recovery results

## Overall outcome

- Recovery protocol: `PASS_WITH_USABILITY_FINDINGS`.
- Mathematics: `RIGOROUS_PARTIAL_RESULT`.
- Independent informal audit: `PASS`.
- Target completion: false.
- Numerical proof premises: none.

## Mathematical delta

The run reduced the n=2 symmetric INF odd-sector all-finite-R problem from an
arbitrary compact-middle first singularity to one one-dimensional same-sign
Jacobi kernel. It obtained:

1. an exact semiseparable Green representation;
2. strict positive odd off-diagonal sign;
3. double-zero exclusion;
4. one explicit positive-cone scalar equality for the corank-one case;
5. exact Jacobi and transfer realization;
6. a Ko-regular branch chart avoiding the singular full Jacobian inverse.

`KP-DET`, simultaneous odd/even singularity, `KO-DET`, non-symmetric roots, and
global G1 prime remain open.

## Recovery delta

W1 completed first. W2 was checkpointed as live, then returned. The canonical
receipt forced W2 reconciliation before any other dispatch, and W2 was ingested
without restart or transcript replay. Sequence 01 then bound the reconciled
package and authorized one fresh independent audit.

## Important qualification

This is a functional recovery experiment, not a scored plugin-versus-control
benchmark. Collaboration-agent token, cache, response, and cost counters were
not available. Only observable artifact counts and deterministic checkpoint
overhead are reported.

## Primary artifacts

- Mathematical package: `workspace/runs/rigorous-open-math-research/R-20260830T020000Z-g1p-live-recovery/`.
- Recovery metrics: `RECOVERY_METRICS.md`.
- Plugin findings: `PLUGIN_FINDINGS.md`.
- Parent tool entry: `tools/kp-odd-firstzero-reduction.md`.
- Lean scaffold: `lean-proof/SL/KpOddFirstZero_Scaffold.lean`.
