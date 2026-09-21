from pathlib import Path
import os,sys
from run_lean import OUT,LEAN,environment,run
SCRIPT=Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/lean-verify/2.0.0/scripts/verify_lean_project.py')
if __name__=='__main__':
	name,contract,folder=sys.argv[1:4]
	os.environ.update(environment())
	args=[sys.executable,str(SCRIPT),'--project',str(OUT/'verifier-project'),'--lean-files','SL/AuditRound5.lean','--contract',str(OUT/contract),'--lean',str(LEAN),'--lake',str(LEAN.parent/'lake.exe'),'--direct','--build-timeout','600','--strict-exit','--output',str(OUT/folder)]
	sys.exit(run(name,args,[OUT/'verifier-project/SL/AuditRound5.lean',OUT/contract,SCRIPT,Path(__file__)]))
