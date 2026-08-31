# Whiteboard

- Run ID: `R-20260831T020156Z-g1p-kpdet`.
- Task packet ID: `Q-20260831-g1p-kpdet`.

## Frozen target

Decide KP-DET on the exact n=2 symmetric finite-interior INF branch. Do not
claim KO-DET, non-symmetric control, or global G1 prime.

## Current strict frontier

The previous first-zero reduction is reused. The new direct theorem proves

```text
gamma_2>b_0,
(Kp_odd)22<0.
```

Therefore the sole active scalar is

```text
S_KP=a_0-gamma_1+b_0^2/(gamma_2-b_0).
```

KP-DET is equivalent to `S_KP<0`.

## Current gate

`ESCALATE`.

## Smallest useful wave

1. Exact transfer and phase elimination of `S_KP`.
2. Independent Jacobi proof or branch-realizable falsification of `S_KP=0`.

No other route is authorized in this wave.
