# Reproducibility manifest

- Run date: 2026-08-24.
- Working directory: `/mnt/f/benchmark/B3-O3-CAL-20260824/arm-a-plugin-run5`.
- Authoritative input: frozen calibration task supplied on stdin in the user message.
- Skill: local `rigorous-open-math-research` instructions supplied and read from `.agents/skills/rigorous-open-math-research/`.
- Internet: forbidden and not used.
- Repository/Git inspection: forbidden and not performed; commit and dirty-state fields are intentionally `UNKNOWN`.
- Outside-current-directory reads: forbidden and not performed.
- Prior solution or memory: forbidden and not used as a premise.
- Computation policy: local symbolic checks may falsify or verify identities, but the theorem requires a self-contained uniform proof.
- Random seeds: none; all exact checks deterministic.
- Formal proof assistant: not known to be available because the blind restriction forbids repository inspection; no existing formalization project is assumed.
- Human contribution: statement, constraints, and requested workflow only.
- Model contribution: proof search, exact derivation, synthesis, and artifact writing.
- External sources/citations: none.

## Deterministic symbolic check

- Purpose: falsify/check determinant, trace, `(EC)_{12}`, and matrix-recurrence transcription. It is non-load-bearing and does not establish the general root theorem.
- Script: `reproducibility/check_identities.py`.
- Script sha256: `590d65eab438a2d26474bf2b13b130225379cbdc72e802f32be92d2a17cabe5a`.
- Command: `python3 reproducibility/check_identities.py`.
- Python: `3.14.4`.
- SymPy: `1.14.0`.
- Expected output: `PASS: determinant, trace, EC entry, and n=1..6 recurrence identities`.
- Exact arithmetic: symbolic rational-function arithmetic and polynomial remainder modulo `c^2+q^2-1`; no floating point.

## Frozen proof and audits

- `problem_contract.md`: sha256 `4e4695334fddcdcc99e1f5f74ecaa3ad9a98ca452a68dd3483d7dbd4d1e1b0d7`.
- `candidate_proof.md`: sha256 `59b46fa2ee1e2d6a38ad4d386c936405ad96f4861db4509872c6160a0c6791b6`.
- `subagents/SUB-AUDIT.md`: sha256 `4c8831a11edbdcb70c4599ef818e96633c507d2feef58a91659953b000f1c92f`.
- `subagents/SUB-ALG.md`: sha256 `9f9111c5031bf50cebd9962edec93d08398d6985dc0558879d95f711b611c51a`.
- `subagents/SUB-OSC.md`: sha256 `9d2dba5b940bce711d8d7a79d581431296b82881ef43a1634b89babf73d95066`.
- `subagents/SUB-ADV.md`: sha256 `5504f0debbfb4ada3d4f036f7add9c254bd5f1970f45c0770c611891a28ceeab`.
- `subagents/SUB-CONVERGENCE.md`: sha256 `412649eec0d07aa5a024e2266481a6e1bbd6778be262fcefc9d15b69ebacf526`.
- `final_report.md`: sha256 `a6c5f4d937d89d27fa10f541d61e7b21c1cecaae6edd62858d483bb5f95063ea`.
- The candidate remains unchanged after audit so its hash binding stays valid; later status is recorded in `audit_report.md`, `obligation_graph.md`, and `final_report.md`.
