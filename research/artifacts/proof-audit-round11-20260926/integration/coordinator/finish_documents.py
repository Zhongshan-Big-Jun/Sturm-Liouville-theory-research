from pathlib import Path
import json,hashlib,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round11-20260926');A=R/'research/artifacts/proof-audit-round11-20260926';Report=R/'reports/proof-audit-round11-20260926'
Names=['math-review','renewal-review','software-review','cofinite-review','formal-readback','formal-comparison']
Roles=['当前四卡及Jacobian解析修订','四张未变卡的精确续审','实际软件及有限数值执行','全窗口余有限解析证明及拟入库卡','37声明盲读','独立Lean编译与契约比对']
Reviews=[];Rows=[]
for N,Role in zip(Names,Roles):
	V=json.loads((O/f'{N}-verified.json').read_text());P=json.loads((O/f'{N}-packet.json').read_text())
	if V['verdict']!='APPROVED' or V['packet_sha256']!=P['packet_sha256']:raise RuntimeError('Final review unavailable '+N)
	Q=O/f'{N}-root.json';Root=Path(json.loads(Q.read_text())['project']) if Q.exists() else R
	Bundle=(Root/V['bundle']).relative_to(R).as_posix();Packet=json.loads((Root/P['packet']).read_text());Ref=f'../../{Bundle}/report.json'
	Reviews.append(dict(role=Role,kind=N,verdict=V['verdict'],reviewer_id=V['reviewer_id'],packet_sha256=V['packet_sha256'],bundle=Bundle,input_count=len(Packet['inputs']),claim_count=len(Packet['claims']),trust=V['trust']))
	Rows.append(f"| {Role} | `{V['reviewer_id']}` | {len(Packet['claims'])}项, APPROVED | [精确回执]({Ref}) |")
Library=json.loads((O/'library-verification.json').read_text())
if Library['status']!='PASS' or Library['available']!=90 or Library['verified_current_obligations']!=19:raise RuntimeError('Current library not verified')
Summary=dict(schema='round11-independent-review-summary/v1',reviews=Reviews,scope='Six distinct fresh fork_context:false reviewers; approvals remain limited to the listed obligations. No complete formalization or canonical acceptance.')
(A/'review-summary.json').write_text(json.dumps(Summary,ensure_ascii=False,indent=2)+'\n')
Table='| 检验 | 独立agent身份 | 义务与结果 | 证据 |\n| --- | --- | --- | --- |\n'+'\n'.join(Rows)
LibraryText=f"实际索引及查询为 **{Library['available']}张可用、1张原撤回**. 原撤回卡仍是 `left-definite-orthogonal-systems.md`. 本轮核对{Library['queried_current_cards']}张关联卡, 包含8张纠错/续审卡和新增卡及其知识关联; 当前19项义务均绑定新回执. 保留{Library['historical_warnings']}条历史警告, 未以删除旧证据或关闭门禁消除它们. [实际检索核对](../../research/artifacts/proof-audit-round11-20260926/integration/library-verification.json)保存精确版本、摘要、依赖和批注身份."
Text=(O/'REPORT.template.md').read_text().replace('{{review_table}}',Table).replace('{{formal_details}}',(O/'formal-details.md').read_text().strip()).replace('{{library_details}}',LibraryText)
if '{{' in Text:raise RuntimeError('Unfilled report placeholder')
Report.mkdir(exist_ok=True);(Report/'REPORT.md').write_text(Text)
Intro='''## 2026-09-26 第十一轮局部形式化

新增 [AuditRound11.lean](SL/AuditRound11.lean): 成对实坐标中的反射/和差变换、条件反对易交叉块和对易对角块、detJ=(-1)^n detC detD、仿射反射增量, 以及显式偶/奇边界矩阵的行列式与唯一实修正. 14个具名定理含13项显式合取根, 12个定义/缩写, 全部导出37项声明. 37项盲读与另一个全新会话的实际重编译、精确根/公理检查及语义比对分别通过. 根公理仅propext、Classical.choice、Quot.sound. 见[第十一轮报告](../reports/proof-audit-round11-20260926/REPORT.md).

`Fin n ⊕ Fin n`的第二半按镜像配对顺序, 不是直接递增的物理接口索引; 此置换桥梁尚未形式化. JP=-PJ是条件. 边界矩阵由条目定义, 未形式化其多项式迹来源、复数桥梁、Sobolev核心、临界迹或余有限分类. 没有完整ODE/Python形式化、全库Lake构建或canonical接收; 原51份SL源保持原字节. 历史条目保留其当时范围.
'''
for N in ['lean-proof/STATUS.md','lean-proof/README.md']:
	P=R/N;S=P.read_text();I=S.index('\n')+1
	if '## 2026-09-26 第十一轮局部形式化' in S:raise RuntimeError('Completion already written '+N)
	P.write_text(S[:I]+'\n'+Intro+S[I:])
P=R/'lean-proof/LEMMA_INDEX.md';S=P.read_text();I=S.index('\n')+1
Defs=json.loads((O/'formal-author/formal-only/packet.json').read_text())['named_declarations']
Index='## 2026-09-26 AuditRound11 additions\n\nThe 26 authored declarations below have a separate 37-entry full export, including generated helpers. Fresh blind readback and another reviewer\'s actual compilation/contract comparison passed. All matrix scalars are real; n may be 0; JP=-PJ remains a premise, and explicit boundary matrices do not formalize their analytic trace identification. [Exact scope and evidence](../reports/proof-audit-round11-20260926/REPORT.md).\n\n'
Index+='| Declaration | Source |\n| --- | --- |\n'+'\n'.join(f'| `{N}` | [AuditRound11.lean](SL/AuditRound11.lean) |' for N in Defs)+'\n'
P.write_text(S[:I]+'\n'+Index+S[I:])
P=R/'AGENTS.md';S=P.read_text().replace('2026-09-26 第十一轮审计修缮 (进行中)','2026-09-26 第十一轮审计修缮 (修订与验收完成)',1)
Anchor='## 2026-09-25 第十轮审计修缮'
Done='第十一轮完成: 两项Jacobian/差分错误已在真实模型中复现, 三个活动程序及四张卡修正. 独立解析补齐固定c>0、0<=s<7/2余有限分类, 含三个临界点和原族非基推论; 12页新PDF、A12/B9地图及理解同步. 六个独立无状态检验通过, 局部Lean14定理/12定义、37声明导出和13项根不等于完整分析形式化. 8张纠错/续审卡19项义务经原版API放行, 新增1卡与8条版本批注; 实际查询90可用/1原撤回, 历史失效记录保留. 原51份Lean、canonical、旧证据及134原untracked/6dirty按字节保护. 插件未改. 精确发布见本轮报告及外部DELIVERY, origin先于fork.\n\n'
S=S.replace(Anchor,Done+Anchor,1);P.write_text(S)
P=R/'state/AGENTS_SESSION_LOG.md';S=P.read_text();I=S.index('\n')+1
Log='''## 2026-09-26 第十一轮审计交付

用户输入: "C:\\Users\\HuangZY\\Downloads\\sl_audit_round11", 指定math-research-workflow2.0.1; 目录首次不可见后补充 "重新看一眼". 再查目录已在, 继续完整修复及既有推送授权.

具体方法与结果: 原12项清单及恢复源码字节核对, 20组输入检查正常/-O回放; 真实R=1反例确认交叉分块和窄层差分路径错误. 三个活动脚本完成修订, 作者86项与独立92项检查、实际四入口及高精度P3比较分别留证. 余有限作者完整展开局部K泛函/四阶核心/临界Fourier证明, 独立解析审查后按精确版本入库; 临界等号归较少迹一侧. 37声明盲读和另一新会话的实际Lean执行/语义核对分离. 六份新fork_context:false最终回执与失败记录保存, 19项纠错/续审义务按原版模块逐步放行, 90可用/1原撤回及8批注实查. 原版逐次全历史检查耗时, 每次结果落盘, 不绕过或重复已完成操作.

维护: 新12页PDF、A12/B9、前沿、理解、README、脚本/Lean导航与续接同步. GitHub首轮TLS预检失败后以单次HTTP/1.1参数读到两个远端基线, 未改全局代理/Git配置. 最终提交、origin后fork推送及远端读回以F:/tools/math-audit-round11-20260926/DELIVERY.json为准. 原dirty/untracked、51旧Lean、canonical与旧冻结证据按字节保护; 不将数值、局部Lean或Git交付误称完整数学认证. 详见reports/proof-audit-round11-20260926/REPORT.md.

'''
P.write_text(S[:I]+'\n'+Log+S[I:])
Resume='''## 2026-09-26 round11 repair and independent verification COMPLETE

Latest user input: C:\\Users\\HuangZY\\Downloads\\sl_audit_round11, workflow2.0.1; follow-up "重新看一眼". Read reports/proof-audit-round11-20260926/REPORT.md and F:/tools/math-audit-round11-20260926/CURRENT.json, then reconcile actual DELIVERY/Git state before any publication retry. Do not restart completed authors or reviews.

Residual-Jacobian CROSS blocks and independent-edge central differences with checked round trips are repaired; commuting Hessian/K blocks remain distinct. Six fresh fork_context:false reviews are APPROVED. The fixed-c>0 cofinite closure classification holds for every0<=s<7/2, including critical1/2,3/2,5/2 with fewer traces at equality; p6 deletion proves the original family cannot be Schauder/Riesz under nonzero scaling/reordering. General infinite deletion, c-uniform estimates and global O1/O2/G1 remain open. New map A12/B9, 12-page PDF and current understanding are synchronized.

Original library API released19 obligations on8 revised/unchanged cards;1 new independently reviewed card and8 version annotations are integrated. Actual query90 available/1 original withdrawn, with12 related exact cards/summary/dependency/source/annotation bindings checked. Preserve historical invalid receipts. Local Lean14 named theorems/12 definitions,37 exported declarations and13-conjunct root have independent actual compilation and semantic review, covering only real paired algebra and explicit boundary matrices; no full ODE, Python, complex/Sobolev/cofinite formalization or Lake rebuild.

Protect baseline4f6b35c,15077 original tracked,134 original untracked/6 dirty,51 old Lean sources, canonical and immutable evidence. All research/review agents completed. Original API calls save incremental results; inspect real current state before resuming, and release identity includes revision plus bundle. Final exact staging and origin-then-fork delivery are recorded externally. No plugin/cache/global configuration change. Older dated entries retain their original scope.

'''
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.1/scripts')
import research_state as S
P=R/'state/RESUME.md';Old=P.read_bytes();Text=Old.decode();I=Text.index('\n')+1
Result=S.save_progress(R,Text[:I]+'\n'+Resume+Text[I:],hashlib.sha256(Old).hexdigest())
(O/'progress-result.json').write_text(json.dumps(Result,indent=2)+'\n')
print('Final report, review summary, Lean navigation, AGENTS/session and progress saved',flush=True)
