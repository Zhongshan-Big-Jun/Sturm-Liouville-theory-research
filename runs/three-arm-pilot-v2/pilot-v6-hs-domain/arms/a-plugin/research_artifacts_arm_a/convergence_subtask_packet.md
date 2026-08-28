# Fresh-context convergence packet

- **subtask_id:** `SUB-CONVERGENCE-final`
- **purpose:** Rebuild the run state from files only, without conversation
  history, and decide whether the package is converging to a valid terminal
  report or still has an open/mismatched obligation.
- **inputs:**
  - `problem_contract.md` sha256 `b0a4b723f1b3d6dd49b6d06f7c26ff543ed3578287e8a1e7c2359e323c394e38`
  - `candidate_proof.md` sha256 `0e36b83891a4b5a509174eb7e367365652c0637267b5d4610f5e01a7c42ec080`
  - `obligation_graph.md` sha256 `d1ac9ed497af8609ef55c3bd4de98c591ff0b357f76550df450511e8a7cb55a4`
  - `approach_registry.md` sha256 `8514f3b9479dd78804e2e1db398778731eceb4e48c62c6ca2d218cbba802a46c`
  - `research_ledger.md` sha256 `312570e038269ed3e520e0db083a9034702d8c2f4c687457ad0b26d03ad5adfe`
  - `audit_report.md` sha256 `663a00d79bed44bb35f344469cdcb3936de3a4e21799641a89e7d64d53ebbc76`
  - `status_and_literature.md` sha256 `c680b6e32fb86aaf934ddfe21ca2f639fd8eba49a3495750a0ed65282224ce68`
- **output:** Return raw JSON only with fields `state` (`CONVERGING`,
  `DIVERGING`, or `UNCERTAIN`), `hashes_verified`, `closed_obligations`,
  `first_open_obligation`, `status_consistency`, `issues`, `terminal_ready`,
  and `decision_delta`.  Do not edit files.
- **constraints:** Read only the seven listed inputs, no conversation, network,
  repository/history, project files, known solution, or child session.  This is
  a state-convergence check, not a second mathematical proof audit.
- **budget:** One short pass; if any input cannot be verified, return `UNCERTAIN`.
