# Author work log

The user assigned a sixth-round formalization author role, explicitly excluding
independent final review, agent spawning, edits to old Lean files/config/objects,
canonical and plugin changes. Authorized writes are the new
`lean-proof/SL/AuditRound6.lean` and this external directory. The coordinator
handles AGENTS, reports, library and Git.

Read root AGENTS.md and the installed lean-verify 2.0.0 SKILL.md plus
`references/v2-verification.md`, and inspected the actual maintained verifier,
runtime and Lean probe source. Also read the two supplied candidate appendices,
the unchanged AuditRound5 source, fifth-round environment.json/run_lean.py,
and relevant local Mathlib source. A brief memory lookup informed only scope
caution; no historical PASS or mathematical boundary was reused as verification.

The scope selected is the four concrete real-algebra targets in CONTRACT.md.
No artificial Boolean model replaces an analytic assertion. The optional
general projection identity and finite-dimensional tail-obstacle theorem are
omitted to keep the deliverable focused. Lean sources use spaces because Lean
rejects tab tokens; external Python scripts use tabs.

Development execution is recorded per attempt, preserving source snapshots and
raw compiler stdout/stderr, actual exit codes, exact arguments, search paths,
executable and source/config hashes. Search uses only this task's fresh objects
and existing package objects. The final maintained verifier uses a minimal
frozen project with two local sources; it rebuilds both in its fresh output.

## Preserved development failures

- Initial runner: an overly strict assertion required a build directory for
  every manifest package. `Cli` has no such directory. Both attempted commands
  failed in Python before any compiler launch. Initial runner, input snapshots,
  captured traceback text and package-path discovery are retained.
- `05-core-first`: an empty higher-priority `SL` directory shadowed the newly
  building dependency; the compiler reported the exact missing object. Later
  development attempts use a single per-attempt library containing a byte-for-
  byte copy of the AuditRound5 object rebuilt by this task. The final verifier
  independently rebuilds dependencies, so it does not consume that copy.
- `06-core-first-elaboration`: the prose sequence `+/-1` nested a Lean comment,
  causing an unterminated comment. The comment now says `1 and -1`.
- `07-core-elaboration`: all-index spans and the Euclidean inner products
  elaborated, but Matrix notation needed its scoped opening; determinant
  indices and polynomial coefficient normalization needed explicit lemmas.
- `08-normalization`, `09-determinant-expansion`, `10-determinant-reduction`:
  determinant simplification hit recursion limits. Source inspection found
  the `Matrix.vecCons`/`Fin.cons` simplification interaction. Replaced unfolding
  with `Matrix.cons_val_two` and `Matrix.cons_val_three`, without changing the
  theorem statement or introducing an assumed determinant.

Subsequent actual outcomes, including packaging or control failures if any,
are in command logs and the final REPORT.md. This log is not an approval.

## Final development compilation

Attempts 11 and 12 retained further finite-index reduction failures. Attempt 13
replaced broad unfolding by three explicitly typed, reflexive index equalities.
The full source then compiled with exit 0 in 28.09 seconds, without stdout or
stderr. Source SHA-256: f765205b55ee454261a1a365e157ffa4f4f0202662c450b8a9c92328820a7c3e.
The frozen replay package was then created. All nine actual package Git heads
matched their manifest revisions, including the source-only Cli dependency.
The maintained verifier rebuilt both local modules; the extracted root type
matched its expected type, with no outer binders and only propext,
Classical.choice and Quot.sound. Final manifest and controls were still pending
at the time of this entry.

## Completed author handoff

The first foreground packaging run ended with outer exit 143 before a final
receipt; its cause is unknown and INTERRUPTED.json preserves the observation.
The installed workflow supervisor reran the unchanged frozen replay as
round6-lean-author-02. Positive maintained verification exited 0; the compiling
positive control exited 0; the deliberately wrong determinant expected type
produced a machine-successful target_mismatch and strict exit 1. The overall
author replay completed successfully. No independent approval is claimed.

The coordinator requested elaborated reachable R5 definitions in blind readback,
not full source with comments/proofs. BLIND_PACKET.json and HANDOFF.json now
select actual types and all 24 reachable local definitions (9 R5), while full
R5 source belongs only to semantic/execution inputs. HANDOFF_RULES.md supersedes
the older handoff suggestion in the already-frozen CONTRACT.md.

Final closure comparison passed for all 36 public declarations. The first
finalization attempt stopped on a concurrent SL/.gitattributes append; its
traceback and script are retained. The append is exactly the new R6 -text rule
and comment; prior bytes remain an exact prefix. It is recorded separately,
not silently counted as unchanged. The other 305 protected files match their
baseline hashes. This author did not write or revert the Git attributes file.
