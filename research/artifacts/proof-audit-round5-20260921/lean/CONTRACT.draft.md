# Fifth-round Lean author contract

Role: mathematical formalization author, not an independent reviewer. This contract describes local real-polynomial algebra and does not certify the supplied analytic proof. Independent blind readback and correspondence review are pending coordinator dispatch.

## Informal sources and scope

The supplied `cofinite_replacement_proof.md`, sections 1, 3 (algebra in Lemma A), and 5 provide the intended local formulas and witnesses. The original `R-20260823T030000Z-leftdef-o1pld/candidate_proof.md` is the historical informal scope: its Claim 4, Theorem 5 and Corollary 6 are original candidates, not assumptions or imported formal results. Both source byte snapshots and hashes are in `input-hashes.json` and `source-snapshot/`.

The formal carrier is exactly `Polynomial ℝ`, with real scalar linear submodules. The supplied analytic proof permits complex functions, but complex coefficients are NOT covered by this file. Natural-number parameters are unbounded. `p_even m` and `p_odd m` are total definitions for every natural number, while their sparse-family assertions require `2 ≤ m`; the invalid low parameters are not silently included.

Definitions are p_zero = 1, p_one = X; p_even(m) = X^(2m) - C(m/(m-1))*X^(2m-2), p_odd(m) = X^(2m+1) - C(m/(m-1))*X^(2m-1). The coefficient division is real division, and the subtraction in exponent indices is natural subtraction. `traces p` is (p.eval 0, p.derivative.eval 0) using Mathlib's actual polynomial derivative. `residues p` is (p.derivative.eval 1 - (p.eval 1-p.eval (-1))/2, p.derivative.eval (-1) - (p.eval 1-p.eval (-1))/2). `krein_polynomials` is the kernel of these two algebraic residues. The file contains no Sobolev domain disguised as this polynomial kernel.

## Exact assertions

- Low traces are (1,0) and (0,1); both low polynomials have zero residues.
- For every natural m >= 2, both high polynomials have zero value and derivative traces and zero endpoint residues.
- For every natural m0, `high_span m0` is the REAL ALGEBRAIC span of the set of both parity polynomials at m >= max(2,m0). It is contained in `zero_traces` and in `krein_polynomials`.
- `oblique` is the polynomial submodule p.eval 0 = p.derivative.eval 0. The polynomial 1+X belongs to its intersection with `krein_polynomials`, while neither 1 nor X belongs. For every m0, 1+X is absent from `high_span m0`, which is therefore strictly smaller than that intersection. This is an algebraic witness, not a theorem about topological closure.
- For each positive EVEN natural L, residue columns of X^L and X^(L+1) are (L,-L) and (L,L). Actual `Matrix (Fin 2) (Fin 2) ℝ` definitions give [[L,L],[-L,L]], determinant 2*L^2, and the explicit two-sided inverse (1/(2L))*[[1,-1],[1,1]]. Matrix determinant and inverse assertions require L > 0; the column identification additionally requires Even L.
- For every real residue pair (r_plus,r_minus), alpha=(r_plus-r_minus)/(2L), beta=(r_plus+r_minus)/(2L) solve the correction system for L > 0. For even positive L and every polynomial p, subtracting C(alpha)X^L+C(beta)X^(L+1) leaves zero residues. If X^L divides p, it still divides the corrected polynomial; this separate divisibility lemma requires no parity or positivity assumption.
- The lift (a,b) -> C(a)+C(b)X is a right inverse of `traces`, always satisfies the polynomial Krein constraints, and gives p - trace_lift(traces p) in the trace kernel. The submodule membership reduction assumes explicitly `zero_traces ≤ W`; under this hypothesis p in W iff trace_lift(traces p) in W. Deriving that kernel-inclusion hypothesis from a cofinite family is NOT proved.

The representative root is `SL.AuditRound5.local_algebra_root`, an explicit conjunction of these nontrivial conclusions, without an opaque True target or an assumption of the conclusion. `positive-contract.json` contains its fully named intended type; the actual elaborated type and every local definition are exported separately.

## Not formalized

No Sobolev spaces, left-definite norm equivalence, trace continuity, topological closedness/density, cutoff approximation, leading-term span equality for divisible Krein polynomials, polynomial H2 approximation, Green function/integration identity, L2 obstacle or moment recursion, K_c isomorphism, complex extension, cofinite closure classification, non-cofinite classification, s=3 claim, or odd change-of-variable integration is formalized. Those remain analytic obligations outside this contract. The old Lean scaffold is neither imported nor edited.

## Execution and evidence policy

All Lean commands use the installed, pinned Lean 4.31.0 executable and pre-existing Mathlib cache, with no full Lake build, package download or modification. Existing project `.olean` objects are excluded from the author LEAN_PATH. Author compilation runs from the external directory against the live root source, with output only under the external directory. The maintained plugin compiles an identical external source snapshot into its own fresh output; the snapshot binding is explicit. No semantic review input is supplied to the verifier.

Actual fourth-round run metadata, current `--version`, and PATH resolution identify a WINDOWS PE executable (x86_64-w64-windows-gnu), launched from WSL. This corrects the request's assumed Linux runtime: no Linux ELF Lean runtime was found in the inspected standard locations. We do not label the run Linux-native.

The write whitelist contains only the new project Lean file and this external directory. The root AGENTS.md requirement to maintain project logs is delegated to the coordinator by the later explicit scope restriction. All earlier Lean sources and project configuration, prior compiled project objects, canonical/cards/Git and prior evidence are preserved. No agents are spawned. Discovery diagnostics, failed elaboration attempts and all actual build logs are retained.
