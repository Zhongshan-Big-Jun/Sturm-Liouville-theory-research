# Report

## Status

**Complete.** The frozen task is proved in full: for every n >= 1 and
R > 1, G_{n,s} has exactly 2n zeros in (0, pi), all simple.

## Main idea

The transfer matrix problem reduces to a one-line Chebyshev identity:

    G_{n,s}(y) = sin(y) [ U_n(T(y)) + s^(-1) U_{n-1}(T(y)) ],
    T(y) = cos^2(y) - (s + s^(-1))/2 sin^2(y).

The factor in brackets is a degree-n polynomial F_n(T) =
U_n(T) + s^(-1) U_{n-1}(T). Its zeros are characterized by writing
T = cos(theta) and using the argument of s^(-1) + e^{i theta}; a
strictly-increasing phase argument gives exactly n simple zeros in
(-1, 1). Since T(y) is an increasing affine function of cos^2(y), each
such T corresponds to two y in (0, pi), yielding exactly 2n simple zeros.

## Artifacts

- `result.md` contains the full proof, including the polynomial formulation
  Q_{n,s}(x) and the requested audits (n = 1, y = 0, y = pi, y = pi/2,
  boundary R = 1).
- Scratch files `scratch_check.py`, `scratch_roots.py` in the arm root were
  used only for numerical/symbolic sanity checks and are not part of the
  proof.

## What remains

Nothing for the stated theorem. The proof is uniform in n and R and does
not rely on finite scans or external numerical evidence.

## Caveat

The boundary R = 1 is outside the hypothesis R > 1 and is reported as an
audit only; it is not needed for the main theorem.
