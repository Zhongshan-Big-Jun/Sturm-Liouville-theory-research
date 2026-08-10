# Failure patterns (recorded, reusable)

1. Itemwise monotonicity traps: B-D is NOT q-monotone even though A-C is (counterexample
   c=0.01, q 5000->20000). Never close a proof on grid-verified itemwise monotonicity alone.
2. Coarse-grid corner values: handoff tables (2.8086/-0.3751/2.4258) were coarse-grid;
   exact corner limits are 2.80613/-0.38773/2.41840. Always resolve corner limits analytically.
3. Secular equation sign errors: odd secular is q*tan(s2u)+tan(s2qv)=0, not tan(s2u)tan(s2qv)=-q.
4. Normalization square-root placement: zero condition is sqrt(N2)sin(alpha1)=sqrt(N1)sin(alpha2).
5. Numerical full-grid pass != theorem: every computational claim needs a proof bridge or certificate.
6. PowerShell heredoc Chinese corruption: always write UTF-8 no-BOM .py files, then execute.
7. Periodic-extension cell merging: unmerged cell-boundary blocks produce spurious jumps that
   falsely refute MW periodicity; merge same-value neighboring cells.
8. Table cross-fill: docs/SL_gap_extremals.tex tab:rscan SUP u-column was mis-filled with INF
   values; verify tables against independent solvers.
9. Oversold convergence claims: do not claim a fixed-point iteration is a global contraction
   (T has spectral radius 1.64 at R=100 with a genuine 2-cycle).
10. Itemwise product lower bounds: u_j >= (A_j/c) u_{j-1} fails; use monotonicity + ratio method.
