from pathlib import Path
import hashlib, json, shutil, zipfile, datetime

O=Path('/mnt/f/tools/math-audit-round8-20260922')
R=Path('/mnt/f/LaTeX/BVE research')
A=R/'research/artifacts/proof-audit-round8-20260922'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):
	p.parent.mkdir(parents=True,exist_ok=True)
	p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def copy(src,dst):
	dst.parent.mkdir(parents=True,exist_ok=True)
	if dst.exists():
		if sha(src)!=sha(dst): raise RuntimeError('Archive conflict '+str(dst))
	else: shutil.copyfile(src,dst)

checks={}
for name,manifest in [('sliver-author','output_manifest.json'),('certificate-author','artifact_hashes.json')]:
	d=json.loads((O/name/manifest).read_text())
	rows=d['files']
	if isinstance(rows,list): rows={v['path']:v for v in rows}
	for n,v in rows.items():
		if sha(O/name/n)!=v['sha256']: raise RuntimeError('Author input changed '+name+'/'+n)
	checks[name]={'manifest_sha256':sha(O/name/manifest),'checked_files':len(rows)}
lm=json.loads((O/'lean-author/handoff-manifest.json').read_text())
for group in ['package_files','raw_evidence_files']:
	for n,h in lm[group].items():
		if sha(O/'lean-author'/n)!=h: raise RuntimeError('Lean manifest mismatch '+n)
if sha(O/'lean-author'/lm['archive']['path'])!=lm['archive']['sha256']: raise RuntimeError('Lean zip mismatch')
checks['lean-author']={'manifest_sha256':sha(O/'lean-author/handoff-manifest.json'),'checked_package_files':len(lm['package_files']),'checked_raw_files':len(lm['raw_evidence_files'])}
for srcname,dstname in [('sliver-author','analytic-author'),('certificate-author','certificate'),('lean-author','lean-author')]:
	for p in (O/srcname).rglob('*'):
		if p.is_file() and '__pycache__' not in p.parts: copy(p,A/dstname/p.relative_to(O/srcname))
	ziptarget=A/(dstname+'-evidence.zip')
	if not ziptarget.exists():
		with zipfile.ZipFile(ziptarget,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
			for p in sorted((A/dstname).rglob('*')):
				if p.is_file(): z.write(p,str(p.relative_to(A/dstname)))
	checks[srcname]['archive_sha256']=sha(ziptarget)
# Preserve the originals needed by the author's optional replay driver.
for p in (O/'certificate-author/inputs/sources').rglob('*'):
	if p.is_file(): copy(p,A/'sources'/p.relative_to(O/'certificate-author/inputs/sources'))
for n in ['sliver-author-spawn.json','sliver-author-completion.json','certificate-author-spawn.json','certificate-author-completion.json','lean-author-spawn.json','lean-author-completion.json']:
	copy(O/n,A/'orchestration'/n)
save(A/'orchestration/sliver-provenance-note.json',{
	'kind':'coordinator_observation_not_native_receipt',
	'observation':'The original author completed and delivered its package by an actual completion notification. A queued follow-up reopened the author before collection; the subsequently saved wait result was timed out and close returned running. That wait is not a completion receipt and is not used as independent verification.',
	'author_package_identity':checks['sliver-author'],
	'independent_review':'A fresh separate reviewer is required for acceptance.'})
save(A/'author-archive-verification.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'AUTHOR_BYTES_VERIFIED_NOT_MATHEMATICAL_APPROVAL','authors':checks})
d=json.loads((O/'lean-author/author-replay-03/declarations.json').read_text())
save(A/'formal-blind/declarations.json',{'public_declarations':d['public_declarations']})
print(json.dumps(checks),flush=True)
