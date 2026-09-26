from pathlib import Path
import hashlib
import json
import sys
Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Source = Out / 'formal-author/blind'
Project = Root / 'research/artifacts/proof-audit-round12-20260926/formal-readback'
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as Review
Manifest = json.loads((Source/'manifest.json').read_text())
Project.mkdir()
(Project/'AGENTS.md').write_text('# Independent formal readback\n\nOnly frozen formal declarations, definitions and environment are in scope. Do not read project history, memory, author conversation or informal intent. Do not edit inputs or main project. Private temporary output only.\n')
Inputs = []
for Name, Expected in Manifest['files'].items():
	Data = (Source/Name).read_bytes()
	if hashlib.sha256(Data).hexdigest() != Expected:
		raise RuntimeError('Blind input changed '+Name)
	Target = Project/'inputs'/Name
	Target.parent.mkdir(parents=True,exist_ok=True)
	Target.write_bytes(Data)
	Role = 'formal-statement' if Name.endswith('.lean') else ('environment' if Name=='lean-toolchain' else 'definitions')
	Inputs.append(dict(path=Target.relative_to(Project).as_posix(), role=Role))
Names = [Entry['name'] for Entry in json.loads((Source/'declarations.json').read_text())]
Spec = dict(kind='formal-readback', author_ids=['01a06f46-dd03-7c83-9267-32048412c359','01a0dce9-5748-7710-9a4e-adff48f38f61'], inputs=Inputs, claims=[dict(id=Name,declaration=Name) for Name in Names])
for Name, Data in [('formal-readback-spec.json',Spec),('formal-readback-root.json',dict(project=str(Project))),('formal-readback-packet.json',Review.create_packet(Project,Spec))]:
	(Out/Name).write_text(json.dumps(Data,ensure_ascii=False,indent=2)+'\n')
print('Frozen blind packet',len(Names),'declarations',flush=True)
