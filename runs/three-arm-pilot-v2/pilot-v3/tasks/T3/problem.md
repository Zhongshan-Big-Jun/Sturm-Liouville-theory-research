# T3: Return probability for lamplighter walk on regular tree

Let `d >= 3` and let `T_d` be the infinite `d`-regular tree.
Let `G = Z_2 wr T_d` be the lamplighter group, and let `mu` be the
switch-walk-switch measure on `G`. Let `p_n(x,y)` denote the `n`-step
transition probability, and `p_{2n}(e,e)` the return probability at the identity.

Let

    rho_d = 2 sqrt(d-1) / d.

Prove the exact asymptotic: there exists `C > 0` and `epsilon(n) = o(1)` such that

    p_{2n}(e,e) = rho_d^{2n} * exp( - (C + epsilon(n)) * n / log^2 n ),

as `n -> infinity`. You may use the fact that the spectral radius of the random walk
on `G` is `rho_d`, but must state it as an external fact with hypotheses.
Do not cite unpublished work.
