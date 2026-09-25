# Author semantic self-check

This is an author explanation, not an independent blind readback or an acceptance review. The machine comparison contract was generated from the declared source signatures; its agreement cannot independently establish faithfulness to the user's intention.

I checked the extracted namespace declarations against the intended local interfaces. The scalar carrier is `Real`; both copies of the coordinate index are `Fin n`; `n` is implicit in the matrix/vector lemmas and ranges over every natural number. No invertibility premise was added to the anti/commuting or determinant statements. The root has no outside parameters or hypotheses and conjoins the 13 full universal statements. The equation `JP = -PJ` remains an explicit premise for the Jacobian application.

The coordinate model pairs the two mirrored halves. `paired_coordinate_actions` identifies the swap and the sum/difference matrix explicitly; it does not identify a NumPy array or a `Fin (2*n)` implementation. Physical reflection is an affine map on unrestricted real vectors. Its increment theorem proves the linear part `-P`; the preserving/reversing equivalences do not themselves say that a base configuration is symmetric or geometrically feasible. Zero vectors satisfy both signs.

The two determinant formulas quantify over real `L`. Positivity has the explicit hypothesis `4 ≤ L`. Unique solvability quantifies over natural `L≥4`, with the cast to `Real` visible in the export; it covers every even natural `L≥4` as a subset. `boundary_full` is explicitly block diagonal in parity residual coordinates. Identifying it with boundary traces of the four polynomial directions is a separate unformalized bridge.

The package deliberately does not claim full ODE or Sobolev formalization, certification of numerical code, independent review, or a proof of the reports' full conclusions. The human contract enumerates those limits in detail. The machine checks can establish only the stated local algebra and exact dependency closure in the recorded environment.
