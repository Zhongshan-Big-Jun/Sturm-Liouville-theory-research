# 第十五轮交付: 三项有限义务

基线及实际起点 HEAD: `ec45bf99ae746b0a3699557e06700a3c00c5a831`. 日期: 2026-10-05. 已直接修订实际工作区, 未扩大到本科讲义、全部历史重审或新理论任务. 本轮没有新云端发布/Lean/canonical回执.

| 编号 | 当前关闭状态 | 证据 |
| --- | --- | --- |
| R15-01 | 已修复并独立软件复审通过 | [活动入口](../../scripts/op03_gap_fixed.py), [92项修后测试](../../research/artifacts/proof-audit-round15-20261005/checks.py), [独立软件回执](../../research/artifacts/proof-audit-round15-20261005/software-final-review.md) |
| C15-A11-SCALE | 已证明并独立初审及最终整合复审通过 | [完整证明第1--6节](../../docs/SL_full_window_deletions_and_finite_constraints.md), [最终独立解析复审](../../research/artifacts/proof-audit-round15-20261005/integration-final-review.md) |
| C15-A3-KREIN | 已证明并独立初审及最终整合复审通过 | [完整证明第7节](../../docs/SL_full_window_deletions_and_finite_constraints.md), [有限约束卡](../../tools/krein-finite-constraint-filtering.md) |

## 实际修改与数学范围

`lams_precise` 保留兼容名称, 委托已有 `indexed_roots(..., RightBoundary='D')`, 返回频率 omega, 特征值为 omega². 原固定网格不是经另一套加密替换. 实际旧源 k=1/3/6 及 R4 正对照在 [baseline-reproduction.json](../../research/artifacts/proof-audit-round15-20261005/baseline-reproduction.json): k3 首项3.2657957507789526由独立物理零点数证实为第五模态. 修后首三频率0.7462197727914001、0.7604843852750858、2.2352811194758186, 数量/位级前缀稳定. tol 成为括号宽度<=tol*max(1,omega)的实际请求, binary64未分辨则拒绝; 松请求仍受共享身份守卫约束. smax_scale 默认5兼容静默, 非默认有限正值发出弃用警告, 非法值拒绝. 传播及加权归一化未改, 无任意最小块宽. [13个直接导入者清点](../../research/artifacts/proof-audit-round15-20261005/callers.json)明确哪些文件实际调用, 哪些独立网格不在本轮重认证范围. FH保留原坐标/平方转换并实跑四个R4点; 反例不扩大为所有旧R4数据错误.

完整新证明保持固定c>0、真实复Hc^s、全部0<=s<7/2及任意N量词. 两奇偶倒数和均发散时, 闭包精确为I(s)遗漏列对应中心迹的坐标核交; 任一和收敛则无限余维. 稠密iff两和均发散且I(s) subset N. I(s)在[0,1/2]、(1/2,3/2]、(3/2,5/2]、(5/2,7/2)分别为{}、{0}、{0,1}、{0,1,4}. 迹对应f(0)、f'(0)、f''(0), 三个临界等号取较少迹.

新增桥从X=H4 intersect ker B出发, 用p4,p5的第二层残差矩阵进入真实D(Kc²), 才得到到目标范数的有界包含. 跨零点的四阶弱导数/H4值全纯及四次增长、复线性变量顺序、Blaschke唯一性、2m-6与m3连续边界均独立核对; 零化泛函等价后才用A12. 收敛侧的Cauchy Gram无限乘积和有限维商反证给无限L2障碍, 限制到Hc^s连续且单射. 本轮定点核实经典引理于原作者 [Liehr arXiv:2409.17563v1, §2 Lemma2.1](https://arxiv.org/html/2409.17563v1#S2); 没有使用其Gaussian平移结论代替本模型证明.

有限连续复线性约束共同核V中, 逐个成员筛选NV={n:p_n in V}完备iff V是I(s)中一部分中心迹坐标核的交. 有限余维排除收敛奇偶侧; 发散侧给必要性; diag(1,1,-4)给充分性及1/2/4/8个不同子空间. 不等于先组合再约束或正交投影.

## 真实执行与独立审查

| 检查 | 普通 | -O | 范围 |
| --- | ---: | ---: | --- |
| 附件基线44项隔离重放 | 44/44 | 44/44 | 保留确认基线错误的期待, 不是修后验收 |
| 实际当前完整源码修后性质 | 92/92 | 92/92 | 首6模态、数量/前缀、异常/参数、R4质量/FH、旧守卫与局部精确代数 |
| 第十四轮驻点旧回归 | 62/62 | 62/62 | 伪驻点/未收敛拒绝, SUP/INF正对照、质量/一般J |
| 第十四轮核旧回归 | 143/143 | 143/143 | DD/DN、模式/目标/几何/覆盖/分母、rawK/SKS |
| 独立软件审查者重放 | 92/92 | 92/92 | 冻结实际完整源及物理参考 |
| 审查者额外独立检查 | 103/103 | 103/103 | 80位物理局部二分/零点数、实际质量求积、故障注入、短块不裁剪 |

解释器为已安装Python3.10 (numpy2.2.6/scipy1.15.3/mpmath1.3.0/sympy1.14.0). 实际命令、stdout/stderr及结果在 [results](../../research/artifacts/proof-audit-round15-20261005/results/runs.json), [独立执行](../../research/artifacts/proof-audit-round15-20261005/software-independent). 各测试用显式异常, 不依赖assert. 44/92/103项有限测试均不代替完整解析证明或区间认证. 复验命令: `python -X utf8 [-O] -B research/artifacts/proof-audit-round15-20261005/checks.py --root <project> --output <outside.json>`.

当前原生能力是collaboration.spawn_agent(task_name, fork_turns='none'), 作者/root与初审/root/r15_analytic_review、软件/root/r15_software_review、最终整合/root/r15_integration_review分开. 每次冻结精确最小材料, 审查者亲算SHA256; 没有伪造UUID或旧fork_context字段. 初审3输入、软件11输入、最终整合9输入的哈希清单与实际回执另存. [最终整合回执](../../research/artifacts/proof-audit-round15-20261005/integration-final-review.md)实际为 APPROVED_FOR_SCOPED_ANALYTIC_INTEGRATION, 九项输入前后哈希匹配, 批准两个精确解析合同且无待补缺口. 本段不把未执行项目算作成功. 两处下方旧日期字段仍保留历史版文字, 顶部R15/实质结论已同步; 独立回执将此记为非阻断元数据观察, 不是证明前提.

已安装原版工具库save_card/version保存三卡, 旧卡快照保留, 新A3明确依赖新A11版本. [操作回执](../../research/artifacts/proof-audit-round15-20261005/card-operations.json)与[实际查询](../../research/artifacts/proof-audit-round15-20261005/library-query.json)表明59项可检索/34项阻断; RETRIEVAL_ONLY不等于自动数学接收. 本轮实际check_spawn再次拒绝原生格式, 原因为 `only the explicit Codex fresh-context tool adapter is supported`, 见[拒收原记录](../../research/artifacts/proof-audit-round15-20261005/review-adapter-rejection.json). 未改插件, 未签发release或canonical回执; 旧整文件绑定失效也不改记为新数学命题失败.

活动TeX/PDF、三卡、地图、理解、脚本/工具导航、AGENTS与续接已同步. 23页阅读版用既有XeLaTeX三遍实际构建, 最终页1/2/17/18/19实际渲染检查. 内置编译器本次失败 `Unable to find standard directories for platform`, 记录及日志见 [compilation](../../research/artifacts/proof-audit-round15-20261005/compilation/compilation.json). 不声称零警告: 既有字体版本/旧段落box警告保留, 新段落未引入裁剪. 第三遍目录页发生改变, 自动同图检查先失败, 重新检查最终渲染后才复制PDF. Lean未执行, 完整形式化未完成.

## 保护与剩余范围

原输入25文件/清单24项、6项上游完整Git blob均核实; 摘录保持为摘录. 基线19283跟踪、134原未跟踪及1原dirty的全字节记录在外部F:/tools/math-audit-round15-20261005/baseline.json. 最终[字节保护核对](../../research/artifacts/proof-audit-round15-20261005/preservation.json)已PASS: 19268个原跟踪文件与全部134原未跟踪文件原字节不变, 只改变明确15个活动文件.  原1dirty/134untracked、canonical、R14代码/完整G2和Hc2证明、冻结历史/旧作者稿/旧回执保留. 新审查输入必须与实际交付文件一致, 不用附件覆盖后续新版. [原清单核对](../../research/artifacts/proof-audit-round15-20261005/input-checks.json)与最终preservation/changes清单给出实际证据. git diff --check 已实际通过, 原始CRLF以窄路径cr-at-eol属性识别而未改写冻结输入.

剩余: 收敛側全部闭包元素的描述; c=0/一致c↓0及窗口之外; 一般非对角H的A3/A4、无限约束、重组/投影问题、稳定基和误差率; ND/G1、无条件全局唯一及其余M3/KP. 到本轮三项有限义务结束, 不开始下一轮理论扩写.
