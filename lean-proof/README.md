# lean-proof

Formal verification (Lean 4 + mathlib) of theorems from the Sturm-Liouville
theory research project. Each file documents the source document it formalizes.

## Project setup

- Lean toolchain: `lean-toolchain` (Lean 4.31.0, mathlib v4.31.0).
- Build: `lake build` (first run downloads/compiles mathlib).
- Each file is standalone: `lake env lean SL/<File>.lean`.

## Formalized results

| File | Source | Content | Status |
| --- | --- | --- | --- |
| `SL/MomentGrowth.lean` | `docs/SL_h2_completeness_proof.tex` | Growth lemma of the moment-jump method: for c > 0 the sequence u (c u_j = A_j u_{j-1} - B_j u_{j-2}, A_j = 2j(2j-1)+cj/(j-1), B_j = 2j(2j-3)) satisfies u_j > 0, u_j <= u_{j+1}, and u_j >= (4/c)^(j-1) j! | done |
| `SL/BalancedPhase.lean` | `docs/SL_ratio_proof.tex`, `tools/balanced-phase.md` | Balanced-phase closed forms: theta = arccos(s/(s+1)) satisfies the sup-configuration secular equation; arccos(-s/(s+1)) = pi - theta; nu(R) closed form; roots of the secular equation in (0, pi) are theta and pi - theta; tan^2 phi = s(s+2) for phi = arccos(1/(s+1)); lambda_1/lambda_2 phase identities | done |
| `SL/KcPolynomial.lean` | `docs/SL_h2_completeness_proof.tex` (Lemma 4.1) | K_c action on the H^2 polynomial basis: K_c p_{2n} = c x^{2n} - A_n x^{2n-2} + B_n x^{2n-4}, K_c p_{2n+1} = c x^{2n+1} - A'_n x^{2n-1} + B'_n x^{2n-3}, and A_n - B_n = 4n + cn/(n-1) (algebraic core of the moment recurrence) | done |

## Roadmap (candidates for next files)

- Moment recurrence c mu_{2j} = A_j mu_{2j-2} - B_j mu_{2j-4} (needs L^2 moments / inner products).
- Mahar-Willner periodic extension and zero-truncation lemmas (analysis heavy).
- The full H^2 completeness theorem (functional analysis: isometry K_c, Weierstrass density).
- Inf ratio = 1 via Weyl asymptotics.
- Keller/MW two-step extremal proof structure.

## Honesty notes

- Formalized statements are theorem-for-theorem transcriptions of the cited
  project documents. Where the source document marks a result as numerical
  evidence or conjecture, it is NOT claimed here as a theorem.
- Remaining work is large; "all proofs formalized" is a long-term goal.
