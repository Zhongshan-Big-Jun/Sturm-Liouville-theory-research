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
- Scored termination: five-hour hard usage limit at 2026-08-27T07:12:25Z.
- Scored status: `PAUSED_QUOTA_WITH_AUDITED_PARTIAL_RESULT`; the independent
  audit was post-hoc and excluded from scored usage.
- Completed Worker artifacts: `subagents/route_a.md` and
  `subagents/route_c.md`. Route B did not return an artifact.
- Neutral audit SHA256:
  `1f5e907b3fcbbe2190cbb6b4611c558d165a8cb51ec28e0f554cadd8d6ce00b8`.
- Repository exact replay: `py -3 reproducibility/audit_exact_claims.py`.
  Its finite outputs are `EVIDENCE`, not proof.
- Artifact hash manifest: `artifact_hashes.sha256`.
- Unknown fields: no canonical knowledge base, formalization project, accepted
  literature snapshot, or novelty audit was supplied.
