"""Independent interpretation of actual outputs; does not call submitted validators."""
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sysconfig
import numpy as np

OWN = Path(__file__).resolve().parent
ROOT = OWN.parent
PACKET = json.loads((ROOT/'PACKET.json').read_text())
ERRORS = []
def check(condition, message):
    if not condition:
        ERRORS.append(message)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    return json.loads(p.read_text())
STDLIB = {Path(sysconfig.get_path(k)).resolve() for k in ('stdlib','platstdlib')}
PACKAGES = {n:Path(importlib.util.find_spec(n).origin).resolve().parent for n in ('numpy','scipy')}
COMMON = ['op03_gap_fh','gap_n1_grad','_tmp_fh_paradox','tmp_fh_test','tmp_verify_endpoints','gap_lib','_gapn2_symmetry_recon','_gapn2_jacobian_probe','_gapn2_jacobian_analytic','_gapn2_hess_verify','_gapn2_hess_sign_and_bigR','_gapn2_hp_scan','_gapn2_jacobian_spectral']
EXPECTED_CASES = {n+'-'+m+s for m in ('normal','optimized') for n,s in [('originals',''),('candidates',''),('op03-cli',''),('candidates','-outside'),('op03-cli','-outside'),('candidates','-missing'),('op03-cli','-missing')]}

def category(path, run, tree, inputs):
    if path.is_relative_to(run):
        rel = path.relative_to(run).as_posix()
        if rel in inputs and (rel.startswith(tree+'/scripts/') or rel.startswith('regression/')):
            return 'fresh-input'
        return 'unexpected'
    if any(path.is_relative_to(p) for p in PACKAGES.values()):
        return 'installed-package'
    if any(path.is_relative_to(p) and not ({'site-packages','dist-packages'} & set(path.relative_to(p).parts)) for p in STDLIB):
        return 'standard-library'
    return 'unexpected'

def numerical(data, run, tree, name):
    rows = data['checks']
    check(len(rows)==117, name+': exactly 117 checks')
    check(len({r['name'] for r in rows})==117, name+': unique check names')
    independent = []
    for row in rows:
        label = row['name']
        if 'actual' in row:
            a,b=np.asarray(row['actual']),np.asarray(row['expected'])
            ok=bool(a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.abs(a-b)<=row['atol']+row['rtol']*np.abs(b)))
            check(row['max_abs_error']==float(np.max(np.abs(a-b))),name+': stored max error '+label)
        elif label.endswith('/nonstationary fixture'):
            ok=abs(row['derivative'])>1
        elif label.endswith('/simple Hessian excluded'):
            ok=row['simple_error']>1
        elif label.endswith('/stationary premise'):
            ok=bool(np.max(np.abs(row['residual']))<1e-9)
        elif label.endswith('/nonzero offdiagonal fixture'):
            ok=row['max_offdiag']>1
        else:
            ok=False
            check(False,name+': unexpected test type '+label)
        check(ok==row['passed'],name+': recomputed status '+label)
        independent.append(ok)
    check(sum(independent)==(38 if tree=='originals' else 117),name+': independently counted passes')
    check(data['passed']==sum(independent) and data['failed']==len(rows)-sum(independent) and data['tests']==len(rows),name+': truthful aggregate')
    for rel,value in data['source_sha256'].items():
        check(value==sha(run/tree/'scripts'/rel),name+': numerical source digest '+rel)
    parsed = {}
    unique = {}
    for e in data['expressions']:
        rel=tree+'/scripts/'+e['source']
        if rel not in parsed:
            parsed[rel]=ast.parse((run/rel).read_text(encoding='utf-8-sig'))
        found=[n for n in ast.walk(parsed[rel]) if getattr(n,'lineno',None)==e['line'] and getattr(n,'end_lineno',None)==e['end'] and hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()==e['ast_sha256']]
        check(bool(found),name+': AST identity '+rel+':'+str(e['line']))
        check(bool(found) and ast.unparse(found[0])==e['expression'],name+': expression text '+rel)
        unique[(e['source'],e['label'],e['line'],e['ast_sha256'])]=e
    check(len({e['source'] for e in data['expressions']})==10,name+': all ten patch files represented')
    for loaded in data['loader']:
        source=run/tree/'scripts'/(loaded['module']+'.py')
        check(sha(source)==loaded['sha256'],name+': loader frozen source '+loaded['module'])
        removed=[]
        for n in ast.parse(source.read_text(encoding='utf-8-sig')).body:
            if isinstance(n,ast.For) or (isinstance(n,ast.If) and any(isinstance(v,ast.Name) and v.id=='__name__' for v in ast.walk(n.test))):
                removed.append(dict(kind=type(n).__name__,line=n.lineno,end=n.end_lineno))
        check(removed==loaded['removed'],name+': loader removal inventory '+loaded['module'])
    return dict(tests=len(rows),passed=sum(independent),failed_names=[r['name'] for r in rows if not r['passed']],source_ast_expressions=list(unique.values()),loader=data['loader'])

def audit_run(package, run, mutant=False):
    summary=read(run/'replay-summary.json')
    manifest=read(package/'manifest.json')['package_files']
    inputs={p:v['sha256'] for p,v in manifest.items()}
    inputs.update({p:sha(package/p) for p in ('manifest.json','manifest.sha256')})
    for p,value in inputs.items():
        check(sha(run/p)==value,str(run)+': copied frozen input '+p)
    check(summary['input_sha256_before']==inputs==summary['input_sha256_after'],str(run)+': before/after maps')
    check(summary['inputs_unchanged'],str(run)+': unchanged flag')
    if not mutant:
        check(inputs==PACKET['files'],str(run)+': packet copy equality')
    for p,value in summary['output_sha256'].items():
        check(sha(run/p)==value,str(run)+': output digest '+p)
    expected_names=EXPECTED_CASES if not mutant else {n for n in EXPECTED_CASES if n.endswith(('-outside','-missing'))}
    check({r['name'] for r in summary['runs']}==expected_names,str(run)+': exact child case set')
    check(summary['accepted']==(not mutant),str(run)+': outer disposition')
    details=[]
    numbers={}
    for row in summary['runs']:
        name=row['name']; cli=name.startswith('op03-cli'); tree='originals' if name.startswith('originals') else 'candidates'
        missing=name.endswith('-missing'); outside=name.endswith('-outside'); opt=int('-optimized' in name)
        result=read(run/'results'/(name+'.json'))
        gate=result if cli else result['provenance']
        receipt=read(run/'receipts'/name/'receipt.json')
        stdout=(run/'receipts'/name/'stdout.txt').read_text()
        check(sha(run/'receipts'/name/'stdout.txt')==receipt['stdout_sha256'],name+': stdout hash')
        check(sha(run/'receipts'/name/'stderr.txt')==receipt['stderr_sha256'],name+': stderr hash')
        check(not receipt['timed_out'],name+': timeout')
        check(receipt['exit_code']==row['exit_code'],name+': raw status')
        expected_exit=86 if missing or (outside and not mutant) else (1 if tree=='originals' else 0)
        check(receipt['exit_code']==expected_exit,name+': expected process exit')
        check(row['accepted']==(not (mutant and outside)),name+': replay control acceptance')
        check(receipt['argv']==row['argv'][row['argv'].index('--')+1:],name+': actual child argv')
        check('-S' in receipt['argv'] and '-B' in receipt['argv'] and ('-O' in receipt['argv'])==bool(opt),name+': child flags')
        check(gate['optimize']==opt and gate['pid']>0,name+': runtime optimize/pid')
        for p,value in receipt['input_sha256'].items():
            check(p in inputs and inputs[p]==value,name+': receipt source binding '+p)
        required={'__main__':'candidates/scripts/op03_gap_fh.py','op03_gap_fixed':'candidates/scripts/op03_gap_fixed.py','provenance':'regression/provenance.py'} if cli else {
            **{n:tree+'/scripts/'+n+'.py' for n in COMMON+['op03_gap_precise' if tree=='originals' else 'op03_gap_fixed']},
            '__main__':'regression/regression.py','backend_probe':'regression/backend_probe.py','provenance':'regression/provenance.py'}
        expected_required={n:dict(path=str(run/p),sha256=inputs[p]) for n,p in required.items()}
        check(gate['required']==expected_required,name+': independent required bindings')
        policy=gate['policy']
        check(set(policy['stdlib_roots'])=={str(p) for p in STDLIB},name+': stdlib policy')
        check(policy['installed_package_roots']=={n:str(p) for n,p in PACKAGES.items()},name+': exact numpy/scipy roots')
        check(set(policy['stdlib_excluded_components'])=={'site-packages','dist-packages'},name+': site excluded')
        check(policy['fresh_input_root']==str(run),name+': fresh root')
        counts=Counter(); problems=[]
        for mod,file in sorted(gate['module_files'].items()):
            path=Path(file)
            cat=category(path,run,tree,inputs);counts[cat]+=1
            check(gate['modules'][mod]['path']==file and gate['modules'][mod]['category']==cat,name+': module classification '+mod)
            if cat=='unexpected':
                problems.append(dict(code='unexpected-module',module=mod,path=file))
            else:
                # Reads only fresh owned copies or installed permitted runtime.
                value=sha(path)
                check(gate['modules'][mod].get('sha256')==value,name+': module digest '+mod)
                if cat=='fresh-input':
                    check(value==inputs[path.relative_to(run).as_posix()],name+': frozen digest '+mod)
        check(set(gate['modules'])==set(gate['module_files']),name+': unfiltered detail map')
        for mod,rel in required.items():
            if mod not in gate['module_files']:
                problems.append(dict(code='missing-required-module',module=mod,expected_path=str(run/rel)))
            else:
                check(gate['module_files'][mod]==str(run/rel),name+': selected path '+mod)
                check(gate['modules'][mod].get('sha256')==inputs[rel],name+': required digest '+mod)
        check(problems==gate['problems'],name+': independently reconstructed problems')
        check(gate['accepted']==(not problems),name+': gate status')
        if not mutant:
            check(counts['installed-package']>0 and counts['standard-library']>0,name+': runtime modules retained outside fresh root')
        fixture=package/'control-fixtures/outside_probe.py'
        if outside:
            imported=gate['controls']['imported']
            check(imported==dict(module='r7_outside_probe',path=str(fixture),sha256=sha(fixture),token='R7-SW-001 real outside import executed'),name+': actual import metadata')
            check('R7-SW-001 real outside import executed' in stdout,name+': executed fixture token')
            check(gate['module_files'].get('r7_outside_probe')==(None if mutant else str(fixture)),name+': outside collection sensitivity')
            expected=[] if mutant else [dict(code='unexpected-module',module='r7_outside_probe',path=str(fixture))]
            check(problems==expected,name+': outside intended reason only')
        if missing:
            removed='op03_gap_fixed' if cli else 'gap_lib'
            check(gate['controls']['removed']==dict(module=removed,path=str(run/required[removed]),sha256=inputs[required[removed]]),name+': actual removed binding')
            check(problems==[dict(code='missing-required-module',module=removed,expected_path=str(run/required[removed]))],name+': missing intended reason only')
        detail=dict(name=name,exit_code=row['exit_code'],pid=gate['pid'],module_count=len(gate['module_files']),categories=dict(counts),required_count=len(required),problems=problems)
        if cli:
            pairs=re.findall(r'^u=([0-9.]+):.*dD/du_num=([+\-0-9.e]+)\s+2\(1-R\)f=([+\-0-9.e]+)',stdout,re.M)
            check([float(p[0]) for p in pairs]==[.4,.43,.45,.458],name+': four actual CLI points')
            check(all(np.isfinite(float(a)) and np.isfinite(float(b)) and abs(float(a)-float(b))<=max(.002,abs(float(a))*2e-4) for _,a,b in pairs),name+': four CLI numerical comparisons')
            detail['cli_cases']=[dict(u=float(u),fd=float(a),fh=float(b)) for u,a,b in pairs]
        else:
            check(result['module_files']==gate['module_files'],name+': duplicate full module map')
            detail['numerical']=numerical(result,run,tree,name)
            numbers[name]=[(r['name'],r['passed']) for r in result['checks']]
        details.append(detail)
    for name,rows in numbers.items():
        if '-normal' in name:
            check(rows==numbers[name.replace('-normal','-optimized')],name+': normal/-O names and statuses identical')
    return dict(package=str(package),run=str(run),mutant=mutant,optimize=summary['optimize'],accepted=summary['accepted'],runs=details)

def main():
    results=[]
    for folder in ['package-normal','package-optimized','mutant-filter-only']:
        package=OWN/folder
        for run in sorted((package/'work').glob('replay-*')):
            if (run/'replay-summary.json').exists():
                results.append(audit_run(package,run,folder.startswith('mutant')))
    check(len(results)==4,'two complete real replays and two complete mutant replays')
    for name in ['verify-normal','verify-optimized','replay-normal','replay-optimized','mutant-verify-normal','mutant-verify-optimized','mutant-replay-normal','mutant-replay-optimized']:
        out=OWN/'executions'/name
        receipt=read(out/'receipt.json')
        check(receipt['frozen_unchanged'] and receipt['package_unchanged'] and receipt['matches_expected_exit'],name+': outer receipt')
        check(sha(out/'stdout.txt')==receipt['stdout_sha256'] and sha(out/'stderr.txt')==receipt['stderr_sha256'],name+': outer streams')
        if 'verify' in name:
            data=read(out/'stdout.txt')
            check(data==dict(files_checked=50,passed=True,problems=[]),name+': actual verifier response')
        if name.startswith('replay-'):
            check(receipt['package_input_sha256_before']==PACKET['files']==receipt['package_input_sha256_after'],name+': original packet identity')
    prior=read(ROOT/'prior-review.json')
    prior_hashes={v['path']:v['actual_sha256'] for v in prior['input_hashes']}
    source_paths=[p for p in PACKET['files'] if p.startswith(('candidates/','originals/'))]
    check(all(PACKET['files'][p]==prior_hashes.get(p) for p in source_paths),'all 36 source/data copies retain prior reviewed identity')
    report=dict(role='independent reviewer output audit; own runs only',passed=not ERRORS,errors=ERRORS,source_copies_matching_prior=len(source_paths),results=results)
    (OWN/'execution-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=not ERRORS,errors=ERRORS,replay_count=len(results),child_count=sum(len(r['runs']) for r in results)),indent=2))
    return int(bool(ERRORS))

if __name__=='__main__':
    raise SystemExit(main())
