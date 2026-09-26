from pathlib import Path
import json,hashlib,shutil,gzip,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round12-20260926');A=R/'research/artifacts/proof-audit-round12-20260926'
def sha(B):return hashlib.sha256(B).hexdigest()
Rows=[]
def copy(S,D):
 B=S.read_bytes();D.parent.mkdir(parents=True,exist_ok=True)
 if D.exists() and D.read_bytes()!=B:raise RuntimeError('Immutable archive drift '+str(D))
 if not D.exists():D.write_bytes(B)
 Rows.append(dict(path=str(D.relative_to(A)),sha256=sha(B),bytes=len(B)))
assert json.loads((O/'formal-comparison-verified.json').read_text())['verdict']=='APPROVED'
Reviewer=Path(sys.argv[1]).resolve()
if not Reviewer.is_relative_to(O/'formal-reviewer') or not Reviewer.is_dir():raise RuntimeError('Invalid independent execution source')
for P in sorted(Reviewer.rglob('*')):
 if not P.is_file() or any(X in P.relative_to(Reviewer).parts for X in ['objects','lib','tmp','__pycache__']) or P.suffix in ['.olean','.ilean','.pyc']:continue
 B=P.read_bytes();Dest=A/'formal-execution'/P.relative_to(Reviewer)
 if len(B)>2000000:
  Encoded=gzip.compress(B,mtime=0);Dest=Dest.with_suffix(Dest.suffix+'.gz');Dest.parent.mkdir(parents=True,exist_ok=True)
  if Dest.exists() and Dest.read_bytes()!=Encoded:raise RuntimeError('Compressed archive drift')
  Dest.write_bytes(Encoded);Rows.append(dict(path=str(Dest.relative_to(A)),sha256=sha(Encoded),bytes=len(Encoded),encoding='gzip',original_sha256=sha(B),original_bytes=len(B),original_path=str(P.relative_to(Reviewer))))
 else:copy(P,Dest)
(A/'formal-execution-archive-manifest.json').write_text(json.dumps({'files':Rows,'scope':'Independent actual formal execution. Large original JSON is losslessly gzip-compressed with original hashes; local binary objects stay in the external run.'},ensure_ascii=False,indent=2)+'\n')
print('Archived independent formal execution',len(Rows),'files',sum(X['bytes'] for X in Rows),'bytes')
