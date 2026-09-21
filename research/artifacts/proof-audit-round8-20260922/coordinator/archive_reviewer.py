from pathlib import Path
import sys,json,hashlib,shutil
O=Path('/mnt/f/tools/math-audit-round8-20260922');A=Path('/mnt/f/LaTeX/BVE research/research/artifacts/proof-audit-round8-20260922')
name=sys.argv[1];source=O/name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checked=[]
if name in ['certificate-reviewer','formal-reviewer']:
    manifests=list(source.glob('review-*/'+('manifest.json' if name=='certificate-reviewer' else 'execution-manifest.json')))
    if len(manifests)!=1:raise RuntimeError('Expected one completed review manifest')
    for m in manifests:
        d=json.loads(m.read_text())
        for n,v in d['files'].items():
            if sha(m.parent/n)!=v['sha256']:raise RuntimeError('Reviewer evidence changed '+n)
        checked.append({'manifest':str(m.relative_to(source)),'sha256':sha(m),'verified_files':len(d['files'])})
rows=[]
for p in sorted(source.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc':continue
    n=p.relative_to(source);target=A/name/n;target.parent.mkdir(parents=True,exist_ok=True)
    h=sha(p)
    if target.exists() and sha(target)!=h:raise RuntimeError('Archive differs '+str(n))
    if not target.exists():shutil.copyfile(p,target)
    if sha(target)!=h:raise RuntimeError('Copy mismatch '+str(n))
    rows.append({'path':str(n),'sha256':h,'bytes':p.stat().st_size})
record={'kind':'coordinator_exact_copy_check_not_new_review','source_root':str(source),'archive_root':str(A/name),'reviewer_manifests_verified':checked,'files':rows}
(A/(name+'-archive.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('Archived',name,len(rows),'files',flush=True)
