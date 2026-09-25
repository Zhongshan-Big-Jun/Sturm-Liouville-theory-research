from pathlib import Path
import json,gzip,hashlib,concurrent.futures,time,datetime
BASE=Path(__file__).resolve().parent
packet=Path(json.loads((BASE/'config.json').read_text())['packet']);p=json.loads(packet.read_text())
m=json.loads(gzip.decompress((packet.parent/p['inputs']['inputs/exact-root/run-manifest.json.gz']['snapshot']).read_bytes()))
allowed=[Path('/mnt/f/LaTeX/BVE research/lean-proof/.lake/packages'),Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0')]
items=list(m['target']['import_artifacts'].items())
def one(it):
 name,old=it;path=Path(old['path'])
 assert any(path.is_relative_to(b) for b in allowed),(name,str(path))
 try:
  s0=path.stat()
  with path.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
  s1=path.stat()
  return name,{'path':str(path),'sha256':h,'expected_sha256':old['sha256'],'matches':h==old['sha256'],'size':s1.st_size,'mtime_ns':s1.st_mtime_ns,'stable_while_hashed':(s0.st_mtime_ns,s0.st_size)==(s1.st_mtime_ns,s1.st_size)}
 except Exception as e:return name,{'path':str(path),'error':repr(e),'matches':False}
start=time.monotonic();results={}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for n,r in pool.map(one,items):
  results[n]=r
  if len(results)%1000==0: print('HASHED',len(results),'of',len(items),round(time.monotonic()-start,1),flush=True)
changed=[]
for n,r in results.items():
 if 'error' not in r:
  st=Path(r['path']).stat()
  if (r['size'],r['mtime_ns'])!=(st.st_size,st.st_mtime_ns):changed.append(n)
summary={'role':'independent-reviewer','utc_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifact_count':len(results),'matches':all(v['matches'] for v in results.values()),'stable_while_hashed':all(v.get('stable_while_hashed',False) for v in results.values()),'changed_on_final_stat':changed,'mismatches':[k for k,v in results.items() if not v['matches']],'seconds':time.monotonic()-start,'artifacts':results}
(BASE/'evidence'/'environment-artifact-check.json').write_text(json.dumps(summary,indent=2)+'\n')
print('ENVIRONMENT_RESULT',{k:v for k,v in summary.items() if k!='artifacts'},flush=True)
