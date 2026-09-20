from pathlib import Path
import sys
from run_lean import run, BIN, OUT, PROJECT, win_path
name, filename = sys.argv[1:3]
p = OUT / filename
sources = [p, PROJECT / 'SL/AuditRound2.lean']
if filename == 'BridgeToExistingSL.lean':
	sources += [PROJECT / 'SL' / s for s in ['Basic.lean','ThirdOrder.lean','ThirdOrderClosedForms.lean','BalancedPhase.lean']]
sys.exit(run(name, [str(BIN / 'lean.exe'), win_path(p)], sources))
