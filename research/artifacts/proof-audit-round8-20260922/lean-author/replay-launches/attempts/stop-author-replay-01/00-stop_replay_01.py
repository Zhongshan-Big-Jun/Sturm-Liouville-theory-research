from pathlib import Path
import json,os,signal,sys
b=Path(__file__).resolve().parent
p=json.loads((b/'author-replay-01/run-start.json').read_text())['pid']
cmd=(Path('/proc')/str(p)/'cmdline').read_bytes().split(b'\0')
expected=[str(Path(sys.executable).resolve()).encode(),b'-B',str(b/'replay.py').encode(),str(b/'author-replay-01').encode()]
if cmd[:4]!=expected: raise RuntimeError('PID command identity mismatch: '+repr(cmd[:4]))
children=(Path('/proc')/str(p)/'task'/str(p)/'children').read_text().strip()
if children: raise RuntimeError('Replay has active child processes; not terminating')
print('Terminating own replay PID',p,'during precompile inventory; exporter smoke already proved the frozen reporter is invalid.',flush=True)
os.kill(p,signal.SIGTERM)
