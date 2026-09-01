RIGOROUS_PARTIAL_RESULT

# Sequence-10 alpha-collision reconciliation

## Dispatch accounting

- W6 prover: `NO_RETURN`. The service rejected the turn at the usage boundary
  before any mathematics or artifact was produced.
- W7 falsifier: `PARTIAL`, artifact `falsifier_result.md`, SHA256
  `191b0a1cd621b8f8451647a5273a2f79efd0d57b71e3a7ba570e8644cae6e044`.
- Valid mathematical responses: 1.
- Worker restarts: 0.
- Duplicate dispatches: 0.
- Transcript replays: 0.

W6 is not retried in this segment because W7 returned an exact candidate
exclusion of the entire target face. Repeating W6 before auditing W7 would
have no demonstrated marginal decision value.

## W7 candidate theorem

W7 claims that no complete admissible sequence can satisfy

```text
m->1+,
alpha->0.
```

The proposed contradiction is:

```text
spectral limits: X/alpha->-1, Y/alpha->2/3,
mass limit:      s/C->3/2,
band limit:      Y/alpha=(s/C)(-X/alpha),
```

which would force `2/3=3/2`. The candidate also removes the apparent
left-layer `0/0` norm terms using the spectral equations and converts the
sequential exclusion to a uniform empty wedge.

## Closure decision

The next action is one fresh independent audit of W7. The audit must verify
all norm limits at `alpha->0`, the signs and limits of `Z` and `T`, the band
ratio, endpoint exclusion, and the equivalence between sequential exclusion
and a uniform wedge. `PHI-SIGN` and KP-DET remain open pending that audit and
outside the near-one region.

decision_delta: One valid response produced an exact candidate exclusion of the only unresolved near-one face; the quota-bound W6 no-return is isolated and not retried before audit.
