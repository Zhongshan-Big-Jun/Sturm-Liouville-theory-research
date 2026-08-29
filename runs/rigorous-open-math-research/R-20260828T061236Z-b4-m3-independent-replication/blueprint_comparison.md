# Post-freeze comparison with Blueprint

## Comparison boundary

The independent report, scripts, machine results, and Whiteboard checkpoint were frozen at `2026-08-28T16:29:22.9905214+08:00`. Only after that freeze was the Blueprint canonical state retrieved.

The retrieved envelope is

```text
blueprint sha256: sha256:3b99f2090d73029fa77498a897979e614ddccbb205b613449fdd2181ce6ccc48
inventory sha256: sha256:0c1e576e4902ffb8720e8a9b7c02a0df1c5425af805f1c9aba05b9968279ed5e
math closure: 4 available claims, 3 proved inferences, 0 contradictions
```

The canonical target is `CLM-SL-B4-M3-TARGET-V1`. The integration receipt is `blueprint/submissions/SUB-20260825-B4M3-FINAL-003/receipt.json`.

## Formula comparison

| Item | Independent Codex plus Whiteboard result | Blueprint canonical result | Verdict |
| --- | --- | --- | --- |
| Scale | `u=R^(-1/6)`, power-law balance `alpha=1/3` | Same scale from two exact Newton faces and analytic IFT | Exact agreement |
| Positive seed | `kappa^3=18pi-48/pi`, `A0=2/kappa`, `B0=1/kappa`, `C0=16/(pi kappa)` | Same seed and coefficients | Exact agreement |
| Parity | Even branch series, excluding `u^21` and `u^27` determinant candidates | Unique analytic germ in `v=u^2`, with odd corrections excluded | Agreement, Blueprint stronger |
| `m3D-m3N` | `-4/kappa^5 u^4+O(u^6)` | Same formula and strict large-R sign | Exact agreement |
| Upstream scalar | Seed value `3/2+4/(pi kappa)>0` | `Chi_up=3/2+4/(pi kappa)+O(u^2)>0` | Agreement, Blueprint adds uniform remainder control |
| `det Kp_odd` | `128kappa^2/pi^2 u^20+O(u^22)>0` | Same coefficient, exponent, and sign | Exact agreement |
| `det Ko` | `2048kappa^2/pi^4 u^26+O(u^28)>0` | Same coefficient, exponent, and sign | Exact agreement |

There is no substantive conflict.

## Strength comparison

Blueprint is stronger in five load-bearing respects:

1. It proves an exact locally unique real-analytic finite-R branch by two blow-ups, nonzero Jacobians, and the analytic implicit-function theorem.
2. It proves entry into and uniqueness within the admitted finite-nonzero-interior chart, excluding Puiseux, logarithmic, inverse-logarithmic, mixed, odd, flat, and non-transseries alternatives there.
3. It computes the branch one-jet and both full determinants in an exact algebraic coefficient field, with omitted-jet and guard-order audits.
4. It proves a single existential finite `R0` controlling all four signs on exact roots.
5. It diagnoses the historical staged D-side mass power error that produced the false odd-correction obstruction.

The independent run adds different evidence:

1. It is a blind replication completed before reading the Blueprint result.
2. It uses a separately written symbolic cascade and a separate full transfer-Jacobian implementation.
3. It exposes the rank-one determinant cancellations and first-versus-third mass cancellation directly.
4. It supplies finite-u regression data independent of the exact Blueprint replay implementation.

The accurate combined description is: the independent run is a blind symbolic-computational replication of the stronger accepted Blueprint theorem, not a replacement proof.

## Resource accounting

| Run | Wall time | Token record | Coverage |
| --- | ---: | ---: | --- |
| Codex plus Whiteboard independent replication | `02:16:46.798`, or `8206.798828` seconds | Exact total unavailable because no goal token tracker was active | Independent derivation, formal and finite-u checks, report, Whiteboard checkpoint |
| Blueprint closed loop | `08:43:55.654`, or `31435.654` seconds | `1556831` tracked tokens at the final pre-close checkpoint; final authoritative total was not stored in the artifact | Multi-route research, exact certificates, gap audit, immutable proposal, independent review, deterministic integration, post-integration verification |

Blueprint used about `3.83044` times the independent wall time. The comparison is not an efficiency ranking because Blueprint covered theorem-grade closure, review, and integration, while the independent run did not expose an exact token count.
