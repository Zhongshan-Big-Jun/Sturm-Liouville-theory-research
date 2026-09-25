from pathlib import Path
import subprocess,json,datetime,time,sys,hashlib
O=Path('/mnt/f/tools/math-audit-round10-20260925');R=Path('/mnt/f/LaTeX/BVE research')
Native=['/mnt/c/Users/HuangZY/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe','F:/tools/math-audit-round10-20260925/run_native_posix.py']
def run(Name,Args):
 P=O/(Name+'.log');Start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with P.open('wb') as F:Result=subprocess.run(Args,cwd=R,stdout=F,stderr=subprocess.STDOUT)
 Row=dict(name=Name,argv=list(map(str,Args)),started_utc=Start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=Result.returncode,log=str(P),log_sha256=hashlib.sha256(P.read_bytes()).hexdigest())
 with (O/'revision-pipeline.jsonl').open('a') as F:F.write(json.dumps(Row)+'\n')
 print(Name,Result.returncode,flush=True)
 if Result.returncode:raise RuntimeError('Stage failed; inspect '+str(P))
while True:
 Records=[json.loads(L) for L in (O/'native-operations.jsonl').read_text().splitlines()]
 End=[X for X in Records if X['command'][-2:]==[str(O/'release_current.py'),'renewals-only']]
 if End:
  if End[-1]['exit_code']!=0:raise RuntimeError('Original release transaction failed; no input changes made')
  break
 time.sleep(3)
if (R/'research/library/writer.lock').exists():raise RuntimeError('Unexpected active writer after completed transaction')
run('math-first-receive-serial',Native+[str(O/'review_ops.py'),'receive','math-review'])
run('apply-math-revision',[sys.executable,str(O/'apply_math_revision.py')])
run('pdf-math-revised',[sys.executable,str(O/'build_pdf.py'),'SL_gap_nge2_symmetry_recon','xelatex'])
run('refresh-math-bindings',Native+[str(O/'refresh_math_bindings.py')])
run('prepare-math-review-revised',Native+[str(O/'prepare_math_review_final.py')])
run('prepare-renewal-final',Native+[str(O/'prepare_renewal_final.py')])
print('Fresh mathematical and renewal packets ready; new agent dispatch required.',flush=True)
