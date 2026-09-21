#!/usr/bin/env python3
"""Rehash the handoff manifest; bind the final receipt by its printed SHA256."""
from pathlib import Path
import concurrent.futures,json,time
from executor import BASE,RUN,pointer,digest,save,stamp
sha=RUN/'SHA256SUMS'
items=[]
for line in sha.read_text().splitlines():
    expected,relative=line.split('  ',1)
    path=(RUN/relative).resolve()
    if not path.is_relative_to(RUN):raise RuntimeError('checksum path escapes run directory')
    items.append((path,expected))
def verify(pair):
    p,h=pair
    return {'path':str(p),'expected_sha256':h,'actual_sha256':digest(p),'bytes':p.stat().st_size}
start=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows=list(pool.map(verify,items))
failures=[r for r in rows if r['expected_sha256']!=r['actual_sha256']]
pre=json.loads((RUN/'preflight.json').read_text())
input_failures=[r['path'] for r in pre['checks'] if digest(r['path'])!=r['expected_sha256']]
packet_ok=digest(BASE/'PACKET.json')==pre['packet']['sha256']
report={'utc':stamp(),'checksum_verification':'all_matched' if not failures and not input_failures and packet_ok else 'FAILED','task_execution_status':'INCOMPLETE','files_verified':len(rows),'bytes_verified':sum(r['bytes'] for r in rows),'failures':failures,'frozen_input_checks':len(pre['checks']),'changed_input_paths':input_failures,'packet_unchanged':packet_ok,'elapsed_seconds':time.monotonic()-start,'verification_program':pointer(__file__),'checksum_list':pointer(sha),'summary':pointer(RUN/'independent-execution.json'),'readme':pointer(RUN/'README.md'),'coverage_note':'The final receipt is written after SHA256SUMS and is excluded from it. Its SHA256 is supplied directly in the execution result/final answer; no circular self-hash is claimed.'}
save(RUN/'delivery-integrity.json',report)
print(json.dumps({'result':report['checksum_verification'],'files_verified':len(rows),'delivery_receipt':pointer(RUN/'delivery-integrity.json'),'sha256sums':pointer(sha),'readme':pointer(RUN/'README.md'),'summary':pointer(RUN/'independent-execution.json')},ensure_ascii=False,indent=2))
raise SystemExit(0 if not failures and not input_failures and packet_ok else 1)
