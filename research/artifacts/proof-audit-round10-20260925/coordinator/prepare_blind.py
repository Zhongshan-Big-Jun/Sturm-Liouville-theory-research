from pathlib import Path
import json, shutil, hashlib
O=Path('/mnt/f/tools/math-audit-round10-20260925')
R=Path('/mnt/f/LaTeX/BVE research/research/artifacts/proof-audit-round10-20260925/formal-readback')
S=O/'formal-author/formal-only'
R.mkdir(parents=True,exist_ok=True)
(R/'AGENTS.md').write_text('# Isolated formal readback\n\nRead only the frozen packet. Do not consult project history, informal intent, memory or other review verdicts. Describe declarations exactly, including all premises. Write only to a private temporary directory.\n')
P=json.loads((S/'packet.json').read_text())
Inputs=[]
for Name,Meta in P['files'].items():
 Data=(S/Name).read_bytes()
 assert hashlib.sha256(Data).hexdigest()==Meta['sha256']
 Dest=R/'inputs'/Name;Dest.parent.mkdir(parents=True,exist_ok=True);Dest.write_bytes(Data)
 Role='formal-statement' if Name=='AuditRound10.lean' else ('definitions' if Name.endswith('.json') and Name=='declarations-full.json' or Name=='print-and-axioms.log' else 'environment')
 Inputs.append({'path':str(Dest.relative_to(R)),'role':Role})
Names=[D['name'] for D in json.loads((S/'declarations-full.json').read_text())]
Spec={'kind':'formal-readback','author_ids':['01a06f46-dd03-7c83-9267-32048412c359','01a0d723-0c42-7142-a358-78252676dccd'],'inputs':Inputs,'claims':[{'id':N,'declaration':N} for N in Names]}
(O/'formal-readback-spec.json').write_text(json.dumps(Spec,indent=2)+'\n')
(O/'formal-readback-root.json').write_text(json.dumps({'project':str(R)})+'\n')
print({'declarations':len(Names),'files':len(Inputs)})
