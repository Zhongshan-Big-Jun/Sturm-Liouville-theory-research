# R13-07..R13-10 author handoff

Status: REPAIRED_AND_AUTHOR_TESTED, not independent approval. Baseline HEAD: 4a82d3c2c8c7c3e5f3f027efcf2be3c54a612983. Work was performed directly in /mnt/f/LaTeX/BVE research. No commit/push, shared documentation, cards, canonical data, old artifacts or PDFs were changed by this author.

## Changed source

- `scripts/_gapn2_symmetry_recon.py`: a single physical state and block mass supply normalized values and derivatives. Midpoint mass removes small-wave cancellation. Existing eigfun uses it. Shared linear/trigonometric/hyperbolic transfer and coordinate-based Green assembly fit inside this already-authorized file.
- `scripts/_gapn2_jacobian_analytic.py`: removes normalization by sampled ratios; routes physical/Green entrypoints to those helpers; implements the full nonstationary quotient derivative; shares all Jacobian terms and preserves legacy return keys.
- `scripts/_gapn2_jacobian_spectral.py`: uses the same general terms, preserving the existing finite spectral sum and its truncation convention (N+1 indexed modes before pole deletion).
- `scripts/_gapn2_half_problem_probe.py`: routes `_propagate` and ordinary DD/DN Green to the real-parameter engine. Reduced Green explicitly requires a positive eigenvalue; use ordinary Green for mu<=0. HalfSpectrum, indexed enumeration and bound pole deletion were preserved.

The complete author derivation is [derivation.md](derivation.md); the patch is [source.diff](source.diff). Baseline and final source identities are in baseline.json and handoff.json.

For f_j=a*u_j^2-b*v_j^2, the full Jacobian is

J_ji = delta_ji*f'_j/b + s_i/b*(2*a*u_i^2*u_j^2 - 2*b*v_i^2*v_j^2 - f_j*v_i^2 - 2*a^2*u_i*u_j*Gt_a + 2*b^2*v_i*v_j*Gt_b).

The normalization and denominator derivatives yield the stated correction s_i/b^2*(a*u_i^2*f_j+2*a*u_j^2*f_i-f_i*f_j). At F=0 this vanishes and the previous stationary formula remains. `analytic_jacobian`, `analytic_jacobian_spectral` and `term_breakdown` all use the full formula; `fprime_id` remains a stationary diagnostic only.

## Actual checks and retained evidence

Every listed command ran against the final four source hashes. `logs/<name>/command.json` records argv, cwd, exit, elapsed time and input hashes; adjacent stdout.txt/stderr.txt retain complete outputs. All final listed commands exited 0.

| Log directory | Actual command (cwd is project root) | Result |
| --- | --- | --- |
| properties-final-normal | `python3 /mnt/f/tools/math-audit-round13-20260927/spectral-author/test_round13.py` | 469 named properties |
| properties-final-optimized | `python3 -O /mnt/f/tools/math-audit-round13-20260927/spectral-author/test_round13.py` | 469 named properties |
| r12-final-normal | `python3 /mnt/f/tools/math-audit-round13-20260927/spectral-author/r12_regression.py '/mnt/f/LaTeX/BVE research'` | Original 136 checks |
| r12-final-optimized | `python3 -O /mnt/f/tools/math-audit-round13-20260927/spectral-author/r12_regression.py '/mnt/f/LaTeX/BVE research'` | Original 136 checks |
| final-analytic-cli | `python3 scripts/_gapn2_jacobian_analytic.py 2 4 both` | Both branches; max FD discrepancies .004488/.001597 (finite sum) |
| final-spectral-cli | `python3 scripts/_gapn2_jacobian_spectral.py 2 4 both 640` | Both branches; max FD discrepancies .01401/.004979 |
| final-half-sup-cli | `python3 scripts/_gapn2_half_problem_probe.py 4 sup 160` | Closed raw Ko vs physical FD: 3.612e-10 |
| final-half-inf-cli | `python3 scripts/_gapn2_half_problem_probe.py 4 inf 160` | Closed raw Ko vs physical FD: 4.543e-10 |
| final-physical-fd-cli | `python3 scripts/_gapn2_jacobian_probe.py 4 2 both` | Physical interface directions and anticommuting cross blocks |
| parity-caller-final | `python3 scripts/_gapn2_parity_global_probe.py` | Actual asymmetric-grid caller runs; parity error remains O(1), as intended |
| static-final | `python3 /mnt/f/tools/math-audit-round13-20260927/spectral-author/static_impacts.py` | 100 import sites/54 files, 76 transitive modules; static inventory, not runtime coverage |

Independent reference.py uses 70-digit physical transfer, direct mass quadrature and implicit differentiation of the secular root/normalized residual, without project imports or the Jacobian/Green formula under test. R1 nodal state discrepancy decreased from 1.1164273 to 1.07e-14; the stated R4 second-mode discrepancy decreased from 6.3920684 to 7.33e-15. Nonstationary x=(.25,.75) Jacobian errors at N=160/640/2560 are .0359818546/.0090796048/.0022752183; additional asymmetric n=1/n=2 and R=1 configurations were checked. These are finite numerical errors, not spectral tail certificates.

The tests also cover independent DD/DN kernels at mu=0,-1,-100 and positive nonpoles, permutation covariance, duplicates, endpoint rows, derivative jump/continuity, spectral comparisons at nonpositive parameters, strict Green domain rejection and explicit overflow/pole rejection. R12 regression retains constant density 100 at N=4/80/160, mode/geometry/boundary binding and raw K vs SKS. Ten protected AST nodes and four complete protected source files were verified unchanged (see static_impacts.json).

Failed attempts are retained: `logs/before` reproduces the original defects; `logs/parity-caller-v1` contains the real new endpoint regression and exit 1. The first shell attempted unavailable `python`; its failure is recorded in research_ledger.md, followed by successful Python 3.14.4 execution. Earlier successful versions are retained separately, not substituted for final-hash evidence.

## Downstream impact and remaining limits

[static_impacts.json](static_impacts.json) records direct call lines and transitive imports. Runtime coverage comprises the tests and six representative CLI commands above, not all 76 modules. Existing analytic diagnostics consume term_breakdown's unchanged M1/M2/M3 keys; M1 now contains the complete quotient/normalization term, with extra M1_stationary/correction keys. Stationary-only collapsed/sector callers retain their mathematical contract.

The caller check found a genuine floating endpoint issue: a [0,1] grid can exceed the floating block sum by a few ulps. Only normalized sampling now snaps endpoints within 8*m*eps*L. Green/unnormalized propagation keep strict rejection. No interfaces or physical-FD directions are clipped by this exception.

Unmodified, out-of-write-set legacy diagnostics require care: `_gapn2_jacobian_pieces.py::pieces` still has historical flipped signs; `_gapn2_largeR_probe2.py` manually scales derivatives from a first-point ratio; `_gapn2_green_check.py` deliberately evaluates a pole sum then subtracts an infinite term before recomputing a pole-excluded sum. These were found by static inspection; they are not called by the repaired entrypoints, and no global repair/validation of them is claimed. `_secular_all` has no current Python callers and retains its old positive-parameter trigonometric helper. Old positive-eigenvalue primitives remain limited to that contract.

Unscaled hyperbolic propagation explicitly raises on unrepresentable intermediate values. Positive near-pole detection is a floating guard, not a rigorous resolvent certificate. The old full-problem subtraction `regularized_green` remains cancellation-prone and is not used in the repaired Jacobian. No uniform tail bound, interval arithmetic, Lean verification, full repository/large-R scan, M3/KP or global theorem certification was attempted. Analytic derivation and finite test evidence are separate; independent review belongs to the coordinator's reviewer.
