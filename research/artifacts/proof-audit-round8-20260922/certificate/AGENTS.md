# Round 8 scoped certificate author

## Working contract

- Role: certificate author, not final reviewer. All writes stay in this directory. The parent, frozen `submitted/` and `sources/`, the project, libraries and Git are read-only. No subagents.
- Author `certificate.py` and a mathematical contract for T3 root isolation, monotone images, values, and the scalar bounds B(t) <= 9, Cz < 0.337 and final ratio < 0.8256. The deep-sliver proof and main TeX belong to the other author/coordinator.
- Proof arithmetic uses standard-library Fraction and exact integers only. Decimal is directed display only. Explicit guards must survive Python -O. Optional SymPy/mpmath/libm observations are separate diagnostics with their real imports and versions recorded.
- Read supplied executable code before replay. Copy it here, preserve its bytes, and retain stdout, stderr, exit status, results and hashes for every attempt. Keep supplied and author failures distinguishable from successful later runs. Isolation means copies and a controlled working directory, not an invented security sandbox.
- Adversarial controls must exercise mathematical obligations and really exit nonzero in normal and -O modes. Positive replays cannot erase failed attempts.
- Python uses tab indentation, snake_case function names and PascalCase multiword variables. Update this file after each work batch; README is the mathematical and replay entry point.

## Dialogue and maintenance

### 2026-09-22 intake

The user requested: "You are a scoped certificate author for round8, NOT final reviewer", "Work only in /mnt/f/tools/math-audit-round8-20260922/certificate-author/", "no repo/library/git writes, no subagents", and a self-contained exact-rational replacement plus honest isolated replays of the supplied 22 checks. Required inputs have been read: parent AGENTS, submitted README/checks/analytic supplement/audit, historical scripts 05 and 19, and the frozen current INF proof. The project AGENTS was consulted read-only. The implementation will separate exact certification, platform-dependent diagnostics and supplied mixed-evidence checks.

This initial file records the scope and evidence discipline. No project or canonical edits are authorized for this author.

### Evidence harness

Added an append-only replay driver, actual-import recorder, separate legacy diagnostics and a clearly labelled continuation hook for platform-dependent failures. Each run snapshots its source and captures raw stdout/stderr, result artifacts, return code and hashes. Input copies are verified against intake hashes, including the supplied initial symbolic failure log. The initial log contains no machine exit-code receipt or corresponding failed source revision, so these remain unknown rather than reconstructed.

### Certificate candidate and supplied replay

Unchanged supplied checks completed 22 groups with exit 0 under normal and -O on Python 3.14.4, mpmath 1.3.0, SymPy 1.14.0, glibc 2.43. The supplied cot leak reproduced here; its exact binary rational input/output and the old root bracket are pinned for oracle-free rechecking. No continuation hook was needed. Added a standalone Fraction certificate with exact outward rational grids, Machin/Taylor enclosures, sign-separated roots, documented-monotonicity interfaces, scalar comparisons, directed display and 14 genuine rejecting controls. Candidate execution and mathematical documentation follow; no final-review claim is made.

### First certificate executions and contract

Runs 004 and 019 completed the 19 exact arithmetic groups normally and under -O. Runs 005-018 and 020-033 rejected all 14 false/invalid candidates with exit 1 in both modes; their actual intended exception messages were read. Added README with the complete Machin branch proof, Lagrange remainder, rational grid rounding, unique G root identity, general lower(L)/upper(H) propagation, full-interval three-range B proof, Cz and scalar ratio contract. Q=893460803/1082206710<0.8256. Added an elementary derivative argument for the scalar cot remainder, avoiding reliance on the old text's misindexed expansion. Full deep-sliver and spectral phase obligations remain outside this author's scope.

### Provenance correction

Inspection of actual imports found `_distutils_hack` and `apport_python_hook` loaded by distro site initialization in initial certificate processes. The draft README's statement that all observed imports were standard library was too broad. Preserved that draft under `development/`, corrected the claim, and added explicit -S replay support to verify standard-library-only execution without hiding or filtering those initial imports. The original passing receipts remain unchanged. This is an author provenance correction, not a mathematical certificate failure or a sandbox claim.

### Bundle verifier

Added `verify_bundle.py` to verify source/output hashes, unchanged supplied-check identities, exact equality of positive results, outward display directions, intended negative-control exception messages, actual module provenance and tab/snake_case style. Its small finite interval regression exercises signs, negative denominators, powers crossing zero, Taylor parity and display direction. These checks support the author submission and do not constitute independent final review.

### Verified executions and export

The additional -S normal/-O runs 034 and 049 succeeded with identical exact results and no external observed modules; their 28 negative-control counterparts all failed for their intended guard. Bundle verification 064 exited 0: 14 input identities, four positive executions, 56 planned rejecting executions, 332 directed rational displays and 10 finite arithmetic/display regressions checked. The replay driver now propagates unexpected child statuses to its own exit status, while retaining every child record. Added an export helper that copies actual outputs, preserves all run records, inventories all changed paths and hashes every artifact except the hash manifest itself. No certificate arithmetic changed after its first successful execution.

### Final author handoff

Final evidence verification 065 exited 0. Exported the unchanged exact outputs from runs 034 and 049, the actual verification output from 065, and a replay summary of all 65 completed runs: 9 exit-0 processes and 56 intended exit-1 negative controls, with no unexpected execution result. The supplied initial failure and the author's corrected provenance draft remain available. `changed_paths.txt` enumerates all 498 delivered files under this author directory; `artifact_hashes.json` binds every other file. The final README clarifies author-only scope and the final verification run. Independent final review and the other author's deep-sliver/main-TeX work remain outside this submission.
