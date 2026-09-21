from pathlib import Path
import json,hashlib,shutil
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round5-20260921');Source=O/'independent-lean-replay';A=R/'research/artifacts/proof-audit-round5-20260921/lean/independent-replay'
assert (O/'independent-execution-completion.json').is_file()
assert (Source/'REPORT.json').is_file() and (Source/'REPORT.md').is_file()
A.mkdir(parents=True,exist_ok=False);Rows=[]
for P in sorted(Source.rglob('*')):
 if not P.is_file():continue
 Rel=P.relative_to(Source)
 if any(N in Rel.parts for N in ['__pycache__','tmp']) or P.suffix=='.pyc':continue
 if 'build' in Rel.parts:
  Q=A/'compiled-objects'/(P.name+'.bin')
 else:Q=A/Rel
 Q.parent.mkdir(parents=True,exist_ok=True);assert not Q.exists();shutil.copyfile(P,Q)
 Rows.append({'original_relative_path':str(Rel),'archived_relative_path':str(Q.relative_to(A)),'sha256':hashlib.sha256(Q.read_bytes()).hexdigest(),'bytes':Q.stat().st_size})
(A/'archive-manifest.json').write_text(json.dumps(Rows,indent=2)+'\n')
for Name in ['independent-execution-spawn.json','independent-execution-completion.json','independent-execution-scope-steering.json']:shutil.copyfile(O/Name,A/Name)
print('Archived independent executor files',len(Rows),'logical bytes',sum(X['bytes'] for X in Rows))
