from pathlib import Path
import datetime,hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent;Old=D.parent/'software-author';P=D/'_gapn2_second_variation_probe.py';Results=[]
for Name,N,R,Mode in [('n2R4SUP',2,4,'sup'),('n3R4SUP',3,4,'sup'),('n2R10SUP',2,10,'sup'),('n2R4INF',2,4,'inf')]:
	Args=[sys.executable,'-B',str(P),str(N),str(R),Mode,'--output',str(D/(Name+'.json'))]
	Start=datetime.datetime.now(datetime.timezone.utc).isoformat()
	with (D/(Name+'.log')).open('wb') as F,(D/(Name+'.stderr.log')).open('wb') as E:Run=subprocess.run(Args,cwd=D,stdout=F,stderr=E)
	Row=dict(case=Name,argv=Args,cwd=str(D),start=Start,end=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=Run.returncode)
	if Run.returncode==0:
		A=json.loads((D/(Name+'.json')).read_text());B=json.loads((Old/(Name+'.json')).read_text());A.pop('source_sha256');B.pop('source_sha256')
		Row.update(all_numerical_data_unchanged=A==B,log_unchanged=(D/(Name+'.log')).read_bytes()==(Old/(Name+'.log')).read_bytes())
	Results.append(Row);(D/'default-replays.json').write_text(json.dumps(Results,indent=2)+'\n');print(Name,Row,flush=True)
	if Run.returncode!=0 or not Row['all_numerical_data_unchanged'] or not Row['log_unchanged']:sys.exit(2)
