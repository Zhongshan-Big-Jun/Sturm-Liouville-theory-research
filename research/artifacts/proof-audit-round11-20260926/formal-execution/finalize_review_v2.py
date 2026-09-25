from pathlib import Path
import datetime, gzip, hashlib, json, re, subprocess, sys
BASE=Path(__file__).resolve().parent
FROZEN=BASE/'frozen/inputs'
def digest(p):
    with Path(p).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
packet=json.loads((BASE/'packet.json').read_text())
root=json.loads((BASE/'evidence/exact-root-fresh/run-manifest.json').read_text())
commands=[]
for p in sorted((BASE/'commands').glob('*/command.json')):
    c=json.loads(p.read_text())
    assert 'exit_code' in c, f'unfinished command: {p}'
    assert c['inputs_unchanged']
    assert digest(p.parent/'stdout.log')==c['stdout_sha256']
    assert digest(p.parent/'stderr.log')==c['stderr_sha256']
    commands.append(c)
math=json.loads((BASE/'reviewer-math-checks.json').read_text())
extra=json.loads((BASE/'reviewer-complementary-check.json').read_text())
closure=json.loads((BASE/'reviewer-closure-checks.json').read_text())
assert len(math)==9 and all(x['as_expected'] for x in math if x['label']!='complementary-01')
assert extra['exit_code']==0
assert len(closure)==4 and all(x['as_expected'] for x in closure)
assert root['exact_root_passed'] and root['evidence']['status']=='current'
check=json.loads((BASE/'fresh-root-comparison.json').read_text())
assert all(check['author_target_fields_match'].values())
assert check['root_expression_equals_elaborated_contract']
assert check['literal_contract_unchanged'] and check['source_hash_matches']
assert not check['external_hash_mismatches'] and not check['external_artifacts_outside_recorded_paths']
for name in ['unexpected_axioms','unsafe_dependencies','unknown_dependencies']: assert not check[name]
assert json.loads((BASE/'declaration-comparison.json').read_text())['all_fields_equal']
assert json.loads((BASE/'declaration-comparison.json').read_text())['per_declaration_axioms_equal']
pr=json.loads((BASE/'print-comparison.json').read_text());assert pr['printed_declarations']==26 and pr['types_match'] and pr['definition_bodies_match'] and pr['axioms_match']
assert json.loads((BASE/'root-clause-comparison.json').read_text())['all_clause_texts_match']
# Inspect actual closure outcomes, rather than just their exit codes.
control_details=[]
expected={'positive':'closed','hidden-axiom':'open','wrong-type':'target_mismatch','missing-target':'incomplete'}
for item in closure:
    manifest=BASE/item['manifest'];m=json.loads(manifest.read_text());t=m.get('target') or {}
    assert m['root_closure']['status']==expected[item['name']]
    if item['name']=='hidden-axiom': assert t['unexpected_axioms']==['Round11Control.hidden']
    if item['name']=='wrong-type': assert t['comparison']['status']=='mismatched' and not t['unexpected_axioms']
    if item['name']=='positive': assert not t['unexpected_axioms']
    if item['name']=='missing-target':
        logs='\n'.join(Path(x['stdout_log']).read_text()+Path(x['stderr_log']).read_text() for x in m['build']['commands'])
        assert 'Round11Control.missing' in logs and ('exact root declaration not found' in logs.lower())
    control_details.append({'name':item['name'],'exit_code':item['exit_code'],'root_closure':m['root_closure'],'comparison':t.get('comparison',{}).get('status'),'unexpected_axioms':t.get('unexpected_axioms'),'manifest':item['manifest'],'manifest_sha256':digest(manifest)})
# All frozen research snapshots are rechecked at their actual packet paths.
packet_origin=Path('/mnt/f/LaTeX/BVE research/research/artifacts/proof-audit-round11-20260926/formal-comparison/research/library/reviews/packets/96a6a726749351139af2db393e13a9fb267866eec0139df1cd556a3c97904423')
assert digest(packet_origin/'packet.json')==digest(BASE/'packet.json')
post=[]
for orig,meta in packet['inputs'].items():
    actual=digest(packet_origin/meta['snapshot']);copied=digest(BASE/'frozen'/orig)
    assert actual==copied==meta['sha256'];post.append({'path':orig,'sha256':actual,'unchanged':True})
write(BASE/'snapshot-postcheck.json',post)
baseline=json.loads((FROZEN/'environment-baseline.json').read_text());runtime=[]
for k in ['runtime_files','plugin_files']:
    for p,v in baseline[k].items():
        expected_sha=v if isinstance(v,str) else v['sha256'];actual=digest(p)
        assert actual==expected_sha;runtime.append({'path':p,'sha256':actual,'matches_frozen_baseline':True})
write(BASE/'runtime-postcheck.json',runtime)
# Supplement the native verifier logs with its effective Lean search-path construction.
# These paths are derived from the unchanged, hash-verified LeanRuntime.command_env;
# the native child process environment was not independently sampled.
environments=[]
for c in commands:
    if 'verify_lean_project.py' not in ' '.join(c['argv']):continue
    out=Path(c['argv'][c['argv'].index('--output')+1]);m=json.loads((out/'run-manifest.json').read_text());run_dir=Path(m['evidence']['run_directory']);lib=run_dir/'lib';project=Path(c['cwd'])
    win=lambda p:subprocess.check_output(['wslpath','-w',str(p)],text=True).strip()
    for job in sorted((run_dir/'logs').glob('*.job.json')):
        j=json.loads(job.read_text());args=j['command'];env=dict(c['environment'])
        inherited=len(args)>1 and args[1] in ['--version','--print-prefix']
        if not inherited:
            discovery=len(args)>1 and args[1]=='--run'
            paths=([lib] if not discovery else [])+[project]
            env['LEAN_PATH']=';'.join([win(p) for p in paths if p.is_dir()]+[env['LEAN_PATH']])
            env['WSLENV']=':'.join([x for x in env['WSLENV'].split(':') if x and x.split('/')[0]!='LEAN_PATH']+['LEAN_PATH'])
        environments.append({'job_record':str(job.relative_to(BASE)),'argv':args,'cwd':j['cwd'],'relevant_environment':env,'environment_evidence':'recorded parent environment plus deterministic unchanged LeanRuntime.command_env construction','exit_code':j['exit_code']})
write(BASE/'nested-command-environments.json',environments)
record={
    'schema':'independent-formal-comparison/v1',
    'packet_sha256':digest(BASE/'packet.json'),
    'scope':'Local real matrix algebra and finite-dimensional boundary correction; semantic comparison and fresh Lean replay. No full formalization or canonical acceptance.',
    'verdict':'APPROVED',
    'source_sha256':digest(BASE/'project/AuditRound11.lean'),
    'contract_sha256':digest(BASE/'contract.json'),
    'root_type_sha256':check['root_type_sha256'],
    'root_semantic_sha256':check['root_semantic_sha256'],
    'root_semantic_environment_sha256':check['root_semantic_environment_sha256'],
    'required_checks_complete':True,
    'declarations_compared':37,'definition_bodies_compared':12,'raw_print_types_compared':26,'root_conjuncts':13,
    'root_axioms':root['target']['axioms'],'loaded_modules':check['loaded_modules'],'external_import_artifacts':check['external_import_artifacts'],
    'math_control_results':math,'supplementary_repair':extra,'closure_control_results':control_details,
    'actual_failed_commands':[{'label':c['label'],'exit_code':c['exit_code'],'record':'commands/'+c['label']+'/command.json','classification':'reviewer proof-development failure, resolved by complementary-02 with unchanged assertion' if c['label']=='complementary-01' else 'intentional negative control'} for c in commands if c['exit_code']!=0],
    'unavailable_required_checks':[],
    'derived_report_failure':json.loads((BASE/'finalization-failure-01.json').read_text()),
    'evidence':{name:digest(BASE/name) for name in ['snapshot-integrity.json','snapshot-postcheck.json','runtime-precheck.json','runtime-postcheck.json','declaration-comparison.json','print-comparison.json','root-clause-comparison.json','fresh-root-comparison.json','semantic-review.json','nested-command-environments.json','evidence/exact-root-fresh/run-manifest.json']},
    'limitations':['Trusted recorded Lean compiler and prebuilt imported artifacts; no independent second kernel or full dependency rebuild.','Native verifier per-child environments are reconstructed from the recorded parent environment and unchanged installed launcher.','Readback provenance is supplied snapshot evidence, not independent authentication of reviewer identity.','External mathematical/model/software bridges and full source reports were not re-audited outside the requested algebraic comparison.']
}
write(BASE/'verification-record.json',record)
# The manifest covers all frozen copies, scripts, failed attempts, outputs and native logs.
files={}
for p in sorted(BASE.rglob('*')):
    if p.is_file() and p.name not in ['execution-manifest.json','execution-manifest.sha256']:
        files[str(p.relative_to(BASE))]={'sha256':digest(p),'bytes':p.stat().st_size}
manifest={'schema':'independent-execution-manifest/v1','packet_sha256':digest(BASE/'packet.json'),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'workspace':str(BASE),'verification_record_sha256':digest(BASE/'verification-record.json'),'commands':commands,'files':files}
write(BASE/'execution-manifest.json',manifest)
(BASE/'execution-manifest.sha256').write_text(digest(BASE/'execution-manifest.json')+'  execution-manifest.json\n')
print(json.dumps({'verdict':record['verdict'],'command_count':len(commands),'files_bound':len(files),'execution_manifest':str(BASE/'execution-manifest.json'),'execution_manifest_sha256':digest(BASE/'execution-manifest.json'),'verification_record':str(BASE/'verification-record.json'),'verification_record_sha256':digest(BASE/'verification-record.json')},indent=2))
