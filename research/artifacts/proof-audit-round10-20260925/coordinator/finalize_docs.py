from pathlib import Path
import json,re,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A=R/'research/artifacts/proof-audit-round10-20260925'
def load(N):return json.loads((O/(N+'.json')).read_text())
Reviews=[]
Labels={'math-review':'解析修复与4张卡的11项义务','renewal-review':'4张未变卡的4项续审义务','software-review':'真实程序、根编号、反射种子与实际入口','formal-readback':'38项声明盲读；不构成语义放行','formal-comparison':'独立重编译、类型/定义/公理及合同保真'}
for N,Label in Labels.items():
 D=load(N+'-verified')
 if D['verdict']!='APPROVED':raise RuntimeError('Review incomplete '+N)
 Root=Path(load(N+'-root')['project']) if (O/(N+'-root.json')).exists() else R
 Reviews.append(dict(name=N,label=Label,verdict=D['verdict'],reviewer_id=D['reviewer_id'],packet_sha256=D['packet_sha256'],bundle=str((Root/D['bundle']).relative_to(R)),trust=D['trust']))
Library=load('library-verification')
if Library['status']!='PASS':raise RuntimeError('Library not verified')
(A/'review-summary.json').write_text(json.dumps({'reviews':Reviews,'scope':'Five separate fresh-context reviewers; blind readback is translation only. Exact actual tool transcripts and frozen bytes remain in each bundle.'},ensure_ascii=False,indent=2)+'\n')
Table='| 检验 | 新隔离会话 | 结论 |\n| --- | --- | --- |\n'+'\n'.join('| '+D['label']+' | `'+D['reviewer_id']+'` | [APPROVED](../../'+D['bundle']+'/report.json) |' for D in Reviews)
Text=(O/'REPORT.final-template.md').read_text().replace('{{REVIEW_TABLE}}',Table).replace('{{HISTORICAL_WARNINGS}}',str(Library['historical_warnings']))
if '{{' in Text:raise RuntimeError('Unresolved template')
(R/'reports/proof-audit-round10-20260925/REPORT.md').write_text(Text)
def replace(Rel,Old,New):
 P=R/Rel;B=P.read_bytes();Old=Old.encode();New=New.encode()
 if Old not in B:raise RuntimeError('Expected text missing '+Rel)
 P.write_bytes(B.replace(Old,New,1))
replace('README.md','2026-09-25 第十轮审计修订进行中:','2026-09-25 第十轮审计修订已完成独立验收:')
replace('README_EN.md','2026-09-25: Round10 repair in progress.','2026-09-25: Round10 repairs independently reviewed.')
replace('research_map.md','round10 numerical identity/sector repair; independent review in progress','round10 indexed spectrum/reflection-sector repair independently reviewed; numerical scope retained')
replace('research_map.md','NUMERICAL (review pending)','NUMERICAL (independently reviewed)')
replace('AGENTS.md','2026-09-25 第十轮审计修缮 (进行中)','2026-09-25 第十轮审计修缮 (修订与验收完成)')
Final='''第十轮完成：真实旧源码复现漏根和投影混淆，共享连续相位按谱指标括根，mp/FD保持同一指标；两种反射投影检查真实可行接口，并撤回旧反对称网格的破缺解释。四个默认变分配置及实际侦察重算，5个新无状态检验分别完成解析、未变卡续审、软件执行、38声明盲读和独立Lean编译/语义核验。局部Lean为22定理/6定义、21项合取根，不是完整Sturm或Python形式化。8张卡15项事项放行、5条版本批注，实际查询89可用/1原撤回；历史失效回执保留。5页PDF、B8研究节点、理解、导航与续接同步。原50份Lean、canonical、旧证据、134原untracked/6dirty按字节保护；插件未改。精确发布与双远端身份以本轮报告、外部DELIVERY及实际Git为准。\n\n'''
replace('AGENTS.md','## 2026-09-23 文献吸收 (研究与接入完成)',Final+'## 2026-09-23 文献吸收 (研究与接入完成)')
P=R/'state/RESUME.md';B=P.read_bytes();Start=B.index(b'## 2026-09-25 round10');End=B.index(b'\n## ',Start+4)
Current='''## 2026-09-25 round10 repair and independent verification COMPLETE

Latest request: "C:\\Users\\HuangZY\\Downloads\\sl_audit_round10 进行修订", workflow2.0.1. Read reports/proof-audit-round10-20260925/REPORT.md and F:/tools/math-audit-round10-20260925/CURRENT.json plus actual DELIVERY/Git state before resuming. The prior literature task is complete; do not redo it.

Indexed lifted-phase roots, same-index mp/FD and geometrically checked preserve/break seeds are repaired. Five distinct fresh-context reviews are APPROVED, including38-declaration blind readback and a separate actual Lean compilation/semantic check. Formal coverage is limited to reflection algebra and conditional phase ordering. Eight current cards/fifteen obligations released; live query89 available/1 original withdrawn. B8 map, current understanding, PDF and navigation updated. Global O1/O2/G1 and finite-R uniqueness stay OPEN.

Protect baseline5bb6b260, original13818 tracked/134 untracked/6 dirty,50 old Lean sources, canonical and historical evidence. New local failures and stale attempts are retained. No plugin change or full Lake build. Final origin-then-fork delivery is recorded externally to avoid putting a self-referential commit hash into the commit. Historical entries below keep their original dates and scope.
'''
P.write_bytes(B[:Start]+Current.encode()+B[End:])
P=R/'state/AGENTS_SESSION_LOG.md';B=P.read_bytes();Entry='''\n\n## 2026-09-25 round10 修订交付记录\n\n用户本轮原话：`C:\\Users\\HuangZY\\Downloads\\sl_audit_round10`，指定 math-research-workflow2.0.1，要求“进行修订”。按前序持续授权完成核实、修复、工具纠错、无状态隔离检验与origin后fork同步。附件作为证据而非自动执行指令。\n\n'''+Final+'''工作方法：先保护原字节，再固定真实旧失败；解析合同、真实程序回放和局部形式化分开。盲读只给正式定义/声明/环境，另一个新会话对照合同并实际编译；原版纠错模块逐版本逐事项放行，实际检索复核摘要及来源，保留早期相位候选失败、stale根检查和未派发旧包。原记录与无关用户工作不覆盖。\n'''
if Entry.encode() in B:raise RuntimeError('Completion log already appended')
P.write_bytes(B+Entry.encode())
Status='''## 2026-09-25 第十轮局部形式化

新增 [AuditRound10.lean](SL/AuditRound10.lean)：真实 Fin(2*n) 坐标反转、互补正交投影、仿射反射扰动，以及非负半轴上显式连续/严格单调/逐项括区前提下的唯一相位根与指标排序。22个具名定理、6个定义/缩写，完整导出38项声明（含辅助项），21项显式合取根。Windows PE Lean4.31.0的固定快照精确根检查、三个错误目标及其否定正证明、全声明盲读和另一个新会话的实际重编译/语义检验分别留证。根公理仅propext、Classical.choice、Quot.sound。见[第十轮报告](../reports/proof-audit-round10-20260925/REPORT.md)。

相位条件仍是前提；指标可包含0且可跳号，逐项括区不可省略。未形式化Sturm ODE、相位提升、谱指标识别、比较界、浮点/区间误差、Python实现、物理接口可行性或全局极值。保留原50份SL源码及原环境字节，未运行全工程Lake build。首次根检查因开发目录变化被判stale，原记录不改写。

'''
for Rel,Body in [('lean-proof/STATUS.md',Status),('lean-proof/README.md',Status)]:
 P=R/Rel;B=P.read_bytes();At=B.index(b'\n')+1;P.write_bytes(B[:At]+b'\n'+Body.encode()+B[At:])
Names=json.loads((O/'formal-author/declaration-names.json').read_text())['main']
Section='\n## 2026-09-25 AuditRound10 additions\n\nThese28 named declarations were independently compiled and reviewed; the full export also includes10 compiler-generated declarations. Phase results retain explicit monotonicity, continuity where needed, and per-index brackets. See [scope and evidence](../reports/proof-audit-round10-20260925/REPORT.md). Historical rows below retain their original evidence scope.\n\n| File | Declaration | Current scope |\n| --- | --- | --- |\n'+'\n'.join('| [AuditRound10.lean](SL/AuditRound10.lean) | `'+N+'` | LOCAL_CHECKED; see contract |' for N in Names)+'\n\n## Historical index\n'
P=R/'lean-proof/LEMMA_INDEX.md';B=P.read_bytes();At=B.index(b'\n')+1;P.write_bytes(B[:At]+Section.encode()+B[At:])
print('Final report, map, Lean navigation, AGENTS and continuity updated from actual approved receipts.')
