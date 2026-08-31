# Approach registry

| Route | Mechanism | Status | Decision delta |
|---|---|---|---|
| DIRECT-LAST-LAYER | Exact final-layer phase and Green formulas | PARTIAL | Proves `gamma_2>b_0`, hence `(Kp_odd)22<0`, and exposes scalar `S_KP` |
| JINV-MONOTONICITY | Differentiate through the full branch Jacobian | BLOCKED | Circular at the target singularity unless a separate regular chart is supplied |
| ABSTRACT-MATRIX | Use only `b_0,gamma_j>0` | CLOSED DEAD END | Abstract equality examples need not be branch-realizable |
| TRANSFER-SCHUR | Eliminate amplitudes and derivatives from `S_KP` using exact three-layer coordinates | READY AFTER GATE | Could prove or refute the remaining scalar sign |
| JACOBI-FALSIFIER | Analyze the same-sign kernel as a parity-crossing Jacobi field | READY AFTER GATE | Independent proof or exact branch-realizable witness |
