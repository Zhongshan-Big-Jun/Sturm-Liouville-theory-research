from pathlib import Path
from collections import Counter
import datetime,hashlib,json,re,shutil
from run_lean import OUT,ROOT,SOURCE,digest

def save(name,data):
	(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def item(p):
	p=Path(p);return {'path':str(p),'sha256':digest(p),'bytes':p.stat().st_size}

positive=json.loads((OUT/'verifier-positive/run-manifest.json').read_text())
negative=json.loads((OUT/'verifier-false-expected/run-manifest.json').read_text())
assert positive['machine_verification_passed'] and positive['exact_root_passed']
assert positive['target']['comparison']['status']=='matched'
assert positive['semantic']['status']=='not_reviewed'
assert negative['machine_verification_passed'] and not negative['exact_root_passed']
assert negative['target']['comparison']['status']=='mismatched'
assert negative['root_closure']['status']=='target_mismatch'
assert negative['semantic']['status']=='not_reviewed'
assert all(x['evidence']['status']=='current' for x in [positive,negative])
assert not any(x['target']['unexpected_axioms']+x['target']['unsafe_dependencies']+x['target']['unknown_dependencies'] for x in [positive,negative])
assert SOURCE.read_bytes()==(OUT/'verifier-project/SL/AuditRound5.lean').read_bytes()==(OUT/'final/AuditRound5.lean').read_bytes()

declarations=json.loads((OUT/'final/declarations.json').read_text())
D=declarations['declarations'];entries=re.findall(r'^(def|theorem) (\w+)',SOURCE.read_text(),re.M)
assert {d['declaration'] for d in D}=={'SL.AuditRound5.'+n for _,n in entries}
assert json.loads((OUT/'closure-consistency.json').read_text())['all_match']
assert all(set(d['transitive_axioms'])<={'propext','Classical.choice','Quot.sound'} for d in D)
assert not any(n.get('missing') or n.get('unsafe') for n in declarations['dependencies'])

modules=json.loads((OUT/'final/module-artifact-hashes.json').read_text())
loaded=json.loads((OUT/'final/loaded-modules.json').read_text())
assert modules['module_count']==loaded['module_count']==len(loaded['modules'])
assert {r['module'] for r in modules['modules']}=={r['module'] for r in loaded['modules']}
for r in modules['modules']:
	for f in r['artifacts']:
		s=Path(f['path']).stat()
		assert (s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(f['bytes'],f['mtime_ns'],f['ctime_ns']),f['path']
actual=next(m for m in modules['modules'] if m['module']=='SL.AuditRound5')
assert actual['resolved_olean']==str(OUT/'build/SL/AuditRound5.olean')
assert actual['artifacts'][0]['sha256']==digest(OUT/'build/SL/AuditRound5.olean')

protected=[]
for fn in ['protected-baseline.json','protected-objects-before.json']:
	baseline=json.loads((OUT/fn).read_text())
	changed=[p for p,h in baseline.items() if not Path(p).is_file() or digest(p)!=h]
	assert not changed,changed
	protected.append({'baseline':fn,'count':len(baseline),'all_byte_identical':True})
save('protection-check.json',{'checks':protected,'author_check':True})

expected={'01-version':0,'02-initial-polynomials':1,'03-expanded-local-algebra':1,'04-residue-normalization':0,'05-complete-root':0,'06-all-declarations':0,'07-maintained-verifier-positive':0,'08-positive-controls':0,'10-false-high-span-equality':1,'11-resolved-imports':0,'12-maintained-verifier-false-expected':1}
logs=[]
for name,code in expected.items():
	p=OUT/'logs'/(name+'.json');r=json.loads(p.read_text())
	assert r['exit_code']==code and r['source_unchanged_during_run'],name
	for stream in ['stdout','stderr']: assert digest(p.with_suffix('.'+stream+'.txt'))==r[stream+'_sha256']
	logs.append({'name':name,'expected_exit':code,'actual_exit':r['exit_code'],'seconds':r['duration_seconds'],'record':item(p)})
for name in ['06-all-declarations','08-positive-controls','10-false-high-span-equality','11-resolved-imports']:
	r=json.loads((OUT/'logs'/(name+'.json')).read_text())
	assert r['source_sha256_before'][str(OUT/'build/SL/AuditRound5.olean')]==digest(OUT/'build/SL/AuditRound5.olean')
	assert r['source_sha256_before'][str(SOURCE)]==digest(SOURCE)
for name in ['05-complete-root','06-all-declarations','08-positive-controls']:
	assert 'warning:' not in (OUT/'logs'/(name+'.stdout.txt')).read_text()
save('command-index.json',logs)

root_objects=[item(OUT/'build/SL/AuditRound5.olean')]
for r in [positive,negative]:
	p=next(c['olean'] for c in r['build']['commands'] if c['kind']=='target')
	root_objects.append(item(p))
for r in [positive,negative]:
	assert r['input_hashes']['SL/AuditRound5.lean']==digest(SOURCE)
save('root-object-bindings.json',{'source':item(SOURCE),'objects':root_objects,'source_snapshots_byte_identical':True,'binary_identity_claimed':False,'note':'Separate compilations have separately bound binary hashes. The root statement and all fields exported for its 12601 dependency nodes match across author and positive-verifier extraction; see author-verifier-binding-checked.json. No binary identity is required or asserted.'})

save('final/public-theorem-axioms.json',{'source_sha256':digest(SOURCE),'object_sha256':root_objects[0]['sha256'],'evidence':'Lean collectAxioms executed on each actual imported declaration; graph recomputation is an additional author check.','theorems':[{'declaration':d['declaration'],'fully_explicit_type':d['fully_explicit_type'],'transitive_axioms':d['transitive_axioms']} for d in D if d['kind']=='theorem']})
save('controls-result.json',{'positive_compilation':item(OUT/'logs/08-positive-controls.json'),'negative_compilation':item(OUT/'logs/10-false-high-span-equality.json'),'false_expected_claim':'forall m0, high_span m0 = oblique inf krein_polynomials','falsity_witness':'1 + X is in the right subspace and absent from high_span for all m0; the positive control compiles its negation.','positive_verifier':{'manifest':item(OUT/'verifier-positive/run-manifest.json'),'exact_root_passed':True,'status':positive['root_closure']['status']},'false_expected_verifier':{'manifest':item(OUT/'verifier-false-expected/run-manifest.json'),'exact_root_passed':False,'status':negative['root_closure']['status']},'semantic_certification':False})

source_hash=digest(SOURCE);object_hash=root_objects[0]['sha256']
commands='''
## Frozen identity and executable commands

- Live source SHA-256: `{source_hash}`.
- Actual author-inspected root object SHA-256: `{object_hash}`.
- Representative declaration: `SL.AuditRound5.local_algebra_root`.
- Exact elaborated type SHA-256 (maintained verifier): `{type_hash}`.
- Verifier semantic identity (NOT a review verdict): `{semantic_hash}`.
- Mathlib manifest revision: `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` (v4.31.0).
- Actual platform/version log: `logs/01-version.stdout.txt`.

Run the following from `/mnt/f/tools/math-audit-round5-20260921/lean-author`. Each runner refuses to overwrite an existing command receipt. Use new receipt/output names for additional replays. Original argument vectors, effective LEAN_PATH and exact external working directory are saved in logs/*.json; the compiler always receives absolute paths.

```bash
python3 run_lean.py replay-version version
python3 run_lean.py replay-live-root build
python3 run_lean.py replay-positive probe controls/PositiveControls.lean
python3 run_lean.py replay-false-claim probe controls/FalseHighSpanEquality.lean
PYTHONDONTWRITEBYTECODE=1 python3 verify_contract.py replay-positive-verifier positive-contract.json replay-positive-verifier
PYTHONDONTWRITEBYTECODE=1 python3 verify_contract.py replay-negative-verifier false-expected-contract.json replay-negative-verifier
```

The false-claim compiler command and negative-verifier command are EXPECTED to exit 1. Other listed commands must exit 0. The original run names are in `command-index.json`. Replaying `build` regenerates only this author's NEW external root object and saves its previous bytes; it never touches pre-existing project objects. An external coordinator should prefer its own fresh output directory. The verifier project is a byte-identical source snapshot; `snapshot-binding.json` and `root-object-bindings.json` bind it to the live root. Do not silently reuse these identities if the live source changes.

## Completed evidence

{theorems} theorems and {definitions} definitions were actually elaborated. Every public theorem and definition has a Lean transitive axiom export, with union {{propext, Classical.choice, Quot.sound}} and no sorryAx, unknown or unsafe dependency. A separate author graph recomputation matches all 59 exports. Actual module inventory: {modules} loaded modules, {artifacts} available olean/private/server/IR artifacts. Artifact bytes were freshly SHA-256 hashed; before/after metadata consistency was also checked. Runtime executable/DLL and project configuration hashes are in `environment.json`.

The maintained positive verifier reports `machine_verification_passed=true`, `exact_root_passed=true`, `root_closure=closed`, and `semantic.status=not_reviewed`. Its second fresh compilation uses the exact saved source. The negative expected equality reports `target_mismatch` with machine execution successful and exact-root pass false. The direct compiler negative fails on the false equality while the positive source compiles the explicit counterexample and its negation. All failed commands remain under logs/ and attempts/.

The author root and verifier root have distinct binary object hashes, both recorded; no binary identity is claimed. Their root expression, axiom set, dependency set and every field exported for the 12,601 common root dependency nodes match exactly. The first comparison diagnostic is preserved: the union-of-59 author export has one extra type_expression field for Nat.instAtLeastTwoHAddOfNat that the root-only export omits. The corrected comparison checks all root-exported fields and retains this explicit difference.

`final/READBACK_INPUTS.json` selects only actual compiler statements and definitions without informal intent or proof scripts. `SEMANTIC_REVIEW_INPUTS.json` selects this contract, source, informal sources and evidence for the separate reviewer. Neither review has been performed by this author. This is not semantic certification, independent proof review, a full project build, nor verification of analytic cofinite classification.
'''.format(source_hash=source_hash,object_hash=object_hash,type_hash=positive['target']['type_sha256'],semantic_hash=positive['target']['semantic_sha256'],theorems=37,definitions=22,modules=modules['module_count'],artifacts=modules['artifact_count'])
(OUT/'CONTRACT.md').write_text((OUT/'CONTRACT.draft.md').read_text()+commands)

review_files=['CONTRACT.md','positive-contract.json','false-expected-contract.json','final/AuditRound5.lean','final/READBACK_INPUTS.json','final/declarations.json','final/public-theorem-axioms.json','final/loaded-modules.json','final/module-artifact-hashes.json','environment.json','root-object-bindings.json','author-verifier-binding-checked.json','closure-consistency.json','controls-result.json','command-index.json','protection-check.json','input-hashes.json','verifier-positive/run-manifest.json','verifier-false-expected/run-manifest.json','source-snapshot/01-cofinite_replacement_proof.md','source-snapshot/02-candidate_proof.md']
save('SEMANTIC_REVIEW_INPUTS.json',{'kind':'Author submission for a separate correspondence reviewer','review_status':'NOT_PERFORMED; independent review reserved to coordinator','files':[item(OUT/n) for n in review_files]})
summary={'status':'AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW','source':item(SOURCE),'root':root_objects[0],'counts':dict(Counter(d['kind'] for d in D)),'all_public_axiom_closures_checked':True,'axioms_union':sorted({a for d in D for a in d['transitive_axioms']}),'loaded_modules':modules['module_count'],'hashed_import_artifacts':modules['artifact_count'],'maintained_positive_exact_root_passed':True,'false_expected_rejected':True,'positive_controls_passed':True,'negative_compiler_exit':1,'semantic_review':'not_reviewed','platform':'Lean 4.31.0 Windows PE via WSL; no Linux-native run claimed','scope':'Real polynomial local algebra only; full exclusions in CONTRACT.md','protected_files':protected,'old_project_objects_on_author_LEAN_PATH':False,'full_lake_build':False,'downloaded_dependencies':False,'spawned_agents':False,'git_operations':False,'canonical_or_card_changes':False,'runtime_identity':item(OUT/'environment.json'),'failed_attempts_preserved':['02-initial-polynomials','03-expanded-local-algebra','10-false-high-span-equality (intentional)','12-maintained-verifier-false-expected (intentional)'],'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
save('FINAL_CHECKS.json',summary)
(OUT/'REPORT.md').write_text(f'''# Fifth-round Lean author submission

37 theorems and 22 definitions in the sole new project file `lean-proof/SL/AuditRound5.lean` compile under actual Lean 4.31.0 (Windows PE runtime via WSL). No Linux-native execution is claimed. The scope is all-index local algebra over `Polynomial ℝ`: two traces, Krein residues, arbitrary sparse-tail spans, the 1+X oblique witness, an actual 2x2 residue matrix and inverse/correction, and explicit trace-lift decomposition.

All 59 declaration axiom closures are exported and author-cross-checked. Only propext, Classical.choice and Quot.sound occur. Positive controls pass; a false high-span equality fails; the maintained verifier accepts the complete representative root contract and rejects the false expected equality. Its semantic status is explicitly not_reviewed. {modules['module_count']} loaded modules and {modules['artifact_count']} import artifacts are hash-bound, along with runtime, source snapshots, objects and actual commands/logs. Prior 45 Lean sources plus 3 project configuration files and 32 compiled project objects remain byte-identical.

- Full scope, hypotheses, exclusions, hashes and executable commands: CONTRACT.md.
- Stripped compiler exports for fresh blind readback: final/READBACK_INPUTS.json.
- Separate reviewer contract/evidence packet: SEMANTIC_REVIEW_INPUTS.json.
- Summary and raw receipts: FINAL_CHECKS.json, command-index.json, logs/, attempts/, verifier-positive/, verifier-false-expected/.
- Every created path: CHANGED_PATHS.txt; final file integrity inventory: FILE_HASHES.sha256.

No Sobolev closure/density, cutoff convergence, Green integral, operator isomorphism, complex result, cofinite analytic classification or full O1pLD is formalized. Author work is complete; independent blind reading and correspondence review are pending coordinator action. No old Lean/configuration/dependency file, canonical/card, Git state or prior evidence was edited; no agents were spawned.

Source SHA-256: {source_hash}
Author inspected object SHA-256: {object_hash}
''')
# Include inventory files themselves in path inventory; exclude a hash manifest's own digest.
paths=[SOURCE]+sorted(p for p in OUT.rglob('*') if p.is_file())
paths+= [OUT/'CHANGED_PATHS.txt',OUT/'FILE_HASHES.sha256']
paths=sorted(set(paths),key=str)
(OUT/'CHANGED_PATHS.txt').write_text('\n'.join(map(str,paths))+'\n')
files=[SOURCE]+sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='FILE_HASHES.sha256')
(OUT/'FILE_HASHES.sha256').write_text('\n'.join(digest(p)+'  '+str(p) for p in files)+'\n')
print(json.dumps({k:summary[k] for k in ['status','counts','loaded_modules','hashed_import_artifacts','maintained_positive_exact_root_passed','false_expected_rejected','semantic_review']},indent=2))
