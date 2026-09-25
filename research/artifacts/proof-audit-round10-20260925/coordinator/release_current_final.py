from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as C
import research_library as L
import research_review as V
def load(N):return json.loads((O/(N+'.json')).read_text())
RenewOnly=len(sys.argv)>1 and sys.argv[1]=='renewals-only'
Bundles={N:load(N+'-dispatch')['bundle'] for N in (['renewal-review'] if RenewOnly else ['math-review','renewal-review'])}
for N,B in Bundles.items():
 if V.verify_review_bundle(R,B)['verdict']!='APPROVED':raise RuntimeError('Review not approved '+N)
Rows=[dict(X,bundle=Bundles['renewal-review'],kind='unchanged-renewal') for X in load('renewals')]
if not RenewOnly:Rows+=[dict(X,bundle=Bundles['math-review'],kind='revised-card') for X in load('current-revisions')]
if len(Rows)!=(4 if RenewOnly else 15):raise RuntimeError('Unexpected current obligation set')
Groups={}
for X in Rows:Groups.setdefault(X['target']['location'],[]).append(X)
if len(Groups)!=(4 if RenewOnly else 8):raise RuntimeError('Unexpected current card set')
Deps={}
for N,Group in Groups.items():
 B=(R/N).read_bytes()
 if hashlib.sha256(B).hexdigest()!=Group[0]['target']['sha256']:raise RuntimeError('Card drift '+N)
 Front,_,_=L.read_metadata(B);Deps[N]={D['location'] for D in C.card_dependencies(Front) if D['location'] in Groups}
Pending=set(Groups);Order=[]
while Pending:
 Ready=sorted(N for N in Pending if not (Deps[N]&Pending))
 if not Ready:raise RuntimeError('Dependency cycle')
 Order+=Ready;Pending.difference_update(Ready)
Out=O/'current-release-results.json';Done=json.loads(Out.read_text()) if Out.exists() else []
for N in Order:
 for X in Groups[N]:
  if any(D['revision']==X['revision'] and D['bundle']==X['bundle'] for D in Done):continue
  Result=C.release(R,X['revision'],X['bundle']);Done.append(dict(X,result=Result));Out.write_text(json.dumps(Done,ensure_ascii=False,indent=2)+'\n')
  print(N,X['issue'][:8],Result['verdict'],flush=True)
  if Result['verdict'] not in ['RELEASED','STILL_BLOCKED']:raise RuntimeError('Unexpected release result')
 Store=C.load_store(R);States,_=C.impact_states(R,Store)
 if not States[C.key(Groups[N][0]['target'])]['reuse_allowed']:raise RuntimeError('Still blocked after all current obligations '+N)
print('Released requested',len(Rows),'obligations on',len(Groups),'current cards through original API.',flush=True)
