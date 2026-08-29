# Problem contract

## Frozen target

Re-derive the large-R behavior of the exact four-equation n=2 symmetric INF system on the nondegenerate finite-interior branch. Determine:

1. The branch scale and positive seed.
2. The leading term and sign of `m3D - m3N`.
3. The leading upstream consistency scalar.
4. The first nonzero asymptotic term and sign of the two full sector determinants `det Kp_odd` and `det Ko`.
5. Whether the previously proposed odd R-exponents can occur.

Use

```text
epsilon = R^(-1/2)
u = R^(-1/6)
```

and the exact branch coordinates

```text
k2 = u K(u)
k3 = u K(u) + u^5 C(u)
p1 = pi/2 + u^2 A(u)
p3 = pi/4 + u^2 B(u).
```

## Permitted inputs

- The exact pre-existing equations `E1 = E2 = E5 = E6 = 0`.
- The source definitions of the two sector matrices and their basis conventions.
- The original task packet's statement of the open M3 obligations.

## Isolation boundary

Before the independent report was frozen, this run did not read or use:

- `blueprint/blueprint.json` or `blueprint/evidence_inventory.csv`.
- Any Blueprint proposal, validation, review, receipt, proof package, or research artifact.
- Any recovered Blueprint output, benchmark answer, or comparison report.

The exact model and sector definitions were shared inputs. The derivation and implementation were independent, but the original model transcription was not independently sourced.

## Acceptance criteria

- Symbolic seed compatibility must be derived from the exact equations.
- Determinants must be reconstructed from the full five-layer transfer system, not inferred from a stored asymptotic formula.
- Numerical work must remain labeled `EVIDENCE` or `VERIFIED_REPLICATION` and cannot close the theorem by itself.
- Any comparison with Blueprint must occur only after the independent report and Whiteboard checkpoint are frozen.

## Scope boundary

The replication concerns the finite, nonzero, nonresonant interior chart with the specified n=2 symmetric INF topology. It does not classify singular limits with `K -> 0`, `K -> infinity`, nonunit `k3/k2`, collapsed phase denominators, or other modal topologies.
