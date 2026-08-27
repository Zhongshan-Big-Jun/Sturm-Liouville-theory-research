# Reproducibility manifest

- Run date: 2026-08-27.
- Working directory: `/mnt/f/benchmark/PILOT-V5-V17-U2-20260827/arm-a-plugin-v17`.
- Authoritative mathematical input: frozen task supplied in the user request.
- Network: forbidden and unused.
- External task files: forbidden and unused for mathematical content.
- Git: current directory is not a Git repository.
- Shell: GNU bash 5.3.9.
- Python: CPython 3.14.4.
- Randomness: none used.
- Exact computation: `reproducibility/exact_small_cases.py`; replay with
  `python3 reproducibility/exact_small_cases.py --triple-max 80 --full-max 12`.
- Route-interface replay: `python3 reproducibility/verify_route_claims.py`.
- Hash-verified worker inputs:
  - `subagents/route_a.md`: `6ce207738f66fcd3b0b5b2c39175cf068be15f8b8532b76593e11b5cd386b647`.
  - `subagents/route_c.md`: `f260fe18d316ad8d58294700ad4bb3cd40514537728a7ac67ae576c19ca7bbf2`.
- Incomplete worker return: `subagents/route_b.md` absent; no retry performed.
- Formal verification: not run; no Lean/formalization project exists in the workspace.
- Fresh-context check: `convergence_check.md`, rebuilt from listed run artifacts only.
- Adversarial audit: `audit_report.md`; coordinator audit only, not an independent-agent or
  formal verification.
- Final result: `final_report.md`; concise handoff: `final_response.md`.
- Authoritative stopping hashes: `artifact_hashes.sha256` (generated after final files).
- Unknown fields: no canonical knowledge base, formalization project, external verifier, or
  accepted literature snapshot was supplied.

## Repository capture note

After the solver generated `artifact_hashes.sha256`, the CLI launcher replaced
`final_response.md` with the actual final answer captured from the completed
turn. Repository archiving therefore updated only the `final_response.md` line
in the manifest from the pre-capture hash to
`0da25db820a397517d28cac2218605c46b9b41a67ae0be19039a492d34012d39`.
No mathematical artifact changed. The solver-time hash of this manifest was
`56161b8b47c303382353992287a6834813bcae5f542a8e809eafb95176f15923`;
the repository-corrected manifest has a different hash reported in the
top-level benchmark results.
