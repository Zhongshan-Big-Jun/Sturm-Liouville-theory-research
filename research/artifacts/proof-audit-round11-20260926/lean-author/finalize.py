from run import *
import re
RootPath=BASE/'evidence/exact-root-01/run-manifest.json'
Root=json.loads(RootPath.read_text())
assert Root['exact_root_passed'] is True
Target=Root['target']
assert Target['comparison']['status']=='matched'
assert Root['semantic']['status']=='not_reviewed'
Controls=json.loads((BASE/'author-checks.json').read_text())
Closure=json.loads((BASE/'closure-controls.json').read_text())
assert len(Controls)==7 and all(X['as_expected'] for X in Controls)
assert len(Closure)==4 and all(X['as_expected'] for X in Closure)
for Check in Controls:
	if Check['expected_exit']==1:
		Log=(BASE/'commands'/Check['label']/'stdout.log').read_text()
		Errors=[Line for Line in Log.splitlines() if 'error:' in Line]
		assert Errors and all('error: unsolved goals' in Line for Line in Errors),(Check['label'],Errors)
Hidden=json.loads((BASE/'evidence/closure-hidden-axiom-01/run-manifest.json').read_text())
assert Hidden['target']['unexpected_axioms']==['Round11Control.hidden']
Wrong=json.loads((BASE/'evidence/closure-wrong-type-01/run-manifest.json').read_text())
assert Wrong['target']['comparison']['status']=='mismatched'
Missing=json.loads((BASE/'evidence/closure-missing-target-01/run-manifest.json').read_text())
assert Missing['exact_root_passed'] is False
assert any('Exact root declaration not found: Round11Control.missing' in P.read_text() for P in (BASE/'evidence/closure-missing-target-01').glob('lean-verification-runs/*/logs/*.stdout.log'))
Recheck=json.loads((BASE/'commands/receipt-recheck-01/stdout.log').read_text())
assert Recheck['exact_root_passed'] is True and Recheck['status']=='current'
Names=json.loads((BASE/'declaration-names.json').read_text())
Decls=json.loads((BASE/'declarations-full.json').read_text())
ByName={X['name']:X for X in Decls}
assert set(Names)<=set(ByName)
assert all(not re.search(r'⋯|\.\.\.',X.get(K,'')) for X in Decls for K in ('type_explicit','value_explicit'))
Allowed={'propext','Classical.choice','Quot.sound'}
assert all(set(X['transitive_axioms'])<=Allowed for X in Decls)
Source=PROJECT/'AuditRound11.lean'
Text=Source.read_text()
Theorems=re.findall(r'^theorem (\w+)',Text,re.M)
assert len(Theorems)==14
assert not re.search(r'\b(sorry|admit|axiom|unsafe)\b',Text)
assert digest(Source)==digest(BASE/'formal-only/AuditRound11.lean')
Cmds=[]
for P in sorted((BASE/'commands').glob('*/command.json')):
	D=json.loads(P.read_text())
	assert 'exit_code' in D and 'utc_end' in D,(P,'unfinished')
	assert D['inputs_unchanged'],P
	assert digest(P.parent/'stdout.log')==D['stdout_sha256'],P
	assert digest(P.parent/'stderr.log')==D['stderr_sha256'],P
	Cmds.append({'label':D['label'],'exit_code':D['exit_code'],'seconds':D['seconds'],'record':str(P.relative_to(BASE)),'record_sha256':digest(P)})
External=[]
for X in json.loads((BASE/'external-inputs.json').read_text()):
	P=Path(X['path'])
	External.append({'path':str(P),'before':X['sha256'],'after':digest(P),'unchanged':digest(P)==X['sha256']})
Existing=json.loads((BASE/'readonly-lean-before.json').read_text())
LeanAfter={P:digest(ORIGINAL.parent/P) for P in Existing['sources']}
PluginBaseline=json.loads((BASE/'environment-baseline.json').read_text())
PluginAfter={P:digest(P) for P in PluginBaseline['plugin_files']}
RuntimeAfter={P:digest(P) for P in PluginBaseline['runtime_files']}
Protected={'external_inputs':External,'old_lean_count':len(LeanAfter),'old_lean_sources_unchanged':LeanAfter==Existing['sources'],'plugin_runtime_files_unchanged':PluginAfter==PluginBaseline['plugin_files'],'lean_runtime_files_unchanged':all(RuntimeAfter[P]==D['sha256'] for P,D in PluginBaseline['runtime_files'].items()),'scope':'Compared the recorded read-only inputs, 52 existing Lean sources, installed verifier files and Lean runtime binaries. This is not a whole-repository or whole-cache filesystem audit.'}
write_json(BASE/'readonly-postcheck.json',Protected)
assert all(X['unchanged'] for X in External) and Protected['old_lean_sources_unchanged'] and Protected['plugin_runtime_files_unchanged'] and Protected['lean_runtime_files_unchanged']
ExportCoverage={'source_sha256':digest(Source),'export_sha256':digest(BASE/'declarations-full.json'),'named_count':len(Names),'named_theorems':len(Theorems),'named_definitions_or_abbreviations':len(Names)-len(Theorems),'actual_namespace_declarations':len(Decls),'compiler_generated_names':sorted(set(ByName)-set(Names)),'missing_names':sorted(set(Names)-set(ByName)),'explicit_type_and_definition_body_truncation':False,'all_actual_transitive_axioms':sorted({A for X in Decls for A in X['transitive_axioms']})}
write_json(BASE/'export-coverage.json',ExportCoverage)
write_json(BASE/'per-declaration-axioms.json',{'source_sha256':digest(Source),'export_sha256':digest(BASE/'declarations-full.json'),'declarations':[{K:X[K] for K in ('name','kind','universes','binder_kinds','transitive_axioms')} for X in Decls]})
write_json(BASE/'execution-summary.json',Cmds)
Environment={'source_sha256':digest(Source),'contract_sha256':digest(BASE/'contract.json'),'human_contract_sha256':digest(BASE/'contract.md'),'environment_sha256':Target['environment_sha256'],'semantic_environment_sha256':Target['semantic_environment_sha256'],'semantic_sha256':Target['semantic_sha256'],'type_sha256':Target['type_sha256'],'runtime_baseline':'environment-baseline.json','runtime_baseline_sha256':digest(BASE/'environment-baseline.json'),'root_manifest':str(RootPath.relative_to(BASE)),'root_manifest_sha256':digest(RootPath),'receipt_recheck':'commands/receipt-recheck-01/command.json'}
write_json(BASE/'source-environment-binding.json',Environment)
Summary={'schema_version':1,'role':'author','status':'AUTHOR_SELF_CHECK_COMPLETE_INDEPENDENT_REVIEW_PENDING','main_source':'project/AuditRound11.lean','root_declaration':'AuditRound11.root','root_clauses':13,'loaded_environment_modules':Target['loaded_module_count'],'imported_artifact_files':len(Target['import_artifacts']),'named_main_theorems':14,'named_definitions_or_abbreviations':12,'actual_exported_namespace_declarations':len(Decls),'source_sha256':digest(Source),'machine_verification_passed':Root['machine_verification_passed'],'exact_root_passed':Root['exact_root_passed'],'receipt_current':Recheck['snapshot_current'],'axioms':Target['axioms'],'semantic_review':'not_reviewed','independent_blind_readback':'pending','independent_acceptance':'pending','binding':'source-environment-binding.json','human_contract':'contract.md','machine_contract':'contract.json','blind_packet':'formal-only/packet.json','explicit_declarations':'declarations-full.json','axiom_export':'per-declaration-axioms.json','root_manifest':str(RootPath.relative_to(BASE)),'controls':{'math_positive_groups':1,'math_negative_groups':4,'exact_verifier_positive_groups':1,'exact_verifier_negative_groups':3,'all_outcomes_expected':True},'development_failures':['commands/main-01/command.json'],'negative_records':[X['command_record'] for X in Controls if X['expected_exit']==1]+[X['manifest'] for X in Closure if not X['expected_exact_root_passed']],'readonly_postcheck':'readonly-postcheck.json','constraints':{'only_author_directory_written':True,'main_repository_modified_by_author':False,'old_lean_cache_or_plugin_modified_by_author':False,'full_lake_build':False,'commit_or_push':False,'subagents':False,'dependencies_copied':False},'limits':['Paired Fin n + Fin n real coordinates; no formal bridge to Fin (2*n) ordering or Python arrays.','JP=-PJ is assumed for the conditional Jacobian interfaces; no ODE or derivative formalization.','Boundary matrices are explicit algebraic inputs; polynomial traces and residual-coordinate identification are not formalized.','All real L determinant identities; positivity for real L>=4; unique real correction for every natural L>=4.','No numerical Python, complex analytic bridge, Sobolev closure, critical trace or cofinite density formalization.'],'handoff':'HANDOFF.md'}
write_json(BASE/'summary.json',Summary)
with (BASE/'AGENTS.md').open('a') as F:F.write('\nFinal author handoff: exact root verification completed with a matched literal contract and only the three allowed foundational axioms. Saved-receipt/import-resolution recheck is current. All seven math/export checks and four exact-verifier controls have their expected outcomes. All failures remain preserved. Recorded input identities, 52 old Lean sources, installed verifier files and runtime binaries are unchanged. Independent readback and acceptance remain pending. Full binding and final counts are in summary.json and source-environment-binding.json.\n')
Manifest={str(P.relative_to(BASE)):{'sha256':digest(P),'bytes':P.stat().st_size} for P in sorted(BASE.rglob('*')) if P.is_file() and P.name!='handoff-manifest.json' and not P.name.endswith('-driver.log') and 'tmp' not in P.relative_to(BASE).parts}
write_json(BASE/'handoff-manifest.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'author','exclusions':['handoff-manifest.json itself','*-driver.log convenience logs (complete immutable command logs are included)','tmp/'],'files':Manifest})
print(json.dumps({'status':Summary['status'],'files_bound':len(Manifest),'source_sha256':digest(Source),'environment_sha256':Target['environment_sha256'],'root_exact':True},indent=2))
