from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import ast
import datetime
import hashlib
import json
import shutil
import subprocess

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Input = Path('/mnt/c/Users/HuangZY/Downloads/sl_audit_round12')
Artifact = Root / 'research/artifacts/proof-audit-round12-20260926'

def git(*Args):
	return subprocess.check_output(['git', *Args], cwd=Root)

def identity(Name):
	with (Root / Name).open('rb') as Stream:
		return Name, hashlib.file_digest(Stream, 'sha256').hexdigest()

def save(Path, Data):
	Path.parent.mkdir(parents=True, exist_ok=True)
	Path.write_text(json.dumps(Data, ensure_ascii=False, indent=2) + '\n')

if (Out / 'baseline.json').exists():
	raise RuntimeError('Baseline already captured')
Head = git('rev-parse', 'HEAD').decode().strip()
if Head != 'be7c0912849a50a46869773eab4b3a2ec655ce88':
	raise RuntimeError('Unexpected head ' + Head)
if git('diff', '--cached', '--name-only', '-z'):
	raise RuntimeError('Index is not initially empty')
Status = git('status', '--porcelain=v1', '-z', '--untracked-files=all').decode()
Tracked = [Name for Name in git('ls-files', '-z').decode().split('\0') if Name]
Untracked = [Name for Name in git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0') if Name]
Dirty = [Name for Name in git('diff', '--name-only', '-z').decode().split('\0') if Name]
with ThreadPoolExecutor(max_workers=6) as Pool:
	TrackedHashes = dict(Pool.map(identity, Tracked))
	UntrackedHashes = dict(Pool.map(identity, Untracked))
if git('rev-parse', 'HEAD').decode().strip() != Head:
	raise RuntimeError('HEAD changed during capture')
save(Out / 'baseline.json', dict(head=Head, captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), tracked=TrackedHashes, untracked=UntrackedHashes, original_dirty=Dirty, status_z=Status))
for Name in Dirty:
	Target = Out / 'original-dirty' / Name
	Target.parent.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(Root / Name, Target)
Manifest = json.loads((Input / 'MANIFEST.json').read_text())
for Name, Expected in Manifest.items():
	Source = (Input / Name).resolve()
	if not Source.is_relative_to(Input.resolve()) or hashlib.sha256(Source.read_bytes()).hexdigest() != Expected:
		raise RuntimeError('Untrusted or mismatched intake path ' + Name)
shutil.copytree(Input, Artifact / 'submitted')
shutil.copytree(Input, Out / 'submitted-replay')
SourceManifest = json.loads((Input / 'source_manifest.json').read_text())
Records = []
for Entry in SourceManifest['entries']:
	Name = Entry['upstream_path']
	Blob = git('rev-parse', 'HEAD:' + Name).decode().strip()
	Current = (Root / Name).read_bytes()
	ExpectedBytes = git('show', 'HEAD:' + Name)
	if Current != ExpectedBytes or Blob != Entry['upstream_blob_reported_by_connector']:
		raise RuntimeError('Whole source identity mismatch ' + Name)
	Tree = ast.parse(Current)
	ExcerptTree = ast.parse((Input / Entry['local_path']).read_bytes())
	ActualNodes = {Node.name: ast.dump(Node, include_attributes=False) for Node in Tree.body if isinstance(Node, ast.FunctionDef)}
	ExcerptNodes = {Node.name: ast.dump(Node, include_attributes=False) for Node in ExcerptTree.body if isinstance(Node, ast.FunctionDef)}
	Matches = {Name: ActualNodes.get(Name) == ExcerptNodes.get(Name) for Name in Entry['functions']}
	Records.append(dict(path=Name, git_blob=Blob, whole_file_sha256=hashlib.sha256(Current).hexdigest(), whole_current_matches_head=True, function_ast_matches=Matches))
for Name in ['scripts/_gapn2_jacobian_probe.py', 'scripts/_gapn2_half_problem_probe.py', 'scripts/_sl_prufer.py', 'tools/green-half-inertia.md', 'tools/half-problem-regularized-green.md']:
	Target = Artifact / 'before' / Name
	Target.parent.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(Root / Name, Target)
(Artifact / '.gitattributes').write_text('* -text\n')
save(Artifact / 'intake-verification.json', dict(status='PASS', original_manifest_entries=len(Manifest), intake_kind='User-supplied source excerpts; independently matched against whole current Git blobs and AST function bodies', sources=Records))
save(Out / 'CURRENT.json', dict(status='IN_PROGRESS', baseline=Head, stage='BASELINE_AND_INTAKE_VERIFIED', pending=['Native quarantine', 'Half-spectrum and pole identity repair', 'Analytic sector derivation', 'Isolated review and scoped Lean', 'Native releases and navigation', 'Origin then fork delivery'], running_cli=[]))
print(json.dumps(dict(tracked=len(Tracked), untracked=len(Untracked), dirty=Dirty, lean_sources=sum(Name.startswith('lean-proof/SL/') and Name.endswith('.lean') for Name in Tracked), intake=Records), ensure_ascii=False), flush=True)
