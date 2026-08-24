# Problem contract

## Objects and definitions

- Domain: `T^2 = [-pi, pi]^2` with periodic boundary conditions.
- Unknown: `rho(t, x, y)`, real or complex valued.
- Equation as written in `task.md`:
  `d_t rho + U(t,y) d_x rho = D rho`.
- `rho(0,.)` is in `L^2_{x,y}`, is mean-zero, and is not the zero function.
- `U(t,y)` is real valued and satisfies `||U||_{L^\infty_t L^2_y} < infinity`.
- `weak solution` is not defined further in the task; we take it to mean a
  distributional solution obtained from the standard energy method for the
  stated linear parabolic problem when `D` is a diffusion operator.

## Hypotheses

- H1: `rho(0,.)` is mean-zero on `T^2` and nonzero.
- H2: `rho(0,.)` is in `L^2(T^2)`.
- H3: `U` satisfies `||U||_{L^\infty_t L^2_y} < infinity`.
- H4: `D` is a dissipation operator. The statement does not define `D`
  precisely. The two readings considered in this run are:
  - (A) `D = Delta = d_x^2 + d_y^2` (isotropic Laplacian).
  - (B) `D = d_y^2` (anisotropic y-only diffusion).
  Without specifying `D`, the claim is not formally well posed.

## Target conclusion

For the weak solution `rho`:

`liminf_{t -> infinity} ||rho(t)||_{dot H^{-1}} / ||rho(t)||_{L^2} > 0`.

Here `dot H^{-1}` is the homogeneous Sobolev space on `T^2`, with Fourier
multiplier `|k|^{-1}` on nonzero frequencies.

## Quantifiers and dependency of constants

The positive lower bound may depend on `rho(0,.)`, `U`, and `D`. It is not
required to be uniform in the initial data or in `U`.

## Equivalent formulations

- If `rho(t) != 0`, the conclusion is equivalent to
  `liminf_{t -> infinity} ||rho(t)||_{L^2} / ||rho(t)||_{dot H^{-1}} < infinity`.
- For a single Fourier mode `k`, the ratio is `1/|k|`; hence the conclusion is
  a statement that the "typical wavenumber" of the solution does not diverge
  to infinity along a sequence of times.

## Boundary and degenerate cases

- If `rho(0,.)` has finite Fourier support, the ratio at `t=0` is positive and
  the conclusion is plausible from spectral damping; this case is not the
  difficult one.
- If the support in `x` is just the zero mode, the pure heat equation in `y`
  has the same structure; the conclusion is then governed by the minimal
  nonzero `y` wavenumber present.
- If `U` is identically zero, the problem reduces to the linear heat equation
  and is strictly solvable.

## Permitted outcomes

- affirmative proof
- negative proof / counterexample (if the statement is false under a reading)
- rigorous partial theorem with exact remaining gap
- reduction to a smaller open core

## Completion criteria

A complete solution must identify `D` and prove the displayed liminf under
exactly the stated regularity of `U` (`L^\infty_t L^2_y`) and a weak solution
notion. If this is not achieved, the result must say so explicitly.

## Results that do not count as completion

- Numerical simulations of truncated Fourier systems.
- A proof under extra regularity on `U` (for example boundedness or
  smoothness) without a passage to the stated assumptions.
- A proof that only handles `U = 0`.
- A proof that silently redefines `D` or the `H^{-1}` norm.

## Tool, citation, and search constraints

- No repository inspection, no git history, no internet searches, no known
  solution to this exact problem.
- Literature results may be used only if stated with exact hypotheses and a
  precise citation.

## Ambiguities or competing interpretations

- `D` is undefined in the task text. The main ambiguity is whether `D` is the
  full Laplacian or a degenerate y-only diffusion. Both are analyzed in the
  result file.
- "Weak solution" is not formalized. The energy identity used in the reduction
  is valid for the standard weak solution of the parabolic initial-value
  problem.

## Contract audit

The contract above is the honest reading of `task.md`. The ambiguity about
`D` and the weak-solution notion must be preserved in the final result.
