# General weighted L2 bridge, independent intended contract

The density remains any measurable real function bounded above and below by
positive finite real constants almost everywhere on (0,L), with L>0. No
continuity or finite partition of the density is assumed. For every complex
function continuous on [0,L], prove that its actual weighted L2 class exists
and that the squared quotient norm equals integral_0^L rho(x)*norm(u(x))^2.
The upper bound must be used to prove finite L2 membership. The lower bound
must justify that the ofReal density in the measure agrees with the signed
real density in the mass almost everywhere. This is a model/norm bridge;
it does not prove existence or completeness of the eigenfunction spectrum.

Independently specified root before construction:

`forall (Length : Real) (LengthPos : 0 < Length)
  (Rho : SL.Weighted.Density Length) (Value : Real -> Complex)
  (Regular : ContinuousOn Value (Set.Icc 0 Length)),
  norm (SL.Weighted.weighted_vector Rho Value Regular)^2 =
    SL.Weighted.mass Length Rho.value Value`

Source model: docs/SL_ratio_proof.tex (positive bounded measurable density)
and docs/SL_bounded_direction_spectral_tail.md Section 1 (weighted mass).
