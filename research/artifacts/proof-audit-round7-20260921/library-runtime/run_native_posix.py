from pathlib import Path
import os,subprocess,sys,json,hashlib,time,datetime
O=Path('F:/tools/math-audit-round7-20260921')
Bin=O/'posix-native-probe/root/usr/bin'
Environment=dict(os.environ)
Environment['PATH']=str(Bin)
Command=[str(Bin/'python3.12.exe'),'-B','-I','-S','-X','utf8','-X','pycache_prefix=/mnt/f/tools/math-audit-round7-20260921/posix-native-probe/unused-pycache',*sys.argv[1:]]
Started=datetime.datetime.now(datetime.timezone.utc).isoformat();Timer=time.monotonic()
Source=Path(sys.argv[1].replace('/mnt/f/','F:/',1))
Before=hashlib.sha256(Source.read_bytes()).hexdigest()
Result=subprocess.run(Command,cwd=O,env=Environment)
Record=dict(start_utc=Started,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 seconds=time.monotonic()-Timer,command=Command,exit_code=Result.returncode,
 script_sha256_before=Before,script_sha256_after=hashlib.sha256(Source.read_bytes()).hexdigest(),
 cwd=str(O),path_override=str(Bin),python_flags='-B -I -S -X utf8; private unused pycache prefix',
 scope='Actual coordinator library/helper execution. Not a new independent mathematical verdict.')
with (O/'posix-native-probe/native-operations.jsonl').open('ab') as Handle:Handle.write((json.dumps(Record,ensure_ascii=False)+'\n').encode())
raise SystemExit(Result.returncode)
