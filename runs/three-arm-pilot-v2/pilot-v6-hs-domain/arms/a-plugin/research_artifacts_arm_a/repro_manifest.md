# Reproducibility manifest

## Frozen input

- Input ID: `arm-a-frozen-v1`.
- Authoritative statement: the user message in the active run; no local copy was
  treated as prior mathematical context.
- Research date/time zone: 2026-08-28, Asia/Shanghai.
- Working root:
  `/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-a-plugin-v17-run1`.

## Restrictions honored

- No network tools, repository history/state, existing project files, known
  solution, or prior project results were inspected.
- Existing worktree state and commit hash are intentionally `UNKNOWN` because
  the frozen contract forbade their inspection, overriding the skill default.
- Only the installed requested skill protocol was read outside the current
  directory; it supplied workflow rules, not mathematical facts.
- Two research child sessions were used: one independent proof audit and one
  fresh-context convergence check (with a same-session repair recheck).  The
  allowed maximum of three was not exceeded.

## Runtime and tools

- Coordinator/independent verifier model identifiers: not exposed; `UNKNOWN`.
- Shell: bash via the local execution environment.
- Python: 3.14.4.
- SymPy: 1.14.0.
- Exact-check script sha256:
  `6be2c58c5761892f254f4f912ca1b2d46f83d28b83c8a1d7453770534d18171a`.
- Computation protocol sha256:
  `262a476e9488739d6bdefe3d503792c3e43425c2e889c7d682cbf8fdc583c561`.
- Random seeds: none; all retained checks are deterministic and exact.
- Formal prover: not used.
- Network/literature tools: not used.

## Audit input bindings

- `problem_contract.md`:
  `b0a4b723f1b3d6dd49b6d06f7c26ff543ed3578287e8a1e7c2359e323c394e38`.
- `candidate_proof.md`:
  `0e36b83891a4b5a509174eb7e367365652c0637267b5d4610f5e01a7c42ec080`.
- `obligation_graph.md`:
  `3b4e07af5709b5104a8f27d9b924cd9fd2f636c7652fef972db90defb7ac53d7`.
- `closure_gate.md`:
  `07996f0733084622d3a913f1eb0aa794eb07ebe30ed2fdcdc4b620a989269ad7`.

These are the pre-audit versions.  If revision occurs, a new audit packet and
new bindings are required; the old values remain provenance history.

## Computation replay outcome

The first run failed because of a recorded script-encoding error.  After the
one-line repair, the exact replay exited 0 and printed
`ALL_EXACT_CHECKS_PASS`.  This checks only the finite domain stated in
`reproducibility/computation_protocol.md` and is not a theorem certificate.

## Final package bindings

The independent audit full-file SHA256 is
`046e7db41ea7f1043b85a172b65e5c535b457cc9d46c61b77a25b4f6edf00c3b`.
The terminal convergence artifact full-file SHA256 is
`2cba1b8beab8818b06fa05a98cb4f7f630246d614c375a8ada513fe865422367`.
At freeze, `SHA256SUMS` binds every retained artifact except itself; its own
SHA256 is reported separately in the handoff.
