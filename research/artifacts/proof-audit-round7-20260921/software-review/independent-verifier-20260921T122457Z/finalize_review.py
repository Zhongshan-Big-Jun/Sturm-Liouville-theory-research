from pathlib import Path
import datetime,hashlib,json,sys
ROOT=Path(__file__).resolve().parent.parent
OWN=Path(__file__).resolve().parent
RUNS=[ROOT/'work/replay-20260921T122812Z-ea7225',ROOT/'work/replay-20260921T122930Z-e64f7d']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
report=read(ROOT/'REVIEW.json');packet=read(ROOT/'PACKET.json')
problems=[]
if report['verdict'] not in ['APPROVED','CHANGES_REQUIRED','INCOMPLETE']:problems.append('invalid verdict')
if report['packet']['sha256_after']!=sha(ROOT/'PACKET.json'):problems.append('PACKET modified')
if len(report['input_hashes'])!=len(packet['files']):problems.append('input count')
for item in report['input_hashes']:
    rel=item['path'];h=sha(ROOT/rel)
    if not (h==packet['files'][rel]==item['actual_sha256']==item['sha256_after']):problems.append('input mismatch '+rel)
for run in RUNS:
    copied=read(run/'copy-manifest.json')
    for rel,h in copied.items():
        if sha(run/rel)!=h or packet['files'].get(rel)!=h:problems.append('replay copy changed '+str(run/rel))
for run in report['executions']+report['replay_child_executions']:
    for stream in ['stdout','stderr']:
        if sha(ROOT/run[stream])!=run[stream+'_sha256']:problems.append('stream changed '+run[stream])
    if sha(ROOT/run['receipt'])!=run['receipt_sha256']:problems.append('receipt changed '+run['receipt'])
for file in ['README-review.md','REVIEW.json','derivation.md']:
    p=ROOT/file if file!='derivation.md' else OWN/file
    if not p.is_file():problems.append('missing deliverable '+file)
if len(report['ten_patch_results'])!=10 or len(report['unchanged_dependencies'])!=8:problems.append('patch/dependency counts')
if any(p['assessment']!='PASS_BOUNDED' for p in report['ten_patch_results']):problems.append('patch result mismatch')
if report['required_fix_ids']!=['R7-SW-001']:problems.append('fix id mismatch')
if not any(f['id']=='R7-SW-001' and f['blocking'] for f in report['findings']):problems.append('missing scope finding')
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':['/usr/bin/python3','-B',str(Path(__file__).relative_to(ROOT))],'cwd':str(ROOT),'script_sha256':sha(Path(__file__)),'exit_code':int(bool(problems)),'problems':problems,'input_count':len(packet['files']),'copied_input_count_per_attempt':45,'candidate_patch_count':10,'unchanged_dependency_count':8,'review_verdict':report['verdict'],'frozen_inputs_unchanged':not problems}
record['stdout']=json.dumps({'final_validation_passed':not problems,'verdict':report['verdict'],'problems':problems})+'\n';record['stderr']=''
(OWN/'final-validation.json').write_text(json.dumps(record,indent=2)+'\n')
if problems:
    print(record['stdout'],end='');sys.exit(1)
paths=[ROOT/'REVIEW.json',ROOT/'README-review.md']
for base in [OWN,*RUNS]:
    paths.extend(p for p in base.rglob('*') if p.is_file() and p!=OWN/'artifact-hashes.json')
hashes={str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(set(paths))}
manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(ROOT),'files':hashes,'exclusions':['independent-verifier-20260921T122457Z/artifact-hashes.json','REVIEW.sha256'],'scope':'Only final review deliverables and outputs from this reviewer, including own frozen input copies; no author execution output was read.'}
(OWN/'artifact-hashes.json').write_text(json.dumps(manifest,indent=2)+'\n')
sidecars=[ROOT/'REVIEW.json',ROOT/'README-review.md',OWN/'artifact-hashes.json']
with (ROOT/'REVIEW.sha256').open('x') as f:
    for p in sidecars:f.write(sha(p)+'  '+str(p.relative_to(ROOT))+'\n')
# Final comparison covers all previously generated artifacts and immutable inputs.
if any(sha(ROOT/rel)!=entry['sha256'] for rel,entry in hashes.items()):raise RuntimeError('artifact changed during finalization')
print(record['stdout'],end='')
print(json.dumps({'artifact_files_bound':len(hashes),'review_sha256':sha(ROOT/'REVIEW.json'),'readme_sha256':sha(ROOT/'README-review.md'),'manifest_sha256':sha(OWN/'artifact-hashes.json')},indent=2))
