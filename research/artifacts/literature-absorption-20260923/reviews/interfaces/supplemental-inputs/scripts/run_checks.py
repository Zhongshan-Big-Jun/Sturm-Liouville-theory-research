"""Retain the actual subprocess result, including failures, under this write area."""
from pathlib import Path
import subprocess,datetime,json,hashlib,sys,time
Root=Path(__file__).resolve().parents[1]
Stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
Out=Root/'evidence'/('run-'+Stamp)
Out.mkdir()
Command=[sys.executable,'-B',str(Root/'scripts/check_calibrations.py')]
Started=datetime.datetime.now(datetime.timezone.utc).isoformat()
Start=time.monotonic()
Result=subprocess.run(Command,cwd=Root,capture_output=True)
(Out/'stdout.json').write_bytes(Result.stdout)
(Out/'stderr.log').write_bytes(Result.stderr)
Record={'started_utc':Started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-Start,'argv':Command,'cwd':str(Root),'exit_code':Result.returncode,'author_script_sha256':hashlib.sha256((Root/'scripts/check_calibrations.py').read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256(Result.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(Result.stderr).hexdigest()}
(Out/'execution.json').write_text(json.dumps(Record,indent=2))
print(json.dumps({'run':str(Out),'exit_code':Result.returncode,'elapsed_seconds':Record['elapsed_seconds']}))
if Result.stdout:
 try:
  Data=json.loads(Result.stdout)
  print(json.dumps({'status':Data['status'],'check_count':Data['check_count'],'failures':[C for C in Data['checks'] if not C['passed']]}))
 except Exception:
  print(Result.stdout.decode()[-1500:])
if Result.stderr:
 print(Result.stderr.decode()[-1500:])
sys.exit(Result.returncode)
