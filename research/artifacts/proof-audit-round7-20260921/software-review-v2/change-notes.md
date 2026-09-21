# Bounded v2 provenance repair

Addressed both requested parts of R7-SW-001 as software author; the prior independent CHANGES_REQUIRED verdict remains unchanged. Final approval belongs to a new agent.

- `regression/regression.py`: replace the Base-filtered module map with unfiltered shared provenance; require selected-path/frozen-digest bindings; retain the raw map, gate result and actual control facts; return 86 on refusal, even if all numerical checks pass. Existing numerical tests, loaders and candidate source bytes are unchanged.
- `regression/replay.py`: copy manifest-listed inputs only; verify the self-contained package; launch normal/-O numerical and instrumented actual CLI processes with controlled `-S` startup; revalidate provenance and required bindings; retain expected original failures; run real outside/missing controls; record full before/after input maps and output hashes. No whole-site-packages or author-directory runtime allowance.
- New `regression/provenance.py` and `control-fixtures/outside_probe.py`: share the observation/enforcement logic across numerical and CLI paths and implement real imported-module/missing-binding controls. The separate old-filter-only mutation is test evidence, never part of the repaired freeze.
- `regression/capture_run.py`, `backend_probe.py` and `verify_package.py`: unchanged. The old verifier now has a supplied v2 `manifest.json` and `manifest.sha256`; it is runnable. Source manifests, original inputs and prior rejection are preserved as historical bytes.
- New AGENTS record, README, final input-only manifest/freeze and author-owned execution receipts document the exact scope, actual first failure and recovery, and lack of independent approval.

Preserved numerical target bytes: `op03_gap_fh.py`, `gap_n1_grad.py`, `_tmp_fh_paradox.py`, `tmp_fh_test.py`, `tmp_verify_endpoints.py`, `_gapn2_hess_verify.py`, `_gapn2_hess_sign_and_bigR.py`, `_gapn2_jacobian_analytic.py`, `_gapn2_o3_scan.py`, `_gapn2_second_variation_probe.py`.

Preserved eight dependencies: `op03_gap_precise.py`, `op03_gap_fixed.py`, `gap_lib.py`, `_gapn2_symmetry_recon.py`, `_gapn2_jacobian_probe.py`, `_gapn2_hp_scan.py`, `_gapn2_jacobian_spectral.py`, `op03_gap_table.json`. Both 18-file trees match the supplied baseline; there is no claim about the live research tree.

First v2 failure remains in execution 01: three unrelated Python startup hooks were observed and rejected. Follow-up changed child startup/search paths, not the allowlist. Both filter-only mutation failures are intentional test-sensitivity evidence; outside imports become incorrectly accepted by that mutant and the unchanged test suite must fail. The historical missing-NumPy/backend/selector failures remain documented in the supplied prior evidence; unsupplied raw historical files were not accessed.

`inputs/tools-AGENTS.md` is omitted as deliberately unsupplied, unrelated private workspace context, not executable input. Its old source-manifest references are not silently removed or rewritten.
