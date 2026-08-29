# Replay validation 2026-08-29

## Environment

- Python: Codex bundled Python 3.12.
- Dependencies: `sympy==1.14.0`, `mpmath==1.3.0`.
- The frozen local dependency directory was used for this validation. The repository records exact requirements instead of vendoring third-party packages.

## Results

| Replay | Exit | Key result |
| --- | ---: | --- |
| `fresh_seed_eliminate.py` | 0 | `A0=2/kappa`, `C0=16/(pi*kappa)`, `m1diff_4=4/kappa^5`, `m3diff_4=-4/kappa^5` |
| `fresh_cascade_even4.py` | 0 | coefficient matrix rank 3; consistency `4(pi*kappa^3-18pi^2+48)/(3pi^2*kappa^2)` |
| `fresh_level4_solution.py` | 0 | `B0=1/kappa`; reduced `E6_7` residual is 0 modulo the cubic relation |
| `fresh_numeric_branch.py` | 0 | direct exact-system root replay succeeded; a default `u=0.25` root had residual about `9.9e-55` |
| `fresh_sector_numeric.py` at `u=0.06` | 0 | refined root residual about `1.9e-58`; `det Kp_odd=5.73e-23>0`; `det Ko=4.38e-30>0` |
| `fresh_sector_series_mp.py` | 0 | first powers 20 and 26; coefficient ratios exactly `1.0` at 80 displayed digits; all odd coefficients through the leading orders are 0 |

The high-precision Laurent coefficients were

```text
154.8810982642140485742150708733564569146993416361592208238515...
251.0837791992862954331951050274682742836923374834967763969446...
```

They were identical for the two higher-jet choices `k2=0` and `k2=1/3`.

## Blueprint package validation

The copied Blueprint project returned `ready`. Snapshot validation reproduced exactly

```text
blueprint: sha256:3b99f2090d73029fa77498a897979e614ddccbb205b613449fdd2181ce6ccc48
inventory: sha256:0c1e576e4902ffb8720e8a9b7c02a0df1c5425af805f1c9aba05b9968279ed5e
nodes: 9
edges: 10
inventory rows: 3
proved inferences: 3
contradictions: 0
```
