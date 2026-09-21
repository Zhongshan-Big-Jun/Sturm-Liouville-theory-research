#!/usr/bin/env python3
"""Preserve only authorized small input files verbatim for the evidence handoff."""
from pathlib import Path
import json,shutil
from executor import BASE,RUN,pointer,save
packet=json.loads((BASE/'PACKET.json').read_text())
freeze=json.loads((BASE/'lean-package/freeze.json').read_text())
paths=[Path('PACKET.json'),Path('lean-package/freeze.json')]+[Path('lean-package')/x for x in freeze['files']]+[Path('numerical')/x for x in packet['numeric_sources']]
rows=[]
for rel in paths:
    source=BASE/rel;dest=RUN/'inputs'/rel
    if dest.exists(): raise RuntimeError('input archive already exists')
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,dest)
    a,b=pointer(source),pointer(dest)
    if a['sha256']!=b['sha256']:raise RuntimeError('input copy is not byte-identical')
    rows.append({'source':a,'archived_copy':b})
save(RUN/'input-snapshots.json',{'purpose':'Verbatim allowed small input archive only; no execution was rerouted to these copies and no missing manifest was supplied. External runtimes remain hash references.','count':len(rows),'files':rows})
print('preserved',len(rows),'small allowed inputs byte-for-byte')
