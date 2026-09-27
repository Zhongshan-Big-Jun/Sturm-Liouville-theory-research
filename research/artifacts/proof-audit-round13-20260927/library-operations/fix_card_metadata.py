from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927');A=R/'research/artifacts/proof-audit-round13-20260927'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
Cards=json.loads((O/'cards.json').read_text())
for Name in ['bang-bang','jump-stability']:
 P='tools/'+Name+'.md';Raw=(R/P).read_bytes();Front,Body,_=L.read_metadata(Raw);Old=L.read_metadata((A/'before'/P).read_bytes())[0]
 Data=dict(content=Body,author_ids=sorted(set(Front.get('author_ids',[])+Old.get('author_ids',[]))))
 if Name=='bang-bang':Data['dependencies']=[dict(location='tools/helly-compactness.md',sha256=Cards['helly-compactness']['sha256'])]
 Cards[Name]=L.save_card(R,Data,P,hashlib.sha256(Raw).hexdigest());print(Name,flush=True)
(O/'cards.json').write_text(json.dumps(Cards,ensure_ascii=False,indent=2)+'\n')
