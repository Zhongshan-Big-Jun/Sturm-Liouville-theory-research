---
type: tool
status: EVIDENCE
tags: [m3, large-r, asymptotic, log-correction, gap-extremals]
---

# M3 log-correction hypothesis

## 解析

For the n=2 symmetric INF branch of the adjacent-gap extremal problem
(`D_n = lambda_{n+1}-lambda_n`, box class `1<=rho<=R`, `R->infinity`), the
M3 obligation is the large-R asymptotics of the band self-consistency system.
The natural ansatz is `u = R^{-1/6}`, `k2 = K(u) u`, `k3 = K(u) u + C(u) u^5`,
`p1 = pi/2 + A(u) u^2`, `p3 = pi/4 + B(u) u^2`.

The exact truncated integer-power cascade (orders through u^7) has no
non-degenerate root near `K0 ~ 3.4553` (R-211, confirmed by bounded search
2026-08-16).  Yet the continuation data `scripts/_gapn2_largeR_big.json`
is fitted almost perfectly by

```text
K(u) ~ K0 + c u^2,   K0 ~ 3.45609, c ~ 2.92648, exponent ~ 2.01675, RMSE ~ 8e-7
```

This contradiction is the signature of a non-pure-power asymptotic, most
plausibly a log correction:

```text
K(u) = K0 + K2 u^2 + L u^2 log u + ...,
C(u) = C0 + C1 u + C2 u^2 + ... (C1 forced nonzero by the hard constant E5_5).
```

## 适用范围

- Applies only to the M3 sub-obligation of `(G1')` for the n=2 symmetric INF
  branch.
- The exact system to re-expand is `scripts/_gapn2_largeR_closed.py`
  (E1=E2=E5=E6=0) with `eps = 1/sqrt(R) = u^3`.
- The claim is a hypothesis / EVIDENCE, not a proved theorem.

## 验证与备注

- Bounded multi-start: `scripts/_tmp_p1_bounded2.py` best residual 3.5e-2,
  no K0~3.4 root.
- Fit: inline python against `_gapn2_largeR_big.json`, RMSE 8.4e-7.
- Log-linear check: `(K-K0)/u^2 ~ K2 + L log u` with `K2 ~ 2.92536`,
  `L ~ 0.04766`, correlation `~0.99999` (EVIDENCE, 2026-08-16).
- STRICT coefficient identity: under ansatz `K = K0 + K2 u^2 + L u^2 log u`
  with no log in A/B/C, the v^1 coefficients are
  `E1_2 v^1 = -sqrt(2) K0^5 L/2`, `E2_2 v^1 = sqrt(2) K0^7 L/2`,
  `E6_5 v^1 = -2 K0^6 L`, hence `L = 0` (simple K-log ansatz inconsistent).
- Source: run notes addendum 2026-08-16, run R-20260812T090000Z-g1prime-g2.
- Status: OPEN; next step is a matched-asymptotics expansion with `log u`
  in C/A/B or higher-order couplings.
