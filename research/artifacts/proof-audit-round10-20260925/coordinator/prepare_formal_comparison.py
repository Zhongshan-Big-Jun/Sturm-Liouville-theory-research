from pathlib import Path
import json,hashlib,shutil,sys,gzip
O=Path('/mnt/f/tools/math-audit-round10-20260925');A=Path('/mnt/f/LaTeX/BVE research/research/artifacts/proof-audit-round10-20260925');R=A/'formal-comparison';S=O/'formal-author'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as V
Readback=json.loads((O/'formal-readback-verified.json').read_text())
if Readback['verdict']!='APPROVED':raise RuntimeError('Blind readback is incomplete')
M=json.loads((S/'evidence/exact-root-02/run-manifest.json').read_text())
assert M['machine_verification_passed'] and M['exact_root_passed'] and M['evidence']['status']=='current'
R.mkdir(parents=True,exist_ok=True)
(R/'AGENTS.md').write_text('# Independent formal comparison\n\nUse only frozen inputs and the recorded read-only compiler/package environment. A different agent authored the proof and another blind reader supplied the readback. Perform a fresh actual compile in your own directory; preserve exact scope and all failures. Do not consult unrelated project history or memory.\n')
Inputs=[]
def put(Name,Data,Role):
 P=R/'inputs'/Name;P.parent.mkdir(parents=True,exist_ok=True)
 if P.exists() and P.read_bytes()!=Data:raise RuntimeError('Frozen input drift '+Name)
 P.write_bytes(Data);Inputs.append(dict(path=str(P.relative_to(R)),role=Role))
for N in ['HUMAN-CONTRACT.md','root-contract.json','root-exact-type.lean.txt','root-clauses.json','formal-declarations-full.json','per-declaration-axioms.json','blind-transform.json','execution-summary.json','run.py','verify_frozen.py','REPLAY.md']:
 put(N,(S/N).read_bytes(),'intended-contract-and-machine-evidence')
for N in ['AuditRound10.lean','Counterexamples.lean','NegativeFlip.lean','NegativeReflection.lean','NegativeIndex.lean','PrintAuditRound10.lean','PrintCounterexamples.lean','ReadbackExportFull.lean','lean-toolchain','lakefile.toml','lake-manifest.json']:
 put('project/'+N,(S/'project'/N).read_bytes(),'formal-source-or-pinned-environment')
put('blind/AuditRound10.lean',(S/'formal-only/AuditRound10.lean').read_bytes(),'blind-source-identity')
put('blind/readback-completion.json',(O/'formal-readback-completion.json').read_bytes(),'actual-independent-blind-readback')
put('blind/verified-receipt.json',(O/'formal-readback-verified.json').read_bytes(),'blind-readback-provenance-only')
put('exact-root/run-manifest.json.gz',gzip.compress((S/'evidence/exact-root-02/run-manifest.json').read_bytes(),mtime=0),'exact-target-machine-evidence-lossless-gzip')
Run=next((S/'evidence/exact-root-02/lean-verification-runs').iterdir())
for P in sorted(Run.rglob('*')):
 if P.is_file() and P.suffix in ['.lean','.log','.json'] and P.name not in ['run-manifest.json','declaration.json']:
  put('exact-root/run/'+str(P.relative_to(Run)),P.read_bytes(),'exact-target-command-or-log')
Scope='''# Required independent work

Personally compare every supplied declaration/definition and the materialized root with the human contract and the actual blind readback. Do not promote the author-machine PASS to semantic approval. In particular distinguish all natural indices (including 0), arbitrary strictly increasing versus consecutive indices, per-index bracket assumptions, classical existence versus execution, and vector algebra versus feasible physical interfaces.

Independently execute the recorded Lean 4.31.0 runtime in a NEW private directory under /mnt/f/tools/math-audit-round10-20260925/formal-reviewer/. Copy only frozen project inputs there. The supplied run.py is an author-side example, not an instruction to write into its directory: adapt your own output/base paths and role, preserve actual source bytes, and record command/environment/log hashes and actual exits. Read-only imports may use exactly the recorded installed Mathlib/package paths under /mnt/f/LaTeX/BVE research/lean-proof/.lake/packages, and the exact runtime under /mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0. Do not read unrelated repo sources/history, other reviews, or memory. Verify source identity and actual imported local object paths; do not silently use old AuditRound10 objects.

Compile the actual module, its literal exact root type, all positive counterexample proofs and declaration/axiom print files. Execute each negative target and inspect that it fails at the intended mathematical contradiction, not imports, syntax, a timeout or a missing binary. Compare each positive proposition with the literal negation of its negative target. Re-export all declarations/definitions at fully explicit printing limits, adapting only the export output path; compare actual types/definitions with the supplied 38-entry export. Check root transitive axioms, no sorryAx/unsafe/custom axioms, exact source/environment/manifest identities and intended-versus-formal fidelity. The large original run manifest is losslessly gzip-compressed; inspect by structured queries instead of dumping its entire expanded type.

The original exact-root machine check was direct, not a full Lake project build. It reports semantic:not_reviewed, which is correct before this review. Your semantic verdict must remain scoped to the local interfaces. The Python phase solver, Sturm ODE, actual spectral identification, interval certification and global extrema are outside this formal contract. Save your new real execution records, scripts, all failures and an evidence manifest in your private directory. Return their exact path in your final limitations/reasons as well as the required packet JSON. Do not edit packet inputs or the author directory.
'''
put('execution-scope.md',Scope.encode(),'review-execution-and-scope-contract')
Spec=dict(kind='mathematics',author_ids=['01a06f46-dd03-7c83-9267-32048412c359','01a0d723-0c42-7142-a358-78252676dccd','01a0d74b-2c67-7a52-b0b8-f43dd64f1c31'],inputs=Inputs,claims=[
 dict(id='R10-formal-reflection-fidelity',verification='formal',statement='Check actual finite coordinate reversal, linear maps, complementary orthogonal projectors, affine reflection and perturbation against the contract and blind readback. Inspect true nontrivial cases and premises; do not claim physical feasibility or optimizer confinement.'),
 dict(id='R10-formal-index-interface-fidelity',verification='formal',statement='Check phase_root, half-line assumptions, unique bracket roots, order equivalence and conditional sequence existence for the exact types and quantifiers. State that arbitrary increasing indices need not be consecutive and bracket existence is a premise; no Sturm operator or executable enumeration is formalized.'),
 dict(id='R10-independent-formal-execution',verification='formal',statement='Personally perform the fresh execution and identity/axiom/definition checks required by execution-scope.md, including actual positive and negative controls and literal root-type matching. Distinguish author machine evidence, blind translation and your own execution/semantic decision; report exact private evidence path and all limitations.')])
(O/'formal-comparison-spec.json').write_text(json.dumps(Spec,ensure_ascii=False,indent=2)+'\n')
(O/'formal-comparison-root.json').write_text(json.dumps({'project':str(R)})+'\n')
(O/'formal-comparison-packet.json').write_text(json.dumps(V.create_packet(R,Spec),ensure_ascii=False,indent=2)+'\n')
print('Prepared independent formal comparison',len(Inputs),'inputs')
