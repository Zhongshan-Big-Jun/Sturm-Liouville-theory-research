RIGOROUS_PARTIAL_RESULT

# Audited failure of the bound `_gapn2_largeR_Pbuild.py` E5 series

## Verdict

The hash-bound series builder is not faithful to the hash-bound exact closed
mass formula in the D-side left-block term. Therefore its E5 coefficients,
including the recorded hard `E5_5` term, must not be used as proof evidence.
The repository source was not modified.

## First invalid step

In `scripts/_gapn2_largeR_closed.py` (SHA-256
`e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4`),
the D-side left-block coefficient is

```text
b = cos(p1)/k2 = cos(p1)/(K*u).
```

Thus a coefficient of degree `m` in `cos(p1)` must be shifted to degree
`m-1`. In `scripts/_gapn2_largeR_Pbuild.py` (SHA-256
`58c98af44d074bdfd9412a1541d4a7a393f0cf3e074653c1108964b62ea6caea`),
line 94 instead implements

```text
b1 = mul(s_cos_p1, {1: 1}, Nmax) / K,
```

which shifts `m` to `m+1`. The same file's N-side code at lines 120-121 uses
the correct `m-1` shift, making the asymmetry directly auditable. In addition,
the D-side assembly at lines 104-107 does not apply the required
`1/k2=1/(K*u)` shift of `-1` to all three left-mass terms; the N-side code
does apply an explicit `inv_k3` beginning at degree `-1`. Line 94 is the first
invalid step, but the complete D-side `mL` block must be regenerated rather
than repaired by changing that line alone.

## Exact affected identities

After the forced coordinate `A=(2+u^2 D)/K`, the invalid builder and an
independent staged expansion of the exact closed formula agree on E1, E2, and
E6 but differ on E5 as follows:

```text
(E5/u^4)_builder - (E5/u^4)_exact = -1/(6*K^2),
(E5_5)_builder = 1/(2*K^2),
(E5_5)_exact = 0.
```

Equivalently, the builder inserts `+96*K^3` into the numerator that is absent
from the exact formula. Under

```text
C=16/(pi*K),
D=-(K^3-18*pi+24)/(6*K),
```

the builder produces the spurious obstruction `E5/u^4=-1/(6*K^2)`, whereas
the exact expression is identically zero.

## Independent checks

- `finite_r_replay.py`, SHA-256
  `d929f0eb0c84cd6cd26515e93928c23fff2126c79876fa03cc75794a07515a56`,
  imports and replays the bound builder and emits the invalid values above.
- `finite_r_direct_check.py`, SHA-256
  `d38ba50947a95a8c47bd3faa03f2ddfc0b742408b21ece638fbdf8cab500eac2`,
  independently re-encodes the exact closed formula and uses staged exact
  Taylor arithmetic; it emits the corrected cancellation and `E5_5=0`.
- A 100-decimal direct evaluation at `K=3`, `B=1/5` and the exact first-blow-up
  relations gives `E5/u^4` at `u=1/20,1/40,1/80,1/160` as approximately
  `7.636e-4,1.918e-4,4.801e-5,1.201e-5`, decreasing by a factor close to four
  on each halving. This is consistent with a zero endpoint and an `O(u^2)`
  next term, and inconsistent with convergence to `-1/54`. This numerical
  sequence is a falsification check only; the exact coefficient comparison is
  the certificate.

## Consequences and restart condition

The addendum statements that `E5_5` is a hard nonzero constant and that an odd
component is forced are refuted for the exact closed residual. The corrected
route must start from the direct closed formula or from a repaired, separately
validated series implementation. The restart condition is a regeneration of
the complete D-side left-mass block followed by an exact equality check of
every generated E5 coefficient against the closed mass formula before any
cascade or numerical seed solve. The corrected direct derivation is carried
through the finite branch theorem in `candidate_branch_proof.md`.
