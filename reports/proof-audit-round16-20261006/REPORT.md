# 第十六轮有限义务交付

实际工作区: F:/LaTeX/BVE research. 本轮起点和交付 HEAD 均为 ec45bf99ae746b0a3699557e06700a3c00c5a831. 已检查本地第十五轮正确修改及未提交状态; 远端没有新提交未被解释为本地成果不存在. 本轮不提交或上传.

## 五项状态

| 编号 | 本轮结果 | 证据位置与适用边界 |
| --- | --- | --- |
| R16-01 | 已修复并独立软件复验 | [完整活动 rigid1d](../../misc/rigid1d.py), [修后性质](../../research/artifacts/proof-audit-round16-20261006/checks.py), [最终软件回执](../../research/artifacts/proof-audit-round16-20261006/reviews/software-review-v4-result.md). 端点先转Fraction; 整数/相邻float负例拒收, 分区/中心/半宽/修正/比较精确; 类型/顺序/计数/宽度/预算拒绝有效. True仍以前提正确的D2区间回调为基础, False只表示未证明. |
| R16-02 | 已修复并独立软件复验 | [活动配对入口](../../scripts/_gapn2_second_variation_probe.py)的BlockDirection、SpectralProbe和P1/P2/P2b/P3. rho=2,h=2的61模态配对恢复单位阵, n=20/60的Q符合原精确值. 一般回调检查实际节点/模态分辨率/两次连续比较/显式预算; 未决拒绝, 已收敛误差仍是估计. |
| R16-03 | 已修复并独立软件复验 | 同一活动入口对全部rho/h断点局部解析配对, 保留每个共同段的半宽; 70位同频锚点传播复用既有共同质量, 小相位和sinc和/差稳定回退, 下溢拒绝. 2^-50及方向独有一ulp、非二进制近节点、真实混合相位对照通过. 普通折叠节点拒绝, 没有扩大块宽或修改数学容许类. |
| C16-TAIL | 已证明并独立解析复审 | [完整谱尾证明](../../docs/SL_bounded_direction_spectral_tail.md), [最终解析回执](../../research/artifacts/proof-audit-round16-20261006/reviews/analytic-final-review-v2-result.md). 完整Parseval剩余、Q-Q_N两侧界及取等例成立. 符号认证需要有限配对/J/特征值/Q_N可靠包络; 当前浮点输出不宣称拥有这些包络. 范围为实际实有界密度方向, 不是delta/delta-prime接口方向. |
| C16-A10-INTEGER | 已证明并独立解析复审 | [完整一般整数证明](../../docs/SL_integer_left_definite_riesz_systems.md), 同一最终解析回执. 每个固定c>0及非负整数r的真实复Hc^r有可构造Hermite-Legendre Riesz替代基; 2ceil(r/2)低提升, 奇阶r+1列, 次数一致上下界和精确多项式张成成立. 误差率需t>=0及加权系数条件. |

这五项的有限合同已完成. 原生独立审查通过不等于工具库旧自动接收、Lean或canonical接收; 下文给出真实门禁和未执行项.

## 输入、旧错误与修后性质

原附件25项清单哈希核对通过, 5项上游完整源码Git blob身份对照真实HEAD. 其中只有两项附件是完整源码, 其余保持摘录身份; 没有用摘录覆盖活动完整源码. [输入核对](../../research/artifacts/proof-audit-round16-20261006/input_validation.json)及[input原包](../../research/artifacts/proof-audit-round16-20261006/input/source_manifest.json)保留.

附件原checks普通/-O各34项只确认基线错误. 另在五份完整冻结实际源上普通/-O重放9个观测: 整数及两个相邻float入口原先错误True; 32点n=20原Q=-1667.47937, 应为202.32689; 64点n=60原Q=1468.85786, 应为597.11107. 2^-50薄段64/128节点均仅9个不同坐标, 质量分别0.93900227/0.93997396. 原Fraction负例本已拒绝, 原低模态正对照本已正确. 这些失败期待只留在[完整源基线重放](../../research/artifacts/proof-audit-round16-20261006/actual-baseline-normal.json), 不成为修后成功条件.

| 实际运行 | 普通 | -O | 日志 |
| --- | --- | --- | --- |
| 当前205项修后性质, 包括严格新负例/正常控制 | 205 PASS | 205 PASS | [normal](../../research/artifacts/proof-audit-round16-20261006/properties-normal-v4.json), [optimized](../../research/artifacts/proof-audit-round16-20261006/properties-optimized-v4.json) |
| R14共享驻点回归 | 62 PASS | 62 PASS | 本轮证据目录 stationary-r14-normal/optimized.json |
| R14核身份、覆盖及raw K/SKS等回归 | 143 PASS | 143 PASS | 本轮证据目录 kernel-r14-normal/optimized.json |
| 当前完整n=2,R=4 CLI,12模态,P1/P2/P2b/P3 | SUP exit0 | INF exit0 | [真实命令及运行](../../research/artifacts/proof-audit-round16-20261006/execution-v4.json), probe-cli-normal/optimized-v4.json及stdout/stderr |
| 新独立软件审查者亲自重放 | 205项及其独立补测通过 | 同样实际执行 | 最终软件回执及其原始JSON/日志 |

CLI的固定宽度P3和有限截断差值不被当作脉冲极限或符号定理. rho=2,h=2的零谱尾是解析恒等式, 不由负浮点剩余截零推断. 回调返回CONVERGED_NUMERICAL_ESTIMATE, 结构化方向返回NUMERICAL_ANALYTIC_EVALUATION; roundoff/black-box enclosure未提供, sign_certified=false. 四数组旧调用兼容, 默认结果携带diagnostics, CLI保存各项诊断.

重放环境是实际科学Python3.10.11、NumPy2.2.6、SymPy1.14.0、mpmath1.3.0. 命令:

    OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1
    C:/Users/HuangZY/AppData/Local/Programs/Python/Python310/python.exe -X utf8 -B research/artifacts/proof-audit-round16-20261006/checks.py --root "F:/LaTeX/BVE research" --output <outside.json>

优化重放再加-O. 基线重放使用actual_baseline_replay.py及同目录baseline_sources完整文件. 源哈希和真实优化标志在各JSON中, 使用显式异常/条件而非assert接收. r=1,...,6的有限Hermite代数检查不替代一般整数证明.

## 独立审查及实际补修

各审查均另启真实collaboration的fork_turns=none会话, 仅提供精确冻结最小材料; 审查者没有读取作者会话/实际AGENTS/记忆. 这是读取范围隔离, 不冒称OS沙箱. 数学与软件互不替代.

| 实际会话 | 裁定与处理 |
| --- | --- |
| /root/r16_integer_review | 原全整数主构造成立, 速率式缺少t>=0及N>=2r-1; 给出t=-1的精确反例, 修订附加速率前提, 没有缩小c/r主量词. |
| /root/r16_tail_review | 原精确Parseval/尾式及取等通过, 明确浮点积分不提供认证包络. |
| /root/r16_final_analytic_review | 首次最终稿退回: d_lower>b_upper不保证d_lower>a_upper, 宽a包络可能使分母错误. 修订利用真实a<b先取aHat_upper=min(a_upper,b_upper), 完整可靠包络合同保留. |
| /root/r16_final_analytic_review_v2 | APPROVED_FOR_SCOPED_ANALYTIC_INTEGRATION, 亲自核对两份完整一般解析证明. |
| /root/r16_software_review | v1退回: 方向独有一ulp段的半宽在密度块偏移中丢失. 改为每个共同段的左锚点. |
| /root/r16_software_review_v2 | v2退回: float(1/3)等近节点的原二进制相位锚点仍失真. 增加70位同频传播并复用原质量. |
| /root/r16_software_review_v3 | v3退回: 混合大小相位的sinc差/和仍消去, 真实61模式入口可放大. 稳定回退改按消去位数选精度, 加入原阈值的严格回归. |
| /root/r16_software_review_v4 | APPROVED_FOR_SCOPED_SOFTWARE_INTEGRATION, 普通/-O各205及105独立补测通过, 当前15完整文件及实际独立执行见最终回执. |

原退回回执、对应冻结字节、自拟失败脚本和真实日志均在本轮reviews目录保留, 未把前版有限全PASS改写成整体批准. 最终两证明SHA-256:

- integer: 786ae7ec05f2b6bc4b781b94315a34cc2e2683da8d04acbb5af0ab37dab4f568
- tail: d5b0309d89650ec7322a45133d4c6794e7199a773b2bcebae7ffc99ee0d3868f

最终解析输入还绑定当前实际算子基础, 三项与活动源一致; 最终软件输入15项与活动源一致. 详见[preservation](../../research/artifacts/proof-audit-round16-20261006/preservation.json).

E1专用_taylor原本在分区前转Fraction, 静态无两助手调用. 软件初审额外启动过一份E1全账重算, 协调器纠正范围并停止; 20条部分输出、RUNNING原状态及停止记录均保留, 不计57项新验收, 原账没有改写. 后续审查只做静态影响核对, 不重启退役Decimal.

## 活动整合与保护

原版save_card/version API保存两张修订卡和一张新精确Taylor卡, 保留旧卡身份与版本; [实际API保存](../../research/artifacts/proof-audit-round16-20261006/library-card-saves.json). 原生解析/软件回执元数据明确各自实际范围. 原版check_spawn本轮仍拒绝当前task_name/fork_turns身份: [真实适配检查](../../research/artifacts/proof-audit-round16-20261006/legacy-adapter-round16.json). 没有改插件、伪造旧UUID或解除旧隔离. 检索状态只表示RETRIEVAL_ONLY, 不表示自动接收.

活动证明、工具卡、研究地图、理解、脚本导航、AGENTS及续接同步. 本轮只改变14个起点跟踪活动文件; 19269个其余跟踪文件和全部233个起点未跟踪文件字节不变. 原R15两个活动TeX/PDF、完整删项证明及其冻结审查、新枚举入口、R14 G2/Hc2完整证明和既有守卫/身份/共同质量/Jacobian/交叉/raw K-SKS均保留. 原KP-DET脏稿、历史回执、旧作者稿和本科讲义没有改写. Git暂存为空, HEAD不变, diff --check通过.

[Round16基于本轮开始实际工作区的源补丁](round16.patch)不以裸HEAD替代R15本地状态. 补丁含活动源、两份完整证明、性质测试、卡片与必要维护文字; 派生索引/版本/运行证据在实际工作区和[变更清单](../../research/artifacts/proof-audit-round16-20261006/changes.json)中交付.

本轮未作TeX/PDF编译、Lean形式化或canonical接收, 未上传云端; 旧编译/历史Lean不能冒称本轮验收. 数学原生审查已经执行, 上述自动接收仍未完成.

## 剩余问题与结束边界

原稀疏族未成为Riesz基. 非整数阶稳定构造、c下降至0或r趋无穷的一致界、任意新增/无限约束、无附加系数条件的速率、一般非对角H的A3/A4、收敛删项侧全部元素描述、ND/G1、无条件全局唯一性及其余M3/KP仍开放. 第十五轮本Krein模型的有限余维逐项筛选和全窗口删项判据保持其已证范围. 本轮到这五项有限义务结束, 不自动启动新理论扩写.
