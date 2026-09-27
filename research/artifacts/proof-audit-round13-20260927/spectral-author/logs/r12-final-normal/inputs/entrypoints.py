"""Actual representative CLI execution; no output-writing scan main is invoked."""
import json
from pathlib import Path
import subprocess
import sys

Own=Path(__file__).resolve().parent
Root=Path('/mnt/f/LaTeX/BVE research')
Commands=[
	('r12-normal',['python3',str(Own/'r12_regression.py'),str(Root)]),
	('r12-optimized',['python3','-O',str(Own/'r12_regression.py'),str(Root)]),
	('analytic-cli',['python3','scripts/_gapn2_jacobian_analytic.py','2','4','both']),
	('spectral-cli',['python3','scripts/_gapn2_jacobian_spectral.py','2','4','both','640']),
	('half-sup-cli',['python3','scripts/_gapn2_half_problem_probe.py','4','sup','160']),
	('half-inf-cli',['python3','scripts/_gapn2_half_problem_probe.py','4','inf','160']),
	('physical-fd-cli',['python3','scripts/_gapn2_jacobian_probe.py','4','2','both']),
]
Results=[]
for Label,Command in Commands:
	Result=subprocess.run(['python3',str(Own/'run_logged.py'),Label,*Command],cwd=Root,text=True,capture_output=True)
	print(Result.stdout,flush=True)
	print(Result.stderr,flush=True)
	Results.append(dict(label=Label,returncode=Result.returncode,command=Command))
	if Result.returncode:
		(Own/'entrypoints_summary.json').write_text(json.dumps(Results,indent=2)+'\n')
		sys.exit(Result.returncode)
(Own/'entrypoints_summary.json').write_text(json.dumps(Results,indent=2)+'\n')
