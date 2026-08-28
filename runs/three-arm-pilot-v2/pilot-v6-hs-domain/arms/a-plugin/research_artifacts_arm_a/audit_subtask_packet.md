# Independent audit subtask packet

- **subtask_id:** `SUB-O7-global-audit`
- **claim:** Audit all three conclusions and both interpretations in
  `candidate_proof.md` against the exact frozen normalization in
  `problem_contract.md`.  Decide whether the package supports an
  `INDEPENDENTLY_AUDITED_PROOF` label.
- **direct_attempt:** Coordinator closed O1--O6 in `candidate_proof.md`; no part
  of that reasoning is accepted merely because the coordinator wrote it.
- **falsification_probe:** The coordinator separately checked the affine equality
  case, the odd half-power boundary count at s=5, degree n=2, and the formal-vs-
  genuine inverse on x^2.  Re-derive rather than trusting these checks.
- **decision_to_change:** O7 is `AUDIT_PENDING`.  Success is a strict `PASS` with
  empty critical-error and gap arrays.  Failure is the first localized
  `REPAIRABLE_GAP`, `FATAL_GAP`, `WRONG_PROBLEM`,
  `CIRCULAR_OR_EQUIVALENT_REDUCTION`, `UNVERIFIED_CITATION`,
  `COMPUTATIONAL_ONLY`, or `UNCERTAIN` verdict.  Budget stop returns `UNCERTAIN`
  with the first unchecked load-bearing claim.
- **inputs:**
  - `research_artifacts_arm_a/problem_contract.md`, sha256
    `b0a4b723f1b3d6dd49b6d06f7c26ff543ed3578287e8a1e7c2359e323c394e38`
  - `research_artifacts_arm_a/candidate_proof.md`, sha256
    `0e36b83891a4b5a509174eb7e367365652c0637267b5d4610f5e01a7c42ec080`
  - `research_artifacts_arm_a/obligation_graph.md`, sha256
    `3b4e07af5709b5104a8f27d9b924cd9fd2f636c7652fef972db90defb7ac53d7`
  - `research_artifacts_arm_a/closure_gate.md`, sha256
    `07996f0733084622d3a913f1eb0aa794eb07ebe30ed2fdcdc4b620a989269ad7`
- **context_slice:** Only the four exact input files.  Check the true Krein
  form, operator-power recursion, both orthogonality contradictions, completion
  maps, canonical equality, literal-span language, genuine-inverse alternative,
  and all c/s/n boundary cases.  State every external theorem and verify its
  hypotheses.  Conduct definition, logic, boundary, and adversarial audits.
- **deliverable:** Write only
  `research_artifacts_arm_a/agent_returns/SUB-O7-global-audit.json`; do not
  mutate any other artifact.  The JSON object must contain `verdict`,
  `critical_errors`, `gaps`, `repair_hints`, `covered_scope`, `residual_risk`,
  `first_error`, `definition_audit`, `logic_audit`, `boundary_audit`,
  `adversarial_audit`, `decision_delta`, and `artifact_sha256` (the last is the
  sha256 of the same file content computed before adding that field, or use a
  detached `.sha256` file and report its value).
- **status labels:** `PASS`, `REPAIRABLE_GAP`, `FATAL_GAP`, `WRONG_PROBLEM`,
  `CIRCULAR_OR_EQUIVALENT_REDUCTION`, `UNVERIFIED_CITATION`,
  `COMPUTATIONAL_ONLY`, `UNCERTAIN`.
- **constraints:** No network, repository/history/project-file inspection,
  unlisted files, known solution, child sessions, or global completion claim.
  Treat the proof as a first-time submission.  No gap may be hidden in residual
  risk under `PASS`.
- **budget:** One focused audit turn.  If incomplete, return `UNCERTAIN` and the
  first unchecked proof gate.
- **decision_delta:** Either close O7 by a strict PASS or expose the smallest
  exact repair/failure obligation.
