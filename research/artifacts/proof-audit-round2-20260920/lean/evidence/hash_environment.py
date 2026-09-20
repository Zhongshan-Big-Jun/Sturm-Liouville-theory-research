from pathlib import Path
import hashlib, json, datetime, time
OUT=Path('/mnt/f/tools/math-audit-round2-20260920/lean-author')

def from_windows(s):
	s=s.replace('\\','/')
	if len(s)>2 and s[1]==':': return Path('/mnt')/s[0].lower()/s[3:]
	raise ValueError(s)

def digest(p):
	h=hashlib.sha256()
	with p.open('rb') as f:
		for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
	return h.hexdigest()

start=time.monotonic()
meta=json.loads((OUT/'loaded-modules.json').read_text())
records=[]
size=0
for i,m in enumerate(meta['modules']):
	p=from_windows(m['olean'])
	artifacts=[]
	for q in [p,Path(str(p)+'.private'),Path(str(p)+'.server')]:
		if q.exists():
			stat_before=q.stat()
			h=digest(q)
			stat_after=q.stat()
			assert stat_before.st_size==stat_after.st_size and stat_before.st_mtime_ns==stat_after.st_mtime_ns, q
			artifacts.append({'path':str(q),'size':stat_after.st_size,'sha256':h})
			size+=stat_after.st_size
	assert artifacts and artifacts[0]['path']==str(p),p
	records.append({'module':m['module'],'resolved_olean':str(p),'artifacts':artifacts})
	if (i+1)%500==0: print('hashed',i+1,'modules',round(size/1024**3,2),'GiB',flush=True)
assert len(records)==meta['module_count']
result={'scope':'All modules actually loaded by successful type/axiom inspection 14. Include available .olean.private and .olean.server companions. This is an artifact-identity inventory, not an independent kernel or a claim that all imported theorems have been audited.','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'module_count':len(records),'artifact_count':sum(len(x['artifacts']) for x in records),'total_bytes':size,'elapsed_seconds':time.monotonic()-start,'modules':records}
(OUT/'imported-artifact-hashes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('DONE',len(records),result['artifact_count'],'files',round(size/1024**3,2),'GiB',round(result['elapsed_seconds'],2),'seconds',flush=True)
