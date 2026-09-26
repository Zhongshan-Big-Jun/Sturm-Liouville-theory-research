from pathlib import Path
import hashlib,json,re,datetime
Base=Path(__file__).resolve().parent

def digest(P):
 with Path(P).open('rb') as F:return hashlib.file_digest(F,'sha256').hexdigest()
def put(P,V):
 Path(P).write_text(json.dumps(V,ensure_ascii=False,indent=2)+'\n')
def read(P):return json.loads(Path(P).read_text())

PosPath=Base/'evidence/exact-root/run-manifest.json'
NegPath=Base/'evidence/negative-contract/run-manifest.json'
Pos=read(PosPath);Neg=read(NegPath)
assert Pos['machine_verification_passed'] and Pos['exact_root_passed']
assert Pos['target']['comparison']['status']=='matched'
assert not Pos['target']['unexpected_axioms']
assert not Pos['target']['unknown_dependencies'] and not Pos['target']['unsafe_dependencies']
assert Pos['semantic']['status']=='not_reviewed'
assert Neg['machine_verification_passed'] and not Neg['exact_root_passed']
assert Neg['target']['comparison']['status']=='mismatched'
assert Neg['root_closure']['status']=='target_mismatch',Neg['root_closure']
Labels=['final-source','export-03','positive-controls','positive-contract-type','blind-source',
 'negative-wrong-sector','negative-mirror-sign','negative-normalization','exact-root','negative-contract']
Commands={L:read(Base/'commands'/L/'command.json') for L in Labels}
for L in Labels:
 Expected=1 if L.startswith('negative-') else 0
 assert Commands[L]['exit_code']==Expected,(L,Commands[L]['exit_code'])
 assert Commands[L]['inputs_unchanged'],L
Source=Base/'project/AuditRound12.lean'
assert Commands['final-source']['inputs_before'][str(Source)]==digest(Source)
Object=Base/'objects/final-source/AuditRound12.olean'
assert Commands['export-03']['inputs_before'][str(Object)]==digest(Object)
FreshObject=Path(Pos['evidence']['run_directory'])/'lib/AuditRound12.olean'
assert digest(FreshObject)==digest(Object)
assert digest(Base/'objects/blind-source/AuditRound12.olean')==digest(Object)
for L,S in [('negative-wrong-sector','Type mismatch'),('negative-mirror-sign','⊢ False'),('negative-normalization','2 • 1 = 1')]:
 assert S in (Base/'commands'/L/'stdout.log').read_text()
Declarations=read(Base/'declarations.json')
Allowed={'propext','Classical.choice','Quot.sound'}
assert all(set(D['transitive_axioms'])<=Allowed and not D['unsafe'] for D in Declarations)
Authored=re.findall(r'^(?:def|abbrev|theorem) (\w+)',Source.read_text(),re.M)
Theorems=re.findall(r'^theorem (\w+)',Source.read_text(),re.M)
assert len(Theorems)==10
assert all('AuditRound12.'+N in {D['name'] for D in Declarations} for N in Authored)
assert '从 -1 开始' not in (Base/'contract.md').read_text()
Env={'runtime':Pos['environment'],'fresh_target_object':str(FreshObject),'fresh_target_object_sha256':digest(FreshObject),'export_object_sha256':digest(Object),'fresh_target_equals_export_object':True,'environment_sha256':Pos['target']['environment_sha256'],
 'semantic_environment_sha256':Pos['target']['semantic_environment_sha256'],
 'type_sha256':Pos['target']['type_sha256'],'semantic_sha256':Pos['target']['semantic_sha256'],
 'loaded_module_count':Pos['target']['loaded_module_count'],
 'imported_artifact_count':len(Pos['target']['import_artifacts']),
 'import_artifacts':Pos['target']['import_artifacts'],
 'verifier_tool_hashes':Pos['evidence']['tool_hashes'],
 'note':'Exact compiler/runtime and loaded import artifact identities as reported by the unmodified installed verifier; not an independent second kernel or complete OS image.'}
put(Base/'environment.json',Env)
ReadSet=read(Base/'read-set.json');Changes=[]
for D in ReadSet:
 assert digest(Base/D['snapshot'])==D['sha256']
 Current=digest(D['path']) if Path(D['path']).is_file() else None
 if Current!=D['sha256']:Changes.append({'path':D['path'],'snapshot_sha256':D['sha256'],'current_sha256':Current})
put(Base/'read-set-current-check.json',{'note':'Frozen read-only snapshots are preserved. Concurrent repository edits are not changes made by this author. This is not a whole-repository modification audit.','changed_since_snapshot':Changes})
Controls=[]
for L in Labels:
 C=Commands[L]
 Controls.append({'label':L,'exit_code':C['exit_code'],'seconds':C['seconds'],'command_record':str(Path('commands')/L/'command.json'),
  'command_record_sha256':digest(Base/'commands'/L/'command.json'),'stdout_sha256':C['stdout_sha256'],'stderr_sha256':C['stderr_sha256'],'inputs_unchanged':C['inputs_unchanged']})
Summary={'status':'AUTHOR_MACHINE_CHECKED_INDEPENDENT_SEMANTIC_REVIEW_PENDING',
 'role':'round12 local Lean author, not final verifier','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'write_scope':str(Base),'source':'project/AuditRound12.lean','source_sha256':digest(Source),
 'contract':'contract.md','machine_contract':'contract.json','root_declaration':'AuditRound12.audit_root',
 'principal_theorems':Theorems,'principal_theorem_count':10,'authored_definitions_or_abbreviations':len(Authored)-len(Theorems),
 'actual_namespace_declarations':len(Declarations),'generated_auxiliary_declarations':len(Declarations)-len(Authored),
 'declarations_export':'declarations.json','declarations_sha256':digest(Base/'declarations.json'),
 'export_scope':'All 59 actual namespace declarations, including generated equation/proof helpers; full explicit types, universe/binder information, definition bodies, and per-declaration transitive collectAxioms. Root extraction separately contains imported dependency/definition closure.',
 'statement_scope':{'n':'all natural numbers, including zero','scalar_field':'Real','K':'arbitrary real (Fin n ⊕ Fin n)-square matrix; no symmetry or reflection-commutation hypothesis',
 'ordered_coordinates':'Fin(n+n), order(inl i)=i; order(inr i)=2n-1-i, actual equivalence',
 'bases':'Be=[I;I], Bo=[I;-I]; normalized bases divide by sqrt(2); full ordered compression and scaling bridges',
 'sign_convention':'One-based j=1: epsilon_j=(-1)^(j+1) starts +1. Zero-based i=j-1: (-1)^i starts +1. E is exactly the left diagonal block of S. The -S bridge is only a general convention conversion, not a necessary correction to current source.',
 'rank_one':'For w=(v,-v): rawKo(ww^T)=4vv^T, rawKe=0, KpOdd=0; nonzero v gives nonzero raw odd compression.',
 'counterexample':'n=1, K=P is symmetric and commutes with reflection; rawKo=-2 and KpOdd=+2 (normalized: -1 and +1).'},
 'machine':{'exact_root_passed':True,'machine_verification_passed':True,'manifest':str(PosPath.relative_to(Base)),'manifest_sha256':digest(PosPath),
  'root_closure':Pos['root_closure'],'axioms':Pos['target']['axioms'],'unexpected_axioms':Pos['target']['unexpected_axioms'],
  'unknown_dependencies':Pos['target']['unknown_dependencies'],'unsafe_dependencies':Pos['target']['unsafe_dependencies'],
  'negative_contract_manifest':str(NegPath.relative_to(Base)),'negative_contract_manifest_sha256':digest(NegPath),'negative_root_closure':Neg['root_closure']},
 'semantic_review':{'status':'pending','independent_readback_performed':False,'independent_execution_review_performed':False,'author_spawned_subagents':False},
 'environment':{'file':'environment.json','sha256':digest(Base/'environment.json'),'environment_sha256':Env['environment_sha256'],'loaded_module_count':Env['loaded_module_count'],'imported_artifact_count':Env['imported_artifact_count']},
 'blind_packet':{'path':'blind','manifest_sha256':digest(Base/'blind/manifest.json'),'source_sha256':digest(Base/'blind/AuditRound12.lean'),'actual_compile_command':'commands/blind-source/command.json','compiled_object_equals_final_source_object':True,'informal_author_contract_included':False},
 'read_set':{'file':'read-set.json','sha256':digest(Base/'read-set.json'),'entries':len(ReadSet),'current_check':'read-set-current-check.json','concurrent_changes':Changes},
 'executions':Controls,
 'retained_development_failures':[P.parent.name for P in sorted((Base/'commands').glob('*/command.json')) if read(P).get('exit_code')!=0 and not P.parent.name.startswith('negative-')],
 'limitations':['No full Green/Pruefer/Sturm-Liouville or numerical Python formalization.','No formal inertia index or Sylvester law theorem.','Runtime/library binaries and imported artifacts are the compiler trust boundary.','No final independent semantic acceptance is claimed.','Read-set concurrent drift is reported against frozen copies; no whole-repository pristine assertion.'],
 'reproduction':{'compile':'python3 -B '+str(Base/'run.py')+' compile UNIQUE_NEW_LABEL',
 'exact_root':'python3 -B '+str(Base/'run.py')+' verify UNIQUE_NEW_LABEL contract.json',
 'negative_contract':'python3 -B '+str(Base/'run.py')+' verify UNIQUE_NEW_LABEL negative-contract.json (expected exit 1, target_mismatch)',
 'copyable_commands':'README.md'},
 'prohibitions_observed':['No main-repository/cache/plugin/history writes by this author','No commit or push','No subagents','No full lake build','No runtime or package installation']}
put(Base/'summary.json',Summary)
Paths=[Source,Base/'summary.json',Base/'contract.md',Base/'contract.json',Base/'negative-contract.json',Base/'declarations.json',Base/'declarations.txt',Base/'environment.json',Base/'read-set.json',Base/'read-set-current-check.json',Base/'README.md',Base/'AGENTS.md',Base/'run.py',Base/'build_contract.py',Base/'freeze_blind.py',Base/'finalize.py',PosPath,NegPath]
Paths += [P for P in (Base/'blind').iterdir() if P.is_file()]
Paths += [Base/'commands'/L/'command.json' for L in Labels]
put(Base/'delivery-manifest.json',{'files':{str(P.relative_to(Base)):digest(P) for P in sorted(set(Paths))},'note':'Does not hash itself. Final artifact bindings; source-independent historical failures stay in commands/ with their own immutable snapshots.'})
print(json.dumps({K:Summary[K] for K in ['status','source_sha256','principal_theorem_count','actual_namespace_declarations','environment','read_set']},ensure_ascii=False,indent=2))
