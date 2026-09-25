from pathlib import Path
import sys,json,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A=R/'research/artifacts/proof-audit-round10-20260925'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
import research_corrections as C
Cards=json.loads((O/'cards.json').read_text());Changed=[]
for Name,Ref in Cards.items():
	Front,Body,_=L.read_metadata((R/Ref['location']).read_bytes());Dirty=[]
	for Source in Front.get('sources',[]):
		if Source.get('path') and Source.get('sha256') and hashlib.sha256((R/Source['path']).read_bytes()).hexdigest()!=Source['sha256']:
			Dirty.append(dict(Source));Source.pop('sha256')
	if Dirty:
		Data=dict(Front,content=Body);New=L.save_card(R,Data,Ref['location'],Ref['sha256'])
		Changed.append(dict(name=Name,old=Ref,new=New,stale_sources=Dirty));Cards[Name]=New
		(O/'cards.json').write_text(json.dumps(Cards,ensure_ascii=False,indent=2)+'\n')
(O/'typesetting-binding-refresh.json').write_text(json.dumps(Changed,ensure_ascii=False,indent=2)+'\n')
Store=C.load_store(R);States,Problems=C.impact_states(R,Store)
Initial={X['release'] for X in json.loads((A/'initial-impact.json').read_text())['review_problems']}
New=[]
for Problem in Problems:
	if Problem['release'] in Initial:continue
	Data=Store['requests'][Problem['release']]['payload'];Revision=Store['requests'][Data['revision']]['payload']
	New.append(dict(old_release=Problem['release'],revision=Data['revision'],target=Revision['new'],issue=Revision['issue'],old_bundle=Data['bundle'],problem=Problem))
Current=[]
for P in (R/'tools').glob('*.md'):
	Ref=dict(location=P.relative_to(R).as_posix(),sha256=hashlib.sha256(P.read_bytes()).hexdigest());State=States.get(C.key(Ref))
	if State and not State['reuse_allowed']:Current.append(dict(target=Ref,state=State))
(O/'renewal-inspection.json').write_text(json.dumps(dict(new_invalid_releases=New,current_blocked=Current,all_review_problems=Problems),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(refreshed=[X['name'] for X in Changed],new_invalid=len(New),cards=sorted(set(X['target']['location'] for X in New)),current_blocked=Current),ensure_ascii=False),flush=True)
