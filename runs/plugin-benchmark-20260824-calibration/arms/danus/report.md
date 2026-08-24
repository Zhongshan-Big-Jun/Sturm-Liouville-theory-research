# Report: Danus arm — B3 O3 root count

## Summary

The frozen task asked to prove or disprove that, for every `n>=1` and `R>1`, the transfer-matrix entry `G_{n,s}(y)` has exactly `2n` zeros in `(0,pi)`, all simple. Using the Danus-style single-session emulation (main orchestrator, worker derivation, independent verifier gates), this arm obtained a **complete STRICT proof** of the statement. No disproof was found; the statement is true.

Key mathematical simplification:
- `C_s = S E` with `E` the 1-block transfer matrix and `S` the R-block transfer matrix, hence `M_{n,s} = A^n E` with `A=ES`.
- The exact polynomial `Q_{n,s}(x)=G(arccos x)/sqrt(1-x^2)` equals `U_n(P)+s^{-1}U_{n-1}(P)`, where `P` is a quadratic with `P(-?)` parameter `alpha=s+2+s^{-1}>4`.
- Roots occur only in the elliptic region `|x|>delta`; the hyperbolic region is excluded by a positive `sinh` inequality.
- In the elliptic region, the argument `Phi(theta)=n theta+arg(e^{i theta}+s^{-1})` is strictly increasing from `0` to `(n+1)pi`, giving exactly one root per `k=1,...,n`.

## Verified facts count

**11 verified facts passed the verifier gate.** They are:

- `F1` Matrix identities for `E,S,C_s`
- `F2` `A=ES`, determinant 1, trace `2P`
- `F3` Chebyshev/Cayley-Hamilton power formula for `A^n`
- `F4` `(AE)_12 = q(alpha x^2-s)` and `alpha x^2-s = 2P+r`
- `F5` Exact polynomial form `Q_n=U_n(P)+r U_{n-1}(P)`
- `F6` Evenness and degree `2n`
- `F7` No roots in hyperbolic region `0<|x|<delta`
- `F8` Elliptic trigonometric representation and monotone argument
- `F9` Exactly `n` simple roots in `(delta,1)`
- `F10` Main theorem: exactly `2n` simple zeros in `(0,pi)`
- `F11` Boundary audits (`n=1`, `y=0`, `y=pi`, `y=pi/2`, `R=1`)

The fact graph is content-addressed under `facts/` (each file named by SHA-256 prefix; `facts/INDEX.md` maps stable IDs to files). The verifier log is in `verifier_log/VERIFIER_LOG.md`.

## Dead ends and discarded routes

1. **Direct expansion of `C_s^n`**: messy; abandoned in favor of the factorized `A^n E` form.
2. **Sturm-Liouville oscillation theorem as the main tool**: not needed; the proof is self-contained matrix/Chebyshev algebra.
3. **Interval pairing without a monotone crossing count**: insufficient to prove exact count; replaced by the strictly increasing `Phi` argument.
4. **Numerical scans**: used only for sanity checks, not as proof. Scans for `n=1..5` and `s=1.1,2,10` always showed `2n` real roots inside `(-1,1)` with `n` positive, consistent with the theorem.
5. **A claimed root in the hyperbolic region**: tested and rejected by the `sinh` positivity argument.

## First unresolved obligation

**None.** The main theorem is fully established for all `n>=1` and `R>1` under the STRICT label. The only optional follow-up would be to extend the same statement to the boundary `R=1`, which was separately audited and also holds (with the same root count), but is outside the frozen quantifier `R>1`.

## Artifacts

- `result.md` — final theorem and proof, citing facts.
- `facts/` — content-addressed fact graph.
- `global_memory/README.md` — findings, dead ends, unresolved-obligation note.
- `verifier_log/VERIFIER_LOG.md` — per-fact verifier gate logs.
- `scratch/README.md` — numerical/symbolic evidence (explicitly not proof).
