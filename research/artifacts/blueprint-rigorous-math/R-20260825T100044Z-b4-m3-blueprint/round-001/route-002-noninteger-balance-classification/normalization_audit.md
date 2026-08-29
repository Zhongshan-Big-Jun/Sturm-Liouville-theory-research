# Exact mass-normalization audit

## Scope and bound sources

This audit compares only the two hash-bound sources
`scripts/_gapn2_largeR_closed.py` (SHA-256
`e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4`)
and `scripts/_gapn2_largeR_Pbuild.py` (SHA-256
`58c98af44d074bdfd9412a1541d4a7a393f0cf3e074653c1108964b62ea6caea`).
No conclusion or artifact from another route was inspected.

## Exact discrepancy

The closed residual defines, on the D side,

```text
a = eps*sin(p1)/k,
b = cos(p1)/k,
mL = (a^2+b^2)*p2/(2*k)
   + (a^2-b^2)*sin(2*p2)/(4*k)
   + a*b*(1-cos(2*p2))/(2*k).
```

With `eps=u^3` and `k=K*u`, the exact series shifts are therefore

```text
a:       u^2*sin(p1)/K,
b:       cos(p1)/(K*u),
p2/k:    (p2/u)/K,
1/k:     u^(-1)/K.
```

The bound P builder instead performs the following D-side operations:

- line 94 multiplies `cos(p1)` by `u` (`{1: ...}`), whereas division by
  `K*u` requires an exponent shift by `-1`;
- lines 104--105 first form `p2/u` and `sin(2*p2)/u`, then multiply each by
  another `u`; the final multipliers must have exponent `0`, not `1`;
- lines 106--107 multiply the cross term by `1/(2K)` at exponent `0`, whereas
  the exact `1/(2k)` requires exponent `-1`.

The N-side code provides an internal control: line 120 shifts `cos(p1t)` by
`-1`, and line 127 represents `1/k3` with exponent `-1`. Those are the shifts
required by the exact closed formula.

## Consequence for the recorded cascade

The staged P builder's D half-mass is not the D half-mass in the frozen exact
residual. Consequently its claimed hard coefficient `P['E5',5]=1/(2*K^2)`
and all deductions from that coefficient are not admissible proof inputs.
In particular, the asserted forced odd pair `(K1,C1)` and the even-only
contradiction are cancelled by replay of the original residual.

For the exact residual, after `A*K-2=q*u^2`, the first-face relations

```text
q = (18*pi-24-K^3)/(6*K),
C = 16/(pi*K)
```

give `E5/u^4 -> 0`, not `-1/(6*K^2)`. The 100-digit direct check in
`high_precision_residual_check.py` shows the purported coefficient differs
from the exact residual by a nonzero limiting amount, while the corrected
secondary coefficients `H6` and `H5` agree off seed to 40+ displayed digits.

## Epistemic classification

- The line-by-line power count above is a proof of a source-normalization
  mismatch.
- The corrected coefficient identities are exact formal computation from a
  direct transcription of the closed residual.
- The 100-digit limits are evidence and an adversarial transcription check;
  they are not used as proof of the identities.
- This audit does not edit or replace either bound source.

