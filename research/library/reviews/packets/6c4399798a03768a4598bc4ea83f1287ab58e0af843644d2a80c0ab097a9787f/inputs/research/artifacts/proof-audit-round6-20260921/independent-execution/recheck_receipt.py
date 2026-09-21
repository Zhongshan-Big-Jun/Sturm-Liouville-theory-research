"""Recheck this session's receipt and live import resolution; never replay proofs."""
from pathlib import Path
import json
import os
import subprocess
import sys
import time
from execute import OUT, AUTHOR, PROJECT, now, digest, write_json

def main():
	assert os.environ.get('PYTHONDONTWRITEBYTECODE') == '1'
	assert json.loads((OUT / 'replay/command-logs/02-maintained-positive.json').read_text())['exit_code'] == 0
	ManifestPath = OUT / 'replay/positive/run-manifest.json'
	Manifest = json.loads(ManifestPath.read_text())
	Config = json.loads((AUTHOR / 'runtime-config.json').read_text())
	Checker = Path(Config['verifier']).parent / 'lean_evidence.py'
	Env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', LEAN_PATH=Manifest['environment']['inherited_lean_path'], LEAN_SRC_PATH=Manifest['environment']['inherited_lean_src_path'])
	Env['WSLENV'] = ':'.join([Part for Part in Env.get('WSLENV', '').split(':') if Part and Part.split('/')[0] not in ('LEAN_PATH', 'LEAN_SRC_PATH')] + ['LEAN_PATH', 'LEAN_SRC_PATH'])
	Args = ['python3', '-B', str(Checker), '--manifest', str(ManifestPath)]
	Record = dict(argv=Args, cwd=str(PROJECT), utc_start=now(), PYTHONDONTWRITEBYTECODE='1', LEAN_PATH=Env['LEAN_PATH'], LEAN_SRC_PATH=Env['LEAN_SRC_PATH'], proof_replay=False, purpose='Rehash saved evidence and resolve every loaded import in the current runtime search context.')
	assert not (OUT / 'receipt-command.json').exists(), 'No automatic recheck rerun.'
	write_json(OUT / 'receipt-command.json', Record)
	Start = time.monotonic()
	with (OUT / 'receipt.stdout.txt').open('xb') as Stdout, (OUT / 'receipt.stderr.txt').open('xb') as Stderr:
		Process = subprocess.Popen(Args, cwd=PROJECT, env=Env, stdout=Stdout, stderr=Stderr)
		Record['pid'] = Process.pid
		write_json(OUT / 'receipt-command.json', Record)
		print(json.dumps(dict(phase='receipt_recheck_started', pid=Process.pid, proof_replay=False)), flush=True)
		Record['exit_code'] = Process.wait()
	Record.update(utc_end=now(), duration_seconds=time.monotonic()-Start, stdout_sha256=digest(OUT / 'receipt.stdout.txt'), stderr_sha256=digest(OUT / 'receipt.stderr.txt'))
	write_json(OUT / 'receipt-command.json', Record)
	print(json.dumps(Record, indent=2), flush=True)
	return Record['exit_code']

if __name__ == '__main__':
	sys.exit(main())
