# Approach registry

| Route | Mechanism | Status | Decision delta |
|---|---|---|---|
| DIRECT-LAST-LAYER | Exact final-layer phase and Green formulas | PARTIAL | Proves `gamma_2>b_0`, hence `(Kp_odd)22<0`, and exposes scalar `S_KP` |
| JINV-MONOTONICITY | Differentiate through the full branch Jacobian | BLOCKED | Circular at the target singularity unless a separate regular chart is supplied |
| ABSTRACT-MATRIX | Use only `b_0,gamma_j>0` | CLOSED DEAD END | Abstract equality examples need not be branch-realizable |
| TRANSFER-SCHUR | Eliminate amplitudes and derivatives from `S_KP` using exact three-layer coordinates | READY AFTER GATE | Could prove or refute the remaining scalar sign |
| JACOBI-FALSIFIER | Analyze the same-sign kernel as a parity-crossing Jacobi field | READY AFTER GATE | Independent proof or exact branch-realizable witness |
| PHI-SPECTRAL-ELIM | Eliminate the outer phase from `Phi` by the two spectral equations | PARTIAL | Exact safe equivalence `Phi<0 iff Xi>0`; mass remains load-bearing |
| MASS-SLOPE-W3 | Convert exact normalization to spectral radial slopes and split `Xi` | PARTIAL | Exact `M-slope`, `K<0`, and `Xi=X^2G-rKDtheta`; bridge from mass slope to `G` or `Xi` remains open |
| GLOBAL-SIGN-COHERENCE | Factor `G` through one scalar and classify mass coefficient chambers | PARTIAL, AUDIT PASS | Exact `G=X(M Dtheta/P)(q-E)` and complete `Bcoef<0`; global scalar sign remains open |
| COMMON-BETA-ORIENTATION | Restore the unsquared common-beta orientation and close a strict chamber | PARTIAL, AUDIT PASS | Complete `0<c<=1/2` KP-DET is strict; the unique acute branch remains open |
| ACUTE-THRESHOLD | Test a scalar threshold and the degenerate collar for `c>1/2` | PARTIAL, UNREVIEWED | W14/W15 are immutable; retry only their independent joint audit after quota recovery |
