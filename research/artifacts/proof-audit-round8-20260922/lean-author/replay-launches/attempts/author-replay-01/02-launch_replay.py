"""Retain the complete Python replay command, stdout/stderr, exit and source snapshot."""
from pathlib import Path
import sys
from run_lean import BASE, environment, run
label=sys.argv[1]
output=BASE/label
inputs=[BASE/n for n in ['replay.py','run_lean.py','launch_replay.py','freeze.json','runtime-config.json','AuditRound8.lean','positive-contract.json','ExporterPrefix.lean.txt','ExporterSuffix.lean.txt']]
r=run(BASE/'replay-launches',label,[sys.executable,'-B',str(BASE/'replay.py'),str(output)],environment(BASE/'replay-launches'),BASE,inputs)
sys.exit(r['exit_code'])
