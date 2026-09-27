from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
import research_review as V
Author='01a06f46-dd03-7c83-9267-32048412c359'
Notes=[]
for Name in ['green-half-inertia','half-problem-regularized-green']:
 P='tools/'+Name+'.md';Notes.append(L.annotate(R,P,hashlib.sha256((R/P).read_bytes()).hexdigest(),author=Author,kind='application-boundary',locator='Round13 shared numerical interfaces',text='Round13 current normalized values and derivatives share one physical solution/mass; nodes are legal. Ordinary DD/DN Green now uses actual coordinates and linear/hyperbolic propagation for mu<=0; positive-eigenvalue reduced kernels keep their narrower contract. General residual Jacobian includes the nonstationary correction and recovers the original formula at F=0. Preserve DD/DN indexed spectra, bound poles, physical-FD cross blocks and raw K versus SKS. Derivation and fresh scoped verification are in reports/proof-audit-round13-20260927/REPORT.md and its verification.json. Finite checks do not certify uniform tails, global signs or complete SL/Lean. This annotation is a retrieval pointer, not a new mathematical release.'))
(O/'annotations.json').write_text(json.dumps(Notes,ensure_ascii=False,indent=2)+'\n')
IndexResult=L.make_index(R);(O/'index-result.json').write_text(json.dumps(IndexResult,ensure_ascii=False,indent=2)+'\n');print('index',IndexResult.get('indexed'),IndexResult.get('blocked'),flush=True)
Index=json.loads((R/'index/tools.json').read_text());Good={x['tool_id']:x for x in Index['items']};Bad={x['tool_id']:x for x in Index['blocked_items']}
Expected={'left-definite-orthogonal-systems','interval-dec-directed-rounding'}
if set(Bad)!=Expected or len(Good)!=89:raise RuntimeError('unexpected current library scope '+repr((len(Good),list(Bad))))
for N in ['helly-compactness','bang-bang','jump-stability','rational-envelope-certificates','true-curve-region-decomposition']:
 if N not in Good or Good[N]['sha256']!=hashlib.sha256((R/Good[N]['location']).read_bytes()).hexdigest():raise RuntimeError('current pointer failed '+N)
Queries={}
for Term in ['round13','interval-dec-directed-rounding']:
 D=L.query_tools(R,Term,limit=50);Queries[Term]=D
 if D['verdict']!='RETRIEVAL_ONLY' or any(x['tool_id']=='interval-dec-directed-rounding' for x in D['hits']):raise RuntimeError('default query allowed retired engine or stale state')
(O/'query-results.json').write_text(json.dumps(Queries,ensure_ascii=False,indent=2)+'\n')
Reviews={}
for N in ['spectral','certificate','mathematics']:
 Bundle=json.loads((O/(('certificate-v2' if N=='certificate' else N)+'-review-dispatch.json')).read_text())['bundle'];D=V.verify_review_bundle(R,Bundle)
 if D['verdict']!='APPROVED':raise RuntimeError('final review invalid '+N)
 Reviews[N]=dict(bundle=Bundle,verification=D)
(O/'final-verification.json').write_text(json.dumps(dict(reviews=Reviews,indexed=len(Good),blocked=list(Bad),default_queries_verified=True,annotations=Notes),ensure_ascii=False,indent=2)+'\n');print('FINAL LIBRARY AND REVIEW CHECKS PASSED',flush=True)
