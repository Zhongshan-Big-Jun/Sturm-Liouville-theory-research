from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

Out = Path('F:/tools/math-audit-round8-20260922')
Bin = Path('F:/tools/math-audit-round7-20260921/posix-native-probe/root/usr/bin')
Environment = dict(os.environ)
Environment['PATH'] = str(Bin)
Source = Path(sys.argv[1].replace('/mnt/f/', 'F:/', 1))
Before = hashlib.sha256(Source.read_bytes()).hexdigest()
Command = [str(Bin / 'python3.12.exe'), '-B', '-I', '-S', '-X', 'utf8', '-X', 'pycache_prefix=/mnt/f/tools/math-audit-round8-20260922/unused-pycache', *sys.argv[1:]]
Started = datetime.datetime.now(datetime.timezone.utc).isoformat()
Timer = time.monotonic()
Result = subprocess.run(Command, cwd=Out, env=Environment)
Record = dict(start_utc=Started, end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), seconds=time.monotonic()-Timer, command=Command, exit_code=Result.returncode, script_sha256_before=Before, script_sha256_after=hashlib.sha256(Source.read_bytes()).hexdigest(), executable_sha256=hashlib.sha256((Bin/'python3.12.exe').read_bytes()).hexdigest(), cwd=str(Out), path_override=str(Bin), scope='Actual coordinator library transaction using existing private POSIX runtime and original plugin sources. Not an independent mathematical verdict. No global configuration changes.')
with (Out/'native-operations.jsonl').open('ab') as Stream:
	Stream.write((json.dumps(Record,ensure_ascii=False)+'\n').encode())
raise SystemExit(Result.returncode)
