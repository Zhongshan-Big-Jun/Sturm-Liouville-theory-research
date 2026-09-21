from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,json,sys

ROOT=Path(sys.argv[1]); B=ROOT/'frozen'
checks=Counter(); observations={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ensure(ok,label):
    checks[label]+=1
    if not ok:raise ArithmeticError('Provenance verification failed: '+label)
def load(p):return json.loads(p.read_text())
packet=load(ROOT/'packet.json')
ensure(sha(ROOT/'packet.json')=='10a8bec28d19a7d77cfe96c73814e1faf51ebe754d590cebb6709145e980a042','packet hash')
for original,entry in packet['inputs'].items():
    snapshot=ROOT/'snapshots'/original
    ensure(sha(snapshot)==entry['sha256'],'packet input hash')
    if original.endswith('.zip'):continue
    short=original.split('proof-audit-round8-20260922/',1)[1]
    member=short[len('certificate/'):] if short.startswith('certificate/') else 'inputs/'+short
    ensure(sha(B/member)==entry['sha256'],'separate snapshot equals archived member')
m=load(B/'artifact_hashes.json')
actual={str(p.relative_to(B)) for p in B.rglob('*') if p.is_file()}
ensure(actual==set(m['files'])|{'artifact_hashes.json'},'archive complete manifest coverage')
for name,entry in m['files'].items():
    p=B/name
    ensure(sha(p)==entry['sha256'] and p.stat().st_size==entry['size_bytes'],'archived manifest file hash and size')
inputs=load(B/'inputs/manifest.json')
for entry in inputs['files']:
    p=B/entry['copy']
    ensure(sha(p)==entry['sha256'],'original intake copy hash')
    if 'size' in entry:ensure(p.stat().st_size==entry['size'],'original intake size')
for name,h in load(B/'inputs/submitted/artifact_hashes.json').items():
    ensure(sha(B/'inputs/submitted'/name)==h,'submitted artifact hash')
source_records=[]
for entry in load(B/'inputs/submitted/source_manifest.json')['sources']:
    p=B/'inputs/sources'/entry['path']
    if not p.is_file():
        source_records.append({'path':entry['path'],'present_in_frozen_zip':False})
        continue
    data=p.read_bytes(); blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    source_records.append({'path':entry['path'],'present_in_frozen_zip':True,'sha256':sha(p),'computed_git_blob_sha1':blob,'connector_reported_blob_sha':entry['connector_reported_blob_sha'],'matches_reported_git_blob':blob==entry['connector_reported_blob_sha']})
observations['source_identities']=source_records
summary=load(B/'replay_summary.json'); inventory=load(B/'verification.json')
records={p.parent.name:(p,load(p)) for p in (B/'runs').glob('*/record.json')}
ensure(set(records)=={r['run'] for r in summary['runs']},'all archived run receipts indexed')
counts=Counter(); positive=[]; negative=[]
for name,(p,rec) in records.items():
    folder=p.parent
    for key in ['input_sha256','files_sha256']:
        for filename,h in rec[key].items():ensure(sha(folder/filename)==h,'archived receipt payload hash')
    ensure(not rec['timed_out'] and rec['return_code']==rec['expected_code'] and rec['expectation_matched'],'archived exit status')
    counts[str(rec['return_code'])]+=1
    if 'certificate.py' in rec['input_sha256']:
        ensure(rec['input_sha256']['certificate.py']==packet['inputs']['research/artifacts/proof-audit-round8-20260922/certificate/certificate.py']['sha256'],'archived certificate source identity')
    cmd=rec['command']; stderr=(folder/'stderr.txt').read_text()
    if '--negative' in cmd:
        control=cmd[cmd.index('--negative')+1]
        fresh=load(ROOT/'fresh_runs'/('negative-'+control+'-normal')/'receipt.json')
        ensure(rec['return_code']==1 and stderr.rstrip().endswith(fresh['required_error']),'archived intended negative guard')
        ensure(not (folder/'results.json').exists(),'archived rejection has no success result')
        negative.append({'control':control,'flags':sorted(f for f in ['-O','-S'] if f in cmd)})
    elif 'certificate.py' in cmd:
        result=load(folder/'results.json')
        ensure(len(result['checks'])==19 and all(r['exact_comparison_passed'] for r in result['checks']),'archived 19 positive groups')
        ensure(not stderr,'archived positive stderr empty')
        positive.append((name,result))
    elif 'checks.py' in cmd:
        result=load(folder/'results.json')
        ensure(result['confirmed_groups']==22 and len(result['checks'])==22 and all(r['confirmed'] for r in result['checks']),'archived supplied 22 checks')
for entry in summary['runs']:
    folder=B/'runs'/entry['run']; rec=records[entry['run']][1]
    ensure(sha(folder/'record.json')==entry['record_sha256'],'summary receipt hash')
    ensure(sha(folder/'stdout.txt')==entry['stdout_sha256'] and sha(folder/'stderr.txt')==entry['stderr_sha256'],'summary raw stdout stderr hash')
    ensure(entry['return_code']==rec['return_code'] and entry['command']==rec['command'],'summary actual argv and status')
ensure(dict(counts)==summary['actual_exit_code_counts']=={'0':9,'1':56},'all archived failures preserved and counted')
ensure(len(positive)==4 and len(negative)==56,'archived positive negative counts')
ensure(len({(r['control'],tuple(r['flags'])) for r in negative})==56,'14 controls in four distinct modes')
reference=load(B/'results.json')
for name,result in positive:
    ensure({k:v for k,v in result.items() if k not in ['python','optimized']}=={k:v for k,v in reference.items() if k not in ['python','optimized']},'all archived positive arithmetic identical')
for mode,key in [('normal','results.json'),('optimized','results_optimized.json')]:
    entry=summary['selected_result_runs'][mode]; folder=B/'runs'/entry['run']
    ensure(sha(folder/'results.json')==entry['result_sha256']==sha(B/key),'exported result exact origin')
    ensure(sha(folder/'record.json')==entry['record_sha256'],'exported result receipt origin')
vr=B/'runs'/summary['verification_run']
ensure(sha(vr/'verification.json')==sha(B/'verification.json') and sha(vr/'record.json')==summary['verification_record_sha256'],'author inventory exported origin')
for entry in inventory['runs']:
    folder=B/'runs'/entry['run']; rec=records[entry['run']][1]
    ensure(sha(folder/'record.json')==entry['record_sha256'] and rec['command']==entry['command'] and rec['return_code']==entry['return_code'],'author inventory raw receipt match')
ensure(set(inventory['current_run_pending_receipt'])==set(records)-{r['run'] for r in inventory['runs']},'pending inventory receipt now supplied')
failure=summary['supplied_initial_failure']
ensure(sha(B/failure['path'])==failure['sha256']=='2eaf2f29275858450bd331ed42a716ccdd7204bb74e5ee5e60975c2b76901fad','original symbolic failure log preserved')
ensure(failure['actual_original_exit_code'] is None and failure['failed_source_revision_available'] is False and inputs['original_failure_exit_code'] is None,'unavailable original failed revision acknowledged')
ensure('ArithmeticError: Check failed: round7 Wronskian identity n=1..4 regression' in (B/failure['path']).read_text(),'original raw failure type')
for name in ['execution_normal.log','execution_optimized.log']:
    log=(B/'inputs/submitted'/name).read_text()
    ensure('22 groups confirmed' in log,'original supplied raw success log')

fresh_records={p.parent.name:(p,load(p)) for p in (ROOT/'fresh_runs').glob('*/receipt.json')}
fresh_counts=Counter();fresh_certificates=[];fresh_module_sets={}
for name,(p,rec) in fresh_records.items():
    folder=p.parent
    for filename,h in rec['files_sha256'].items():ensure(sha(folder/filename)==h,'fresh receipt payload hash')
    for filename,h in rec['source_sha256'].items():
        source=ROOT/filename if filename=='reviewer_runner.py' else folder/filename
        ensure(sha(source)==h,'fresh input source hash')
    ensure(rec['expectation_matched'] and rec['exit_code']==rec['expected_exit_code'],'fresh expected exit')
    fresh_counts[str(rec['exit_code'])]+=1
    if rec['required_error']:
        ensure((folder/'stderr.txt').read_text().rstrip().endswith(rec['required_error']),'fresh intended negative guard')
    if name.startswith('certificate-'):
        result=load(folder/'results.json')
        ensure(len(result['checks'])==19,'fresh certificate 19 groups')
        ensure({k:v for k,v in result.items() if k not in ['python','optimized']}=={k:v for k,v in reference.items() if k not in ['python','optimized']},'fresh complete certificate equals author')
        mods=load(folder/'imports.json')['modules']
        fresh_module_sets[name]=[r for r in mods if r.get('file') and any(k in r['file'] for k in ['dist-packages','site-packages','sitecustomize'])]
        if '-S' in rec['argv']:ensure(not fresh_module_sets[name],'no external startup modules observed in no-site runs')
        fresh_certificates.append(name)
    if name.startswith('supplied-'):
        result=load(folder/'results.json')
        ensure(result['confirmed_groups']==22 and all(r['confirmed'] for r in result['checks']),'fresh supplied 22 groups')
        ensure(result['checks']==load(B/'inputs/submitted/results.json')['checks'],'fresh supplied results reproduce original')
observations['fresh_certificate_runtime_modules']=fresh_module_sets
observations['fresh_count_before_current_provenance_receipt']=dict(fresh_counts)
observations['legacy_miss_reproduced_here']=load(ROOT/'fresh_runs/legacy-platform/observations.json')['supplied_miss_reproduced_here']
observations['author_exit_counts']=dict(counts)
observations['author_run_count']=len(records)
observations['frozen_manifest_entries']=len(m['files'])
output={'status':'PASS','counts':dict(checks),'observations':observations,'limitations':['Historical source commit membership is not verified against unsupplied Git data.','Original failed source revision and original exit-code receipt unavailable.','Runtime module inventories are post-execution observations, not complete import-event isolation.']}
Path(sys.argv[2]).write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
