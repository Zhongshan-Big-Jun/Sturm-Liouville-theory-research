from pathlib import Path
import sys,json,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A=R/'research/artifacts/proof-audit-round9-20260923'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
import research_corrections as C
Store=C.load_store(R);States,Problems=C.impact_states(R,Store)
Initial={x['release'] for x in json.loads((A/'initial-impact.json').read_text())['review_problems']}
New={x['release']:x for x in Problems if x['release'] not in Initial}
Rows=[]
for Release,Problem in New.items():
	Data=Store['requests'][Release]['payload'];Revision=Store['requests'][Data['revision']]['payload'];Target=Revision['new']
	Rows.append(dict(old_release=Release,revision=Data['revision'],target=Target,issue=Revision['issue'],old_bundle=Data['bundle'],problem=Problem))
Report=dict(new_invalid_releases=Rows,all_review_problems=Problems,current_blocked=[dict(path=p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),state=States.get((p.relative_to(R).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()))) for p in sorted((R/'tools').glob('*.md')) if (p.relative_to(R).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()) in States and not States[(p.relative_to(R).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest())]['reuse_allowed']])
(O/'renewal-inspection.json').write_text(json.dumps(Report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(new_invalid=len(Rows),cards=sorted({r['target']['location'] for r in Rows}),reasons=sorted({r['problem']['error'] for r in Rows})),ensure_ascii=False,indent=2),flush=True)
