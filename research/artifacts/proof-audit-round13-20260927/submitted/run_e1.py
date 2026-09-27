"""Replay the recovered E1 driver in isolated directories, including one false obligation."""
import sys, json, shutil, subprocess, hashlib, difflib, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MODE='optimized' if not __debug__ else 'normal'
rows=[]
source=(ROOT/'source_excerpts/zz_verify_e1_dec.py').read_text(encoding='utf-8')
for case in ('unmodified_logic','negative_control'):
    wd=ROOT/'work'/f'e1_{MODE}_{case}'
    (wd/'misc').mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT/'source_excerpts/rigid_dec.py',wd/'misc/rigid_dec.py')
    text=source
    if case=='negative_control':
        before="lb(lambda g: comps(g)['B1'], D('0.85'), '1/200')"
        after="lb(lambda g: comps(g)['B1'], D('0.85'), '100')"
        if text.count(before)!=1: raise RuntimeError('mutation anchor not unique')
        text=text.replace(before,after)
        (ROOT/'evidence/e1_negative_control.patch').write_text(''.join(difflib.unified_diff(source.splitlines(True),text.splitlines(True),fromfile='recovered_driver.py',tofile='negative_control.py')))
    (wd/'misc/zz_verify_e1_dec.py').write_text(text,encoding='utf-8')
    cmd=[sys.executable]+(['-O'] if not __debug__ else [])+['misc/zz_verify_e1_dec.py']
    t=time.monotonic(); p=subprocess.run(cmd,cwd=wd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=60)
    prefix=ROOT/'evidence'/f'e1_{MODE}_{case}'
    prefix.with_suffix('.stdout.txt').write_text(p.stdout);prefix.with_suffix('.stderr.txt').write_text(p.stderr)
    ledger_path=wd/'misc/e1_facts_ledger.json'
    ledger=json.loads(ledger_path.read_text()) if ledger_path.exists() else None
    if ledger: prefix.with_suffix('.ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
    row=dict(case=case,mode=MODE,command=cmd,cwd=str(wd),exit_code=p.returncode,seconds=time.monotonic()-t,
         facts=len(ledger['facts']) if ledger else None,failed=[r[0] for r in ledger['facts'] if not r[1]] if ledger else None)
    rows.append(row); print(json.dumps(row,ensure_ascii=False),flush=True)
(ROOT/'evidence'/f'e1_{MODE}_runs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
