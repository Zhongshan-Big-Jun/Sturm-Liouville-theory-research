from pathlib import Path
from collections import Counter
import json

O=Path('/mnt/f/tools/math-audit-round9-20260923')
R=Path('/mnt/f/LaTeX/BVE research')
A=R/'research/artifacts/proof-audit-round9-20260923'
def read(n):return json.loads((O/(n+'.json')).read_text())
def require(v,m):
    if not v:raise RuntimeError(m)
def replace(p,old,new):
    b=p.read_bytes();x=old.encode();y=new.encode()
    if y in b:return
    require(b.count(x)==1,'Replacement identity: '+str(p)+' '+old[:60])
    p.write_bytes(b.replace(x,y,1))

Names=['math-review2','renewal-review','software-isolated-review2','formal-isolated-readback','formal-isolated-semantic']
Final={n:read(n+'-received') for n in Names}
require(all(x['verdict']=='APPROVED' for x in Final.values()),'Missing final approval')
Gate=read('library-final-check');require(Gate['status']=='PASS','Library not ready')
require((A/'formal-review/execution-archive.json').is_file(),'Independent formal execution not archived')
Integration=json.loads((A/'software-final-integration.json').read_text())
require(Integration['exit_code']==0 and Integration['numerical_payload_identical_to_accepted_candidate'],'Software integration not checked')
Report=R/'reports/proof-audit-round9-20260923/REPORT.md'
replace(Report,'本轮仍在验收中; 下文明确区分已确认修复、作者执行和独立检验. 最终工具放行、Lean 独立复验及云端交付记录将在完成后补齐.',
    '四项报告发现及本轮独立复核追加发现均已修复. 数学修订、未变卡片续检、数值程序、Lean 盲读和独立编译/语义核查共五份最终隔离检验通过; 首次退回完整保留. 工具库已恢复78项可用、1项原有撤回. 本报告限定于下述修复, 不代表全项目证明认证.')
replace(Report,'另一新 agent 正在单独重编译并对照非形式合同; 其最终结果将另行登记.',
    '另一新 agent 在新目录亲自执行固定编译器和三个错误目标控制, 对照非形式合同及盲读结果后返回 APPROVED. [独立执行归档](../../research/artifacts/proof-audit-round9-20260923/formal-review/execution-archive.json)保存实际运行证据; 源码、类型/定义导出、根身份、传递公理和环境绑定分别核对, 不以作者机器报告替代独立执行.')
replace(Report,'研究地图、项目理解、双语首页、研究/脚本导航随当前数学范围更新; 工具指针表和续接记录待最终放行后核对.',
    '研究地图、项目理解、双语首页、研究/脚本导航、工具指针表、Lean 状态、AGENTS 和续接记录已随当前数学范围更新.')
replace(Report,'精确暂存、提交及主仓库后 fork 的同步将在最终交付核对中登记.',
    '交付使用精确路径清单与实际 Git blob 字节核对, 主仓库 origin 先推送, fork 后推送; [发布清单](publication-manifest.json)绑定本次全部文件. 提交后的实际双远端 HEAD 与原工作树恢复核对保存在外部工作目录 F:/tools/math-audit-round9-20260923/DELIVERY.json, 不在提交前预写推送成功或自引用提交哈希.')

Rows=[]
Labels={'math-review':'数学首次退回','math-review2':'数学修订最终复核','renewal-review':'12张未变卡续检','software-review':'数值程序首次退回','software-isolated-review2':'数值程序最终复核','formal-isolated-readback':'形式声明盲读','formal-isolated-semantic':'独立编译与语义核查'}
for n,label in Labels.items():
    d=read(n+'-received')
    root=('research/artifacts/proof-audit-round9-20260923/formal-review/' if n.startswith('formal-isolated-') else 'research/artifacts/proof-audit-round9-20260923/software-review2/' if n=='software-isolated-review2' else '')
    path=root+d['bundle']
    require((R/path/'report.json').is_file(),'Missing review report '+n)
    Rows.append(f"| {label} | {d['verdict']} | [{d['reviewer_id'][:8]}](../../{path}/report.json) |")
Counts=Counter(x['classification'] for x in Gate['historical_classifications'])
Section='''## 最终回执与当前检索

| 独立义务 | 实际结论 | 原始结构化报告 |
| --- | --- | --- |
'''+ '\n'.join(Rows)+f'''

三个修订版本已由原纠错模块逐项 RELEASED; 十二张未改数学内容的卡片完成22项同版本续发. [实际工具检索](../../research/artifacts/proof-audit-round9-20260923/current-tool-query.json)及[最终门禁核对](../../research/artifacts/proof-audit-round9-20260923/library-final-check.json)确认78可用、1项原有撤回, 并逐一核对15张当前卡的内容哈希、摘要、依赖和来源状态. 三张修订卡各有版本绑定研究注释.

保留57条历史 REVIEW_NO_LONGER_VALID 警告: {Counts.get('same-current-version-reviewed-again',0)}条对应已重新审查的同一当前版本, {Counts.get('superseded-card-version',0)}条对应被替代版本. 这些历史警告不能当作当前复用授权, 也不能为让页面显得干净而删除. 当前复用由新回执决定.

独立检验回执的原生工具来源强度为 COORDINATOR_ATTESTED_TOOL_TRANSCRIPT. 分别归档实际派发、真实完成内容与插件接收结果; 不将其夸大为外部签名的数学证书. 软件最终复核和形式化复核使用本轮证据下各自的隔离审查项目; 主工具库的修订/续发保持单一写入者. [协调执行证据](../../research/artifacts/proof-audit-round9-20260923/coordinator/manifest.json)记录真实操作、早期失败和队列调整.

'''
data=Report.read_bytes();marker='## 局部形式化的实际范围'.encode()
if '## 最终回执与当前检索'.encode() not in data:
    require(data.count(marker)==1,'Report insertion marker');Report.write_bytes(data.replace(marker,Section.encode()+marker,1))

Status=R/'lean-proof/STATUS.md'
replace(Status,'作者当前实跑通过, 三类错误目标均拒收; 新盲读与独立语义/执行验收进行中, 最终以',
    '作者实跑与另一新目录的独立执行均通过, 三类错误目标均拒收; 全部59声明盲读及另一新会话的语义/执行验收均 APPROVED, 精确证据与边界以')

Agents=R/'AGENTS.md';data=Agents.read_bytes()
Old='- 2026-09-23: 第九轮修订进行中. 以2a81b608d53e3decee04c46716a8d8f8c2d9b1b4为基线, 保存12666个tracked文件与原6项dirty/134项untracked身份. 收入外部四项审计及候选序列补证, 三张工具卡先隔离. 使用已安装2.0.1原版纠错/检验工具; 源码和文档修订、全摘要绑定续检、独立软件检验与Lean局部接口完成前不恢复复用. 具体对话见state/AGENTS_SESSION_LOG.md.'.encode()
if Old in data:data=data.replace(Old+b'\n',b'',1)
Heading='## 2026-09-23 第九轮审计修缮 (研究与验收完成)'
Block='''
## 2026-09-23 第九轮审计修缮 (研究与验收完成)

用户原话: "C:\\Users\\HuangZY\\Downloads\\sl_audit_round9 继续修复", 指定 math-research-workflow 2.0.1. 核对附件和基线2a81b608后修复真实积分投影、有限Green核、归一化导数核项、物理世俗函数频率因子; 新补证仅闭合规定平衡候选序列的单调性与极限, O1/O2、G1仍开放. 两份PDF、研究地图、理解、导航、工具注释和续接记录同步. 详见[本轮报告](reports/proof-audit-round9-20260923/REPORT.md).

方法: 附件作为待核实证据; 作者与无状态fork_context:false检验者分离, 冻结精确输入, 保存原生调用和真实回执. 两次首次退回另修: 卡片集中极限遗漏质量收敛, 极窄脉冲在浮点坐标中塌缩. 五份最终独立检验通过; Lean59声明经盲读及另一个新会话亲自编译/语义核查, 仅认证局部代数接口. 使用已安装2.0.1原版纠错模块释放3张修订卡, 12张未变卡完成22项续发; 实际检索78可用/1原撤回. 保留57条历史失效回执, 不绕过门禁.

保护基线12666个tracked、134个原untracked、6项既有dirty, 49份旧Lean源、历史证据及canonical. 不改插件/cache或全局环境. 外部F:/tools/math-audit-round9-20260923保存真实执行与发布状态; 中断后先核对CURRENT/DELIVERY、实际双远端和原工作树, 不重跑已完成研究者. 精确暂存, origin先于fork推送; 具体对话与操作见state/AGENTS_SESSION_LOG.md.
'''
if Heading.encode() not in data:
    key=b'# \xe9\xa1\xb9\xe7\x9b\xae\xe7\xbb\xb4\xe6\x8a\xa4\n';require(data.count(key)==1,'AGENTS marker');data=data.replace(key,key+Block.encode(),1)
Agents.write_bytes(data)

Resume=R/'state/RESUME.md';data=Resume.read_bytes()
Block='''
## 2026-09-23 ninth-round audit repair completed

Current report: reports/proof-audit-round9-20260923/REPORT.md. The four supplied defects and two independent-review findings are repaired: use true integral constraints for tangency; the normalized eigenfunction derivative needs a kernel term; the one-dimensional reduced Green kernel is bounded; physical F has a varying frequency factor whereas omega*F is reflection symmetric. A nested Jacobi proof gives strict decrease and the limit of the prescribed balanced candidate sequence only. B3 remains PARTIAL; global optimum identification O1/O2 and G1 remain open. Signed concentrated measures need convergent mass for a limit. Unresolvable pulse width/quadrature nodes now cause an explicit CLI error.

Five final fresh fork_context:false reviews approved mathematics, unchanged-card renewals, software, 59-declaration formal blind readback, and independent formal compilation plus semantic matching. The first mathematics/software rejections are retained. Local Lean25 named theorems/13 definitions, a fifteen-conjunct root and actual three negative controls cover finite Euclidean projection, normalization-kernel correction and actual matrix/physical-frequency identities. No formal infinite spectral/Green/ODE/root-count/candidate-limit/global-extremum proof or full Lake build is claimed. Three revised cards and22 same-version issue renewals on12 unchanged cards yield78 available/1 originally withdrawn;15 current summaries, dependencies and source bindings checked. Preserve57 historical invalid-release warnings and use current exact receipts.

Two PDFs were rebuilt and visually inspected; maps, understanding, navigation, annotations and AGENTS are updated. Preserve baseline2a81b608,12666 original tracked files outside the exact change scope,134 original untracked and6 preexisting dirty files,49 old Lean sources, old frozen evidence and canonical. Plugin code/cache and global proxy/environment are unchanged. All research/review agents completed; do not rerun them. External F:/tools/math-audit-round9-20260923 contains actual calls, CURRENT.json, exact-stage verification and post-publication DELIVERY.json. Before retrying interrupted publication, reconcile the delivery receipt with actual origin/fork main HEADs and original worktree bytes; push origin before fork. Earlier entries below are historical.
'''
if b'## 2026-09-23 ninth-round audit repair completed' not in data:
    require(data.startswith(b'# RESUME\n'),'RESUME prefix');Resume.write_bytes(data.replace(b'# RESUME\n',b'# RESUME\n'+Block.encode(),1))

Log=R/'state/AGENTS_SESSION_LOG.md';LogMarker='## 2026-09-23 round9 final independent acceptance'
if LogMarker.encode() not in Log.read_bytes():
    with Log.open('ab') as f:f.write(('\n\n'+LogMarker+'\n\n用户请求: C:\\Users\\HuangZY\\Downloads\\sl_audit_round9 继续修复; 指定math-research-workflow2.0.1. 沿用既有云端同步授权. 核实修复4项报告发现, 独立数学/软件首审各退回1项新缺陷并另版修复. '+
        '最终5份独立APPROVED: '+', '.join(n+'='+Final[n]['reviewer_id'] for n in Names)+'. '+
        '3修订卡释放,12未变卡22续发,78可用/1原撤回,15当前摘要/依赖核对通过;57历史失效回执保留. 当前数值程序f846705159ed经真实项目位置CLI复跑一致. Lean59声明盲读和另一次实际新编译/精确目标/三错误目标/语义核对通过, 不扩张到解析谱结论. 两PDF重建及关键页面目视确认. 地图新增B3-CANDIDATE-LIMIT且B3保持PARTIAL;O1/O2/G1未证. 根AGENTS、RESUME、导航、项目理解同步. 保留49旧Lean、canonical、134原untracked与6既有dirty;最终精确提交与origin后fork发布以外部DELIVERY.json实测为准. 本条按原字节追加, 未归一化混合换行旧日志.\n').encode())

for p,entry in [(A/'AGENTS.md','\n2026-09-23 final maintenance: all four findings and the two fresh-review findings repaired. Five final stateless review approvals, exact library release/query and current-code replay archived. Preserve rejected candidates and raw author/independent execution separately. New coordinator manifests describe actual evidence; publication uses an exact allowlist and original-work protection. See the current report and state/AGENTS_SESSION_LOG.md.\n'),(R/'reports/proof-audit-round9-20260923/AGENTS.md','\n2026-09-23验收维护: 报告已按真实5份最终隔离APPROVED回执、3卡释放/22项未变卡续发和当前程序重放补齐, 保留首次退回与形式化边界. 发布清单仅记录精确文件, 提交后远端结果放外部DELIVERY.json核对, 不预写成功.\n')]:
    if entry.encode() not in p.read_bytes():
        with p.open('ab') as f:f.write(entry.encode())
for p,entry in [(O/'AGENTS.md','\n2026-09-23 acceptance complete: the four submitted findings plus two first-review findings were repaired and five final stateless reviews received. Installed original library APIs released three revisions and22 unchanged-card obligations. Final document, archive and exact-publication helpers are coordinator work, not independent approvals. Preserve frozen packets, original user work and the actual operation records; origin precedes fork.\n'),(A/'formal-review/AGENTS.md','\n2026-09-23: blind readback of59 exports and a different fresh agent\'s actual compiler/three-negative/semantic review approved. Actual completion envelopes were received through the installed runtime; preserve independent execution archive separately from author evidence. Scope remains local algebra, not full analytic spectral formalization.\n'),(A/'software-review2/AGENTS.md','\n2026-09-23: the fresh F1 acceptance review approved40 inputs and3 claims. Archived actual independent execution evidence; exact accepted source f846705159ed was integrated only after the prior rejection was received, then the live project CLI was executed and its numerical payload matched. No arbitrary-parameter numerical error bound is claimed.\n')]:
    if entry.encode() not in p.read_bytes():
        with p.open('ab') as f:f.write(entry.encode())
Current=read('CURRENT');Current.update(status='RESEARCH_ACCEPTED_PUBLICATION_PENDING',stage='final-evidence-and-exact-publication',pending='final metadata checks, exact staged Git blob verification, commit and origin/fork push',remaining_sequence=['archive coordinator evidence','final document/protection checks','prepare and stage exact files; commit; verify local state; push origin then fork; verify delivery'],parent_library_release_session=None,queued_receipt_session=None,current_script_is_first_candidate_until_prior_rejection_received=False,math_review2='APPROVED_RECEIVED_CLOSED',renewal_review='APPROVED_RECEIVED_CLOSED; 22 exact releases completed',formal_semantic_reviewer='APPROVED_RECEIVED_CLOSED',software_review2='APPROVED_RECEIVED_CLOSED; integrated exact approved bytes')
(O/'CURRENT.json').write_text(json.dumps(Current,ensure_ascii=False,indent=2)+'\n')
print('Final documents, AGENTS and byte-appended continuity updated from received evidence.')
