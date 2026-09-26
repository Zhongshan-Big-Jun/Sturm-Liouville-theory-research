from pathlib import Path
import hashlib
import json
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = Root / 'research/artifacts/proof-audit-round12-20260926'
Report = Root / 'reports/proof-audit-round12-20260926'
Names = ['math-review', 'renewal-review', 'software-review2', 'formal-readback2', 'formal-comparison']
Roles = ['三张修订卡及解析证明', '未变卡精确版本续审', '实际软件与有限数值执行', '59 项完整声明盲读', '独立 Lean 执行及契约比对']
Reviews, Rows = [], []
for Name, Role in zip(Names, Roles):
	Verified = json.loads((Out / (Name + '-verified.json')).read_text())
	Packet = json.loads((Out / (Name + '-packet.json')).read_text())
	if Verified['verdict'] != 'APPROVED' or Verified['packet_sha256'] != Packet['packet_sha256']:
		raise RuntimeError('Missing current approval: ' + Name)
	Location = Out / (Name + '-root.json')
	Project = Path(json.loads(Location.read_text())['project']) if Location.exists() else Root
	Bundle = (Project / Verified['bundle']).relative_to(Root).as_posix()
	Frozen = json.loads((Project / Packet['packet']).read_text())
	Reviews.append(dict(kind=Name, role=Role, verdict='APPROVED', reviewer_id=Verified['reviewer_id'], packet_sha256=Verified['packet_sha256'], bundle=Bundle, input_count=len(Frozen['inputs']), claim_count=len(Frozen['claims']), trust=Verified['trust']))
	Rows.append(f"| {Role} | `{Verified['reviewer_id']}` | {len(Frozen['claims'])} 项，APPROVED | [精确回执](../../{Bundle}/report.json) |")
if len({Row['reviewer_id'] for Row in Reviews}) != 5:
	raise RuntimeError('Independent reviewer identities are not distinct')
Library = json.loads((Out / 'library-verification.json').read_text())
if Library['status'] != 'PASS' or Library['available'] != 90 or Library['original_withdrawn'] != 1:
	raise RuntimeError('Library verification incomplete')
Summary = dict(schema='round12-independent-review-summary/v1', reviews=Reviews, retained_nonapprovals=['software-review CHANGES_REQUIRED', 'formal-readback INCOMPLETE'], scope='Five distinct final fork_context:false reviewers; local declared scopes only. No complete formalization or canonical acceptance.')
(Artifact / 'review-summary.json').write_text(json.dumps(Summary, ensure_ascii=False, indent=2) + '\n')
Table = '| 检验 | 独立 agent 身份 | 义务与结果 | 证据 |\n| --- | --- | --- | --- |\n' + '\n'.join(Rows)
LibraryText = f"实际索引和查询为 **90 张可用、1 张原撤回**，原撤回卡仍为 `left-definite-orthogonal-systems.md`。本轮 {Library['verified_current_cards']} 张当前卡共 {Library['verified_current_obligations']} 项纠错/续审义务经原版 API 放行，保留 {Library['historical_warnings']} 条历史失效回执提示。[实际检索核对](../../research/artifacts/proof-audit-round12-20260926/integration/library-verification.json)保存精确版本及绑定。"
Text = (Out / 'REPORT.template.md').read_text().replace('{{review_table}}', Table).replace('{{library_details}}', LibraryText).replace('{{formal_details}}', (Out / 'formal-details.md').read_text().strip())
if '{{' in Text:
	raise RuntimeError('Unfilled report placeholder')
(Report / 'REPORT.md').write_text(Text)
(Artifact / 'README.md').write_bytes((Out / 'ARTIFACT_README.template.md').read_bytes())

def replace_exact(Name, Before, After):
	Path = Root / Name
	Raw = Path.read_bytes()
	Old, New = Before.encode(), After.encode()
	if Raw.count(Old) != 1:
		raise RuntimeError('Unexpected active text occurrence: ' + Name)
	Path.write_bytes(Raw.replace(Old, New, 1))

replace_exact('README.md', '第十二轮修订进行中', '第十二轮修订与独立验收完成')
replace_exact('README_EN.md', 'round12 repair in progress', 'round12 repair and independent verification completed')
replace_exact('docs/research-guide.md', '正在进行独立检验.', '修订卡、解析推导、实际程序执行和局部形式化已分别通过独立检验.')
replace_exact('literature/maps/FRONTIER.md', '半问题谱身份与原 K / SKS 的扇区对象正在修订及隔离检验.', '半问题谱身份与原 K / SKS 的扇区对象已完成修订及隔离检验.')
replace_exact('scripts/README.md', '六份活动程序修改与两份历史 debug 调用的静态范围', '四份活动程序与两份历史 debug 调用的修改及检验范围')
replace_exact('research_map.md', 'round12 half-spectrum/pole/sector repair under independent review', 'round12 scoped half-spectrum/pole/sector repair independently reviewed')
replace_exact('research_map.md', '| B10 | Half-spectrum identity, bound poles and raw/conjugated sectors | UNDER REVIEW |', '| B10 | Half-spectrum identity, bound poles and raw/conjugated sectors | SCOPED REPAIR VERIFIED |')
replace_exact('AGENTS.md', '2026-09-26 第十二轮审计修缮 (进行中)', '2026-09-26 第十二轮审计修缮 (修订与验收完成)')
Anchor = '## 2026-09-26 第十一轮审计修缮'
Done = f"第十二轮完成: 六份程序与三张工具卡修复半谱、极点身份及原/共轭扇区传播；同时撤回负秩一项的错误减号充分判据。136 项普通/-O回归及独立实际执行通过。首轮软件溢出发现和首轮 Lean 类型省略导致 INCOMPLETE 均保留，修复后换全新会话复验。五个最终独立检验通过，原版模块完成 {Library['verified_current_obligations']} 项纠错/续审义务，实际90可用/1原撤回及3条精确批注实查。Lean59声明及真实坐标/归一化桥接只认证有限实矩阵代数。B10、理解、前沿、导航和续接同步；52旧Lean、canonical、历史证据及原134untracked/6dirty按字节保护。发布依次origin、fork，以本轮报告及外部DELIVERY.json为准。\n\n"
replace_exact('AGENTS.md', Anchor, Done + Anchor)
Insight = '负半定秩一项的符号也须贯穿全部判据: 若块按 A+E 定义，研究 A−E 的下界并不能证明该块正定。正确的负秩一判据先要求 A 正定，再检查对应标量是否小于 1；移植到另一扇区或 INF 必须重新核对符号。这条有限维教训和未证研究方向应分开保存。\n\n'
replace_exact('docs/PROJECT_UNDERSTANDING.md', '由此得到的研究方向 (未证):', Insight + '由此得到的研究方向 (未证):')
Intro = '''## 2026-09-26 第十二轮局部形式化

新增 [AuditRound12.lean](SL/AuditRound12.lean): 对任意自然数 n（含0）和实矩阵，建立真实配对/递增坐标 Equiv、反转与交错符号、基的 Gram 矩阵、sqrt(2) 归一化、原 K 与 SKS 的镜像压缩交换、奇秩一项存留及 n=1 反例。22 个作者定义/缩写，10 个主要定理含九项根，完整导出59声明。独立完整盲读与另一个新会话的实际 Lean 执行/契约比对通过；公理闭包仅 propext、Classical.choice、Quot.sound。首轮含省略号的导出和 INCOMPLETE 回执保留。见[第十二轮报告](../reports/proof-audit-round12-20260926/REPORT.md)。

压缩交换不以 K 对称或与反转对易为前提；不变子空间分块另需对易。新文件补上自身配对模型到递增坐标的桥梁，不追改旧源或宣称旧命题新增全模型认证。未形式化 Green/ODE、相位单调性、数值 Python、惯性指标/Sylvester 定律或全局 G1。原52份SL源和依赖保持原字节，未作全库Lake构建或canonical接收。
'''
for Name in ['lean-proof/STATUS.md', 'lean-proof/README.md']:
	Path = Root / Name
	Raw = Path.read_bytes()
	At = Raw.index(b'\n') + 1
	if '第十二轮局部形式化'.encode() in Raw:
		raise RuntimeError('Lean entry already exists')
	Path.write_bytes(Raw[:At] + ('\n' + Intro).encode() + Raw[At:])
Source = (Out / 'formal-author/project/AuditRound12.lean').read_bytes()
if hashlib.sha256(Source).hexdigest() != '21f0a2d46770474e6c32f78ead52c977dcec2f0e589308584d5499c253efa768':
	raise RuntimeError('Lean source drift')
(Root / 'lean-proof/SL/AuditRound12.lean').write_bytes(Source)
Definitions = json.loads((Out / 'formal-export2/declarations.json').read_text())
Declarations = [Row['name'] for Row in Definitions if Row['name'].count('.') == 1]
if len(Declarations) != 32:
	raise RuntimeError('Authored declaration count differs')
Index = '## 2026-09-26 AuditRound12 additions\n\n32 authored declarations; complete 59-entry export includes generated helpers. All n including zero, real matrices, actual coordinate Equiv, normalized compression and odd rank-one algebra. [Scope and independent execution](../reports/proof-audit-round12-20260926/REPORT.md).\n\n| Declaration | Source |\n| --- | --- |\n' + '\n'.join(f'| `{Name}` | [AuditRound12.lean](SL/AuditRound12.lean) |' for Name in Declarations) + '\n\n'
Path = Root / 'lean-proof/LEMMA_INDEX.md'
Raw = Path.read_bytes()
At = Raw.index(b'\n') + 1
Path.write_bytes(Raw[:At] + ('\n' + Index).encode() + Raw[At:])
Log = f'''\n## 2026-09-26 第十二轮审计完成与交付记录

用户原话: “C:\\Users\\HuangZY\\Downloads\\sl_audit_round12 继续修订”，指定工作流2.0.1。延续原先修复和推送授权。附件16项清单及9函数AST核对；34项原检查与完整旧源码的失败分别回放。修复DD/DN指标身份、共享谱表去极点、原K/SKS扇区及H/E/秩一判据传播。程序136项普通/-O回归和独立执行通过。第一次软件审查的极端溢出问题修复后由新会话复验；首次Lean盲读发现根类型省略，实际完整导出后换新会话，另由独立检验者亲自重编译与比对契约。原失败和协调器导出工具失败全部留存。

采用原版纠错API逐事项修订/续审/放行，{Library['verified_current_cards']}张当前卡的{Library['verified_current_obligations']}项义务核对，90可用/1原撤回和3条当前批注实查；不以重写历史或绕过门禁恢复可用。B10、项目理解、前沿、双语首页、脚本/Lean/工具导航和续接检查点同步。原52份SL Lean、canonical、旧冻结证据及134原untracked/6dirty保留字节。局部Lean和有限数值不宣称全Green/ODE、全R符号或G1。精确提交及origin后fork实际读回见F:/tools/math-audit-round12-20260926/DELIVERY.json。\n'''
with (Root / 'state/AGENTS_SESSION_LOG.md').open('ab') as Stream:
	Stream.write(Log.encode())
Resume = f'''## 2026-09-26 round12 repair and independent verification COMPLETE

Latest user input: C:\\Users\\HuangZY\\Downloads\\sl_audit_round12, workflow2.0.1, "继续修订". Before any retry read reports/proof-audit-round12-20260926/REPORT.md, F:/tools/math-audit-round12-20260926/CURRENT.json and actual DELIVERY/Git state. Do not restart completed authors or reviews.

Indexed DD/DN half spectra, immutable shared pole tables, raw K versus SKS sectors and H/E fields are repaired. Correct n2 normalized Green formulas and rank-one criterion are in analytic-repair.md and three current cards. All five final stateless reviews passed after preserving a software CHANGES_REQUIRED and formal-readback INCOMPLETE. Current library{Library['verified_current_obligations']} obligations/{Library['verified_current_cards']} cards,90 available/1 original withdrawn,3 exact annotations verified through original APIs. No new mathematical card was added. Local Lean59 declarations establish finite real matrix/coordinate/normalization identities only; no complete Green/ODE/Python/inertia or interval certification.

Maps B10 and understanding/navigation are synchronized; round11 cofinite classification keeps its accepted scope. Global signs, G1, all-R branches and certified spectral tails remain open. Baseline be7c091,16541 tracked,134 original untracked,6 dirty and52 old SL Lean sources protected, including canonical and frozen history. Final exact staging and origin-then-fork delivery are external records. Keep all failed attempts and original invalid historical receipts.\n\n'''
Path = Root / 'state/RESUME.md'
Raw = Path.read_bytes()
Text = Raw.decode()
Start = Text.index('## 2026-09-26 round12 repair')
End = Text.index('\n## ', Start + 3)
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.1/scripts')
import research_state as State
Result = State.save_progress(Root, Text[:Start] + Resume + Text[End:], hashlib.sha256(Raw).hexdigest())
(Out / 'progress-result.json').write_text(json.dumps(Result, indent=2) + '\n')
print('Final report, maps, Lean source/navigation, AGENTS and continuity written', flush=True)
