# Formalization progress

- Decision: `scaffold`.
- Scaffold: `../../../lean-proof/SL/KpOddFirstZero_Scaffold.lean`.
- Status: `RIGOROUS_PARTIAL_RESULT`.
- Independent informal audit: `PASS`.
- Machine state: Tier 0 scaffold only, with `sorry`; not formally verified.
- Encoded strict algebra: positive off-diagonal excludes double zero, and the
  two-by-two determinant reduces to the scalar first-zero equality.
- Open declarations: branch-realizable same-sign Jacobi kernel, simultaneous
  odd/even singularity, and `KO-DET`.

The parent repository also carries the identical scaffold at
`lean-proof/SL/KpOddFirstZero_Scaffold.lean` so the existing Lean project can
compile the structural skeleton.
