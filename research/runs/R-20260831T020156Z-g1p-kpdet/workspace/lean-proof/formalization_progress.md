# Formalization progress

## Obligation map

| Informal obligation | Lean declaration | Status |
| --- | --- | --- |
| P1 positivity algebra after the trigonometric gap identities | `pivot_bracket_positive` | Closed algebraic core |
| P2 determinant and Schur equivalence | `schur_sign_equivalence` | Closed |
| P3 exact phase expression | `phasePhi` | Definition only |
| P3 full admissibility and `Phi<0` | `ExactFivePhaseSystem`, `phi_sign_open` | Scaffold, open |
| P4 Jacobi geometry | None | Informal audit only |
| Global `KP-DET` | None | Open |

The placeholder `ExactFivePhaseSystem` records only elementary domain inequalities. It is intentionally insufficient for `Phi<0`; the spectral, band, mass, and mode-index equations must be formalized before the open theorem can be trusted.
