RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-K: explicit-modulus attempt

## Result

No valid rational `t_*`, `h_*`, or `y_*` cutoff can be extracted from the
currently frozen C2-C/C2-E artifacts.  The exact obstruction is now narrower
than “compactness”: the off-boundary inverse maps and normalized remainder
functions were never enclosed on a finite stable-coordinate box.

For the C2-E compensating corner this route derives the exact inverse
Jacobian

```text
J_E=h u { k/[sin(k theta)cos(k theta)]
          +1/[sin(eta)cos(eta)] } -> 1.
```

It also proves a useful exact leading majorant: all four retained boundary
polynomials satisfy `P_i<=32/pi^2<4`.  Hence an explicit bound

```text
|rho_i/h^2-P_i| <= M_E h
```

would give a dyadic `h_*` immediately.  The frozen replay, however, replaces
the exact negative angle by a truncated formal ansatz and supplies neither a
finite-box lower bound for `J_E` nor the constant `M_E`.

For the C2-C charts the implicit boundary derivatives are exactly nonzero
(`1` and `-pi^2/8`), but the required finite-chart suprema of `Psi_0,Psi_1`
and quantitative lower bounds for the `Knew`-containing denominators are
absent.  Moreover, the nontriple part of the `t=0` face was closed only by an
existential finite-subcover argument with no effective Lebesgue number.

This is a genuine information gap.  Adding an arbitrary analytic term
`M h` to a normalized remainder preserves every leading limit checked by the
existing replays while making the safe collar arbitrarily thin.  Therefore
continuity plus the frozen boundary polynomials cannot imply any prescribed
dyadic cutoff.

The exact replay in this route verifies the Jacobians, the bound
`32/pi^2<4`, and this underdetermination statement.  It performs no floating
sign test and no original-coordinate subdivision.

## Restart condition

Build full exact stable-coordinate evaluators, including the implicit angle
inverse, normalized endpoint sums, and `Knew`; certify finite-box derivative
and denominator bounds; then compute a rational Lebesgue number for every
complementary boundary patch.  Only after those data are frozen can compact
annular Arb boxes be preregistered.

```text
route_id: MIN-REFL-C2-K
status: rigorous_partial_result
cutoff_status: not_obtained
first_failing_step: no finite-chart bound for the exact normalized remainder
                    after the implicit chart inverse
coefficient_cube_consequence: no additional dyadic cell is certified
physical_bridge_status: noncanonical / not reproved
canonical_status: no propagation
formalization_status: not_requested
```

