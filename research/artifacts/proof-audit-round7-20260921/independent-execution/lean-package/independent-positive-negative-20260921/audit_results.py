#!/usr/bin/env python3
"""Independent verification of this execution's fresh receipts and byte evidence."""
from pathlib import Path
import collections, concurrent.futures, datetime, decimal, hashlib, json, re, shutil, time
from executor import BASE, RUN, digest, host, pointer, save, stamp

CHECKS=[]
def check(name, condition, detail=None):
    CHECKS.append({'name':name,'passed':bool(condition),'detail':detail})
    if not condition:
        print('CHECK FAILED:',name,flush=True)
def read(path):
    return json.loads(Path(path).read_text())
def canonical_sha(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def main():
    outer=read(RUN/'executor-logs/lean-replay.json')
    if 'returncode' not in outer:
        raise RuntimeError('replay still running; no final execution assessment')
    pre=read(RUN/'preflight.json')
    before=read(RUN/'runtime-before.json')
    baseline={a['path']:a for a in before['artifacts']}
    after_inputs=[]
    for row in pre['checks']:
        p=Path(row['path']);current=digest(p) if p.is_file() else None
        after_inputs.append({'path':str(p),'expected_sha256':row['expected_sha256'],'actual_sha256':current,'match':current==row['expected_sha256']})
    save(RUN/'final-input-identity.json',{'utc':stamp(),'checks':after_inputs,'all_match':all(x['match'] for x in after_inputs),'packet_unchanged':digest(BASE/'PACKET.json')==pre['packet']['sha256']})
    check('all_27_declared_input_hashes_unchanged',len(after_inputs)==27 and all(x['match'] for x in after_inputs))
    check('packet_unchanged',digest(BASE/'PACKET.json')==pre['packet']['sha256'])
    check('supplied_replay_actual_inspection_failure',outer['returncode']==1 and 'Public declaration inspection failed' in (RUN/'executor-logs/lean-replay.stderr.log').read_text())
    observed=[json.loads(l) for l in (RUN/'executor-logs/lean-replay.observations.jsonl').read_text().splitlines()]
    observed += [json.loads(l) for l in (RUN/'executor-logs/supplemental-wrong-target-verifier.observations.jsonl').read_text().splitlines()]
    check('replay_destination_was_absent',outer['replay_directory_existed_before'] is False)
    owned=read(RUN/'all-module-declarations.json')
    probe_receipt=read(RUN/'all-module-declarations.execution.json')
    check('independent_environment_probe_completed',probe_receipt['returncode']==0)
    check('independent_probe_imported_new_object',host(owned['resolved_olean']).resolve()==Path(probe_receipt['input_olean_before']['path']).resolve())
    check('probe_object_unchanged',probe_receipt['input_olean_before']['sha256']==probe_receipt['input_olean_after']['sha256'])
    source=BASE/'lean-package/snapshot/SL/AuditRound7.lean'
    entries=re.findall(r'^(def|theorem|lemma)\s+([A-Za-z_][A-Za-z_0-9]*)',source.read_text(),re.M)
    names={'SL.AuditRound7.'+n:k for k,n in entries}
    rows=owned['declarations'];declarations={r['declaration']:r for r in rows}
    check('all_source_named_declarations_exported',set(names)<=set(declarations),{'source_count':len(names),'environment_count':len(rows)})
    check('no_duplicate_module_declarations',len(declarations)==len(rows))
    check('every_export_has_actual_type_and_axioms',all(r['actual_type'] and r['type_expression'] and isinstance(r['transitive_axioms'],list) for r in rows))
    check('every_source_definition_has_exported_body',all(declarations[n]['definition'] is not None and declarations[n]['definition']['expression'] for n,k in names.items() if k=='def'))
    allowed={'propext','Classical.choice','Quot.sound'}
    check('all_32_module_constants_only_allowed_transitive_axioms',all(set(r['transitive_axioms'])<=allowed for r in rows))
    check('all_module_constants_safe',all(not r['is_unsafe'] for r in rows))
    check('original_public_export_missing_after_retained_failure',not (RUN/'replay/public-declarations.json').exists())
    inspect_text=(RUN/'replay/logs/04-all-declarations.stdout.txt').read_text()
    check('original_inspection_failure_is_reserved_Type_syntax', 'unsupported pattern in syntax match' in inspect_text and 'Inspection.lean:75:8' in inspect_text and 'let Type' in (RUN/'replay/Inspection.lean').read_text())
    manifests={};external={};manifest_summaries={};command_records=[]
    for branch in ('positive','negative'):
        path=(RUN/'replay/positive/run-manifest.json') if branch=='positive' else (RUN/'supplemental-negative/run-manifest.json')
        m=read(path);manifests[branch]=m;t=m['target']
        check(branch+'_manifest_canonical_payload_hash',canonical_sha({k:v for k,v in m.items() if k!='report_sha256'})==m['report_sha256'])
        check(branch+'_manifest_copies_byte_identical',digest(path)==digest(Path(m['evidence']['run_directory'])/'run-manifest.json'))
        check(branch+'_fresh_evidence',m['evidence']['status']=='current' and not m['evidence']['changed_inputs'] and not m['evidence']['changed_imports'] and not m['evidence']['changed_tools'])
        check(branch+'_machine_execution_passed',m['machine_verification_passed'] and m['build']['status']=='passed')
        check(branch+'_source_hash_bound',m['input_hashes']['SL/AuditRound7.lean']==digest(source))
        check(branch+'_root_axioms_no_unproved_leaves',set(t['axioms'])<=allowed and not t['unexpected_axioms'] and not t['unsafe_dependencies'] and not t['unknown_dependencies'])
        for cmd in m['build']['commands']:
            for stream in ('stdout','stderr'):
                check(branch+'_'+cmd['job_id']+'_'+stream+'_bytes',digest(cmd[stream+'_log'])==cmd[stream+'_sha256'])
            check(branch+'_'+cmd['job_id']+'_job_exit',read(cmd['job_record'])['exit_code']==cmd['exit_code']==0)
            command_records.append({'branch':branch,'kind':cmd['kind'],'argv':cmd['command'],'exit_code':cmd['exit_code'],'job':pointer(cmd['job_record'])})
        targets=[c for c in m['build']['commands'] if c['kind']=='target']
        check(branch+'_one_actual_candidate_recompile',len(targets)==1 and '-o' in targets[0]['command'] and host(targets[0]['command'][-1]).resolve()==source.resolve())
        for c in targets:
            check(branch+'_recompile_process_observed',any(e['kind']=='process' and '-o' in e.get('argv',[]) and str(c['command'][c['command'].index('-o')+1]) in e['argv'] for e in observed))
            check(branch+'_new_olean_creation_observed',any(e['kind']=='candidate_artifact_observed' and e['path']==c['olean'] for e in observed))
        for p,h in m['evidence']['compiled_artifacts'].items():
            check(branch+'_compiled_'+Path(p).name,digest(p)==h)
        check(branch+'_declaration_export_hash',digest(t['extraction_file'])==m['evidence']['extraction_sha256'])
        module_names=[x['module'] for x in t['imported_modules']]
        check(branch+'_complete_loaded_module_count',len(module_names)==len(set(module_names))==t['loaded_module_count'])
        for name,item in t['import_artifacts'].items():
            p=str(Path(item['path']).resolve())
            if p in external and external[p]['sha256']!=item['sha256']:
                check('same_import_hash_in_two_runs:'+name,False)
            external[p]=item
        manifest_summaries[branch]={'manifest':pointer(path),'exact_root_passed':m['exact_root_passed'],'root_status':m['root_closure']['status'],'comparison':{k:v for k,v in t['comparison'].items() if k not in ('expected_type_expression',)},'declaration':t['declaration'],'axioms':t['axioms'],'loaded_modules':t['loaded_module_count'],'import_artifacts':len(t['import_artifacts']),'target_recompilations':len(targets)}
    p,n=manifests['positive'],manifests['negative']
    check('positive_exact_root_and_type_match',p['exact_root_passed'] and p['root_closure']['status']=='closed' and p['target']['comparison']['status']=='matched' and p['target']['comparison']['definitionally_equal'])
    check('wrong_target_fails_for_expected_type_mismatch',not n['exact_root_passed'] and n['root_closure']['status']=='target_mismatch' and n['target']['comparison']['status']=='mismatched' and not n['target']['comparison']['definitionally_equal'] and n['machine_verification_passed'])
    step_receipts={}
    for f in sorted((RUN/'replay/logs').glob('*.json')):
        j=read(f);step_receipts[f.stem]=j
        for stream in ('stdout','stderr'):
            check(f.stem+'_'+stream+'_receipt_hash',digest(f.with_suffix('.'+stream+'.txt'))==j[stream+'_sha256'])
    check('supplied_runner_stopped_after_step_four',list(step_receipts)==['01-version','02-exact-root','03-positive-control','04-all-declarations'] and step_receipts['04-all-declarations']['exit_code']==1)
    check('positive_control_exit_zero',step_receipts['03-positive-control']['exit_code']==0)
    check('supplemental_wrong_target_process_exit_one',read(RUN/'executor-logs/supplemental-wrong-target-verifier.json')['returncode']==1)
    factor=(RUN/'executor-logs/supplemental-wrong-mirror-factor.stdout.log').read_text()
    factor_reason='Type mismatch' in factor and '-2 * eigenvalue * jump * leftValue ^ 2' in factor and '-eigenvalue * jump * leftValue ^ 2' in factor
    check('wrong_mirror_factor_fails_for_factor_mismatch',read(RUN/'executor-logs/supplemental-wrong-mirror-factor.json')['returncode']==1 and factor_reason)
    resolved=(RUN/'executor-logs/supplemental-import-resolution.stdout.log').read_text().splitlines()
    native=(RUN/'executor-logs/supplemental-wrong-target-native.stdout.log').read_text()
    check('wrong_target_native_type_mismatch_also_observed',read(RUN/'executor-logs/supplemental-wrong-target-native.json')['returncode']==1 and 'Type mismatch' in native and '-4' in native and '-6' in native)
    obj=Path(p['evidence']['run_directory'])/'lib/SL/AuditRound7.olean'
    check('runner_deps_matches_independent_findOLean',any(host(s).resolve()==obj.resolve() for s in resolved) and host(owned['resolved_olean']).resolve()==obj.resolve())
    check('fresh_candidate_hash_matches_independent_artifact',read(RUN/'independent-root-artifact.json')['olean']['sha256']==digest(obj))
    # Hash the actual external objects against both the before-run baseline and the fresh manifests.
    def audit_import(item):
        path,record=item;old=baseline.get(path)
        p=Path(path);st=p.stat() if p.is_file() else None
        h=digest(p) if st else None
        return {'path':path,'before_sha256':old['sha256'] if old else None,'recorded_sha256':record['sha256'],'after_sha256':h,'same':old is not None and old['sha256']==record['sha256']==h,'mtime_unchanged':old is not None and st is not None and old['mtime_ns']==st.st_mtime_ns,'bytes':st.st_size if st else None}
    start=time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        actual=list(pool.map(audit_import,sorted(external.items())))
    save(RUN/'runtime-after-imports.json',{'utc':stamp(),'hash_count':len(actual),'elapsed_seconds':time.monotonic()-start,'artifacts':actual})
    check('all_loaded_external_artifacts_byte_unchanged',all(a['same'] for a in actual),{'count':len(actual)})
    check('all_loaded_external_artifacts_mtime_unchanged',all(a['mtime_unchanged'] for a in actual))
    # Unused prehashed objects are metadata-checked only at the end, and clearly labeled.
    metadata=[]
    for old in before['artifacts']:
        path=Path(old['path'])
        try:
            st=path.stat()
            if (old['bytes'],old['mtime_ns'])!=(st.st_size,st.st_mtime_ns): metadata.append(str(path))
        except OSError: metadata.append(str(path))
    save(RUN/'runtime-stability.json',{'baseline_artifact_count':len(before['artifacts']),'post_run_sha256_rechecked_loaded_artifacts':len(actual),'all_loaded_sha256_match':all(a['same'] for a in actual),'all_baseline_metadata_change_paths':metadata,'unused_artifact_limit':'Unused baseline files were only restatted after the run, not all rehashed; metadata-preserving changes to unused objects would not be detected.'})
    check('no_baseline_runtime_metadata_changes',not metadata)
    print('independent runtime import rehashes',len(actual),'seconds',round(time.monotonic()-start,2),flush=True)
    # Preserve newly produced normal receipts verbatim inside the new run directory.
    dest=RUN/'numerical-preserved';dest.mkdir(exist_ok=True)
    for name in ('normal.execution.json','normal.stdout.log','normal.stderr.log'):
        target=dest/name
        if target.exists(): raise RuntimeError('preserved numerical receipt already exists')
        shutil.copyfile(BASE/'numerical/receipts'/name,target)
    normal_receipt=read(dest/'normal.execution.json')
    for stream in ('stdout','stderr'):
        check('normal_numeric_'+stream+'_receipt',digest(dest/('normal.'+stream+'.log'))==normal_receipt[stream+'_sha256'])
    normal=(dest/'normal.stdout.log').read_text()
    opt=(RUN/'executor-logs/numerical-optimized-direct.stdout.log').read_text()
    def group_status(text):
        return [(line.split(' ',1)[0],line.split(' ',1)[1].split(':',1)[0]) for line in text.splitlines() if line.startswith(('PASS ','FAIL '))]
    check('direct_numeric_modes_same_group_statuses',group_status(normal)==group_status(opt) and len(group_status(normal))==25)
    check('direct_numeric_each_24_pass_1_fail',sum(s=='PASS' for s,n in group_status(normal))==24 and sum(s=='FAIL' for s,n in group_status(normal))==1)
    check('normal_numeric_failed_missing_manifest',normal_receipt['returncode']==1 and 'FileNotFoundError' in (dest/'normal.stderr.log').read_text() and 'numerical/inputs/manifest.json' in (dest/'normal.stderr.log').read_text())
    optimized_rec=read(RUN/'executor-logs/numerical-optimized-direct.json')
    check('optimized_numeric_failed_missing_manifest',optimized_rec['returncode']==1 and '-O' in optimized_rec['argv'] and 'FileNotFoundError' in (RUN/'executor-logs/numerical-optimized-direct.stderr.log').read_text())
    check('numerical_runner_retained_early_failure',read(RUN/'executor-logs/numerical-runner.json')['returncode']==1 and 'normal unexpected exit status' in (RUN/'executor-logs/numerical-runner.stderr.log').read_text())
    a=read(RUN/'numeric-observation-normal.json');b=read(RUN/'numeric-observation-optimized.json')
    good=lambda v:[(g['name'],g['kind'],g['status'],g['details']) for g in v['groups'] if g['status']=='PASS']
    check('observer_preserved_original_failure_in_both_modes',a['status']==b['status']=='INCOMPLETE' and a['exception']['type']==b['exception']['type']=='FileNotFoundError')
    py_a={v['path']:v['sha256'] for v in read(RUN/'python-loaded-files-normal.json')['files']}
    py_b={v['path']:v['sha256'] for v in read(RUN/'python-loaded-files-optimized.json')['files']}
    common=set(py_a)&set(py_b)
    check('observed_python_module_files_common_to_modes_unchanged',all(py_a[n]==py_b[n] for n in common),{'common_module_files':len(common),'normal_files':len(py_a),'optimized_files':len(py_b)})
    check('numeric_library_versions_and_precision_agree',a['runtime']['mpmath']==b['runtime']['mpmath'] and a['runtime']['sympy']==b['runtime']['sympy'] and a['runtime']['decimal_precision']==b['runtime']['decimal_precision']==90)
    check('observed_optimization_flags_are_real',a['optimize']==0 and a['__debug__'] and b['optimize']==1 and not b['__debug__'])
    check('all_24_completed_numeric_details_identical',good(a)==good(b) and len(good(a))==24)
    failed_a=[g['name'] for g in a['groups'] if g['status']=='FAIL'];failed_b=[g['name'] for g in b['groups'] if g['status']=='FAIL']
    check('both_observers_retain_integrity_group_failure',failed_a==failed_b==['execution_contract_explicit_raise_and_input_identity'])
    neg_results=[]
    for mode in ('normal','optimized'):
        prefix=RUN/'executor-logs'/('numerical-old-fh-'+mode)
        j=read(str(prefix)+'.json');err=Path(str(prefix)+'.stderr.log').read_text()
        match=re.search(r'intentional old FH formula rejection: error=([0-9.eE+-]+)',err)
        correct=j['returncode']==1 and match is not None and 'FileNotFoundError' not in err
        check('old_fh_'+mode+'_actual_expected_formula_failure',correct)
        neg_results.append({'mode':mode,'returncode':j['returncode'],'error_magnitude':match.group(1) if match else None,'expected_formula_failure':correct,'receipt':pointer(str(prefix)+'.json')})
    d={g['name']:g.get('details') for g in a['groups'] if g['status']=='PASS'}
    decimal.getcontext().prec=80
    fh=decimal.Decimal(d['symmetric_FH_vs_independent_central_difference']['FH'])
    old=decimal.Decimal(d['legacy_symmetric_formula_is_half']['old'])
    fd=decimal.Decimal(d['symmetric_FH_vs_independent_central_difference']['differences'][-1]['central_difference'])
    check('fh_observed_factor_two_decimal_crosscheck',abs(fh-2*old)<decimal.Decimal('1e-55'))
    check('negative_error_matches_observed_fd_minus_old',all(abs(decimal.Decimal(x['error_magnitude'])-abs(fd-old))<decimal.Decimal('1e-55') for x in neg_results))
    absent={n:not (BASE/'numerical'/n).exists() for n in ('inputs/manifest.json','outputs.json','outputs.optimized.json','receipts/execution-summary.json')}
    # Missing inputs are an actual blocker, not a passed computational group.
    check('no_missing_manifest_fabricated',absent['inputs/manifest.json'])
    numerical={'status':'INCOMPLETE','reason':'numerical/inputs/manifest.json absent; not supplied or hash-bound by PACKET','prescribed_runner_returncode':1,'direct_modes':{'normal':{'returncode':normal_receipt['returncode'],'passed':24,'failed':1,'total':25},'optimized':{'returncode':optimized_rec['returncode'],'passed':24,'failed':1,'total':25}},'direct_statuses':group_status(normal),'captured_detail_comparison':{'same_completed_24_groups':good(a)==good(b),'method':'Additional original-script executions via runpy; capture traceback locals only after original exception; both remain exit 1. No bypass or replacement input.'},'negative_controls':neg_results,'check_script_executions':{'prescribed_normal':1,'supplemental_optimized':1,'old_fh_negative':2,'passive_observer_normal_and_optimized':2,'total':6},'absent_paths':absent,'selected_observed_results':{n:d[n] for n in ('W_n2_half_counterexample','Taylor_pi4_general','n2_normalized_determinant_exact','symmetric_FH_vs_independent_central_difference','legacy_symmetric_formula_is_half','R7_P01_rho2_Schrodinger_counterexample')},'input_scripts':{n:pointer(BASE/'numerical'/n) for n in ('checks.py','run_checks.py')}}
    save(RUN/'numerical-crosscheck.json',numerical)
    lean={'status':'INCOMPLETE_SUPPLIED_RUNNER','runner_failure':'Generated Inspection.lean:75:8 uses let Type; unsupported pattern in syntax match. Original runner stops before --deps and negative controls. Original files unchanged. Independent full export and original negative inputs were executed separately.','runner_exit':outer['returncode'],'runner_steps':len(step_receipts),'step_exit_codes':{k:v['exit_code'] for k,v in step_receipts.items()},'source_declarations':len(names),'source_theorems':sum(k in ('theorem','lemma') for k in names.values()),'source_definitions':sum(k=='def' for k in names.values()),'all_module_constants':len(rows),'generated_constants':sorted(set(declarations)-set(names)),'all_module_theorems':sum(r['is_theorem'] for r in rows),'axiom_union':sorted({ax for r in rows for ax in r['transitive_axioms']}),'public_definition_bodies_exported':sum(r['definition'] is not None for r in rows),'fresh_olean':pointer(obj),'independent_findOLean':owned['resolved_olean'],'manifests':manifest_summaries,'independent_root_check':'AllModuleDeclarations.lean includes example : original positive-contract expected_type := SL.AuditRound7.local_algebra_root','semantic_verdict':'not_issued'}
    save(RUN/'lean-crosscheck.json',lean)
    # All actual Lean command job receipts, including runtime version probes, counted once.
    jobs=[]
    for file in sorted(list((RUN/'replay').glob('*/lean-verification-runs/*/logs/*.job.json'))+list((RUN/'supplemental-negative').glob('lean-verification-runs/*/logs/*.job.json'))):
        j=read(file);jobs.append({'kind':'verifier_runtime_or_compile','argv':j['command'],'exit_code':j['exit_code'],'receipt':pointer(file)})
    direct=[(k,j) for k,j in step_receipts.items() if str(j['argv'][0]).lower().endswith('lean.exe')]
    direct_jobs=[{'kind':label,'argv':j['argv'],'exit_code':j['exit_code'],'receipt':pointer(RUN/'replay/logs'/(label+'.json'))} for label,j in direct]
    for label in ('supplemental-wrong-mirror-factor','supplemental-wrong-target-native','supplemental-import-resolution'):
        j=read(RUN/'executor-logs'/(label+'.json'))
        direct_jobs.append({'kind':label,'argv':j['argv'],'exit_code':j['returncode'],'receipt':pointer(RUN/'executor-logs'/(label+'.json'))})
    extras=[{'kind':'independent_module_probe','argv':probe_receipt['argv'],'exit_code':probe_receipt['returncode'],'receipt':pointer(RUN/'all-module-declarations.execution.json')},{'kind':'independent_api_probe','argv':read(RUN/'executor-logs/lean-api-probe.json')['argv'],'exit_code':read(RUN/'executor-logs/lean-api-probe.json')['returncode'],'receipt':pointer(RUN/'executor-logs/lean-api-probe.json')}]
    save(RUN/'command-inventory.json',{'lean_and_lake_executable_calls':jobs+direct_jobs+extras,'total_lean_lake_processes':len(jobs)+len(direct_jobs)+len(extras),'verifier_calls':2,'candidate_source_recompilations':2,'inspection_helper_recompilations':2,'numeric_checks_executions':6,'original_runner_expected_steps':7,'original_runner_executed_steps':4,'supplemental_native_controls_and_resolution':3})
    result={'utc':stamp(),'checks':CHECKS,'total':len(CHECKS),'passed':sum(c['passed'] for c in CHECKS),'failed':sum(not c['passed'] for c in CHECKS),'meaning':'Evidence-integrity checks may pass while task status remains INCOMPLETE because the original replay generated invalid inspection syntax and the numerical program lacks its input manifest. No semantic review verdict.'}
    save(RUN/'independent-checks.json',result)
    print('independent evidence checks',result['passed'],'/',result['total'],'original numerical task remains INCOMPLETE',flush=True)
    return 0 if result['failed']==0 else 1

if __name__=='__main__':
    raise SystemExit(main())
