from pathlib import Path
import json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A='research/artifacts/proof-audit-round8-20260922'
readback=json.loads((O/'formal-readback-received.json').read_text())
if readback['verdict']!='APPROVED':raise RuntimeError('Blind readback unavailable')
authors=[json.loads((O/(n+'-spawn.json')).read_text())['result']['agent_id'] for n in ['sliver-author','certificate-author','lean-author']]+['01a06f46-dd03-7c83-9267-32048412c359']
inputs=[{'path':p,'role':role} for p,role in [
('lean-proof/SL/AuditRound8.lean','current exact formal source'),
(A+'/lean-author/round8-lean-frozen-inputs.zip','frozen executable replay source, external environment identities, author contracts and scope'),
(A+'/lean-author/handoff-manifest.json','author archive identities, no independent approval'),
(A+'/lean-author/author-replay-03/declarations.json','actual author elaborated types, definitions, root dependencies and transitive axioms'),
(A+'/lean-author/author-replay-03/evidence.json','author replay execution summary'),
(readback['bundle']+'/report.json','independent blind readback'),
(readback['bundle']+'/dispatch.json','blind reviewer provenance'),
(readback['bundle']+'/spawn.json','actual blind spawn transcript'),
('docs/SL_gap_n1_inf_limit_proof.tex','informal current target; full proof separately audited'),
(A+'/submitted/proof_audit_round8_20260922.md','external reported counterexamples to verify')]]
for x in inputs:
	if not (R/x['path']).is_file():raise RuntimeError('Missing formal input '+x['path'])
claims=[
{'id':'fresh-kernel-replay','verification':'formal','statement':'Personally perform a fresh compiler replay from the supplied frozen zip, in your own output directory /mnt/f/tools/math-audit-round8-20260922/formal-reviewer only. Copy/extract the zip there, inspect replay.py/run_lean.py before executing, then run copied replay.py with a NEW output directory. Reading installed pinned Lean/Mathlib artifacts and runtime metadata only as required by that supplied runner is authorized; do not inspect unrelated project files, memory, skills or author conversations. No global config changes, downloads or Lake rebuild. Keep every real argv/exit/stdout/stderr receipt and failure. Verify source matches current standalone file, root object freshly compiled/resolved, nine-conjunct exact contract, full actual declarations and definitions, closed transitive dependencies, allowed axioms, before/after imported artifact identities, positive target and three genuinely false/wrong target controls. A preexisting author olean must not count as your fresh root. Use your independent actual result, not author pass labels.'},
{'id':'semantic-correspondence','verification':'formal','statement':'Compare the supplied independent blind readback and your actual exported declarations against the intended local targets in the current informal source and frozen author scope. Check phase at R1600/u1/1600 uses explicit 0<=lambda2<=4pi², the real definitions of C/S/I2 and their trigonometric bridge, all nonzero and interval hypotheses, stationary coefficient identity/positivity, exact rational 0.8256 ratio, and both B/D curved-coverage witnesses with actual pi/sqrt. No conclusion may be assumed as its own evidence. Total division/sqrt definitions do not imply theorem hypotheses outside their domains.'},
{'id':'scope-provenance','verification':'formal','statement':'Verify 47 public declarations (including compiler auxiliaries) are all accounted for and semantic dependency/definition bodies are the actual compiled ones. Check the reported constants and curve witnesses are meaningful local facts, not full spectral minmax, I2 integral identification, analytic implicit-function expansions/remainders, global sliver/T1 or general optimal-parameter convergence. Inspect supplied identities and all failures; report machine execution and semantic approval separately with exact limitations. Save your execution manifest under your output directory and name its paths/hashes in your final JSON reasons or limitations for the coordinator to archive.'}]
spec=dict(kind='mathematics',author_ids=authors,inputs=inputs,claims=claims)
(O/'formal-semantic-spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
print('Formal semantic/execution packet specification ready')
