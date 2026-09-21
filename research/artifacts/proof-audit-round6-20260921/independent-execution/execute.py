"""Independent capture wrapper. It never edits the frozen input package."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
AUTHOR = OUT.parent / 'lean-author'
PROJECT = Path('/mnt/f/LaTeX/BVE research')

def now():
	return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(path):
	with Path(path).open('rb') as Handle:
		return hashlib.file_digest(Handle, 'sha256').hexdigest()

def write_json(path, value):
	Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def identities():
	Freeze = json.loads((AUTHOR / 'freeze.json').read_text())
	Rows = []
	for Group in ('files', 'runtime_and_tools'):
		for Name, Expected in Freeze[Group].items():
			Source = AUTHOR / Name if Group == 'files' else Path(Name)
			Actual = digest(Source) if Source.is_file() else None
			Rows.append(dict(group=Group, path=str(Source), expected_sha256=Expected, actual_sha256=Actual, passed=Actual == Expected))
	for Name in ('AuditRound5.lean', 'AuditRound6.lean'):
		Source = PROJECT / 'lean-proof/SL' / Name
		Snapshot = AUTHOR / 'snapshot/SL' / Name
		Expected = Freeze['files']['snapshot/SL/' + Name]
		Rows.append(dict(group='original_project_source', path=str(Source), snapshot=str(Snapshot), expected_sha256=Expected, actual_sha256=digest(Source), passed=digest(Source) == Expected == digest(Snapshot)))
	Rows.append(dict(group='freeze_original_source_binding', path=Freeze['original_source'], expected_sha256=Freeze['original_source_sha256'], actual_sha256=digest(Freeze['original_source']), passed=digest(Freeze['original_source']) == Freeze['original_source_sha256'] == Freeze['files']['snapshot/SL/AuditRound6.lean']))
	return dict(utc=now(), freeze_sha256=digest(AUTHOR / 'freeze.json'), checks=Rows, passed=all(Row['passed'] for Row in Rows), snapshot_files=sorted(str(P.relative_to(AUTHOR / 'snapshot')) for P in (AUTHOR / 'snapshot').rglob('*') if P.is_file()))

def preflight():
	assert os.environ.get('PYTHONDONTWRITEBYTECODE') == '1'
	assert not (OUT / 'replay').exists(), 'Replay output must be fresh; refusing reuse.'
	assert not (OUT / 'preflight.json').exists(), 'Preserve previous evidence; refusing overwrite.'
	Thread = os.environ.get('CODEX_THREAD_ID')
	assert Thread, 'A real CODEX_THREAD_ID is required.'
	Session = dict(schema_version=1, CODEX_THREAD_ID=Thread, identity_source='os.environ[CODEX_THREAD_ID] in this native session', role='independent_execution_verifier_not_author_not_final_semantic_approver', utc_started=now(), inherited_coordinator_history_used=False, other_review_sessions_read=False, author_verdicts_read=False, final_semantic_approval=False, negative_control_independently_run=False, python_dont_write_bytecode=os.environ.get('PYTHONDONTWRITEBYTECODE'), python_executable=sys.executable, work_root=str(PROJECT), output_root=str(OUT), replay_directory_previously_existed=False, fork_context_claim='Not independently attested; no fork metadata fabricated.')
	write_json(OUT / 'native-session.json', Session)
	Result = identities()
	write_json(OUT / 'preflight.json', Result)
	print(json.dumps(dict(phase='preflight', passed=Result['passed'], identity_checks=len(Result['checks']), freeze_sha256=Result['freeze_sha256'], CODEX_THREAD_ID=Thread), indent=2), flush=True)
	return 0 if Result['passed'] else 1

def replay():
	assert os.environ.get('PYTHONDONTWRITEBYTECODE') == '1'
	assert json.loads((OUT / 'preflight.json').read_text())['passed']
	assert not (OUT / 'replay').exists(), 'Replay output must be new.'
	assert not (OUT / 'replay-command.json').exists(), 'No automatic rerun.'
	Args = ['python3', '-B', str(AUTHOR / 'replay.py'), str(OUT / 'replay'), '--skip-negative-control']
	Record = dict(argv=Args, cwd=str(PROJECT), utc_start=now(), CODEX_THREAD_ID=os.environ['CODEX_THREAD_ID'], PYTHONDONTWRITEBYTECODE='1', attempts=1, replay_directory_existed_at_start=False)
	write_json(OUT / 'replay-command.json', Record)
	Start = time.monotonic()
	with (OUT / 'replay.stdout.txt').open('xb') as Stdout, (OUT / 'replay.stderr.txt').open('xb') as Stderr:
		Process = subprocess.Popen(Args, cwd=PROJECT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), stdout=Stdout, stderr=Stderr)
		Record['pid'] = Process.pid
		write_json(OUT / 'replay-command.json', Record)
		print(json.dumps(dict(phase='replay_started', pid=Process.pid, argv=Args)), flush=True)
		Record['exit_code'] = Process.wait()
	Record.update(utc_end=now(), duration_seconds=time.monotonic() - Start, stdout_sha256=digest(OUT / 'replay.stdout.txt'), stderr_sha256=digest(OUT / 'replay.stderr.txt'))
	write_json(OUT / 'replay-command.json', Record)
	print(json.dumps(Record, indent=2), flush=True)
	return Record['exit_code']

if __name__ == '__main__':
	sys.exit({'preflight': preflight, 'replay': replay}[sys.argv[1]]())
