from pathlib import Path
import json,hashlib,datetime
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A='research/artifacts/proof-audit-round8-20260922';P=R/'reports/proof-audit-round8-20260922';P.mkdir(exist_ok=True)
def read(n):return json.loads((O/(n+'.json')).read_text())
reviews={n:read(n+'-received') for n in ['certificate-review','math-review','formal-readback','formal-semantic','renewal-review','summary-review']}
if any(d['verdict']!='APPROVED' for d in reviews.values()):raise RuntimeError('Pending review')
lib=read('library-final')
if lib['status']!='PASS':raise RuntimeError('Actual query not passed')
(P/'.gitattributes').write_text('* -text\n')
review_rows='\n'.join('| '+n+' | `'+d['reviewer_id']+'` | APPROVED | [原始结论](../../'+d['bundle']+'/report.json), [实际调用](../../'+d['bundle']+'/spawn.json), [完成回执](../../'+d['bundle']+'/completion.json) |' for n,d in reviews.items())
cards='\n'.join('| ['+n+'](../../'+c['location']+') | `'+c['sha256']+'` |' for n,c in lib['cards'].items())
report=r'''# 第八轮审计修订报告

日期: 2026-09-22. 输入为用户提供的 `sl_audit_round8` 全部11份文件, 按待核查证据处理. 基线为 `d1462eb444938554b17da1db398763b31efb4ef4`. **本轮五项发现与直接传播已修订, 解析证明、精确证书和所列局部 Lean 分别通过新的隔离检验.** 这不是全项目重新认证.

当前主证明为 [TeX](../../docs/SL_gap_n1_inf_limit_proof.tex) / [11页PDF](../../docs/SL_gap_n1_inf_limit_proof.pdf). [n=1主文稿](../../docs/SL_gap_n1_proof.tex)与[谱综述](../../docs/SL_spectral_topics_summary.tex)的 INF 部分同步更新. 研究入口见[地图](../../research_map.md)、[项目理解](../../docs/PROJECT_UNDERSTANDING.md)、[工具库](../../tools/README.md).

## 逐项处理

| 发现 | 核实与修订 | 当前证据 |
| --- | --- | --- |
| R8-F01 根像上端点取反 | 旧05把右端参数的根下界当作像上界. 新证书采用正确方向的根与单调像包络; 全部证明运算为有理数 | Fraction证书、端点异号、独立精确/符号重放 |
| R8-F02 超越函数漏包 | 一次nextafter不能控制libm误差; 未包络的v与浮点pi终点也不能作可靠边界 | Machin交错界、Taylor余项、显式除法守卫; 旧libm反例按实际平台另记 |
| R8-F03 连续域漏覆盖 | 原B/D曲边条带、任意小w及无穷R尾部没有完整覆盖. 新主证明用全域连续相位界替代网格作用 | 全域解析下界与隔离数学审阅; Lean只证明明确曲边见证 |
| R8-F04 无条件奇相位分支 | 全域使用无极点匹配; theta2>pi/2及delta方程明确限制R>=1500,w>=2 | 真正偶/奇基态识别; R=1600,u=1/1600的反例及带谱前提的局部Lean |
| R8-F05 固定u误差阶 | 对t=1/R的解析隐函数展开给C(u)/R, 驻点系数严格正 | 解析导数、内部紧区间余项; Lean检查实际C/S定义之间的三角及代数桥接 |
| P01-P03 直接传播 | 余切Laurent幂次改为2k−1; 只称紧子区间一致收敛; arctan上界趋pi/2而非发散; 更新u*、证据指针、工具摘要与依赖 | 四卡精确版本复核与实际默认查询 |

原05/16/19源文件和历史输出保持原字节, 当前正文、工具卡与脚本导航撤回其相关认证作用. 17/18及其它未重跑程序保留历史地位. 本轮没有重新运行旧全域网格或完整全仓扫描. 第七轮主链和左定成果没有因这些发现被自动撤回.

## 替代证明与新增理解

令 epsilon=R^(-1/2), ell=1/2−u, w=u/epsilon, G=R(lambda2−lambda1). 对全部R>=1,0<u<1/2,

    G >= pi^2 / [2*epsilon*(w+ell)*(w+epsilon*ell)].

证明使用射击接口向量的连续展开相位. 第一偶模与第二奇模在半区间对应相位pi/2与pi; 控制相位增长速度及第一频率, 得到实际谱隙下界. 对整个R>=1500,0<w<=2,

    G > (2888/765)*pi^2 > 15*pi^2/4 > 3*pi^2 > M.

大w区域的新引理A''只需初等粗界d1>4alpha、d2<3alpha, 得到

    G > Dbar(u) + ell/(R*u^3) > Dbar(u),  R>=1500, w>=2.

结合T2的唯一极小点和端点结构, T1不再需要旧二维覆盖或T3高精度数值. 有

    R*m_R -> M,    0 <= R*m_R-M = O(1/R),

且误差eta_j>=0、R_j*eta_j->0的任意近极小化子均趋于u*. 这仍限于明确的对称阱族.

T3作为独立数值定位结果重新证明:

    u* in [0.32992250812006654958, 0.32992250812006654960],
    M  in [24.9438661384324768968, 24.9438661384324769084].

固定内部u另有G=Dbar+C(u)/R+O_u(R^-2), 余项在内部紧区间上一致. 在u*处C=pi^2(1/2−u*)/[3(u*)^3]>0, 约15.5807908501. 未据此声称最优值的精确首项系数、最优参数速度、全端点一致展开、非对称族或高阶间距结论.

新的研究经验是把覆盖问题转为连续相位控制, 并把主证明所需粗界与辅助细常数分开. 更多层的相位导数传播是待证想法, 已作为带版本的经验批注和人机讨论入口记录, 没有升级为通用定理.

## 独立验证

所有最终检验均由新的 `fork_context:false` 会话承担, 作者身份列入冻结包排除表. 检验者只接收所列冻结材料; 证书和Lean复跑写入各自的独立目录, 其它检验使用只读审查或临时计算. 这是明确的会话/文件访问范围, 不声称操作系统级沙箱或服务方加密证明. 下面的原生调用、实际完成结果和输入哈希均保留.

| 检验 | 新会话 | 结论 | 绑定证据 |
| --- | --- | --- | --- |
__REVIEWS__

精确证书独立执行: 附件22项在普通/-O下通过; 19组证书检查在普通、-O、-S、-O -S下通过; 14个负对照在四种模式共56次按对应守卫失败. 检验者自行增加3950条边界断言, 在-S及-O -S各通过一次, 并通过22项符号/端点核对. 源码、所有输出和来源检查见[独立证书工件](../../research/artifacts/proof-audit-round8-20260922/certificate-reviewer/), [证书源码](../../research/artifacts/proof-audit-round8-20260922/certificate/certificate.py). 数值抽样与平台特定的libm观察仍不证明连续域或无限极限.

局部Lean新增[AuditRound8.lean](../../lean-proof/SL/AuditRound8.lean), 15个手写定理与11个定义, 连同21个编译器辅助定理共47项公开声明. 九合取根对象与预期类型匹配; 盲读、另一会话的新编译及语义对照分别留证. 正目标通过, 三个错误目标实际编译失败. 传递公理限于propext、Classical.choice、Quot.sound. Lean4.31.0与Mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` 的实际工件身份见[作者环境与原始尝试](../../research/artifacts/proof-audit-round8-20260922/lean-author/)和[独立执行](../../research/artifacts/proof-audit-round8-20260922/formal-reviewer/).

**形式化边界:** 谱min-max仍为显式前提; I2的定义是闭式表达式, 不是已形式化的积分识别. 完整相位速度/T1证明、解析隐函数及余项、无穷维谱分析与全局收敛没有因此全部形式化. 本轮未做全项目Lake build. 48份旧SL源码和环境配置保留原字节.

## 工具库、文献与恢复

事项 `round8-inf-limit-certificates` 先隔离四张旧卡. 新卡逐张声明摘要、范围、源文件与依赖哈希, 经四项“精确版本×事项”义务审查后放行. 随后的实际查询仅70张可用、9张隔离: 综述INF段落更新使第六轮绑定整份综述的审查失效, 额外影响八张内容未变的左定工具卡. [失败状态](../../research/artifacts/proof-audit-round8-20260922/retrieval-before-renewal.json)原样保留. 对旧包逐个输入核对, 只有该综述变化; 新隔离会话对八卡涉及的18项既有义务逐一复核, 以新审查续发原修订的放行回执, 没有伪造新卡版本或改写旧包.

数量恢复78/1后, 内容检查再次拒绝了旧摘要: 八张原字节卡没有显式summary字段, 索引沿用了历史文本; 其中三张摘要与当前正文不同, Krein摘要仍显示错误的二阶导数边界与过时的开放状态. 另外两张分别为jump-stability和leftdef-o1pld-l2-structural, 残留旧增长分类及已被反证的尾部声明. 没有把缺少显式summary本身判作数学错误. 使用已有from-index恢复接口生成候选索引, 从当前正文逐字提取摘要, 经另一个新隔离会话核对后才替换派生索引. 所有卡片、依赖、放行状态和其它索引行保持原样; [前后对比](../../research/artifacts/proof-audit-round8-20260922/summary-recovery/comparison.json)及失败查询保存.

最终实际查询恢复78张可用、1张原隔离, 且当前正文与摘要一致. 本轮共四张修订卡与八张原字节卡, 22项精确事项义务; 全部12张的版本与检索摘要核对. 原隔离卡仍为left-definite-orthogonal-systems. __WARNINGS__个历史失效回执保留, 分为17个已有后继版本的旧回执及18个同一版本已有新审查的旧回执; 没有删除警告来制造通过. 详见[默认查询](../../research/artifacts/proof-audit-round8-20260922/default-query.json)、[库状态](../../research/artifacts/proof-audit-round8-20260922/library-final.json)、[续审身份和唯一变化](../../research/artifacts/proof-audit-round8-20260922/renewal-identities.json).

| 当前卡 | 精确SHA-256 |
| --- | --- |
__CARDS__

余切部分分式来源为实际读取的[NIST DLMF4.22.3](https://dlmf.nist.gov/4.22.E3). 库内source_id为 `bb729c250eb36b380f0ab4f7be158562340ba3b2bf505887681952e3aab405e6`. 保存的是实际web工具响应和明确标明的公式转录, 不是声称下载到网站原始TeX; 原始TeX读取失败也被保留. 未宣称读过所引参考书. 当前卡可通过来源指针和精确版本批注接续研究.

维护使用已有维护版插件的三份原字节运行时模块. 缓存2.0缺少的纠错接口由已有维护版提供, 没有改插件源码或绕过门禁. 库事务复用上一轮验证过的私有POSIX运行时, 新操作日志独立保存; 没有修改全局环境、代理或网络配置.

## 失败记录与交付范围

保留附件中的原符号检查失败日志, 但没有收到那次失败的原源码版本和退出码回执, 因而不补写. Lean作者早期证明、导出器和公开声明数量检查失败均留原字节, 最终接受的是完成的新执行. 独立Lean检验自身三次Python检查器失败涉及嵌套合取解码、投影依赖和额外生成的定义方程; 修正后的9102项结构/精确算术检查通过, 失败源码和退出回执保留. 独立新编译核对16511项传递依赖、4427个外部模块的17708件导入工件及10个运行时二进制; 导入工件核对身份后复用, 没有重编整个Mathlib. 全部错误目标失败属于设计的负对照, 与基础设施失败分开.

解析作者原完成通知到达时, 一条排队跟进消息使后续等待得到超时; 该超时原样保存并明确不是完成或独立验收回执. 作者包自身清单逐字节核对; 最终数学接受来自另一个新会话. 见[作者编排说明](../../research/artifacts/proof-audit-round8-20260922/orchestration/sliver-provenance-note.json).

三份PDF重建为11/17/20页, 主证明全页及两个伴随文稿的改动页已目视检查; 构建成功不代替数学证明. [版面检查](../../research/artifacts/proof-audit-round8-20260922/pdf-visual-check.json)给出精确页范围. 当前地图、项目理解、中英文首页、研究导航、工具及脚本入口、Lean状态、AGENTS和续接记录同步更新.

基线10236个跟踪文件、134个原未跟踪文件与6项原脏文件以字节身份保护. canonical Blueprint与先前冻结证据保持原字节; 本轮不向canonical写入新数学节点. [发布清单](publication-manifest.json)绑定本轮精确提交范围; 提交后按主仓库、fork顺序推送并检查实际远端HEAD和提交blob. 最终提交与云端状态由项目外 `F:/tools/math-audit-round8-20260922/DELIVERY.json` 记录, 避免把提交自身哈希写入自身内容的循环.

若交付中断, 从 `state/RESUME.md` 与项目外 `CURRENT.json`/`DELIVERY.json` 核对实际状态. 不重复已经完成的研究或检验会话, 不改写冻结证据, 不把“等待超时”改作通过.
'''
report=report.replace('__REVIEWS__',review_rows).replace('__CARDS__',cards).replace('__WARNINGS__',str(lib['distinct_historical_warning_releases']))
(P/'REPORT.md').write_text(report)
print('Final scoped report written',len(report),'characters',flush=True)
