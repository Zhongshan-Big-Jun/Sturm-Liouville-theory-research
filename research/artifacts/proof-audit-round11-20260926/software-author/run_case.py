from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round11-20260926')
Name=sys.argv[1];D=O/'replays'/Name;D.mkdir(parents=True,exist_ok=False)
Sources=['_gapn2_symmetry_recon.py','_sl_prufer.py','reflection_seeds.py','_gapn2_second_variation_probe.py','_gapn2_jacobian_probe.py','_gapn2_jacobian_analytic.py','_gapn2_jacobian_spectral.py','_gapn2_o3_scan.py','op03_gap_table.json']
Before={N:hashlib.sha256((R/'scripts'/N).read_bytes()).hexdigest() for N in Sources}
if Name=='jacobian-cli':Args=[sys.executable,'-B',str(R/'scripts/_gapn2_jacobian_probe.py'),'1,4','2','both']
elif Name in ('o3-cli','o3-cli-final'):Args=[sys.executable,'-B',str(R/'scripts/_gapn2_o3_scan.py'),'2,3','4','both','80']
else:
	Mode={'probe-n2R4SUP':'sup','probe-n2R4INF':'inf'}[Name]
	Args=[sys.executable,'-B',str(R/'scripts/_gapn2_second_variation_probe.py'),'2','4',Mode,'--output',str(D/'result.json')]
Record=dict(name=Name,argv=Args,cwd=str(R),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_before=Before,status='RUNNING',scope='coordinator actual finite numerical execution; not independent acceptance or interval certification')
def save(): (D/'execution.json').write_text(json.dumps(Record,indent=2)+'\n')
save(); Timer=time.monotonic();Environment=dict(os.environ);Environment['PYTHONDONTWRITEBYTECODE']='1';Environment['OPENBLAS_NUM_THREADS']='1'
with (D/'stdout.log').open('wb') as Out,(D/'stderr.log').open('wb') as Err:
	Process=subprocess.Popen(Args,cwd=R,env=Environment,stdout=Out,stderr=Err)
	Record['pid']=Process.pid;save();Exit=Process.wait()
After={N:hashlib.sha256((R/'scripts'/N).read_bytes()).hexdigest() for N in Sources}
Record.update(ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-Timer,exit_code=Exit,source_after=After,source_unchanged=Before==After,status='COMPLETED' if Exit==0 and Before==After else 'FAILED');save()
print(json.dumps({K:Record[K] for K in ['name','status','exit_code','seconds','source_unchanged']}),flush=True)
raise SystemExit(Exit or (0 if Before==After else 1))
