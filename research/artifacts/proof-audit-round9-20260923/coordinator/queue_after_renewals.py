from pathlib import Path
import json,os,subprocess,time
O=Path('/mnt/f/tools/math-audit-round9-20260923');R=Path('/mnt/f/LaTeX/BVE research')
Pid=34428;Start=time.monotonic()
while Path('/proc/'+str(Pid)).exists():
	if time.monotonic()-Start>3600:raise RuntimeError('Renewal process has not finished; no concurrent writer started')
	time.sleep(1)
Rows=json.loads((O/'renewal-release-results.json').read_text())
if len(Rows)!=22:raise RuntimeError('Renewals incomplete; inspect actual job result')
Runtime='/mnt/c/Users/HuangZY/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
for Mode,Name in [('receive','software-review'),('receive','math-review2')]:
	Args=[Runtime,'-B','-I','-X','utf8','F:/tools/math-audit-round9-20260923/run_native_posix.py',str(O/'review_ops.py'),Mode,Name]
	Run=subprocess.run(Args,cwd=R)
	if Run.returncode:raise RuntimeError('Review operation failed: '+Mode+' '+Name)
print('Renewals finished; both actual completions received; formal review is in its separate scoped project.',flush=True)
