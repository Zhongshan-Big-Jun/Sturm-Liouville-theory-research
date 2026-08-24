# Problem contract

## Objects and definitions
- Torus T^2 = R^2/(2pi Z)^2 with period 2pi in each coordinate.
- theta_0 in C^infty(T^2), nonzero, mean zero on T^2.
- u(y,t) in L_t^infty(W_y^{1,1}(T)); equivalently there is C such that
  int_T |partial_y u(y,t)| dy <= C for a.e. t.
- theta solves theta_t + u(y,t) partial_x theta = 0, theta(x,y,0)=theta_0.
- Norm:
  ||theta||_{dot H^{-1}_{x,y}}^2 = sum_{|n|>0, n in Z^2} (1/|n|^2) |hat theta(n,t)|^2,
  with |n|^2 = n_1^2+n_2^2.

## Hypotheses
- theta_0 smooth, periodic, mean zero, nonzero.
- u periodic in y, W^{1,1} in y uniformly in t with derivative L^1 bound.

## Target conclusion
Determine: does there exist such theta_0 and u with
  ||theta||_{dot H^{-1}} <= C_1 e^{-C_2 t}
for some constants C_1,C_2?

## Quantifiers and dependency of constants
- A "Yes" answer requires explicit choice of theta_0,u and constants C_1,C_2.
- A "No" answer must hold for every theta_0,u under the hypotheses;
  constants in any lower bound may depend on theta_0,C,k.

## Boundary and degenerate cases
- k=0 (x-independent) mode is time-invariant; must be handled.
- theta_0 may have only x-independent nonzero modes; still no exponential decay.
- u may have arbitrary y-independent part; it does not produce mixing.

## Permitted outcomes
- affirmative proof (explicit construction)
- negative proof (universal impossibility)

## Completion criteria
A complete admissible outcome is either a verified explicit construction with
exponential decay, or a rigorous proof that exponential decay is impossible
for all admissible theta_0,u.

## Answer space
The result must support exactly one of the two permitted outcomes.

## Forbidden moves
- Numerical evidence as proof.
- Silent use of a recalled theorem without stating hypotheses.
- Inspecting repository/git history/internet or known solution.

## Contract audit
- The problem is unambiguous; one interpretation likely.
- Fourier normalization affects only constants and not the exponential-vs-polynomial
  dichotomy.
