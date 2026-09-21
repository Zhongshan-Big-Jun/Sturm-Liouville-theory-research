"""Copy only the frozen local inputs and run bounded tests in fresh processes.

Entry: python -B regression/replay.py
Outputs: work/replay-<UTC>-<id>/. The original software-author tree is read-only
apart from this new output directory. No main-repository path is imported.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

Base=Path(__file__).resolve().parents[1]


def digest(P):
	return hashlib.sha256(P.read_bytes()).hexdigest()


def main():
	Parser=argparse.ArgumentParser()
	Parser.add_argument('--label',default='')
	Args=Parser.parse_args()
	Stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
	Run=Base/'work'/('replay-'+Stamp+'-'+uuid.uuid4().hex[:6])
	Run.mkdir(parents=True)
	SourceHashes={}
	for Folder in ('originals','candidates','regression','inputs'):
		shutil.copytree(Base/Folder,Run/Folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
		for P in sorted((Run/Folder).rglob('*')):
			if P.is_file(): SourceHashes[P.relative_to(Run).as_posix()]=digest(P)
	for Folder in ('results','receipts','work'):
		(Run/Folder).mkdir()
	(Run/'copy-manifest.json').write_text(json.dumps(SourceHashes,indent=2)+'\n',encoding='utf-8')
	Results=[]
	for P in sorted((Run/'originals').rglob('*.py'))+sorted((Run/'candidates').rglob('*.py')):
		compile(P.read_bytes(),str(P),'exec')
	Environment=os.environ.copy()
	Environment.update(PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',TMPDIR=str(Run/'work'),PYTHONUTF8='1')
	print('Replay directory: '+str(Run),flush=True)
	for Mode in ('normal','optimized'):
		Flags=['-B']+(['-O'] if Mode=='optimized' else [])
		for Tree,Expected in [('originals',1),('candidates',0)]:
			Name=Tree+'-'+Mode
			Argv=[sys.executable,'-B',str(Run/'regression'/'capture_run.py'),'--name',Name,'--timeout','180','--',sys.executable,*Flags,str(Run/'regression'/'regression.py'),'--tree',Tree,'--output','results/'+Name+'.json']
			Start=time.monotonic()
			Proc=subprocess.run(Argv,cwd=Run,env=Environment,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=200)
			(Run/'receipts'/(Name+'-launcher.stdout')).write_bytes(Proc.stdout)
			(Run/'receipts'/(Name+'-launcher.stderr')).write_bytes(Proc.stderr)
			Data=json.loads((Run/'results'/(Name+'.json')).read_text())
			Passed=Proc.returncode==Expected and Data['tests']==117 and Data['optimize']==int(Mode=='optimized') and not any(R['name'].endswith('/exception') for R in Data['checks'])
			if Tree=='candidates': Passed=Passed and Data['failed']==0
			else: Passed=Passed and Data['failed']>0
			Results.append(dict(name=Name,argv=Argv,exit_code=Proc.returncode,expected_exit=Expected,tests=Data['tests'],passed_checks=Data['passed'],failed_checks=Data['failed'],accepted=Passed,seconds=time.monotonic()-Start))
			print(json.dumps(Results[-1]),flush=True)
		# This CLI has exactly four n=1 points; no historical large-R/n scan.
		Name='op03-cli-'+Mode
		Argv=[sys.executable,'-B',str(Run/'regression'/'capture_run.py'),'--name',Name,'--cwd','candidates','--timeout','90','--',sys.executable,*Flags,'scripts/op03_gap_fh.py']
		Proc=subprocess.run(Argv,cwd=Run,env=Environment,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=100)
		(Run/'receipts'/(Name+'-launcher.stdout')).write_bytes(Proc.stdout)
		(Run/'receipts'/(Name+'-launcher.stderr')).write_bytes(Proc.stderr)
		Stdout=(Run/'receipts'/Name/'stdout.txt').read_text()
		Pairs=[(float(A),float(B)) for A,B in re.findall(r'dD/du_num=([+\-0-9.e]+)\s+2\(1-R\)f=([+\-0-9.e]+)',Stdout)]
		CliPassed=Proc.returncode==0 and len(Pairs)==4 and all(abs(A-B)<=max(.002,abs(A)*2e-4) for A,B in Pairs)
		Results.append(dict(name=Name,argv=Argv,exit_code=Proc.returncode,expected_exit=0,pairs=Pairs,accepted=CliPassed))
		print(json.dumps(Results[-1]),flush=True)
	FinalHashes={K:digest(Run/K) for K in SourceHashes}
	Unchanged=FinalHashes==SourceHashes
	Outside=[]
	for Mode in ('normal','optimized'):
		for Tree in ('originals','candidates'):
			Data=json.loads((Run/'results'/(Tree+'-'+Mode+'.json')).read_text())
			for Name,PathStr in Data['module_files'].items():
				if not Path(PathStr).resolve().is_relative_to(Run.resolve()): Outside.append((Name,PathStr))
	# Source parity is not inferred from a process return code.
	Normal=json.loads((Run/'results'/'candidates-normal.json').read_text())
	Optimized=json.loads((Run/'results'/'candidates-optimized.json').read_text())
	NamesAgree=[R['name'] for R in Normal['checks']]==[R['name'] for R in Optimized['checks']]
	Summary=dict(role='software author; independent review pending',label=Args.label,root=str(Run),python=sys.executable,runs=Results,compiled_python_files=34,inputs_unchanged=Unchanged,external_project_modules=Outside,normal_optimized_names_agree=NamesAgree,accepted=all(R['accepted'] for R in Results) and Unchanged and not Outside and NamesAgree)
	Summary['output_sha256']={P.relative_to(Run).as_posix():digest(P) for Folder in ('results','receipts') for P in sorted((Run/Folder).rglob('*')) if P.is_file()}
	(Run/'replay-summary.json').write_text(json.dumps(Summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
	print('AUTHOR REPLAY '+('PASS' if Summary['accepted'] else 'FAIL')+' '+str(Run/'replay-summary.json'),flush=True)
	return int(not Summary['accepted'])

if __name__=='__main__':
	sys.exit(main())
