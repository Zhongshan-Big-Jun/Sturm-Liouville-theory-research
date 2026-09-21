# Independent source assessment

This is a review of the supplied ten original/candidate deltas and the v2 harness, not an acceptance of the previous review or author results. `ten-deltas.diff` records the independently generated complete deltas. All formulas below are conditional on the stated positive block densities, ordered interior interfaces, simple Dirichlet eigenvalues and weighted normalization. They explain the local code corrections; no global mathematical theorem is certified.

## Local calculus checked against the code

For a right-moving interface x_j, let s_j = rho_right - rho_left. Its distributional density variation is -s_j delta(x-x_j) dx_j. Differentiating -u'' = lambda rho u with Dirichlet boundary conditions, multiplying by u, and using self-adjointness cancels the eigenfunction derivative terms. With integral rho u^2 = 1, this gives d lambda = -lambda integral (d rho) u^2, hence partial_j lambda_k = lambda_k s_j u_k(x_j)^2.

Define D = lambda_{n+1} - lambda_n and f_i = lambda_n u_n(x_i)^2 - lambda_{n+1} u_{n+1}(x_i)^2. Then grad_x D = -diag(s) f. In width coordinates x_1=a, x_2=a+b, the derivative is (g_1+g_2, g_2). SUP has s=(R-1, -(R-1)); INF reverses both entries. The conditional expression in `gap_n1_grad.py:44` has exactly these two signs.

For the symmetric family (x_1,x_2)=(u,1-u), dD/du=g_1-g_2. The two interface contributions add: SUP gives -(R-1)(f_1+f_2), INF gives +(R-1)(f_1+f_2). Reflection symmetry makes the two squared-eigenfunction values equal, yielding the corresponding factor of two. For the INF eigenvalues separately, d lambda_k/du=-lambda_k(R-1)(u_k(u)^2+u_k(1-u)^2). This agrees with all five scalar/gradient patches, including their printed expressions.

Put lambda=lambda_{n+1}, F=f/lambda and J_{ij}=partial_j F_i in independent edge coordinates. Product differentiation yields

    Hess D = -diag(s) @ (lambda*J + outer(F, grad lambda)).

At F=0 the outer-product term vanishes. Thus the stationary Hessian is -lambda*diag(s) @ J. The sign and matrix product matter: NumPy elementwise multiplication by a diagonal matrix zeros the off-diagonal entries. The transposed expression is -lambda*J.T @ diag(s); it equals the Hessian at an exact stationary point by Hessian symmetry. A small computed residual is a finite numerical premise, not a proof of exact stationarity.

The width-to-edge transform x=Lw requires H_x=L^{-T} H_w L^{-1}. A linear mirror restriction x=x0+B y gives H_y=B.T H_x B and g_y=B.T g_x. The actual `hess_fd` and `jac_fd` functions use these coordinate conventions. Neither restriction permits omitting the outer-product term at a general nonstationary point.

## Ten delta dispositions

| Candidate source | Checked change | Executed scope and limit |
| --- | --- | --- |
| op03_gap_fh.py:5,23 | Select existing fixed backend; paired SUP factor 2(1-R) | Actual Df_at/backend functions, independent IVP/quadrature comparisons in the supplied harness, exact printed AST, and the complete four-point instrumented CLI |
| gap_n1_grad.py:44 | INF reverses both edge-jump contributions before width chain rule | Actual functions and exact gFH AST; six original top-level fixture iterations are not run |
| _tmp_fh_paradox.py:27-28 | Sum paired interfaces; opposite SUP/INF signs; symmetric factor two | Actual D_and_f and both exact expression ASTs; original scan loop omitted |
| tmp_fh_test.py:26-30 | Negative INF eigenvalue derivatives; positive paired gap coefficient | Actual lam_of and source expression ASTs; original loop omitted |
| tmp_verify_endpoints.py:30 | Correct SUP/INF paired signs | Actual D_and_f and exact fh AST; endpoint scan and brentq search not run |
| _gapn2_hess_verify.py:40,46-47,60-61 | Correct lower eigenvalue in f, gradient sign, and both stationary Hessian signs | Actual D_edges; f, printed gradient, H1/H2 ASTs supplied with actual spectral data and finite-difference J; main/analytic_jacobian_hp not executed |
| _gapn2_hess_sign_and_bigR.py:61 | Matrix multiplication in both sign alternatives | Actual hess_fd and exact H AST; stationary comparisons use jac_fd, not the historical high-precision Jacobian; extended-R scan not run |
| _gapn2_jacobian_analytic.py:289 | Preserve all Jacobian entries in stationary Hessian | Actual eigen_data and exact H AST with Jfd; analytic_jacobian and its main continuation loop not certified |
| _gapn2_o3_scan.py:74 | Matrix product before Hessian eigenspectrum | AST expression only with jac_fd input; module/scan/analytic_jacobian_spectral not executed |
| _gapn2_second_variation_probe.py:213 | Matrix product in stationary Hessian | AST expression only with Jfd; module and P1/P2/P3 density-path probes not executed |

The eight unchanged dependencies in each tree are `gap_lib.py`, `op03_gap_fixed.py`, `op03_gap_precise.py`, `_gapn2_symmetry_recon.py`, `_gapn2_jacobian_probe.py`, `_gapn2_hp_scan.py`, `_gapn2_jacobian_spectral.py`, and `op03_gap_table.json`. The fixed backend composes P_block @ M and uses the resulting block-start state for its weighted norm and point values. The legacy precise backend composes in reverse order; its normalization failures are reobserved in original-tree tests. This review does not repair it or infer that its tested roots must be wrong. Changing the selected import is the relevant bounded correction.

## Harness assessment

`provenance.py:53-57` enumerates every currently file-backed entry of a snapshot of sys.modules with no path filter. `classify:74-89` admits only selected-tree or harness files listed in the supplied manifest, exact installed NumPy/SciPy package roots, and configured stdlib paths excluding site/dist-packages. It grants no blanket allowance for an outer package, fresh root, or site-packages parent.

`validate:92-123` hashes admitted files, compares fresh-source digests, and requires exact selected paths, presence and frozen digests for 17 numerical or 3 CLI bindings. Unexpected external modules are reported without reading their source for hashing. The owned outside fixture is a real import; the missing control removes a genuinely executed binding. `report` records the raw map, classified map, explicit policy, required names, controls, PID and optimization flag. Both entry points return 86 using explicit branches when this gate refuses.

The instrumented CLI compiles the entire unchanged candidate source under its real file name into __main__, sets argv/search path/cwd, and executes the four-point loop before observing provenance. This is stronger than the numerical loader's source-expression checks but remains an instrumented launch. The numerical loader intentionally removes top-level For loops and __main__ guards, and reports the removed spans. The required source digest is not a claim that the entire digested file executed.

`replay.py` runs normal and -O children under -B -S with explicit installed NumPy/SciPy discovery paths. The parent repeats validation against its own manifest and policy, checks raw exit codes, requires exactly 117 checks and 79 original failures, checks four CLI comparisons, and requires the exact intended sole refusal reason for each control. The reviewer independently reinterprets these outputs without calling this validator, rather than trusting PASS fields. The standalone verifier is actually runnable: all 50 manifest entries and the digest sidecar are supplied inside PACKET.

The separate filter-only mutant changes only the collector condition and explicitly rebinds its manifest and sidecar. It retains required-name checks and all actual controls. Its evidence is a test of repair sensitivity, never part of the repaired candidate's acceptance evidence.

No substantive discrepancy was found in these local deltas or the inspected acceptance logic. Final acceptance also depends on completed own executions and final input integrity, recorded separately. The gate observes one point in each process; it cannot prove OS isolation, prevent imports before execution, capture transient/unloaded modules, resist malicious sys.modules metadata, trace arbitrary data reads, or certify shared-library provenance.
