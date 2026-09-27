from pathlib import Path
import datetime,hashlib,json,subprocess,time
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927');Results=[]
for Mode,Flag in [('normal',[]),('optimized',['-O'])]:
 for Name,Args in [('receiver',['misc/e1_cert_receive.py']),('tables',['misc/e1_cert_tables.py','--output',str(O/('tables-'+Mode+'.tex'))]),('properties',['scripts/test_round13_certificates.py'])]:
  Cmd=['python3',*Flag,'-B',*Args];Start=time.monotonic();Stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
  with (O/(Name+'-'+Mode+'.stdout')).open('w') as Out,(O/(Name+'-'+Mode+'.stderr')).open('w') as Err:P=subprocess.run(Cmd,cwd=R,stdout=Out,stderr=Err)
  Row=dict(mode=Mode,name=Name,argv=Cmd,exit_code=P.returncode,seconds=time.monotonic()-Start,start_utc=Stamp);Results.append(Row)
  (O/'certificate-checks.json').write_text(json.dumps(Results,indent=2)+'\n');print(json.dumps(Row),flush=True)
print('finished',flush=True)
raise SystemExit(0 if all(r['exit_code']==0 for r in Results) else 1)
