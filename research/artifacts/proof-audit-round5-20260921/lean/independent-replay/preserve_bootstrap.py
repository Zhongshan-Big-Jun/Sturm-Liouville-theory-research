"""Preserve the two initial discovery commands and deterministically reconstruct their stdout.
The initial tool transport truncated its displayed text. These are explicitly reconstructed
bootstrap streams, not falsely labelled raw captures. All eight Lean runs have raw captures.
"""
from pathlib import Path
import contextlib, hashlib, io, json, os
from audit_runner import OUT, PACKET, sha, write_json, packet
pkt=packet()
agent=os.environ['CODEX_THREAD_ID']
code1="""import os, pathlib, hashlib
p=pathlib.Path('/mnt/f/LaTeX/BVE research/research/library/reviews/packets/98b6920270e96b30b58dd75e49271e97ed00e0a8ea60e116f88c17dba9dd8140/packet.json')
b=p.read_bytes()
print('CODEX_THREAD_ID='+str(os.environ.get('CODEX_THREAD_ID')))
print('PACKET_PATH='+str(p))
print('PACKET_BYTES_SHA256='+hashlib.sha256(b).hexdigest())
print(b.decode())
"""
code2="""from pathlib import Path
import hashlib,json,os,datetime
packet=Path('/mnt/f/LaTeX/BVE research/research/library/reviews/packets/98b6920270e96b30b58dd75e49271e97ed00e0a8ea60e116f88c17dba9dd8140/packet.json')
out=Path('/mnt/f/tools/math-audit-round5-20260921/independent-lean-replay')
assert not out.exists(), 'Write area must be NEW; refusing reuse'
out.mkdir(parents=True)
(out/'receipts').mkdir()
def digest(b): return hashlib.sha256(b).hexdigest()
b=packet.read_bytes()
assert digest(b)==packet.parent.name
p=json.loads(b)
rows=[]
for name,v in p['inputs'].items():
 s=packet.parent/v['snapshot']
 assert s.is_relative_to(packet.parent) and '..' not in Path(v['snapshot']).parts
 data=s.read_bytes()
 h=digest(data)
 rows.append(dict(input=name,snapshot=v['snapshot'],size=len(data),expected_sha256=v['sha256'],actual_sha256=h,match=h==v['sha256']))
verification={'packet_path':str(packet),'packet_sha256':digest(b),'native_agent_id':os.environ.get('CODEX_THREAD_ID'),'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'snapshots':rows,'all_match':all(r['match'] for r in rows)}
(out/'packet-verification.json').write_text(json.dumps(verification,indent=2)+'\\n')
assert verification['all_match'], 'Snapshot mismatch'
src=p['inputs']['lean-proof/SL/AuditRound5.lean']
assert src['sha256']=='035043c154c215e995a210b798f80cf131414eee5529ad54396a5af3d669ae45'
(out/'packet.json').write_bytes(b)
print(json.dumps({'native_agent_id':os.environ.get('CODEX_THREAD_ID'),'packet_sha256':digest(b),'snapshot_count':len(rows),'all_match':verification['all_match'],'write_area':str(out)},indent=2))
base='research/artifacts/proof-audit-round5-20260921/lean/'
for key in ('environment.json','final/module-artifact-hashes.json','InspectAuditRound5.lean','coordinator-replay/ContractCheck.lean','controls/PositiveControls.lean','controls/FalseHighSpanEquality.lean','pins/lakefile.lean','pins/lean-toolchain','CONTRACT.md'):
 v=p['inputs'][base+key]
 data=(packet.parent/v['snapshot']).read_bytes()
 print('\\nFILE '+key+' '+str(len(data))+' bytes')
 if key=='final/module-artifact-hashes.json':
  obj=json.loads(data)
  print('shape:',type(obj).__name__)
  if isinstance(obj,dict):
   for k,x in obj.items():
    print(k, 'len='+str(len(x)) if isinstance(x,(list,dict)) else x)
    if isinstance(x,list): print(json.dumps(x[:2],indent=2))
    elif isinstance(x,dict): print(json.dumps(dict(list(x.items())[:2]),indent=2))
  else: print(json.dumps(obj[:2],indent=2))
 else: print(data.decode())
print('\\nINPUT_KEYS')
print('\\n'.join(p['inputs']))
"""
stdout1='CODEX_THREAD_ID='+agent+'\nPACKET_PATH='+str(PACKET)+'\nPACKET_BYTES_SHA256='+sha(PACKET)+'\n'+PACKET.read_bytes().decode()+'\n'
buffer=io.StringIO()
with contextlib.redirect_stdout(buffer):
    print(json.dumps({'native_agent_id':agent,'packet_sha256':sha(PACKET),'snapshot_count':len(pkt['inputs']),
                     'all_match':True,'write_area':str(OUT)},indent=2))
    base='research/artifacts/proof-audit-round5-20260921/lean/'
    for key in ('environment.json','final/module-artifact-hashes.json','InspectAuditRound5.lean',
                'coordinator-replay/ContractCheck.lean','controls/PositiveControls.lean',
                'controls/FalseHighSpanEquality.lean','pins/lakefile.lean','pins/lean-toolchain','CONTRACT.md'):
        v=pkt['inputs'][base+key]
        data=(PACKET.parent/v['snapshot']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==v['sha256']
        print('\nFILE '+key+' '+str(len(data))+' bytes')
        if key=='final/module-artifact-hashes.json':
            obj=json.loads(data)
            print('shape:',type(obj).__name__)
            if isinstance(obj,dict):
                for k,x in obj.items():
                    print(k,'len='+str(len(x)) if isinstance(x,(list,dict)) else x)
                    if isinstance(x,list):print(json.dumps(x[:2],indent=2))
                    elif isinstance(x,dict):print(json.dumps(dict(list(x.items())[:2]),indent=2))
            else:print(json.dumps(obj[:2],indent=2))
        else:print(data.decode())
    print('\nINPUT_KEYS')
    print('\n'.join(pkt['inputs']))
for n,code,output in [('01-initial-packet',code1,stdout1),('02-snapshot-verification',code2,buffer.getvalue())]:
    (OUT/'receipts'/('bootstrap-'+n+'.stdout.txt')).write_text(output)
    (OUT/'receipts'/('bootstrap-'+n+'.stderr.txt')).write_bytes(b'')
    write_json(OUT/'receipts'/('bootstrap-'+n+'.json'),
               {'cmd':"python3 - <<'PY'\n"+code+"PY",'cwd':'/mnt/f','exit_code':0,
                'exit_evidence':'Original exec_command returned exit_code=0',
                'stdout_provenance':'Deterministic reconstruction of print-only bootstrap output from byte-verified frozen inputs; original tool displayed a truncated result.',
                'stderr_provenance':'No stderr reported; reconstructed empty stream. The bootstrap tool provides a merged stream.',
                'stdout_sha256':sha(OUT/'receipts'/('bootstrap-'+n+'.stdout.txt')),
                'stderr_sha256':sha(OUT/'receipts'/('bootstrap-'+n+'.stderr.txt'))})
print('Preserved exact bootstrap command text and explicitly marked reconstructed bootstrap streams.')

