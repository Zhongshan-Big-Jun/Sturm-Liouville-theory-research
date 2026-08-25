# T1: Modified Bessel function monotonicity

For `n >= 0` integer, consider the modified Bessel ODE

    r^2 f'' + r f' - (r^2 + n^2) f = 0.

Its independent solutions are `I_n(r)` and `K_n(r)`, with `I_n` regular at `r=0`
and `K_n` singular at `r=0`. For `lambda > 0`, `l >= 2` integer, and `R > 0`,
define

    F_{lambda,l}(R)
      = l/(sqrt(lambda) R C_lambda(R)) * ( C_{1,lambda}(R)/C_{l,lambda}(R) * K_l(R) I_l(sqrt(lambda) R) - K_1(R) I_1(sqrt(lambda) R) )
        - 1/C_lambda(R) * ( C_{1,lambda}(R)/C_{l,lambda}(R) * K_l(R) I_l'(sqrt(lambda) R) - K_1(R) I_1'(sqrt(lambda) R) ),

where

    C_{j,lambda}(R) = K_j'(R) I_j(sqrt(lambda) R) - sqrt(lambda) I_j'(sqrt(lambda) R) K_j(R),
    C_lambda(R)     = sqrt(lambda) K_0(R) I_1(sqrt(lambda) R) + K_1(R) I_0(sqrt(lambda) R).

Prove:
1. `F_{lambda,l}(R)` is well-defined for all `R > 0`, i.e. `C_lambda(R) != 0` and `C_{l,lambda}(R) != 0`.
2. If `0 < lambda <= 1`, then `F_{lambda,l}(R)` is negative and monotonically increasing for `R > 0`.
3. If `lambda > 1`, there exists `R_1 > 0` such that `F_{lambda,l}` is increasing on `(0,R_1)`,
   decreasing on `(R_1, infinity)`, and `F_{lambda,l}(R_1) > 0`.

State all external facts with hypotheses; numerical evidence is not a proof.
