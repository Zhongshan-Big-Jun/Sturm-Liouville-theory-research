"""Read-only v2 saved-receipt check with the exact recorded package search path."""
from pathlib import Path
import json, sys
import replay

Base = Path(__file__).resolve().parent
Output = Path(sys.argv[1]).resolve()
Config = json.loads((Base / 'runtime-config.json').read_text())
import os
Env = os.environ.copy()
Env['PYTHONDONTWRITEBYTECODE'] = '1'
Env['LEAN_PATH'] = ';'.join(replay.win(p) for p in Config['package_search_paths'])
Env['LEAN_SRC_PATH'] = ''
Env['WSLENV'] = ':'.join([v for v in Env.get('WSLENV', '').split(':') if v and v.split('/')[0] not in ('LEAN_PATH', 'LEAN_SRC_PATH')] + ['LEAN_PATH', 'LEAN_SRC_PATH'])
Checker = Path(Config['verifier']).parent / 'lean_evidence.py'
Result = replay.run(Output, '07-maintained-receipt-recheck', [sys.executable, '-B', str(Checker), '--manifest', str(Output / 'positive/run-manifest.json')], Env, Base / 'snapshot')
sys.exit(Result['exit_code'])
