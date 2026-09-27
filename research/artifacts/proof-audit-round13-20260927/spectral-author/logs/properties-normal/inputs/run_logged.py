"""Run a command with immutable stdout/stderr, source snapshots, and exit metadata."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

Root = Path('/mnt/f/LaTeX/BVE research')
Own = Path(__file__).resolve().parent
Label = sys.argv[1]
Command = sys.argv[2:]
Target = Own / 'logs' / Label
Target.mkdir()
Inputs = Target / 'inputs'
Inputs.mkdir()
Hashes = {}
for Source in sorted((Own / 'baseline').glob('*.py')):
	Current = Root / 'scripts' / Source.name
	Data = Current.read_bytes()
	(Inputs / Source.name).write_bytes(Data)
	Hashes[str(Current)] = hashlib.sha256(Data).hexdigest()
for Source in sorted(Own.glob('*.py')):
	Data = Source.read_bytes()
	(Inputs / Source.name).write_bytes(Data)
	Hashes[str(Source)] = hashlib.sha256(Data).hexdigest()
Started = time.time()
Environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1')
with (Target / 'stdout.txt').open('w') as Out, (Target / 'stderr.txt').open('w') as Err:
	Result = subprocess.run(Command, cwd=Root, env=Environment, stdout=Out, stderr=Err)
Record = dict(command=Command, cwd=str(Root), returncode=Result.returncode,
	started_unix=Started, seconds=time.time()-Started, source_sha256=Hashes)
(Target / 'command.json').write_text(json.dumps(Record, indent=2)+'\n')
print(json.dumps({Key:Value for Key,Value in Record.items() if Key!='source_sha256'}, indent=2))
print((Target / 'stdout.txt').read_text()[-12000:])
print((Target / 'stderr.txt').read_text()[-4000:])
sys.exit(Result.returncode)
