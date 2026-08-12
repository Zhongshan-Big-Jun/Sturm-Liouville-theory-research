# Problem contract (run R-20260812T090000Z-g1prime-g2)

## Goal
Advance the n>=2 adjacent spectral gap extremal problem for the Dirichlet weighted
string -u'' = lambda*rho*u, u(0)=u(1)=0, rho in {1,R} bang-bang with exactly 2n
switches, alternating pattern SUP (first/last block 1) or INF (first/last block R).
D_n = lambda_{n+1} - lambda_n.  Target: prove that for every R>1 and n>=2, the band
self-consistency system F_sigma(R,x)=0 (F_j = f(x_j)/lambda_{n+1}, f = lambda_n u_n^2
- lambda_{n+1} u_{n+1}^2, x in ascending region U) has exactly one solution, which is
reflection symmetric; hence the global SUP/INF extremizers of D_n are unique and
symmetric.

## Current status (2026-08-12, from docs/SL_gap_nge2_symmetry_local_proof.pdf)
- STRICT: structure theorem for band-consistent points; R=1 explicit analysis
  (exactly 2n simple symmetric zeros, sgn det J(1,x*) = (-1)^n); R->1 local theorem
  (unique symmetric analytic branch); classification framework: conditions (G1') and
  (G2) imply the global conjecture (topological degree + equivariance + finite block
  reduction).
- OPEN: (G1') det D_xF_sigma(R,x) != 0 with sgn = (-1)^n on the whole solution set
  Sigma_sigma; (G2) block widths uniformly positive on compact R ranges (no boundary
  accumulation).

## This run's targets (concrete sub-obligations)
- O-1: Derive and numerically verify the exact analytic Jacobian structure
  J = (D~ + M~)/lambda_{n+1} where D~ = diag(f'(x_j)) and M~ is given by regularized
  resolvent kernels; verify the identity f'(x_j) = -2 lambda_{n+1} eps_j c W(x_j).
- O-2: Reformulate (G1'): at band-consistent points, Hess(D_n) = diag(s_i) * lambda
  * J on the family, so (G1') <=> det Hess(D_n) > 0 at every critical point.
- O-3: Numerically map det A, det B (symmetric/antisymmetric Jacobian blocks at
  symmetric points) and the Hessian spectrum along the symmetric branch for
  n = 2..5, R in [1.05, 100], SUP/INF; identify sign patterns and margins.
- O-4: Boundary analysis for (G2): coalescence of adjacent switches produces a single
  simple zero of the limiting f (pair acts as one effective switch: blocks j-1, j+2
  have different values); endpoint hitting forces q0 = c at the limit.  Both remain
  open; record precise obstructions.
- O-5: Attempt det B != 0 along the symmetric branch (no symmetry-breaking
  bifurcation) via sign structure / monotonicity.

## Completion criteria
- Any STRICT theorem closing (G1') or (G2) (or a piece of them), written up with
  proof; OR a precise reduction with strictly smaller open core; OR a falsified
  sub-claim with exact obstruction.  Numerical-only results are EVIDENCE and do not
  close obligations.

## Results that do not count
- Numerical verification of det J != 0 along the symmetric branch only (already
  known EVIDENCE).

## Tools / constraints
- Python C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe with
  PYTHONUTF8=1; scipy/numpy available.
- Reuse scripts/_gapn2_symmetry_recon.py (Recon class, spectral engine via transfer
  matrices) and scripts/_gapn2_jacobian_probe.py (FD Jacobian, sym/antisym
  decomposition).
- All numerical results are EVIDENCE and must be labeled as such; STRICT claims need
  complete proofs.

## Contract audit
- The contract matches the open conditions (G1')/(G2) as stated in
  docs/SL_gap_nge2_symmetry_local_proof.pdf section 5 (verified 2026-08-12 by
  re-reading the tex source).
