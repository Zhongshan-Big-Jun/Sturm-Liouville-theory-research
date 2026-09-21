from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round8-20260922')
Submitted = Path('/mnt/c/Users/HuangZY/Downloads/sl_audit_round8')

def git(*Args):
	return subprocess.check_output(['git', *Args], cwd=Root)

def digest(Path):
	with Path.open('rb') as Stream:
		return hashlib.file_digest(Stream, 'sha256').hexdigest()

if (Out / 'baseline.json').exists():
	raise RuntimeError('Baseline already exists; do not overwrite')
Head = git('rev-parse', 'HEAD').decode().strip()
if Head != 'd1462eb444938554b17da1db398763b31efb4ef4':
	raise RuntimeError('Unexpected baseline head: ' + Head)
Status = git('status', '--porcelain=v1', '-z', '--untracked-files=all').decode()
Tracked = git('ls-files', '-z').decode().rstrip('\0').split('\0')
Untracked = git('ls-files', '--others', '--exclude-standard', '-z').decode().rstrip('\0').split('\0')
Dirty = git('diff', '--name-only', '-z', 'HEAD').decode().rstrip('\0').split('\0')
if git('diff', '--cached', '--name-only', '-z'):
	raise RuntimeError('Preexisting staged files require separate preservation')
Intake = {}
for File in sorted(Submitted.rglob('*')):
	if not File.is_file():
		continue
	Relative = File.relative_to(Submitted)
	Target = Out / 'submitted' / Relative
	Target.parent.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(File, Target)
	Intake[str(Relative)] = {'sha256': digest(Target), 'size': Target.stat().st_size}
Sources = [
	'AGENTS.md', 'docs/SL_gap_n1_inf_limit_proof.tex',
	'tools/inf-limit-comparison.md', 'tools/gap-band-extremals.md',
	'scripts/op03_gap_inflimit.py', 'scripts/verify_inflimit.py',
]
Run = 'runs/rigorous-open-math-research/R-20260806T200000Z-inflimit-5B2C7D/reproducibility/'
Sources += [Run + Name for Name in ['05_interval_value.py', '16_certify_all_regions.py', '19_verify_lemma_A_doubleprime_chain.py']]
SourceInfo = {}
for Name in Sources:
	Target = Out / 'sources' / Name
	Target.parent.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(Root / Name, Target)
	Bytes = Target.read_bytes()
	SourceInfo[Name] = {'sha256': digest(Target), 'raw_git_blob_sha1': hashlib.sha1(b'blob ' + str(len(Bytes)).encode() + b'\0' + Bytes).hexdigest(), 'committed_blob': git('rev-parse', Head + ':' + Name).decode().strip()}
(Out / 'intake.json').write_text(json.dumps({'request': 'C:\\Users\\HuangZY\\Downloads\\sl_audit_round8 继续修订; math-research-workflow 2.0', 'source': str(Submitted), 'head': Head, 'files': Intake, 'sources': SourceInfo}, ensure_ascii=False, indent=2) + '\n')
print('Frozen author inputs and supplied audit copied; complete protection baseline in progress.', flush=True)
for Name in Dirty:
	Target = Out / 'original-dirty' / Name
	Target.parent.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(Root / Name, Target)
Baseline = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'head': Head, 'status_z': Status, 'tracked': {Name: digest(Root / Name) for Name in Tracked}, 'untracked': {Name: digest(Root / Name) for Name in Untracked if Name}, 'original_dirty': Dirty}
if Status != git('status', '--porcelain=v1', '-z', '--untracked-files=all').decode():
	raise RuntimeError('Worktree changed while recording baseline')
(Out / 'baseline.json').write_text(json.dumps(Baseline, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'head': Head, 'tracked': len(Baseline['tracked']), 'untracked': len(Baseline['untracked']), 'original_dirty': Dirty, 'audit_files': len(Intake)}, ensure_ascii=False), flush=True)
