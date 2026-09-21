#!/usr/bin/env python3
from pathlib import Path
import json,os,subprocess
from executor import BASE,RUN,pointer,save,run
config=json.loads((BASE/'lean-package/runtime-config.json').read_text())
m=json.loads((RUN/'replay/positive/run-manifest.json').read_text())
library=Path(m['evidence']['run_directory'])/'lib'
win=lambda p:subprocess.check_output(['wslpath','-w',str(p)],cwd=BASE,text=True).strip()
tmp=RUN/'tmp';tmp.mkdir(exist_ok=True)
os.environ.update(LEAN_PATH=win(library)+';'+config['LEAN_PATH'],LEAN_SRC_PATH='',TEMP=win(tmp),TMP=win(tmp),TMPDIR=str(tmp),PYTHONDONTWRITEBYTECODE='1')
os.environ['WSLENV']=':'.join([v for v in os.environ.get('WSLENV','').split(':') if v and v.split('/')[0] not in ('LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP')]+['LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP'])
code=run('supplemental-import-resolution',[config['lean'],'--deps',win(RUN/'replay/PositiveControl.lean')])
save(RUN/'independent-root-artifact.json',{'source':pointer(BASE/'lean-package/snapshot/SL/AuditRound7.lean'),'olean':pointer(library/'SL/AuditRound7.olean'),'probe':pointer(RUN/'AllModuleDeclarations.lean'),'positive_control':pointer(RUN/'replay/PositiveControl.lean'),'driver':pointer(__file__),'resolution':pointer(RUN/'executor-logs/supplemental-import-resolution.stdout.log'),'environment':{k:os.environ[k] for k in ('LEAN_PATH','LEAN_SRC_PATH','WSLENV','TEMP','TMP')}})
raise SystemExit(code)
