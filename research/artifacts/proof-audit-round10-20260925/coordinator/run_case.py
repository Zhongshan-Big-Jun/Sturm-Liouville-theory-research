from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925')
Name=sys.argv[1];D=O/'replays'/Name;D.mkdir(parents=True,exist_ok=False)
Sources=['_gapn2_symmetry_recon.py','_sl_prufer.py','reflection_seeds.py','_gapn2_second_variation_probe.py','_gapn2_jacobian_probe.py','_gapn2_jacobian_analytic.py','op03_gap_table.json']
Before={N:hashlib.sha256((R/'scripts'/N).read_bytes()).hexdigest() for N in Sources}
if Name=='recon-n2R4':
	Args=[sys.executable,'-B',str(R/'scripts/_gapn2_symmetry_recon.py'),'2','4','16','both','4','--output-dir',str(D)]
else:
	N,Rho,Mode={'probe-n2R4SUP':(2,4,'sup'),'probe-n2R4INF':(2,4,'inf'),'probe-n3R4SUP':(3,4,'sup'),'probe-n1R1SUP':(1,1,'sup')}[Name]
	Args=[sys.executable,'-B',str(R/'scripts/_gapn2_second_variation_probe.py'),str(N),str(Rho),Mode,'--output',str(D/'result.json')]
Started=datetime.datetime.now(datetime.timezone.utc).isoformat();Timer=time.monotonic()
Environment=dict(os.environ);Environment['PYTHONDONTWRITEBYTECODE']='1';Environment['OPENBLAS_NUM_THREADS']='1'
with (D/'stdout.log').open('wb') as Out,(D/'stderr.log').open('wb') as Err:
	Result=subprocess.run(Args,cwd=R,env=Environment,stdout=Out,stderr=Err)
After={N:hashlib.sha256((R/'scripts'/N).read_bytes()).hexdigest() for N in Sources}
Record=dict(name=Name,argv=Args,cwd=str(R),started_utc=Started,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-Timer,exit_code=Result.returncode,source_before=Before,source_after=After,source_unchanged=Before==After,scope='actual coordinator finite numerical execution; not independent acceptance or interval certification')
(D/'execution.json').write_text(json.dumps(Record,indent=2)+'\n')
print(json.dumps(dict(name=Name,exit_code=Result.returncode,seconds=Record['seconds'],source_unchanged=Before==After)),flush=True)
raise SystemExit(Result.returncode or (0 if Before==After else 1))
