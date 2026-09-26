from pathlib import Path
import json,hashlib,gzip
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round12-20260926');A=R/'research/artifacts/proof-audit-round12-20260926';S=O/'formal-author';D=A/'lean-author'
Rows=[];Excluded=[]
for P in sorted(S.rglob('*')):
	if not P.is_file():continue
	N=P.relative_to(S)
	if any(X in N.parts for X in ['objects','lib','tmp','__pycache__','.lake']) or P.suffix in ['.olean','.ilean','.pyc']:
		Excluded.append(N.as_posix());continue
	B=P.read_bytes();T=D/N;Row=dict(original_path=N.as_posix(),original_sha256=hashlib.sha256(B).hexdigest(),original_bytes=len(B))
	if len(B)>2000000:B=gzip.compress(B,mtime=0);T=T.with_suffix(T.suffix+'.gz');Row['encoding']='gzip'
	else:Row['encoding']='identity'
	T.parent.mkdir(parents=True,exist_ok=True)
	if T.exists() and T.read_bytes()!=B:raise RuntimeError('Immutable archive drift '+str(T))
	T.write_bytes(B);Row.update(path=T.relative_to(A).as_posix(),sha256=hashlib.sha256(B).hexdigest(),bytes=len(B));Rows.append(Row)
for Name in ['spawn','completion']:
	P=O/f'formal-author-{Name}.json';T=D/f'native-{Name}.json';T.write_bytes(P.read_bytes())
(A/'lean-author-archive-manifest.json').write_text(json.dumps(dict(files=Rows,excluded_local_build_or_temp_paths=Excluded,scope='Author execution only. Large originals are lossless gzip with raw and encoded hashes. No dependency tree or local compiled object is published; source, commands, import bindings and all failures are retained.'),indent=2)+'\n')
print('Archived formal author',len(Rows),'files',sum(X['bytes'] for X in Rows),'bytes',flush=True)
