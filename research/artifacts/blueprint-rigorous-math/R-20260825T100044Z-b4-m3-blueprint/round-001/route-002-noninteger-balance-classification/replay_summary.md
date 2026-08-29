# Replay summary and command log

All commands ran from `E:\ai_benchmark\source_repo` with the Windows Store
Python 3.11.9 executable recorded in `reproducibility_manifest.json`.

## Hash verification

The six observed source hashes exactly matched the frozen contract:

```text
problem_contract.md                 1de731ba...2700148
run_notes_addendum_2026-08-14.md    a4b5c8b7...1d7284cb
_gapn2_largeR_closed.py             e357d8e4...8ac13a4
_gapn2_largeR_Pbuild.py             58c98af4...b62ea6caea
_gapn2_largeR_big.json              1e3c924b...f0d66f45
SL_gap_nge2_symmetry_local_proof.tex 6c2029fb...9efe0a
```

## Defective staged replay

Command: run `replay_coefficients.py`.

Key exact output from the bound staged helper:

```text
E1[0]=-sqrt(2)*(A*K-2)/4
E2[0]= sqrt(2)*(A*K-2)/4
E6[3]=-A*K+2
E5[5]=1/(2*K^2)
```

The first three identities agree with the original residual. The fourth does
not, for the D-half-mass power-shift reason in `normalization_audit.md`.
Therefore no conclusion using staged `E5` coefficients was retained.

## Corrected exact face

Command: run `corrected_bounded_general.py`.

Key exact output:

```text
F1=-sqrt(2)*(K^3+6*K*q-18*pi+24)/(24*K)
F2= sqrt(2)*(3*pi*C*K+K^3+6*K*q-18*pi-24)/(24*K)
F6=-(3*pi*C*K+2*K^3+12*K*q-36*pi)/(12*K)
q0=-(K^3-18*pi+24)/(6*K)
C0=16/(pi*K)
H6=8*(B*K-1)/K^2
H5=2*(6*pi^2*B*K+pi*K^3-24*pi^2+48)/(3*pi*K^6)
resultant_B=16*K*(pi*K^3-18*pi^2+48)
```

Command: run `seed_rank_check.py`.

```text
FIRST_JACOBIAN=-pi/16
SEED_EQUATION=(pi*K^3-18*pi^2+48)/pi
SEED_DERIVATIVE=3*K^2
K0=3.4557641714085382002415793930295412437596203215540
```

Algebraic substitution of the seed relation in the printed second Jacobian
gives `16/K0^5>0`.

## High-precision original-residual reconciliation

Command: run `high_precision_residual_check.py` with mpmath 1.3.0 at 100
decimal digits.

At `K=3`, after the first-face substitutions, the staged prediction is
`-1/(6K^2)=-0.0185185...`, whereas the direct original residual gives

```text
u=1e-4   E5/u^4=3.0741821149e-9
u=1e-8   E5/u^4=3.0741821821e-17
u=1e-12  E5/u^4=3.0741821821e-25
```

so the exact limiting coefficient is zero.

At the corrected common seed, the first uncancelled displayed residuals have
the predicted higher orders:

```text
E1=O(u^6), E2=O(u^6), E6=O(u^9), E5=O(u^8).
```

At the off-seed point `K=3,B=0.37`, the exact predictions and direct limits
are

```text
H6= 0.097777777777777777777777777777777777777777777777778
E6/u^7 at u=1e-9
   =0.097777777777777785916133024815302236506475073740652

H5=-0.011153490696319215840081751241248469370526558202177
E5/u^6 at u=1e-9
   =-0.011153490696319215607788456028200643594845846321775
```

These decimal checks are evidence for transcription fidelity, not the proof
of the exact identities.

## Continuation evidence

The bound JSON contains 270 rows. Its last row has

```text
R=89895.8770666598, u=0.149408981192478,
K=3.51937425428511, A=0.565322729161273, B=0.280215260655945,
D*R=10.8806266871887.
```

The exact seed lies in the direction of the recorded trend, but no row,
fit, or extrapolation is used in the proof.

## Failed computation retained

`general_phase_chart.py` attempted an untruncated monolithic symbolic series
and was interrupted after SymPy expansion became impractical. The bounded
piecewise truncation in `general_phase_chart_fast.py` replaced it with an
auditable power budget. No result from the failed computation was promoted.

