# Independent execution record

## Scope and method

- User request, 2026-09-21: act as the independent Lean execution verifier, not the author or final semantic approver. First read `/mnt/f/LaTeX/BVE research/AGENTS.md` read-only.
- Read only the designated frozen author inputs, their original source counterparts, and the maintained verifier/runtime needed to execute them. Do not consume author verdicts, other audit sessions, or the research tool library.
- Write only beneath `/mnt/f/tools/math-audit-round6-20260921/independent-execution/`. Do not change the author package, project sources, plugins, canonical data, or Git.
- Hash frozen inputs and original sources before and after execution. Run the unchanged replay once with `--skip-negative-control`, `python3 -B`, and `PYTHONDONTWRITEBYTECODE=1`. Preserve failures, logs, exit codes, commands, hashes, and the real `CODEX_THREAD_ID`.
- Verify the actual runtime, fresh AuditRound5 and AuditRound6 objects, exact target/type comparison, imports, public declarations, and their dependency/axiom closure. Do not infer mathematical meaning from compilation alone.
- The expensive wrong-expected-type negative control is explicitly not independently rerun. Its author evidence belongs to a separate semantic review.
- Use nonblocking process polling with waits at most 60 seconds. Diagnose before any repetition.

## Session maintenance

- Initial entry: root AGENTS read; frozen replay, contracts, source, and maintained verifier execution path inspected. The output and its replay subdirectory did not previously exist. Independent capture and checking scripts are being created here.
- Execution maintenance: before launching the first replay, 33 frozen input/runtime/original-source identity checks passed. The live root extraction reports exact type, universe, and binder matching. Independent graph traversal also recomputed the 20,642-node root closure. New scripts capture the receipt recheck, per-public-declaration consistency, final reports, and the complete file inventory; all remain within this directory.
- Report precision: local-definition checks distinguish dependency-edge comparison from additional exact AST comparison where the root extraction includes those ASTs. No missing AST is claimed to have been compared.
- Receipt scheduling: once the maintained positive verifier's immutable run has completed, its read-only receipt recheck can overlap the remaining replay controls. The latter only write separate files and read the already-built objects; there is no repeated root proof compilation.
- Independent checks are run once after replay completion and preserve a structural checkpoint while the receipt recheck finishes. Final input hashes and the final verdict are written only after that recheck returns.

- Final maintenance: one actual fresh replay and one receipt recheck completed; independent expression/graph/axiom checks captured in CHECKS.json. REPORT.md and native-session.json state the real execution identity, omitted negative control, and separate semantic-review boundary. Every created artifact is enumerated in FILES.json. No writes were made outside this output scope.
