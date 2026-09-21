from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

Root=Path(__file__).resolve().parent
Plugin=Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/openai-bundled/latex/0.2.7')
Build=Root/'build'
Build.mkdir(exist_ok=True)
for Name in ['texmf-var','texmf-config']:
	(Build/Name).mkdir(exist_ok=True)
Env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TEXMFVAR=str(Build/'texmf-var'),TEXMFCONFIG=str(Build/'texmf-config'))
Command=[sys.executable,str(Plugin/'scripts/compile_latex.py'),str(Root/'fragment_check.tex'),'--compiler','texlive','--engine','pdflatex','--output-directory',str(Build),'--json']
Started=datetime.datetime.now(datetime.timezone.utc).isoformat()
Run=subprocess.run(Command,cwd=Plugin,env=Env,text=True,capture_output=True)
Out=Root/'logs/latex.stdout.json'
Err=Root/'logs/latex.stderr.txt'
Out.write_text(Run.stdout)
Err.write_text(Run.stderr)
Record={'command':Command,'cwd':str(Plugin),'started_utc':Started,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':Run.returncode,'source_hashes':{Name:hashlib.sha256((Root/Name).read_bytes()).hexdigest() for Name in ['fragment_check.tex','sliver_t1_fragment.tex']},'stdout':str(Out),'stdout_sha256':hashlib.sha256(Out.read_bytes()).hexdigest(),'stderr':str(Err),'stderr_sha256':hashlib.sha256(Err.read_bytes()).hexdigest(),'role':'author syntax/typesetting validation, not mathematical independent review'}
(Root/'logs/latex_receipt.json').write_text(json.dumps(Record,indent=2)+'\n')
print('LaTeX compiler wrapper exit:',Run.returncode)
print(Run.stdout[-2400:])
print(Run.stderr[-1500:])
sys.exit(Run.returncode)
