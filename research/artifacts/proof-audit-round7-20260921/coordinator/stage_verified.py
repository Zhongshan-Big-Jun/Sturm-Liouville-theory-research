from pathlib import Path
import subprocess,json,hashlib
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round7-20260921')
Paths=json.loads((Out/'stage-paths.json').read_text());Expected=json.loads((Out/'stage-expected-sha256.json').read_text())
ManifestPath='reports/proof-audit-round7-20260921/publication-manifest.json'
Manifest=json.loads((Root/ManifestPath).read_text())
Published={X['path']:X['sha256'] for X in Manifest['files']}
assert len(Published)==len(Manifest['files'])
assert set(Published)|{ManifestPath}==set(Paths),'Publication manifest and exact staged scope differ'
assert all(Expected[N]==H for N,H in Published.items()),'Candidate changed after publication manifest'
Existing=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=Root)
assert not Existing,'Unexpected preexisting staged changes; inspect before staging.'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=Root,text=True).strip()=='636dac87c269795a520824101f1b2abd2c583c9b'
for Name in Paths: assert hashlib.sha256((Root/Name).read_bytes()).hexdigest()==Expected[Name],Name
List=Out/'pathspec.nul';List.write_bytes(b'\0'.join(N.encode() for N in Paths)+b'\0')
subprocess.run(['git','add','--force','--pathspec-from-file='+str(List),'--pathspec-file-nul'],cwd=Root,check=True)
Staged=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=Root).decode().rstrip('\0').split('\0')
assert set(Staged)==set(Paths),(set(Staged)-set(Paths),set(Paths)-set(Staged))
Process=subprocess.Popen(['git','cat-file','--batch'],cwd=Root,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for Name in Paths:
	Process.stdin.write((':'+Name+'\n').encode());Process.stdin.flush()
	Header=Process.stdout.readline().split();assert len(Header)==3 and Header[1]==b'blob',Header
	Left=int(Header[2]);Hash=hashlib.sha256()
	while Left:
		Chunk=Process.stdout.read(min(1_048_576,Left));assert Chunk;Hash.update(Chunk);Left-=len(Chunk)
	assert Process.stdout.read(1)==b'\n'
	assert Hash.hexdigest()==Expected[Name],('Git conversion changed bytes',Name)
Process.stdin.close();assert Process.stdout.read()==b'' and Process.wait()==0
Check={'status':'PASS','staged_paths':len(Paths),'actual_git_blobs_match_worktree_sha256':True,'publication_manifest_matches_exact_staged_scope_and_bytes':True,'scope':'Exact allowlist only; ignored raw execution logs were force-added by individual path. No unrelated baseline changes staged.'}
(Out/'staged-verification.json').write_text(json.dumps(Check,indent=2)+'\n')
print(json.dumps(Check))
