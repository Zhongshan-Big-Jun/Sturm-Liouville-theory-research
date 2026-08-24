# Report

## Summary

I solved the frozen benchmark problem in the negative direction.

**Result:** No. For every nonzero smooth mean-zero `theta_0` on `T^2` and
every time-dependent shear `u in L_t^infty(W_y^{1,1}(T))` satisfying
`int_T |partial_y u(y,t)| dy <= C`, the solution satisfies a universal
polynomial lower bound

    ||theta(t)||_{dot H^{-1}_{x,y}} >= c / (1 + t^2)

for some `c > 0` depending on `theta_0` and `C`. Therefore exponential
decay `<= C_1 e^{-C_2 t}` is impossible.

The final proof is in `result.md`.

## What remains

Nothing remains for the stated problem if the proof survives an independent
audit. Because the task explicitly forbade spawning nested subagents, I could
not run a fresh-context independent adversarial audit; I performed an internal
self-audit instead. The label is therefore `CANDIDATE_COMPLETE_PROOF`, not
`INDEPENDENTLY_AUDITED_PROOF`. A human or a later allowed independent verifier
can audit the short argument.

## Main proof idea

1. Since `u` depends only on `y`, the solution is
   `theta(x,y,t) = theta_0(x - U(y,t), y)` with `U(y,t)=int_0^t u(y,s)ds`.
2. Fourier in `x` decouples: the `k`-th mode is
   `e^{-ik U(y,t)} F_k(y)`.
3. The `k=0` mode is frozen, so exponential decay already forces
   `F_0 = 0`; then some `k != 0` has `F_k != 0`.
4. Because `||partial_y U||_{L^1} <= C t`, the phase-modulated profile
   `g=e^{-ikU}F_k` is in `W^{1,1}` with variation growing at most linearly.
5. A `W^{1,1}` function with variation `V` has a low-frequency projection
   at least `~L^2 - O(V^2/N)`, giving
   `||g||_{H^{-1}_y} >= c(L)/(1+V^2) >= c'/(1+t^2)`.
6. The single nonzero mode contribution dominates the full `H^{-1}` norm;
   polynomial lower bound contradicts exponential decay.

## Artifacts in arm root

- `result.md` — final proof and strictness labels
- `report.md` — this report
- `problem_contract.md` — contract used
- `research_ledger.md` — brief route log
- `audit_report.md` — internal self-audit record

## Complete?

I am **complete** for the requested deliverable: a rigorous negative proof
has been produced and written to `result.md`. If an external independent
audit is later run, the status can be upgraded from
`CANDIDATE_COMPLETE_PROOF` to `INDEPENDENTLY_AUDITED_PROOF`.
