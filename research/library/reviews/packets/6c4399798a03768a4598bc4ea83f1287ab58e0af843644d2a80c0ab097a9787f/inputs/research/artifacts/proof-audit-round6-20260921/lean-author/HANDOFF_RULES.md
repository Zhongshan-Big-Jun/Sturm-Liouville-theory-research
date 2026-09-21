# Current handoff selection

The coordinator's later instruction changes packet selection, not mathematics:
blind readback receives only actual elaborated types and reachable definition
data, including the reachable fifth-round definitions. No complete fifth-round
source, source comments, proof scripts, expected contract or author verdict is
part of the blind packet. `HANDOFF.json` gives the exact selected files/hashes.

Full unchanged `snapshot/SL/AuditRound5.lean` belongs to the semantic/execution
packet only. That packet also includes the fixed contract, both candidate
appendices, exact source/runtime/pin bindings and raw execution evidence.

This selection supersedes the sentence suggesting a preserved AuditRound5
source in the blind packet in the already-frozen `CONTRACT.md`. The frozen file
is retained byte for byte because the running job binds it as an input. Its
mathematical scope and exclusions remain unchanged.

Author checking followed by the coordinator's fresh independent execution is
the intended procedure. There is no need for repeated full environment dumps
for each theorem. `public-declarations.json` contains per-declaration types and
axiom lists; `shared-public-dependency-graph.json` is the shared closure graph.
