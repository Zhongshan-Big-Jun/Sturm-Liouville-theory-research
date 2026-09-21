"""Save real process outputs, hashes and exit codes inside this author directory."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

Root = Path(__file__).resolve().parent
LogDir = Root/'logs'
LogDir.mkdir(exist_ok=True)
Env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
Receipts = []
for Script in ['exact_checks.py','explore.py']:
	Start = datetime.datetime.now(datetime.timezone.utc).isoformat()
	Command = [sys.executable, str(Root/Script)]
	Run = subprocess.run(Command, cwd=Root, env=Env, text=True, capture_output=True)
	Out = LogDir/(Script+'.stdout.json')
	Err = LogDir/(Script+'.stderr.txt')
	Out.write_text(Run.stdout)
	Err.write_text(Run.stderr)
	Receipt = {'command':Command,'cwd':str(Root),'started_utc':Start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':Run.returncode,'script_sha256':hashlib.sha256((Root/Script).read_bytes()).hexdigest(),'stdout':str(Out),'stdout_sha256':hashlib.sha256(Out.read_bytes()).hexdigest(),'stderr':str(Err),'stderr_sha256':hashlib.sha256(Err.read_bytes()).hexdigest()}
	Receipts.append(Receipt)
	print(Script+': exit '+str(Run.returncode), flush=True)
	if Run.returncode != 0:
		print(Run.stderr, flush=True)
(LogDir/'execution_receipts.json').write_text(json.dumps({'role':'author self-checks, no independent verdict','executions':Receipts},indent=2)+'\n')
if any(Receipt['exit_code']!=0 for Receipt in Receipts):
	sys.exit(1)
