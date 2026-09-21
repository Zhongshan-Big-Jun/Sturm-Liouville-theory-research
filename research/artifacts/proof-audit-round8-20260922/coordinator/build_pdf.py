from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import os

Root=Path('/mnt/f/LaTeX/BVE research')
Out=Path('/mnt/f/tools/math-audit-round8-20260922/pdf-build')
Helper='/mnt/c/Users/HuangZY/.codex/plugins/cache/openai-bundled/latex/0.2.7/scripts/compile_latex.py'
Name,Engine=sys.argv[1:3]
Source=Root/'docs'/(Name+'.tex')
Digest=hashlib.sha256(Source.read_bytes()).hexdigest()
Folder=Out/Name/(Digest[:12]+('-'+sys.argv[3] if len(sys.argv)>3 else ''))
Folder.mkdir(parents=True,exist_ok=False)
Args=[sys.executable,Helper,str(Source),'--compiler','texlive','--engine',Engine,'--output-directory',str(Folder),'--json']
Start=datetime.datetime.now(datetime.timezone.utc).isoformat()
Result=subprocess.run(Args,cwd=Root/'docs',text=True,capture_output=True)
(Folder/'driver.stdout.txt').write_text(Result.stdout)
(Folder/'driver.stderr.txt').write_text(Result.stderr)
Record={'argv':Args,'utc_start':Start,'exit_code':Result.returncode,'source':str(Source.relative_to(Root)),'source_sha256':Digest,'source_unchanged':Digest==hashlib.sha256(Source.read_bytes()).hexdigest(),'TEXINPUTS':os.environ.get('TEXINPUTS')}
Pdf=Folder/(Name+'.pdf')
if Result.returncode==0 and Pdf.is_file() and Record['source_unchanged']:
	Record['pdf_sha256']=hashlib.sha256(Pdf.read_bytes()).hexdigest()
	shutil.copyfile(Pdf,Root/'docs'/Pdf.name)
(Folder/'run.json').write_text(json.dumps(Record,indent=2)+'\n')
print(json.dumps(Record),flush=True)
if Result.returncode:
	print(Result.stdout[-4000:]);print(Result.stderr[-2000:])
raise SystemExit(Result.returncode if Result.returncode else (0 if Record.get('pdf_sha256') else 1))
