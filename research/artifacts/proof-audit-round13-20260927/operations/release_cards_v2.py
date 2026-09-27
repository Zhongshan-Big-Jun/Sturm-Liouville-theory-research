from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as C
import research_library as L
import research_review as V
def load(N):return json.loads((O/(N+'.json')).read_text())
Only=sys.argv[1] if len(sys.argv)>1 else None
Bundles={N:load(('certificate-v2' if N=='certificate' else N)+'-review-dispatch')['bundle'] for N in ['spectral','certificate','mathematics']}
for N,B in Bundles.items():
 if Only and N!=Only:continue
 if V.verify_review_bundle(R,B)['verdict']!='APPROVED':raise RuntimeError('Review not approved '+N)
Rows=[dict(X,bundle=Bundles['mathematics'],kind='unchanged-renewal') for X in load('renewals')]
Rows += [dict(X,bundle=Bundles['certificate' if X['name'] in ['rational-envelope-certificates','true-curve-region-decomposition'] else 'mathematics'],kind='revised-card') for X in load('revisions')]
if Only:Rows=[X for X in Rows if X['bundle']==Bundles[Only]]
if len({(X['revision'],X['bundle']) for X in Rows})!=len(Rows):raise RuntimeError('Duplicate obligation')
Groups={}
for X in Rows:Groups.setdefault(X['target']['location'],[]).append(X)
Deps={}
for N,Group in Groups.items():
 Raw=(R/N).read_bytes()
 if hashlib.sha256(Raw).hexdigest()!=Group[0]['target']['sha256']:raise RuntimeError('Card drift '+N)
 Front,_,_=L.read_metadata(Raw);Deps[N]={D['location'] for D in C.card_dependencies(Front) if D['location'] in Groups}
Pending=set(Groups);Order=[]
while Pending:
 Ready=sorted(N for N in Pending if not (Deps[N]&Pending))
 if not Ready:raise RuntimeError('Dependency cycle')
 Order+=Ready;Pending.difference_update(Ready)
Out=O/'release-results.json';Done=json.loads(Out.read_text()) if Out.exists() else []
for N in Order:
 for X in Groups[N]:
  if any(D['revision']==X['revision'] and D['bundle']==X['bundle'] for D in Done):continue
  Result=C.release(R,X['revision'],X['bundle'])
  Summary={K:Result[K] for K in ['request_id','reused','path','sha256','reuse_allowed','verdict'] if K in Result}
  Done.append(dict(X,result=Summary));Out.write_text(json.dumps(Done,ensure_ascii=False,indent=2)+'\n')
  print(len(Done),'/',len(Rows),N,X['issue'][:8],Result['verdict'],flush=True)
  if Result['verdict'] not in ['RELEASED','STILL_BLOCKED']:raise RuntimeError('Unexpected release result')
 # Each authoritative C.release already derives the full impact state.
 Last=next(D for D in reversed(Done) if D['target']['location']==N and D['bundle']==Groups[N][-1]['bundle'])
 if not Last['result'].get('reuse_allowed',False):raise RuntimeError('Still blocked after current obligations '+N)
print('Complete:',len(Rows),'obligations;',len(Groups),'current cards',flush=True)
