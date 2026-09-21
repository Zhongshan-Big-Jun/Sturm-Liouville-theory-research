# Round 8 sliver/T1 author handoff

Status: author candidate complete; final independent verification pending. No agents were spawned. No repository, library, git, historical run, or parent work-area files were changed.

The requested finite threshold is proved, with a stronger margin:

\[
G(R,u)\ge\frac{\pi^2}{2\varepsilon(w+\ell)(w+\varepsilon\ell)}
>\frac{15\pi^2}{4}>25
\quad(R\ge1500,\ 0<w\le2).
\]

The first inequality is valid for all R>=1 and 0<u<1/2. It comes from the continuous, pole-free half-interval phase `Phi(k)=ell*k+arg_continuous(cos(w*k)+i*epsilon*sin(w*k))`. The first two full eigenvalues have `Phi(k1)=pi/2`, `Phi(k2)=pi`; `Phi'<=ell+w/epsilon` and `k1>=pi/[2(w+ell)]` yield the estimate. No global theta2>pi/2 assumption is used.

This margin is larger than 3*pi^2. Hence T1 only needs the analytic T2 inequality M<3*pi^2; no T3 enclosure or claim M<25 is required. The complete near-minimizer conclusion allows every error eta_j with R_j*eta_j->0, not just eta_j=R_j^(-2). The value error is bounded by O(R^(-1)), without asserting its leading coefficient or a rate for u_j.

Main files:

- `proof.md`: complete reusable proof, quantifiers, root identity, finite threshold, T1 and dependency checks. Appendix A contains an optional coarse elementary proof of the necessary large-w inequality, already developed before the scalar work was assigned independently. Appendix B records the retained T2 sign argument. Neither appendix is an independent review verdict or T3 certificate.
- `sliver_t1_fragment.tex`: insertion blocks replacing the old lem:sliver and thm:T1, preserving these labels. Keep the repaired thm:lemAdp and analytic thm:T2 in the target document.
- `fragment_check.tex` and `build/fragment_check.pdf`: compilation harness only. The PDF states the large-w and T2 integration dependencies by reference to proof.md; it does not replace that complete proof.
- `input_manifest.json`, `output_manifest.json`: source and deliverable SHA-256 bindings.
- `logs/execution_receipts.json`, `logs/latex_receipt.json`: real commands, stdout/stderr, return codes and input/output bindings.
- `CHANGED_PATHS.md`: complete list of created paths, all in this private author directory.

Author validation: 16 exact rational comparisons; 120 exploratory high-precision sliver points and 84 exploratory large-w points; all returned exit code 0. The numerical points are explicitly not proof or interval certificates. The fragment compiled successfully with TeX Live 2026, producing three pages without undefined references or over/underfull-box warnings.

Coordinator integration should replace the old sliver grid narrative and keep historical scripts immutable. The coordinator's mode/fixed-u candidate was read and copied to inputs/coordinator-math.md with its hash. T3, arbitrary-density extremal reduction, round 7, library acceptance, and final independent review remain outside this author's scope.
