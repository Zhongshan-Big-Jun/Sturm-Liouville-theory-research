# Append-only research ledger

## L-001. Independent run start

- Started: `2026-08-28T14:12:36.1916934+08:00`.
- Repository source head: `df35eb6357ea1d75551af323848fc06f6e7b84b6`.
- Isolation rule: no Blueprint process or result could be read before freeze.
- Whiteboard was used only as bounded durable memory for independent intermediate results and the final freeze checkpoint.

## L-002. Symbolic branch reconstruction

- Derived the only nondegenerate finite-phase power-law balance `u=R^(-1/6)`.
- Derived `kappa^3=18pi-48/pi`, `A0=2/kappa`, `B0=1/kappa`, and `C0=16/(pi kappa)`.
- Reconstructed the rank-3 compatibility condition and the leading mass cancellation.

## L-003. Sector reconstruction

- Rebuilt the full switch Jacobian and both mirror-sector matrices from the five-layer transfer system.
- The first nonzero determinants were found at `u^20` and `u^26`, with positive coefficients `128kappa^2/pi^2` and `2048kappa^2/pi^4`.
- A 140-digit Laurent run, two free-jet choices, and truncation orders 30 and 46 agreed.

## L-004. Finite-u checks

- At `u=0.06`, the original four-equation residual was about `6.6e-50`.
- Direct full-Jacobian sector determinants were positive and their scaled values converged to the formal coefficients.
- These checks remain EVIDENCE and are not used as theorem-grade closure.

## L-005. Freeze and Whiteboard checkpoint

- Ended: `2026-08-28T16:29:22.9905214+08:00`.
- Wall time: `8206.798828` seconds, or `02:16:46.798`.
- Exact token total: unavailable. No goal token tracker was active, and no estimate was substituted.
- The independent report, scripts, machine results, and Whiteboard checkpoint were frozen before Blueprint retrieval.

## L-006. Post-freeze Blueprint comparison

- Retrieved canonical Blueprint snapshot `sha256:3b99f2090d73029fa77498a897979e614ddccbb205b613449fdd2181ce6ccc48` and inventory `sha256:0c1e576e4902ffb8720e8a9b7c02a0df1c5425af805f1c9aba05b9968279ed5e`.
- Canonical closure contains 4 available claims, 3 proved inferences, and 0 contradictions.
- Every headline independent formula agrees exactly with `CLM-SL-B4-M3-TARGET-V1`.
- Blueprint remains the stronger theorem-grade source because it proves analytic branch existence, admitted-class exhaustiveness, exact determinant coefficients, and a uniform finite-R sign bridge.
