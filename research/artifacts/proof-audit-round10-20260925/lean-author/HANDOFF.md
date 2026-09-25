# Round10 author handoff checkpoint

Snapshot time: 2026-09-25T06:30:09.267646+00:00. Author delivery only. No independent readback, independent recompilation/semantic review, or full-project build is claimed. The coordinator requested handoff within the existing scope while a long machine check may still be running; no proof was expanded in response.

## Direct blind packet

Send only `formal-only/packet.json` and its listed files to the fresh blind reader. Its main source is `formal-only/AuditRound10.lean`, retaining the actual imports, definitions, theorem names, declarations and proofs, with the single generation-marker comment removed. It has been separately compiled with exit 0. `formal-only/declarations-full.json` has the complete fully explicit declaration types and definition bodies; the ordinary readable variant can suppress proof terms. `formal-only/print-and-axioms.log` is the actual per-named-declaration #print and #print axioms output. `formal-only/environment.json` records the real pinned Lean executable, package versions and search path. Do not give the blind reader HUMAN-CONTRACT.md or this author explanation.

## Current precise target

`AuditRound10.root` in `project/AuditRound10.lean`, byte-identical to frozen `root-project/AuditRound10.lean`. Source SHA-256: `821e19a77ed105f1642cd7dcc660a9992fa05fe0fa40e1021eaca24a178e8bc7`. The full literal conjunction type is in `root-exact-type.lean.txt` and `root-contract.json`; individual clauses are in `root-clauses.json`. The separate natural-language per-target contract is `HUMAN-CONTRACT.md` for the later comparison reviewer. This conjunction covers actual coordinate reversal, derived linear projection/reflection/Euclidean dot-product laws and the explicitly conditional IVT phase/index interface. It does not assert a formalized Sturm theory or a verified executable enumerator.

## Actual completed execution

The final core source compiled with exit 0; the comment-stripped blind source compiled with exit 0. All three false mathematical controls were actually rejected with exit 1 and False remaining. Counterexamples.lean proves their exact negations and compiled with exit 0. All requested named #print/#print axioms commands and the full structured exporter completed. The extracted root type matches the literal contract; transitive axioms are propext, Classical.choice, Quot.sound. Compiler evidence and a root-extraction match are separate from the unfinished overall fresh-evidence receipt.

| Command | Actual exit |
| --- | --- |
| runtime-version | 0 |
| development-01 | 1 |
| development-02 | 0 |
| development-03 | 1 |
| final-source-01 | 0 |
| positive-refutations-01 | 1 |
| positive-refutations-02 | 0 |
| negative-flip-01 | 1 |
| negative-reflection-01 | 1 |
| negative-index-01 | 1 |
| print-main-01 | 0 |
| print-controls-01 | 0 |
| explicit-export-01 | 0 |
| explicit-export-full-01 | 0 |
| blind-source-01 | 0 |
| exact-root-01 | 1 |

Development-01, development-03 and positive-refutations-01 are retained author errors; their snapshots and full logs show the exact fixes. Exact-root-01 returned 1 with stale evidence because Counterexamples.lean changed and ReadbackExportFull.lean was added during its project-wide snapshot. That first run is not a pass. The ongoing successor uses a separate frozen minimal project; its source must remain unchanged.

## Long machine job and continuation

- Job: `exact-root-02-durable`. State at this timestamp: `RUNNING`.
- Supervisor PID/identity: `406656` / `c500489f-6dfc-4fac-ae24-cf69d32ebc1c:15532379`.
- Child PID/identity: `406665` / `c500489f-6dfc-4fac-ae24-cf69d32ebc1c:15532537`.
- Live state: `.research-state/jobs/exact-root-02-durable.json`.
- Actual command, input snapshot and exit: `commands/exact-root-02/command.json`; complete stdout/stderr alongside it.
- Final original-verifier result, once materialized: `evidence/exact-root-02/run-manifest.json`. Do not infer pass from dispatch, zero Lean subcommand exits or file existence alone; read final flags, evidence status and terminal process state.
- At this checkpoint, all Lean subprocesses in the second run had returned 0, declaration comparison was matched, and the original verifier was finishing its environment/freshness evidence. No second overall pass is asserted here.
- An already-running local completion waiter may write REPORT.md, author-result.json and handoff-manifest.json after exact-root-02 actually ends successfully. Those are later author-side observations; this checkpoint and its frozen source/contract files remain the timestamped handoff. If the verifier fails, it leaves the failed run intact and withholds that success report.

`REPLAY.md` contains exact non-overwriting author-side entry points. To start a new root replay against the frozen inputs use `python3 -B launch_frozen.py NEW_LABEL`, or `python3 -B verify_frozen.py NEW_LABEL` in the foreground, from this directory. Do not restart the running job simply because its final report is not yet present. The coordinator's fresh second compilation and semantic check should use their own output directory and preserve these author artifacts.

## Remaining scope

Independent blind readback and the second independent compilation/semantic comparison are assigned to the coordinator. Phase continuity, strict increase and valid per-index brackets remain explicit assumptions. Indices can skip levels; no coverage of every natural level follows unless the caller chooses consecutive indices and supplies those brackets. No phase ODE/lift, Sturm operator, spectral identification, interval arithmetic, numerical solver termination/correctness, interface feasibility after clipping or global symmetry theorem is claimed. All author writes are under formal-author; no project, old evidence, plugin or commit was changed.
