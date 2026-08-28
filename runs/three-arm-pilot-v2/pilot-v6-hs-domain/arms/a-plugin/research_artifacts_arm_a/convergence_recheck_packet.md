# Fresh-context convergence recheck packet

- **subtask_id:** `SUB-CONVERGENCE-recheck`
- **purpose:** Verify that the exact metadata defects found in the first
  fresh-context pass were repaired and decide terminal readiness from files only.
- **inputs:**
  - `problem_contract.md` sha256 `b0a4b723f1b3d6dd49b6d06f7c26ff543ed3578287e8a1e7c2359e323c394e38`
  - `candidate_proof.md` sha256 `0e36b83891a4b5a509174eb7e367365652c0637267b5d4610f5e01a7c42ec080`
  - `obligation_graph.md` sha256 `d1ac9ed497af8609ef55c3bd4de98c591ff0b357f76550df450511e8a7cb55a4`
  - `approach_registry.md` sha256 `e1d1c632fa8599f4b1232dbdc9c068456cd4b87453aaa0742f712ff3502ec89b`
  - `research_ledger.md` sha256 `414281e549a6e81b4fdf7f13115a7a52da646121ff00ab035a1f747040e17a26`
  - `audit_report.md` sha256 `71ad474b2c7278626af1693772c610a44bfaaa4beb22dc620f88d89e46dbd948`
  - `status_and_literature.md` sha256 `1a84f86c94e7d8fd9df25788f51ed8919b40969b7be752e1460dce958e9035d1`
  - `convergence_report.md` sha256 `6c3d9f6b0f152861804919ccbaade79d4fddfc94c08f15c2873e6d112489aa85`
- **deliverable:** Write only
  `agent_returns/SUB-CONVERGENCE-recheck.json` as raw valid JSON with fields
  `state`, `hashes_verified`, `repairs_verified`, `closed_obligations`,
  `first_open_obligation`, `status_consistency`, `issues`, `terminal_ready`, and
  `decision_delta`.  Do not edit other files.
- **success:** `state=CONVERGING`, no issues, all O0--O7 closed, consistent
  `INDEPENDENTLY_AUDITED_PROOF`, and `terminal_ready=true`.
- **constraints:** Read only the eight listed inputs; no conversation, network,
  repository/history, other project files, mathematical re-proof, or children.
