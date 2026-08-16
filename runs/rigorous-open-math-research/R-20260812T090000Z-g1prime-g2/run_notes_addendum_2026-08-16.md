# Run addendum 2026-08-16 (P1 attempt): bounded seed search and log-correction evidence

Continuation of M3/P1.  All numerics are EVIDENCE unless marked STRICT.

## 1. Bounded multi-start confirms the truncated integer-power seed has no non-degenerate root

Using the exact pre-cleared 8-equation seed (E1_2, E2_2, E6_5, E5_4, E5_5,
E5_6, E5_7, E6_7) with a0=2/K0 and a1=-2K1/K0^2 enforced, we ran
`scripts/_tmp_p1_bounded2.py` with bounds K0 in [1,10] and 20 random starts.
Best bounded least-squares residual was 3.5e-2 at K0 ~ 1.008; no start
converged to K0 ~ 3.4.  This is independent confirmation of the R-211
conclusion: the truncated integer-power system through order u^7 does not
have the physical branch root at K0 ~ 3.4553.

## 2. Continuation data is extremely well fitted by K = K0 + c u^2 (u = R^{-1/6})

Fitting `scripts/_gapn2_largeR_big.json` (R = 6908..89895) to
K(R) = K0 + c u^alpha gives:

    K0    ~ 3.45609479
    c     ~ 2.92648014
    alpha ~ 2.01674753
    RMSE  ~ 8.38e-07

The exponent is numerically close to 2, so the data is consistent with an
even leading correction K ~ K0 + K2 u^2.  This is the same even-only fit
(K0 ~ 3.4553, K2 ~ 2.937) that is NOT a root of the truncated system.

## 3. Interpretation and next route

The apparent contradiction indicates that the true large-R expansion of the
n=2 symmetric INF branch is not a pure integer-power series in u at the
orders tested (or the integer-power series has coefficients that cannot be
determined independently of log terms).  The natural next rigorous route is
a log-corrected / matched-asymptotics ansatz, e.g.

    K(u) = K0 + K2 u^2 + L u^2 log u + ...,
    C(u) = C0 + C1 u + C2 u^2 + ... (with C1 forced nonzero by E5_5),

and re-expansion of the exact closed 4-equation system
(`scripts/_gapn2_largeR_closed.py`) including log u terms.  This is the
recorded P1 obstacle; M3 remains NOT closed.

## Scripts

- `scripts/_tmp_p1_bounded.py`, `scripts/_tmp_p1_bounded2.py` -- bounded
  multi-start searches (EVIDENCE).
- Fit used inline python against `scripts/_gapn2_largeR_big.json`.
