#!/usr/bin/env python3
"""Run the author's exact check and preserve actual process output."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

Root = Path('/mnt/f/tools/math-audit-round11-20260926/cofinite-author')
Script = Root / 'checks/exact_algebra.py'
Started = datetime.datetime.now(datetime.timezone.utc)
RunName = 'algebra-' + Started.strftime('%Y%m%dT%H%M%S%fZ')
Env = os.environ.copy()
Env['PYTHONDONTWRITEBYTECODE'] = '1'
Env['TMPDIR'] = str(Root / 'logs')
Command = [sys.executable, '-B', str(Script)]
Result = subprocess.run(Command, cwd=Root, env=Env, capture_output=True)
StdoutPath = Root / 'logs' / (RunName + '.stdout.json')
StderrPath = Root / 'logs' / (RunName + '.stderr.txt')
StdoutPath.write_bytes(Result.stdout)
StderrPath.write_bytes(Result.stderr)
Ended = datetime.datetime.now(datetime.timezone.utc)
Manifest = {
	'role': 'AUTHOR_SELF_CHECK_NOT_INDEPENDENT_ACCEPTANCE',
	'started_at_utc': Started.isoformat(), 'ended_at_utc': Ended.isoformat(),
	'elapsed_seconds': (Ended - Started).total_seconds(),
	'command': Command, 'cwd': str(Root),
	'environment_overrides': {'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': Env['TMPDIR']},
	'script_sha256': hashlib.sha256(Script.read_bytes()).hexdigest(),
	'returncode': Result.returncode,
	'stdout': {'path': str(StdoutPath), 'sha256': hashlib.sha256(Result.stdout).hexdigest()},
	'stderr': {'path': str(StderrPath), 'sha256': hashlib.sha256(Result.stderr).hexdigest()},
}
ManifestPath = Root / 'logs' / (RunName + '.execution.json')
ManifestPath.write_text(json.dumps(Manifest, indent=2) + '\n')
if Result.returncode == 0:
	Data = json.loads(Result.stdout)
	print(json.dumps({'execution_manifest': str(ManifestPath), 'returncode': 0,
		'total_checks': Data['total_checks'], 'category_counts': Data['category_counts']}, indent=2))
else:
	print(json.dumps({'execution_manifest': str(ManifestPath), 'returncode': Result.returncode,
		'stderr': Result.stderr.decode(errors='replace')}, indent=2))
sys.exit(Result.returncode)
