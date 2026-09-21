"""Run an argv without shell; bind inputs, raw streams and exit status."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

Base = Path(__file__).resolve().parents[1]

def digest(PathIn):
	return hashlib.sha256(PathIn.read_bytes()).hexdigest()

def main():
	Parser = argparse.ArgumentParser()
	Parser.add_argument('--name', required=True)
	Parser.add_argument('--cwd', default='.')
	Parser.add_argument('--timeout', type=float, default=180)
	Parser.add_argument('argv', nargs=argparse.REMAINDER)
	Args = Parser.parse_args()
	Argv = Args.argv[1:] if Args.argv[:1] == ['--'] else Args.argv
	Out = Base / 'receipts' / Args.name
	Out.mkdir(parents=True, exist_ok=False)
	Inputs = {}
	for Folder in ('originals','candidates','inputs','regression'):
		for P in sorted((Base / Folder).rglob('*')):
			if P.is_file() and '__pycache__' not in P.parts:
				Inputs[P.relative_to(Base).as_posix()] = digest(P)
	Cwd = (Base / Args.cwd).resolve()
	if not Cwd.is_relative_to(Base):
		raise RuntimeError('cwd must stay inside this author directory')
	Environment = os.environ.copy()
	Environment.update(PYTHONDONTWRITEBYTECODE='1', MPLCONFIGDIR=str(Base/'work'), OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', TMPDIR=str(Base/'work'), PYTHONUTF8='1')
	Start = datetime.datetime.now(datetime.timezone.utc).isoformat()
	Clock = time.monotonic()
	TimedOut = False
	with (Out/'stdout.txt').open('wb') as Stdout, (Out/'stderr.txt').open('wb') as Stderr:
		try:
			Proc = subprocess.run(Argv, cwd=Cwd, env=Environment, stdout=Stdout, stderr=Stderr, timeout=Args.timeout)
			ExitCode = Proc.returncode
		except subprocess.TimeoutExpired:
			ExitCode = 124
			TimedOut = True
	Receipt = dict(argv=Argv,cwd=str(Cwd),started_utc=Start,seconds=time.monotonic()-Clock,exit_code=ExitCode,timed_out=TimedOut,input_sha256=Inputs,stdout_sha256=digest(Out/'stdout.txt'),stderr_sha256=digest(Out/'stderr.txt'))
	(Out/'receipt.json').write_text(json.dumps(Receipt,indent=2)+'\n',encoding='utf-8')
	print(json.dumps({K:Receipt[K] for K in ('argv','cwd','seconds','exit_code','timed_out')},ensure_ascii=False))
	print((Out/'stdout.txt').read_text(encoding='utf-8',errors='replace'))
	print((Out/'stderr.txt').read_text(encoding='utf-8',errors='replace'),file=sys.stderr)
	return ExitCode

if __name__ == '__main__':
	sys.exit(main())
