from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess,datetime,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/sl-literature-absorption-20260923');B=json.loads((O/'baseline.json').read_text());Report='reports/literature-absorption-20260923'
Allowed=set('''AGENTS.md
README.md
README_EN.md
research_map.md
docs/SL_fixed_n_supremum.tex
docs/SL_fixed_n_supremum.pdf
docs/PROJECT_UNDERSTANDING.md
docs/research-guide.md
state/RESUME.md
state/AGENTS_SESSION_LOG.md
tools/secular-chebyshev-jacobi-rootcount.md
tools/bloch-band.md
tools/README.md
index/tools.json
literature/maps/FRONTIER.md
literature/maps/PAPER_MAP.md
research/library/card-bindings/catalog.json
research/library/corrections-journal.json'''.splitlines())
def require(x,m):
	if not x:raise RuntimeError(m)
def sha(p):
	with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def read(n):return json.loads((O/(n+'.json')).read_text())
def protect():
	def one(item):
		n,h=item;require((R/n).is_file(),'Removed original '+n);return n,sha(R/n)!=h
	with ThreadPoolExecutor(max_workers=6) as pool: changed=[n for n,c in pool.map(one,B['tracked'].items()) if c]
	require(set(changed)<=Allowed,'Out of scope changed: '+str(set(changed)-Allowed))
	for n,h in B['untracked'].items():require((R/n).is_file() and sha(R/n)==h,'Original untracked changed '+n)
	for n in B['original_dirty']:require(sha(R/n)==B['tracked'][n],'Original dirty changed '+n)
	oldlean=[n for n in B['tracked'] if n.startswith('lean-proof/SL/') and n.endswith('.lean')]
	for n in oldlean:require(sha(R/n)==B['tracked'][n],'Old Lean changed '+n)
	# Git HEAD and exact staging are checked separately by stage() under the Linux Git runtime.
	d=dict(status='PASS',baseline_head=B['head'],original_tracked=len(B['tracked']),unchanged_original_tracked=len(B['tracked'])-len(changed),authorized_changed_tracked=changed,unchanged_original_untracked=len(B['untracked']),old_Lean_sources_preserved=len(oldlean),original_dirty_preserved=list(B['original_dirty']),canonical_and_old_immutable_evidence='Every original file outside the explicit active-file allowlist retains baseline SHA256, including all old canonical, frozen runs, versions, reviews and correction events.')
	save(O/'protection-result.json',d);print('Protection PASS',len(changed),'authorized changes;',len(oldlean),'old Lean sources preserved',flush=True)
def prepare():
	protection=read('protection-result');require(protection['status']=='PASS','Protection missing')
	paths=set(protection['authorized_changed_tracked'])
	for prefix in [Report,'research/artifacts/literature-absorption-20260923','research/library','literature/absorption-20260923']:
		for p in (R/prefix).rglob('*'):
			if not p.is_file():continue
			n=str(p.relative_to(R))
			if n in B['tracked'] or n in B['untracked']:continue
			require('__pycache__' not in p.parts and p.suffix!='.pyc','Unintended cache '+n)
			require(not(n.startswith('research/library/') and (p.name=='writer.lock' or p.name.startswith('.library-'))),'Unfinished library transaction '+n)
			require(p.stat().st_size<100_000_000,'Oversized artifact '+n);paths.add(n)
	for group in ['domains','approximation','interfaces']:
		for card in read(group+'-cards'):paths.add(card['location'])
	for name in read('checkpoint-files'):paths.add(name)
	require(not paths.intersection(B['untracked']),'Original untracked in staging scope')
	require(not paths.intersection(B['original_dirty']),'Original dirty in staging scope')
	manifest=Report+'/publication-manifest.json';paths.discard(manifest)
	rows=[dict(path=n,sha256=sha(R/n)) for n in sorted(paths)]
	save(R/manifest,dict(schema='literature-absorption-publication/v1',baseline_head=B['head'],scope='Exact authorized13-source absorption,11 scoped new cards, reviewed bibliography correction and immutable evidence only',self_exclusion=manifest,files=rows));paths.add(manifest)
	expected={n:sha(R/n) for n in sorted(paths)}
	save(O/'stage-paths.json',sorted(paths));save(O/'stage-expected-sha256.json',expected)
	current=git('ls-files','--others','--exclude-standard','-z').decode().rstrip('\0').split('\0')
	extra=[n for n in current if n and n not in paths and n not in B['untracked']]
	require(not extra,'Unassigned new paths '+str(extra));print('Exact publication candidate',len(paths),'files',flush=True)
def verify_objects(ref,expected):
	proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
	for n,h in expected.items():
		proc.stdin.write((ref+':'+n+'\n').encode());proc.stdin.flush();head=proc.stdout.readline().split();require(len(head)==3 and head[1]==b'blob','Invalid Git object '+n)
		left=int(head[2]);digest=hashlib.sha256()
		while left:
			chunk=proc.stdout.read(min(1048576,left));require(bool(chunk),'Unexpected object end');digest.update(chunk);left-=len(chunk)
		require(proc.stdout.read(1)==b'\n','Missing object delimiter');require(digest.hexdigest()==h,'Git conversion changed reviewed bytes '+n)
	proc.stdin.close();require(proc.stdout.read()==b'' and proc.wait()==0,'Object reader failed')
def stage():
	expected=read('stage-expected-sha256');paths=read('stage-paths');manifest=Report+'/publication-manifest.json';d=json.loads((R/manifest).read_text());bound={x['path']:x['sha256'] for x in d['files']}
	require(set(bound)|{manifest}==set(paths),'Manifest scope differs');require(all(expected[n]==h for n,h in bound.items()),'Manifest hash differs')
	require(not git('diff','--cached','--name-only','-z'),'Unexpected staged files')
	require(git('rev-parse','HEAD').decode().strip()==B['head'],'HEAD changed')
	for n in paths:require(sha(R/n)==expected[n],'Changed after freeze '+n)
	p=O/'pathspec.nul';p.write_bytes(b'\0'.join(n.encode() for n in paths)+b'\0')
	subprocess.run(['git','add','--force','--pathspec-from-file='+str(p),'--pathspec-file-nul'],cwd=R,check=True)
	staged=git('diff','--cached','--name-only','-z').decode().rstrip('\0').split('\0');require(set(staged)==set(paths),'Staged set differs');verify_objects('',expected)
	save(O/'staged-verification.json',dict(status='PASS',staged_paths=len(paths),actual_git_blobs_match_worktree_sha256=True,publication_manifest_matches_exact_staged_scope_and_bytes=True));print('Staged exact scope and byte verification PASS',len(paths),flush=True)
def delivery(local=False):
	expected=read('stage-expected-sha256');require(read('staged-verification')['status']=='PASS','Stage verification missing');require(read('final-document-check')['status']=='PASS','Final document verification missing')
	head=git('rev-parse','HEAD').decode().strip();require(git('rev-parse','HEAD^').decode().strip()==B['head'],'Unexpected commit parent')
	committed=git('diff-tree','--no-commit-id','--name-only','-r','-z','HEAD').decode().rstrip('\0').split('\0');require(set(committed)==set(expected),'Committed scope differs');require(not git('diff','--cached','--name-only','-z'),'Index still dirty');verify_objects(head,expected)
	for n,h in expected.items():require(sha(R/n)==h,'Current committed artifact differs '+n)
	require(git('status','--porcelain=v1','-z','--untracked-files=all').decode()==B['status_z'],'Post-commit state differs from original work')
	for n,h in B['untracked'].items():require(sha(R/n)==h,'Original untracked changed '+n)
	for n in B['original_dirty']:require(sha(R/n)==B['tracked'][n],'Original dirty changed '+n)
	def remote(name):
		value=git('ls-remote','--exit-code',name,'refs/heads/main').decode().strip().split();require(value==[head,'refs/heads/main'],'Remote differs '+name);return name,dict(branch=value[1],sha=value[0],verification='actual git ls-remote')
	remotes={}
	if not local:
		with ThreadPoolExecutor(max_workers=2) as pool:remotes=dict(pool.map(remote,['origin','fork']))
	d=dict(status='PASS',scope='LOCAL_COMMIT_ONLY' if local else 'DELIVERED_TO_BOTH_REMOTES',verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline_head=B['head'],commit=head,committed_paths=len(expected),remote_heads=remotes,actual_committed_blobs_and_worktree_match_manifest=True,post_commit_status_matches_original_exactly=True,original_untracked_preserved=len(B['untracked']),original_dirty_preserved=list(B['original_dirty']),plugin_source_changed=False,report=Report+'/REPORT.md',formalization_scope='No new Lean or complete formalization. Scoped independent analytic reviews and exact/computational replay of literature adaptations; existing formal artifacts preserved.')
	save(O/('LOCAL_COMMIT_VERIFICATION.json' if local else 'DELIVERY.json'),d);print(json.dumps(d,ensure_ascii=False,indent=2),flush=True)
mode=sys.argv[1]
if mode=='protect':protect()
elif mode=='prepare':prepare()
elif mode=='stage':stage()
elif mode=='local':delivery(True)
elif mode=='delivery':delivery(False)
else:raise ValueError(mode)
