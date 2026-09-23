from pathlib import Path
import json,shutil,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A=R/'research/artifacts/proof-audit-round9-20260923';P=A/'formal-review'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as V
P.mkdir();(P/'inputs').mkdir()
(P/'AGENTS.md').write_text('# Isolated round9 formal review project\n\nThis scoped review uses its own library writer lock, independent of the parent correction journal. Inputs are exact frozen copies; never edit completed packets or receipts. The coordinator receives actual stateless-agent transcripts through the installed review runtime. User requested continued round9 repair, with prior isolated-verification authorization. Parent README/report tracks the distinction between author execution, blind readback and final semantic/compiler review.\n')
Spec=json.loads((O/'formal-readback-spec.json').read_text())
for X in Spec['inputs']:
	Src=R/X['path'];Dst=P/'inputs'/Src.name;shutil.copyfile(Src,Dst);X['path']='inputs/'+Src.name
Result=V.create_packet(P,Spec)
for N,D in [('formal-isolated-readback-spec.json',Spec),('formal-isolated-readback-packet.json',Result)]:
	(O/N).write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
(O/'formal-review-root.json').write_text(json.dumps(dict(project=str(P),relative_project=str(P.relative_to(R))),indent=2)+'\n')
print('Created independent formal review project and packet',Result['packet_sha256'],flush=True)
