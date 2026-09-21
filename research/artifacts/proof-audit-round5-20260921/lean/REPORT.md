# Fifth-round Lean author submission

37 theorems and 22 definitions in the sole new project file `lean-proof/SL/AuditRound5.lean` compile under actual Lean 4.31.0 (Windows PE runtime via WSL). No Linux-native execution is claimed. The scope is all-index local algebra over `Polynomial ℝ`: two traces, Krein residues, arbitrary sparse-tail spans, the 1+X oblique witness, an actual 2x2 residue matrix and inverse/correction, and explicit trace-lift decomposition.

All 59 declaration axiom closures are exported and author-cross-checked. Only propext, Classical.choice and Quot.sound occur. Positive controls pass; a false high-span equality fails; the maintained verifier accepts the complete representative root contract and rejects the false expected equality. Its semantic status is explicitly not_reviewed. 3712 loaded modules and 14845 import artifacts are hash-bound, along with runtime, source snapshots, objects and actual commands/logs. One style-only unnecessarySeqFocus warning remains and is documented in linter-warnings.json. Prior 45 Lean sources plus 3 project configuration files and 32 compiled project objects remain byte-identical.

- Full scope, hypotheses, exclusions, hashes and executable commands: CONTRACT.md.
- Stripped compiler exports for fresh blind readback: final/READBACK_INPUTS.json.
- Separate reviewer contract/evidence packet: SEMANTIC_REVIEW_INPUTS.json.
- Summary and raw receipts: FINAL_CHECKS.json, command-index.json, logs/, attempts/, verifier-positive/, verifier-false-expected/.
- Every created path: CHANGED_PATHS.txt; final file integrity inventory: FILE_HASHES.sha256.

No Sobolev closure/density, cutoff convergence, Green integral, operator isomorphism, complex result, cofinite analytic classification or full O1pLD is formalized. Author work is complete; independent blind reading and correspondence review are pending coordinator action. No old Lean/configuration/dependency file, canonical/card, Git state or prior evidence was edited; no agents were spawned.

Source SHA-256: 035043c154c215e995a210b798f80cf131414eee5529ad54396a5af3d669ae45
Author inspected object SHA-256: 75a9eedebebb71504b663c4c49b8abc1109ff7aa108cabc371b86b53281c2c90
