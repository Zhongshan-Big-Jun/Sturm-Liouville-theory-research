# Approach Registry - K(1) strict anchor run

Run: `R-20260824T184147Z-k1-e4-ab`

| Route | State | Exact outcome |
|---|---|---|
| R1: factorial scaling and second differences | SUCCEEDED | The third-order recurrence factors as `d_j = c_j d_{j-1}` with `c_j = 1/(2(j-1)(2j-1))`. |
| R2: finite backward summation | SUCCEEDED | Exact positive finite formula for every `mu_j^(N)` and `mu_0^(N) > 0`. |
| R3: fixed-index limit | SUCCEEDED | Positive factorial tails converge to the normalized minimal solution. |
| R4: minimal-branch uniqueness | SUCCEEDED | The scaled solution space is `A + B j + C phi_j`; the subfactorial branch is one-dimensional. |
| R5: asymptotic tail bound | SUCCEEDED | The first tail term gives `e/4`; the remaining positive tail is `O(j^-2)` after multiplication by `j^3`. |
| R6: endpoint audit | SUCCEEDED | `j=3`, the terminal step, signs, and the `N=3` case agree exactly. |

The Blueprint arm explored multiple routes and performed an internal fresh
mathematical review.  The independent post-run review was conducted on
neutralized outputs after both solver arms had terminated.
