from pathlib import Path
import hashlib,json,zipfile,shutil
O=Path('/mnt/f/tools/math-audit-round9-20260923');P=O/'formal-reviewer';D=Path('/mnt/f/LaTeX/BVE research/research/artifacts/proof-audit-round9-20260923/formal-review')
def require(v,m):
    if not v:raise RuntimeError(m)
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
Index=P/'review/output-index.json';Data=json.loads(Index.read_text());require(Data['file_count_including_index']==len(Data['files'])==265,'Expected independent file count')
require(json.loads((O/'formal-isolated-semantic-received.json').read_text())['verdict']=='APPROVED','Actual review receipt missing')
Archive=D/'execution-evidence.zip';Rows=[]
require(not Archive.exists(),'Do not overwrite an existing independent archive')
with zipfile.ZipFile(Archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for x in Data['files']:
        p=Path(x['path']);name=str(p.relative_to(P));h=sha(p)
        if x.get('sha256'):require(h==x['sha256'],'Reviewer file changed '+name)
        else:require(p==Index,'Missing non-self hash '+name)
        if x.get('bytes') is not None:require(p.stat().st_size==x['bytes'],'Reviewer size changed '+name)
        z.write(p,name);Rows.append(dict(path=name,sha256=h,bytes=p.stat().st_size))
with zipfile.ZipFile(Archive) as z:
    require(len(z.infolist())==265,'Archive member count')
    for x in Rows:
        with z.open(x['path']) as f:require(hashlib.file_digest(f,'sha256').hexdigest()==x['sha256'],'Archived member differs '+x['path'])
Small=['review/output-index.json','review/final-validation.json','review/semantic-assessment.md','review/declaration-comparison.json','review/export-audit.json','review/root-clause-binders.json','review/replay-command-audit.json','review/wrapper-command-audit.json','review/review-result.json','review-d2ce43668d73481b9710a0a541cd57ef-summary.json']
for name in Small:
    p=P/name;target=D/'execution'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target);require(sha(p)==sha(target),'Small evidence copy '+name)
Result=dict(status='EXACT_INDEPENDENT_EXECUTION_ARCHIVE',reviewer_id='01a0cc20-968f-7f91-b030-1f216c592dcc',packet_sha256=Data['packet_sha256'],private_source=str(P),archive='execution-evidence.zip',archive_sha256=sha(Archive),archive_bytes=Archive.stat().st_size,files=Rows,scope='Actual new compilation, three wrong-target controls,59 exported declarations and separate semantic/axiom assessment; not a full analytic formalization')
(D/'execution-archive.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print('Verified independent formal archive',len(Rows),'files;',Archive.stat().st_size,'bytes;',Result['archive_sha256'],flush=True)
