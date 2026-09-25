from run import *

LABEL = 'exact-root-02'
while True:
	Manifest = BASE / 'evidence' / LABEL / 'run-manifest.json'
	Command = BASE / 'commands' / LABEL / 'command.json'
	Job = BASE / '.research-state/jobs' / (LABEL + '-durable.json')
	if Manifest.is_file() and Command.is_file() and Job.is_file():
		Record = json.loads(Command.read_text())
		JobRecord = json.loads(Job.read_text())
		if Record.get('exit_code') is not None and JobRecord.get('state') not in ['RUNNING', 'DISPATCHED']:
			break
	time.sleep(5)
print('Exact-root process ended:', Record.get('exit_code'), JobRecord.get('state'), flush=True)
if Record['exit_code'] != 0:
	print('Finalization withheld: inspect the recorded failed verifier output.', flush=True)
	sys.exit(Record['exit_code'])
with (BASE / 'finalization.log').open('wb') as Log:
	Result = subprocess.run([sys.executable, '-B', BASE / 'finalize.py'], cwd=BASE, stdout=Log, stderr=subprocess.STDOUT)
print('Finalization exit:', Result.returncode, flush=True)
print((BASE / 'finalization.log').read_text()[-10000:], flush=True)
sys.exit(Result.returncode)
