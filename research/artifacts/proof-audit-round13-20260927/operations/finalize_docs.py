from pathlib import Path
import json,hashlib,shutil
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927');A=R/'research/artifacts/proof-audit-round13-20260927';P=R/'reports/proof-audit-round13-20260927'
V=json.loads((O/'final-verification.json').read_text())
if V['indexed']!=89 or any(x['verification']['verdict']!='APPROVED' for x in V['reviews'].values()):raise RuntimeError('Final verification incomplete')
V['release_obligations']=len(json.loads((O/'release-results.json').read_text()))
V['claims_scope']='Scoped Round13 repairs; analytical arguments, exact rational witnesses, finite numerical tests and historical local Lean remain distinct. No new Lean run or full-project theorem certification.'
V['certificate_ledger_sha256']=hashlib.sha256((R/'misc/e1_cert_ledger.json').read_bytes()).hexdigest()
V['certificate_tests']='research/artifacts/proof-audit-round13-20260927/certificate-checks-v2/results.json'
V['reading_versions']=['research/artifacts/proof-audit-round13-20260927/reading-versions.json','research/artifacts/proof-audit-round13-20260927/reading-versions-v2.json']
(P/'verification.json').write_text(json.dumps(V,ensure_ascii=False,indent=2)+'\n')
PathValue=R/'AGENTS.md';T=PathValue.read_text();T=T.replace('第十三轮复核修订 (进行中)','第十三轮复核修订 (修订与验收完成)',1)
Anchor='## 2026-09-26 第十二轮审计修缮'
Paragraph='''第十三轮完成: 57条完整证书重新计算, 有理端点/目标谓词/原语包络/失败传播修复; 节点共同归一化、坐标Green、非正参数传播及一般Jacobian补项修复. 普通/-O性质与第十二轮回归实际通过, 3份最终新隔离回执按当前哈希验收. 首次证书审查退回的CLI负对照、旧引擎漏引用和开闭区域错误已另版修复, 原回执保留. Helly和直接bang-bang前提、研究地图与活动状态同步; 四份活动PDF编译并检查修改页. 原版API接收31项义务, 当前89可用/2阻断(含退役Decimal), 两条版本批注已查询核对. 无新Lean/全局理论扩写, canonical、旧讲义和原6dirty/134untracked保留; 报告见reports/proof-audit-round13-20260927/REPORT.md, 最终发布另核对外部DELIVERY.json及真实远端.

'''
if Paragraph not in T:T=T.replace(Anchor,Paragraph+Anchor,1)
T=T.replace('- 旧文档中 G2 的闭合范围表述存在差异, 需要按定义与量词对齐. 本轮维护不改写历史证明来消除差异.','- G2 当前活动入口已区分: 全部残差零点且含 R↓1 的一致桥梁仍待证; 历史符号相容分支且 R0>1 的有限结论不被扩大. 第十三轮对齐活动量词, 历史证明/日志保持原字节.')
PathValue.write_text(T)
Entry='''
## 2026-09-27 第十三轮修订与范围验收完成

用户具体要求: “请基于我提供的第十三轮复核包，直接修复……实际工作区”, “每项ok必须验收该行完整命题”, “普通模式和-O下的重要拒绝逻辑均应有效”, “达到上述目标后结束”. 逐项关闭表和证据入口为 reports/proof-audit-round13-20260927/REPORT.md. 输入基线4a82d3c与实际接手源码相符; 没有用附件旧源码覆盖活动文件.

修复证书完整合同、精确有理端点及正确包络, 重算57条; 修复节点质量归一化、任意点序Green/端点/非正参数及非驻点Jacobian. 普通/-O执行、独立质量积分/Green匹配/隐式求导与原R12性质回归分别留证. Helly补齐TV、闭性和半连续性, 保留不取到反例及可测盒存在性; 不撤回A1/A12、相容Legendre、正确驻点公式和原扇区区分. 研究地图/活动总览/稳定性/比值前提与四份阅读PDF已同步, 修改页实际检查.

作者和最终fork_context:false审查者分离. 首次证书回执CHANGES_REQUIRED指出CLI参数导致假负对照、漏掉的旧引擎引用以及开闭区域表述; 已修复并换全新隔离审查, 原错误测试与退回记录保持冻结. 三份最终回执APPROVED仅适用于各自列明的当前义务. 原版工具纠错接收31项修订/续审, 默认查询89可用、2阻断, 旧Decimal保留历史而禁止可信复用. 两条精确版本批注另记应用边界. 未执行新Lean、全库CI或完整数学认证; 无canonical/插件代码改动. 原17892tracked之外的允许变更范围、6dirty/134untracked及精确提交blob另核对; origin先于fork,真实推送结果记录外部DELIVERY.json. 完成本轮后停止理论扩写.
'''
PathValue=R/'state/AGENTS_SESSION_LOG.md';T=PathValue.read_text()
if Entry not in T:PathValue.write_text(T+Entry)
Entry='''## 2026-09-27 round13 repair and independent verification COMPLETE

Read reports/proof-audit-round13-20260927/REPORT.md and verification.json, then F:/tools/math-audit-round13-20260927/CURRENT.json and DELIVERY.json plus actual Git state before retrying publication. Do not restart completed authors/reviews. The baseline is 4a82d3c; original17892 tracked,134 untracked and6 dirty remain protected outside the declared scope.

57 exact certificate contracts retain nonzero/strict targets and directed endpoints. Physical-state mass normalization, coordinate Green kernels and nonpositive-parameter propagation, general residual Jacobian and R12 identities are repaired. Helly topology/closedness/semicontinuity and active A1/A12/G2 scope are aligned. Three final fresh reviews pass; first certificate rejection and earlier failed attempts remain.31 obligations on20 current cards were received through original APIs;89 usable/2 blocked, including retired Decimal. Four PDFs were built and modified pages inspected. No new Lean or canonical integration, no global G1/M3/KP extension. Stage only exact Round13 paths; deliver origin before fork and verify remote heads. Older entries remain historical.

'''
PathValue=R/'state/RESUME.md';T=PathValue.read_text()
if Entry not in T:PathValue.write_text(T.replace('# RESUME\n\n','# RESUME\n\n'+Entry,1))
PathValue=P/'REPORT.md';T=PathValue.read_text();T=T.replace('最终回执登记于本报告旁的 `verification.json`，以原版工具的当前哈希核验为准。','修后由另一名全新隔离审查者验收通过。三份最终回执及当前哈希复验详见 [verification.json](verification.json)。')
T+='\n最终工具库接收 31 项义务，涉及 20 张当前卡；默认检索实查 89 张可用、2 张阻断（原有撤回卡与退役 Decimal）。两条版本绑定应用批注已接入；这不把所有卡升级成全定理证明。\n'
PathValue.write_text(T)
print('Final reports, AGENTS, dialogue log and RESUME updated')
