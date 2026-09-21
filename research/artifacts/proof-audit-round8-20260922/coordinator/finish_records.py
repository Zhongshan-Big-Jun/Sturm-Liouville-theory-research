from pathlib import Path
import json,datetime
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922')
lib=json.loads((O/'library-final.json').read_text())
if lib['status']!='PASS':raise RuntimeError('Retrieval not finalized')
for name in ['math-review','certificate-review','formal-readback','formal-semantic','renewal-review','summary-review']:
 if json.loads((O/(name+'-received.json')).read_text())['verdict']!='APPROVED':raise RuntimeError('Review not approved '+name)
summary='''第八轮F01-F05及P01-P03直接传播已修订. 连续展开相位给出全R>=1统一谱隙下界, 覆盖完整薄层域; 大w初等正余量比较与T2解析结构闭合T1, 不再依赖旧网格或T3数值. 固定内部u的首项为C(u)/R, 在u*处C严格正; 最优值满足非负O(1/R)误差. 精确最优系数与参数速度未在本轮证明. 新证书只以有理数、Machin/Taylor误差和显式守卫作证明运算. 独立证书重放及56次预期失败负对照、独立解析审阅、局部Lean新编译/盲读/语义核对均分别留证; Lean不等于完整谱论或隐函数展开形式化.

四卡放行后的实际查询暴露综述整文件绑定问题: 70可用/9隔离. 只有INF段落变化, 但八张未变的左定卡的第六轮审查已失效; 保留失败状态, 对18项既有事项义务另启新无状态审查, 原卡/证明字节不变, 以新审查续发同一修订的回执. 最终78可用/1原隔离, 四改动卡加八原字节卡共22项义务. 35个历史失效回执保留: 17项后继版本、18项同版本新审查; 逐张核对当前检索摘要/哈希/依赖. 今后修改综合文档应检查所有绑定它的有效审查, 不能只检索直接数学依赖. 随后实际摘要检查又发现三张原卡的索引继承了过时摘要, 其中Krein仍有错误边界条件和开放状态. 通过已有from-index恢复流程, 从已审查的当前卡正文重建摘要, 另一个新隔离会话检查后替换派生索引; 卡片及纠错门禁状态不变. 对无显式summary的旧卡比较正文导出的摘要, 而不是要求它们凭空新增字段. 数量恢复不是摘要正确的证据.

三PDF重建为11/17/20页, 主文全页与伴随改动页检查; 研究地图新增B4-INF-LIMIT, 维持B4总体PARTIAL, 更新项目理解、双语首页、研究/工具/脚本导航、Lean状态和续接. 研究经验另存精确版本批注, 更多层的相位传播明确为待证想法. 作者早期失败、检验器三次失败及修正、作者通知/排队跟进造成的等待超时均留原始证据, 不伪造完成回执. 六次最终检验均为新fork_context:false会话. 48份旧SL Lean源、canonical、冻结旧证据和原无关工作按基线保护. 本轮未改插件源码/缓存或全局环境. 精确提交范围与主仓库后fork交付以第八轮报告及项目外DELIVERY.json为准.'''
p=R/'AGENTS.md';t=p.read_text();t=t.replace('## 2026-09-22 第八轮审计修缮 (进行中)','## 2026-09-22 第八轮审计修缮 (本轮完成)',1)
anchor='## 2026-09-21 第七轮审计修缮 (本轮完成)'
if summary not in t:
 if t.count(anchor)!=1:raise RuntimeError('AGENTS anchor mismatch')
 t=t.replace(anchor,summary+'\n\n'+anchor,1)
p.write_text(t)
p=R/'state/AGENTS_SESSION_LOG.md';t=p.read_bytes().decode('utf-8')
if '## 2026-09-22 第八轮审计修订完成' not in t:p.write_bytes((t+'\n\n## 2026-09-22 第八轮审计修订完成\n\n'+summary+'\n').encode('utf-8'))
resume='''## 2026-09-22 eighth-round audit repair completed

Current report: reports/proof-audit-round8-20260922/REPORT.md. All five supplied findings and direct propagation are repaired. The symmetric-well INF limit now uses a continuous phase bound over the entire thin-layer region and an elementary positive-margin large-w comparison; T1 relies on analytic T2, not the old grids or numerical T3. Exact T3 enclosures and fixed-interior-u C(u)/R expansion are repaired; the scaled optimized value has nonnegative O(1/R) error. Exact optimized coefficients, parameter rates and non-symmetric/all-box/general-n conclusions are outside this repair. B4-INF-LIMIT is solved in its declared subproblem; B4 overall remains partial.

Six final stateless reviews are approved: analytic/correction, exact-certificate execution, formal blind readback, a different fresh formal replay+semantic review, unchanged-card review renewal, and derived-summary recovery review. Four revised cards and eight unchanged left-definite cards have22 exact issue duties, with actual retrieval78 available/1 original block. The failed70/9 query is retained: an INF-only summary edit invalidated a whole-document round6 binding and required18 scope renewals. All35 historical invalid releases remain as historical warnings with precise successors. Do not delete them or bypass the gate. After count recovery, three stale inherited summaries were also detected and regenerated through the existing from-index interface. A separate fresh review checked literal current-body extraction and unchanged gate identities. All current hashes, query summaries and dependencies were checked.

LocalLean15 authored theorems/11 definitions plus21 generated theorems underwent fresh compilation,47-declaration blind readback and semantic matching, nine-conjunct root identity, transitive axiom inspection and three wrong-target controls. Complete minmax/phase-speed/T1, integral identification, analytic implicit functions and remainders are not fully formalized; no full Lake build. Independent Python checker failures remain separate from the final9102-check pass. Exact rational certificate checks run normally, under-O and-S, with56 intended rejection receipts; finite checks do not prove the continuous domain.

Preserve baseline d1462eb, all10236 original tracked paths outside the explicit change scope,134 original untracked files,6 preexisting dirty files,48 old SL Lean sources, old frozen evidence and canonical. Three PDFs, human map/understanding, tool annotations and navigation are updated; plugin code/cache and global proxy/environment are unchanged. All research/review agents are completed; do not rerun them. External F:/tools/math-audit-round8-20260922 contains actual native dispatches/completions, exact staging checks and CURRENT.json/DELIVERY.json. If publication was interrupted, reconcile these records and actual origin/fork HEADs before retrying; push origin first then fork. Frozen files must retain exact bytes. Older dated status entries below are historical and do not supersede this scoped repair.

'''
p=R/'state/RESUME.md';t=p.read_text()
if resume not in t:
 if not t.startswith('# RESUME\n'):raise RuntimeError('Unexpected RESUME title')
 p.write_text('# RESUME\n\n'+resume+t[len('# RESUME\n'):].lstrip('\n'))
p=O/'AGENTS.md';t=p.read_text()
if '## Final local verification' not in t:p.write_text(t+'\n\n## Final local verification\n\n'+summary+'\n')
current=json.loads((O/'CURRENT.json').read_text());current.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='READY_FOR_PUBLICATION',pending='All six reviews and exact query passed. Final document/protection/staging and sequential origin/fork push remain; consult actual DELIVERY.json before assuming delivery.',library_writer_session=None,main_candidate_scope='Approved exact analytic source and all three PDF outputs; local Lean limitations remain explicit.',library_result='library-final.json',agents='ALL_COMPLETED_AND_CLOSED')
current['reviews']={n:json.loads((O/(n+'-dispatch.json')).read_text())|{'state':'APPROVED'} for n in ['certificate-review','math-review','formal-readback','formal-semantic','renewal-review','summary-review']}
(O/'CURRENT.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
print('AGENTS, session log and continuity updated; publication still separate.',flush=True)
