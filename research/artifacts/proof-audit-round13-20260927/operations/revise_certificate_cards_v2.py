from pathlib import Path
import hashlib,json,sys,shutil
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927');A='research/artifacts/proof-audit-round13-20260927/'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
import research_corrections as C
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for n in ['cards.json','revisions.json']:
 if not (O/(n[:-5]+'-attempt1.json')).exists():shutil.copyfile(O/n,O/(n[:-5]+'-attempt1.json'))
Cards=json.loads((O/'cards.json').read_text());Rows=json.loads((O/'revisions.json').read_text());Baseline=json.loads((O/'baseline.json').read_text())
for Name in ['rational-envelope-certificates','true-curve-region-decomposition']:
 PathValue='tools/'+Name+'.md';Raw=(R/PathValue).read_bytes();Front,Body,_=L.read_metadata(Raw)
 if Name=='true-curve-region-decomposition':
  Old='''   `Q=[1,2]x[0.4,0.5]` 上真实相位曲线的像包含于 `T1,T2` (由
   `c1(alpha1(q,c),q)=c` 与端点包含引理).'''
  New='''   内部盒 `Q°=(1,2)x(0.4,0.5)` 的相位像包含于 `T1,T2`；闭盒
   `Q=[1,2]x[0.4,0.5]` 的像包含于相应闭包，由相位连续性及内部点逼近得到。
   例如 `q=1,c=1/2` 给出 `alpha1=gamma=pi/3`，不在严格的 `Ti` 内。
   边界严格符号分别由 T1 闭包上的统一下界 `6499/7500` 与整个闭盒上的 J2 定理保证，
   不能只靠严格不等式的连续延拓。'''
  if Old not in Body:raise RuntimeError('Missing domain anchor')
  Body=Body.replace(Old,New)
  Old='全部单变量事实由区间引擎认证 (55 项, 见 [[interval-dec-directed-rounding]]).'
  if Old not in Body:raise RuntimeError('Missing old dependency anchor')
  Body=Body.replace(Old,'55 项解析事实由当前 [[rational-envelope-certificates]] 的有理包络支持；57 条台账合同完整验收。退役 Decimal 引擎不再作为依据。')
 else:
  Body=Body.replace('certificate-repair.md) 与活动 O3a 正文附录','certificate-repair-v2.md) 与活动 O3a 正文附录')
 Sources=[dict(path='docs/SL_gap_n1_O3a_phase_rigidity_proof.tex',locator='Current exact certificate and closed-parameter-box scope'),dict(path=A+'certificate-repair-v2.md',locator='Independent-review corrections F1-F3; prior rejection retained')]
 Data=dict(content=Body,created=str(Front['created']),updated='2026-09-27',sources=Sources,author_ids=Front['author_ids'])
 NewCard=L.save_card(R,Data,PathValue,hashlib.sha256(Raw).hexdigest());Cards[Name]=NewCard;save('cards.json',Cards)
 Previous=next(x for x in Rows if x['name']==Name)
 Result=C.propose_revision(R,Previous['issue'],dict(location=PathValue,sha256=Baseline['tracked'][PathValue]),dict(location=PathValue,sha256=NewCard['sha256']),'01a06f46-dd03-7c83-9267-32048412c359','Complete the first isolated review F1-F3: true receiver negative controls and matching positive controls, remove remaining retired-engine dependency, distinguish interior phase image from closure while preserving uniform J1/J2 boundary bounds. Original CHANGES_REQUIRED receipt retained; new version requires fresh review.')
 Previous.update(revision=Result['revision_id'],target=dict(location=PathValue,sha256=NewCard['sha256']))
 save('revisions.json',Rows);print('revised',Name,Result['revision_id'],flush=True)
