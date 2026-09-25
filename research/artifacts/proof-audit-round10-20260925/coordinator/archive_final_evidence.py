from pathlib import Path
import json,hashlib,shutil,gzip,datetime
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A=R/'research/artifacts/proof-audit-round10-20260925'
def sha(B):return hashlib.sha256(B).hexdigest()
def copy(S,D):
 B=S.read_bytes();D.parent.mkdir(parents=True,exist_ok=True)
 if D.exists() and D.read_bytes()!=B:raise RuntimeError('Refuse archive overwrite '+str(D))
 if not D.exists():D.write_bytes(B)
 return {'path':str(D.relative_to(A)),'sha256':sha(B),'bytes':len(B)}
Records=[]
S=O/'software-reviewer/stateless-8b23fae8-e2gp58jk'
for P in sorted(S.rglob('*')):
 if P.is_file() and '__pycache__' not in P.parts:Records.append(copy(P,A/'software-execution'/P.relative_to(S)))
Records.append(copy(O/'sector-author/reflection_seeds.py',A/'sector-author/reflection_seeds.py'))
S=O/'pdf-build/SL_gap_nge2_symmetry_recon/a0a065e5ed17'
for P in sorted(S.iterdir()):
 if P.is_file() and P.suffix not in ['.aux','.toc','.out','.pdf','.synctex']:Records.append(copy(P,A/'pdf-final'/P.name))
for N in ['final-pdf-page1.png','final-pdf-page3.png']:Records.append(copy(O/N,A/'pdf-final'/N))
S=O/'formal-author';D=A/'lean-author'
for Folder in ['project','root-project','commands','handoff-checkpoint']:
 for P in sorted((S/Folder).rglob('*')):
  if P.is_file() and P.suffix not in ['.olean','.ilean','.pyc'] and '__pycache__' not in P.parts:Records.append(copy(P,D/P.relative_to(S)))
for P in sorted(S.iterdir()):
 if P.is_file() and P.suffix in ['.json','.md','.py','.txt'] and P.name not in ['handoff-manifest.json']:
  Records.append(copy(P,D/P.name))
for Label in ['exact-root-01','exact-root-02']:
 E=S/'evidence'/Label
 for P in sorted(E.rglob('*')):
  if not P.is_file() or 'lib' in P.relative_to(E).parts or P.name=='run-manifest.json' and P.parent!=E:continue
  B=P.read_bytes();Dest=D/'evidence'/Label/P.relative_to(E)
  if len(B)>2000000:
   Encoded=gzip.compress(B,mtime=0);Dest=Dest.with_suffix(Dest.suffix+'.gz');Dest.parent.mkdir(parents=True,exist_ok=True)
   if Dest.exists() and Dest.read_bytes()!=Encoded:raise RuntimeError('Compressed archive drift')
   Dest.write_bytes(Encoded)
   Records.append({'path':str(Dest.relative_to(A)),'sha256':sha(Encoded),'bytes':len(Encoded),'encoding':'gzip','original_sha256':sha(B),'original_bytes':len(B),'original_path':str(P.relative_to(S))})
  else:Records.append(copy(P,Dest))
Jobs=S/'.research-state/jobs'
for P in sorted(Jobs.glob('exact-root-02-durable*')):
 if P.is_file():Records.append(copy(P,D/'durable-job'/P.name))
Proof=(S/'root-project/AuditRound10.lean').read_bytes();Target=R/'lean-proof/SL/AuditRound10.lean'
if Target.exists() and Target.read_bytes()!=Proof:raise RuntimeError('Different active Lean source')
Target.write_bytes(Proof)
Inventory=A/'caller-inventory.json';Initial=A/'author-development/caller-inventory-before-integration.json'
if not Initial.exists():shutil.copyfile(Inventory,Initial)
Data=json.loads(Initial.read_text())
for Row in Data['callers']:Row['sha256']=sha((R/Row['path']).read_bytes())
Data['binding_stage']='final active Python sources after actual main integration; static import closure unchanged'
Inventory.write_text(json.dumps(Data,ensure_ascii=False,indent=2)+'\n')
(A/'execution-archive-manifest.json').write_text(json.dumps({'files':Records,'scope':'Author, coordinator and independent software executions kept distinct. Large original JSON evidence is losslessly gzip-compressed; hashes identify both encodings. Compiled local objects stay in the external run; recorded hashes and rebuild instructions are retained.'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'files':len(Records),'bytes':sum(X['bytes'] for X in Records),'lean_sha256':sha(Proof)}))
