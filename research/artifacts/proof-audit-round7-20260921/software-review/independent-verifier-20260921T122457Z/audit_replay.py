"""Reviewer audits actual replay data, AST identities, and the provenance predicate."""
from pathlib import Path
import ast,hashlib,json,sys,types
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
OWN=Path(__file__).resolve().parent
RUN=ROOT/'work/replay-20260921T122930Z-e64f7d'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def astsha(n):return hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()
packet=json.loads((ROOT/'PACKET.json').read_text())
problems=[];audits=[];representatives=[]
summary=json.loads((RUN/'replay-summary.json').read_text())
copyhash=json.loads((RUN/'copy-manifest.json').read_text())
for rel,h in copyhash.items():
    if packet['files'].get(rel)!=h or sha(RUN/rel)!=h:problems.append('copied input identity '+rel)
for rel,h in summary['output_sha256'].items():
    if sha(RUN/rel)!=h:problems.append('output identity '+rel)
reports={}
for mode in ('normal','optimized'):
    for tree in ('originals','candidates'):
        label=tree+'-'+mode
        report=json.loads((RUN/'results'/(label+'.json')).read_text())
        reports[label]=report
        checks=report['checks'];actual_pass=[]
        for c in checks:
            if 'actual' in c and 'expected' in c:
                a=np.asarray(c['actual']);b=np.asarray(c['expected'])
                value=bool(a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.allclose(a,b,atol=c['atol'],rtol=c['rtol']))
                if c['max_abs_error']!=float(np.max(np.abs(a-b))):problems.append('error metric '+label+' '+c['name'])
            elif 'residual' in c:value=bool(np.max(np.abs(c['residual']))<1e-9)
            elif 'max_offdiag' in c:value=c['max_offdiag']>1.
            elif 'simple_error' in c:value=c['simple_error']>1.
            elif 'derivative' in c:value=abs(c['derivative'])>1.
            else:raise RuntimeError('Unrecognized check '+c['name'])
            actual_pass.append(value)
            if value!=c['passed']:problems.append('claimed pass mismatch '+label+' '+c['name'])
        if len(set(c['name'] for c in checks))!=len(checks):problems.append('duplicate tests '+label)
        if len(checks)!=report['tests'] or sum(actual_pass)!=report['passed']:problems.append('count mismatch '+label)
        for file,h in report['source_sha256'].items():
            if packet['files'][f'{tree}/scripts/{file}']!=h:problems.append('source digest '+label+' '+file)
        for item in report['expressions']:
            path=ROOT/tree/'scripts'/item['source']
            source=ast.parse(path.read_text(encoding='utf-8-sig'))
            nodes=[node for node in ast.walk(source) if getattr(node,'lineno',None)==item['line'] and getattr(node,'end_lineno',None)==item['end'] and astsha(node)==item['ast_sha256']]
            if not nodes or ast.unparse(nodes[0])!=item['expression']:problems.append('AST mismatch '+label+' '+str(item))
        for item in report['loader']:
            source=ast.parse((ROOT/tree/'scripts'/(item['module']+'.py')).read_text(encoding='utf-8-sig'))
            if packet['files'][f"{tree}/scripts/{item['module']}.py"]!=item['sha256']:problems.append('loader digest '+label)
            for removed in item['removed']:
                matches=[node for node in source.body if node.lineno==removed['line'] and node.end_lineno==removed['end'] and type(node).__name__==removed['kind']]
                if len(matches)!=1 or not isinstance(matches[0],ast.For):problems.append('unexpected loader removal '+label)
        receipt=json.loads((RUN/'receipts'/label/'receipt.json').read_text())
        for stream in ('stdout','stderr'):
            if sha(RUN/'receipts'/label/(stream+'.txt'))!=receipt[stream+'_sha256']:problems.append('receipt stream '+label)
        if receipt['input_sha256']!=copyhash:problems.append('receipt input '+label)
        audits.append({'label':label,'exit_code':receipt['exit_code'],'recomputed_tests':len(checks),'recomputed_passed':sum(actual_pass),'recomputed_failed':len(checks)-sum(actual_pass),'ast_evaluations_bound':len(report['expressions']),'unique_ast_expressions':len({(x['source'],x['ast_sha256']) for x in report['expressions']}),'loader_modules_checked':len(report['loader'])})
original={c['name']:c for c in reports['originals-normal']['checks']}
candidate={c['name']:c for c in reports['candidates-normal']['checks']}
name_map={
 'op03_gap_fh.py':'op03_gap_fh paired SUP u=0.3',
 'gap_n1_grad.py':'gap_n1_grad INF/width chain rule',
 '_tmp_fh_paradox.py':'_tmp_fh_paradox SUP/fh',
 'tmp_fh_test.py':'tmp_fh_test INF/fh1',
 'tmp_verify_endpoints.py':'tmp_verify_endpoints SUP/paired',
 '_gapn2_hess_verify.py':'hess_verify sup/lower eigenvalue in f',
 '_gapn2_hess_sign_and_bigR.py':'_gapn2_hess_sign_and_bigR n=2 sup/H actual matrix',
 '_gapn2_jacobian_analytic.py':'_gapn2_jacobian_analytic n=2 sup/H actual matrix',
 '_gapn2_o3_scan.py':'_gapn2_o3_scan n=2 sup/evH',
 '_gapn2_second_variation_probe.py':'_gapn2_second_variation_probe n=2 sup/Hess actual matrix'}
for file,name in name_map.items():
    a=original[name];b=candidate[name]
    if a['passed'] or not b['passed']:problems.append('not discriminating '+file)
    representatives.append({'file':file,'test':name,'original':a,'candidate':b})
# Execute the exact module collection expression with a synthetic external file path.
# No external file is read/imported/created. This is a predicate counterexample.
regtree=ast.parse((ROOT/'regression/regression.py').read_text())
node=next(n for n in ast.walk(regtree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='Bindings' for t in n.targets))
base=OWN/'synthetic-isolation'/'run'
fakepath=OWN/'synthetic-isolation'/'outside'/'gap_lib.py'
fakesys=types.SimpleNamespace(modules={'gap_lib':types.SimpleNamespace(__file__=str(fakepath))})
bindings=eval(compile(ast.Expression(node.value),str(ROOT/'regression/regression.py'),'eval'),{'Path':Path,'sys':fakesys,'Base':base})
replaytree=ast.parse((ROOT/'regression/replay.py').read_text())
loop=next(n for n in ast.walk(replaytree) if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [getattr(t,'id',None) for t in n.target.elts]==['Name','PathStr'])
env={'Path':Path,'Run':base,'Data':{'module_files':bindings},'Outside':[]}
exec(compile(ast.Module(body=[loop],type_ignores=[]),str(ROOT/'regression/replay.py'),'exec'),env)
provenance={'kind':'real harness logic defect demonstrated on synthetic module metadata, no external read','collector_line':node.lineno,'collector_ast_sha256':astsha(node.value),'collector_expression':ast.unparse(node.value),'gate_line':loop.lineno,'input_module_file':str(fakepath),'isolated_base':str(base),'reported_bindings':bindings,'reported_outside':env['Outside'],'outside_module_was_omitted':not bindings and not env['Outside'],'impact':'An outside project import is discarded before replay validates module paths, so the empty external_project_modules output is not evidence of isolation. This does not demonstrate an outside import occurred in the actual replay.'}
output={'replay_directory':str(RUN),'audit_problems':problems,'all_numerical_and_identity_audits_passed':not problems,'runs':audits,'negative_control_per_target':representatives,'scope_gate_counterexample':provenance,'candidate_stationary_residual_max':max(float(np.max(np.abs(c['residual']))) for c in candidate.values() if 'residual' in c),'candidate_full_matrix_max_abs_error':max(c['max_abs_error'] for c in candidate.values() if c['name'].endswith('actual matrix')),'copied_input_count':len(copyhash),'output_digests_rechecked':len(summary['output_sha256'])}
(OWN/'replay-audit.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k not in ['negative_control_per_target']},indent=2))
sys.exit(int(bool(problems)))
