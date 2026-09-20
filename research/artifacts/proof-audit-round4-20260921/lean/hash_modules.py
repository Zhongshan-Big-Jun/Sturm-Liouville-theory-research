from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import re
import time

OUT = Path('/mnt/f/tools/math-audit-round4-20260921/lean-author')


def wsl_path(Value):
	Value = Value.replace('\\', '/')
	Match = re.match(r'^([A-Za-z]):/(.*)$', Value)
	if not Match:
		raise ValueError('Expected absolute Windows module path: ' + Value)
	return Path('/mnt/' + Match[1].lower() + '/' + Match[2]).resolve()


def hash_one(Module):
	Main = wsl_path(Module['olean'])
	if not Main.is_file():
		raise FileNotFoundError(Main)
	Paths = [Main, Path(str(Main) + '.private'), Path(str(Main) + '.server'), Main.with_suffix('.ir')]
	Records = []
	for P in Paths:
		if not P.is_file():
			continue
		Before = P.stat()
		with P.open('rb') as Handle:
			Digest = hashlib.file_digest(Handle, 'sha256').hexdigest()
		After = P.stat()
		if (Before.st_size, Before.st_mtime_ns, Before.st_ctime_ns) != (After.st_size, After.st_mtime_ns, After.st_ctime_ns):
			raise RuntimeError('Artifact changed while hashing: ' + str(P))
		Records.append({'path': str(P), 'sha256': Digest, 'bytes': After.st_size,
			'mtime_ns': After.st_mtime_ns, 'ctime_ns': After.st_ctime_ns})
	return {'module': Module['module'], 'resolved_olean': str(Main), 'artifacts': Records}


if __name__ == '__main__':
	Destination = OUT / 'final/module-artifact-hashes.json'
	if Destination.exists():
		raise SystemExit('Refusing to overwrite final module inventory.')
	Loaded = json.loads((OUT / 'final/loaded-modules.json').read_text())
	Modules = Loaded['modules']
	assert len(Modules) == Loaded['module_count'] == len({M['module'] for M in Modules})
	Root = [M for M in Modules if M['module'] == 'SL.AuditRound4']
	assert len(Root) == 1 and wsl_path(Root[0]['olean']) == OUT / 'final/build/SL/AuditRound4.olean'
	Start = time.monotonic()
	Records = []
	print('Hashing actual loaded modules:', len(Modules), flush=True)
	with concurrent.futures.ThreadPoolExecutor(max_workers=8) as Pool:
		for Record in Pool.map(hash_one, Modules):
			Records.append(Record)
			if len(Records) % 500 == 0:
				print('Hashed modules:', len(Records), flush=True)
	Result = {'scope': 'Actual inspection loaded modules; olean and available private/server/IR companions',
		'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
		'duration_seconds': time.monotonic() - Start, 'module_count': len(Records),
		'artifact_count': sum(len(R['artifacts']) for R in Records),
		'bytes': sum(A['bytes'] for R in Records for A in R['artifacts']), 'modules': Records}
	Destination.write_text(json.dumps(Result, ensure_ascii=False, indent=2) + '\n')
	print('Completed:', Result['module_count'], 'modules,', Result['artifact_count'], 'artifacts,',
		round(Result['duration_seconds'], 2), 'seconds', flush=True)
