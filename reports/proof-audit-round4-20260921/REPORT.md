# 第四轮证明审计修缮报告

日期: 2026-09-21. 解析修缮、程序最终复检、Lean局部语义审计及工具库释放完成. 云端交付以本报告所在提交及外部DELIVERY.json核验记录为准.

用户提供 `C:/Users/HuangZY/Downloads/sl_audit_round4_20260920`, 要求依审计继续修缮, 并指定数学研究工作流. 延续此前授权的无状态隔离检验和云端同步. 基线为 `2e9bf3d66fa21a41e16bf779782739ddd9505233`.

## 核实与修订

输入的10个文件按原字节保存于 [submitted](../../research/artifacts/proof-audit-round4-20260921/submitted/), 清单列出的9个文件哈希全部相符. 附件说明和补证作为待核查材料, 没有代替用户指令或独立验收. 其检查程序在项目外独立副本中实际执行, 退出0并确认28项具名检查; [本轮复放](../../research/artifacts/proof-audit-round4-20260921/submitted-rerun/)与提交者原结果分开保存.

| 问题 | 核实结果 | 当前修订 |
| --- | --- | --- |
| F01 代表与商类 | n=2,3 的普通H1极限比标准Q_n多出1/sqrt(6)、x/sqrt(10), 差范数平方1/3、4/15 | 全部固定n>=2的商类极限为[Q_n]; 普通函数极限仅在n>=4为Q_n; 不声称关于n一致 |
| F02 向下取整 | 四处 `//` 在c=3,j=3产生残差117/2、-189、-621/2、165/2; 精确除法全为零 | 修四个闭式、降阶与有限向后算法; 检查失败显式返回非零退出码 |
| F03 参数表缺项 | (-1/4,-3/8,-3/4,0) 表示偶E+却不在旧表 | 完整处理公共因子、两类例外参数和尾部表示; 区分原分母定义域与约分后恒等式 |
| F04 降阶前提 | E0=1不能推出每项非零; 旧中间式残差69/224 | 补逐项非零、正确收集项及r0,s1,s2反向初始化; 变差公式补非零条件 |
| F05 余项尺度 | a6-(63/c)a4=1+42/c, 并非O(1) | 用O(a_n)和相对O_n(c)误差完成固定阶按奇偶归纳 |

另外补入两处传播问题: A=0尾部允许d不为0的二次表示, 例如偶族(3/2,-1,1,-2); 有理比值子类的排除不能推广到全部齐次解. 偶族c=1、z0=1、z1=2、z2=5/2给出delta1=1/2、delta2=0、delta3=-1/480, 且属于根1分支, 推翻旧无条件盒式排除.

修订前证明、PDF、程序与卡片见 [before](../../research/artifacts/proof-audit-round4-20260921/before/). 第三轮稳定性主链和商空间谱截断不因邻接发现被整体撤回.

## 解析补证与范围

[退化极限证明](../../docs/SL_krein_c0_limit.tex) 从Legendre正交性、分部积分与首项系数证明 `S_n'=(2n-1)P_(n-1)`, 得到 `Q_n=S_n/sqrt(2(2n-1))`. 正的奇偶递推与有限多项式展开给出全部固定阶的系数/范数主项和H1收敛率O_n(c). 连续商映射消去低阶仿射差. 既有算子设置、根空间、等距映射与第三轮完备性段落保留原字节.

[三阶证明](../../docs/SL_third_order_recurrence_theory.tex) 仅处理逐项列出的P,Q,R, epsilon=0或1、固定实数c>0. 阶乘缩放化为 `d_j=theta_j*d_(j-1)`, 正项尾级数给出全部解 `v_j=A+B*j+C*Phi_j`, 有限边界的归一化收敛及唯一归一化正最小解. 其常数为

\[
K_0(c)=\frac{c^2}{4(c\cosh\sqrt c-\sqrt c\sinh\sqrt c)},\qquad
K_1(c)=\frac{c^{5/2}}{4((c+3)\sinh\sqrt c-3\sqrt c\cosh\sqrt c)}.
\]

这里 `mu_j^*=K_epsilon(c)*j^(-3)*(1-(2epsilon+3)/j+O_c(j^(-2)))`, 分母在c>0为正, K0(1)=e/4. 尾估计针对固定c, 不含关于c一致或c=0的断言. 当前有限边界是z_N=1、z_(N+1)=z_(N+2)=0, N>=2; 原K1锚点有不同的有限未归一化边界. 两者不能逐项混用, 归一化无穷极限相同.

有限极点与多项式次数论证排除C不为0时的有理相邻比值, 没有次数上限. C=0的分类区分全局E0=1、最终有理恒等式和原分母定义域. 既有root-1证明及原REPAIRABLE_GAP审计保持原身份, 不借旧审计充当新批准; [历史核对记录](../../research/artifacts/proof-audit-round4-20260921/historical-root1-audit-scope.json)单列.

三阶文稿封存于作者提交时, 首页保留“作者修订稿/需独立复审”的提交阶段说明. 当前验收以本报告的实际回执为准, 不事后改写冻结输入. 历史高阶渐近系数和数值表仍明确标为未重新认证.

## 程序反馈与真实执行

原活动程序实际输出闭式False、降阶False和nan, 却退出0. 当前 [d4程序](../../scripts/d4_third_order_theory.py) 用精确有理数处理代数, 用正二阶差分避免向后计算中的相减消失, 用mpmath任意指数范围保留有限解. 有限N数值结果不是区间误差证书或无穷极限证明.

两次独立退回均保留. 首次发现整数/Fraction混用使-1/5变成浮点-0.2, 已统一除法前转换. 第二次发现包装函数提前转SymPy Float及符号零漏检, 已让包装函数直接交给精确转换, 并拒绝 `is_zero is True` 的基准值. 不可判定的符号非零仍由调用者保证. Python float解释为实际二进制有理数, 原SymPy表达式保留语义.

正常与 `-O` 模式的程序和行为测试均通过: 36项行为检查、624项独立原mu递推的有限有理数对照、8项非零退出注入. [最终程序证据](../../research/artifacts/proof-audit-round4-20260921/script-checks-revision3/). 恒零解被误作负对照、P4(3)误期待96而正确为348的两项测试设计更正也保留, 没有冒称生产缺陷.

## 证据与隔离审计

每次最终审计另启 `fork_context:false`, 仅提供冻结输入, 不继承作者对话. `research/library/reviews/` 保留真实spawn调用、身份、包哈希和返回JSON. 批准仅适用于列出的义务.

| 检查 | 实际范围 |
| --- | --- |
| 附件复放 | 28项具名检查, 非全项目验证 |
| 退化极限 | 作者260项有限精确数学检查+14项保留/结构检查; 独立审计复放274项并检查全指标证明 |
| 三阶递推 | 作者2804项精确/符号断言+32项高精度诊断; 最终1413项静态检查单列; 独立审计复核解析链并复放数学检查 |
| 活动程序 | 正常/-O执行与36项行为测试; 有限参考递推和失败注入分列 |
| Lean | 41个局部定理、23个定义; 原生编译、对象导出、正负对照和协调器复放; 语义审核另计 |
| PDF | 三份构建退出0, 分别8/11/20页; 改动公式/表格页抽查无裁切重叠; 三阶文稿有2处Underfull hbox, 无Overfull/缺字/未定义引用警告 |

三阶独立审计未收到原root-1审计文件或活动d4源码, 因而不认证它们的历史过程或程序行为; 协调器另查历史身份, 程序交专门隔离审计. 有限计算、静态检查、解析审计与形式化不合并为“全部正确”计数.

<!-- independent-review-results -->
| 独立检验 | 真实回执 | 结果 |
| --- | --- | --- |
| 退化极限与卡片 | [a1a0a349410f](../../research/library/reviews/runs/a1a0a349410f62ae5670beb31beb62cc36ed57fa6a274cc083f15ea1b44659e9-01a0bfc0-579b-7640-a201-1c8b0f5fdd4e/report.json) | APPROVED, 限所列义务 |
| 三阶递推与K1 | [f8807ce08a12](../../research/library/reviews/runs/f8807ce08a1206de1c42fbeb0f80d2192e7527b62db8162c808b8dfceac37954-01a0bfcd-1254-7d51-8b33-6c083e198e1a/report.json) | APPROVED, 限所列义务 |
| K1继承上游纠错的依赖义务 | [c5c821de8630](../../research/library/reviews/runs/c5c821de86304b4af1a008f7dd3dd0f11306bdd70ca141fbb4256cbb8a01b18b-01a0bfea-9a67-7640-b135-4eab62d43dbb/report.json) | APPROVED, 限所列义务 |
| 稳定性与四张原卡的绑定续接 | [1cdda12180d6](../../research/library/reviews/runs/1cdda12180d647ffe29f5442006a3a0f16548650b8da39a0d9b62fd221688abf-01a0bfd7-0f50-7fa0-a8da-7fcb26b570e3/report.json) | APPROVED, 限所列义务 |
| 程序最终修订 | [1a698290c923](../../research/library/reviews/runs/1a698290c9232e6caccb4087b95affb1667c9a058ae7898d911b344b6246bab4-01a0bfd8-477c-7131-9b85-bd832ec2731b/report.json) | APPROVED, 限所列义务 |
| Lean独立盲读 | [155918f59978](../../research/library/reviews/runs/155918f59978ee79e953f48081d76c30f0bbba72a798be86caf97b6db2e7aa1a-01a0bfce-26b1-7231-81f7-ecd1c2b3f164/report.json) | APPROVED, 限所列义务 |
| Lean契约与机器证据对照 | [e8b081883b66](../../research/library/reviews/runs/e8b081883b6631a923f6d526f66de3e5fd4f2b56863e403e92a8f0e5ceb4a945-01a0bfdf-9579-7c93-b9e3-b9598afc65f7/report.json) | APPROVED, 限所列义务 |
| 程序首次退回 | [269b8022d0b0](../../research/library/reviews/runs/269b8022d0b00bc9c5756dd51665fd4ab119395360154e6cb17010b7b6b5aebd-01a0bfb3-20bc-7300-87e3-5a9dc693c9f3/report.json) | CHANGES_REQUIRED, 历史原样保留 |
| 程序第二次退回 | [da6c5ae3a3b8](../../research/library/reviews/runs/da6c5ae3a3b8ad92b0112cf9d20f54d11506c1ef75f641e4c2a4a228720820f2-01a0bfc8-4fc2-7d10-b35f-ff218490bda1/report.json) | CHANGES_REQUIRED, 历史原样保留 |
<!-- independent-review-results:end -->

## Lean准确边界

新增 [AuditRound4.lean](../../lean-proof/SL/AuditRound4.lean). 一般差分、有限求和与降阶在任意域上; 具体奇偶P,Q,R和阶乘桥接在有理数上, 没有宣称全部实数参数已形式化. 条件、下标和排除范围见 [契约](../../research/artifacts/proof-audit-round4-20260921/lean/CONTRACT.md).

Lean4.31.0编译成功. 协调器在新目录重编译四个依赖及根文件, 四份声明/定义导出和根对象字节一致. 两个错误公式负对照在False处失败, 正对照和输入契约通过. 实际加载的3217个模块对应12853个工件及10个运行时文件均重新核对哈希. 目标闭包仅用propext、Classical.choice、Quot.sound, 没有sorryAx或unsafe. [实际复放](../../research/artifacts/proof-audit-round4-20260921/lean/coordinator-replay/RESULT.json).

四个旧依赖仅在外部副本中收窄import, 数学正文逐字一致并重新编译, 未重建原广泛导入的全工程. 首次遗漏 `--root` 的命令错误, 以及新目录模块路径被误要求逐字一致的比对错误均保留. 后者核对五个允许的本地路径变化及所有对象哈希后通过, 没有改证明来通过检查.

尚未形式化: Sobolev/商收敛, Legendre正交与范数积分识别, 无穷Phi尾和、最小解与常数、解析尾估计和完整有理分类. 低阶代表差只作代数证明; reciprocal序列给出任意大余项反例, 不冒称Lean的IsBigO/Tendsto定理.

## 工具库与交付

当前程序第三轮独立复检、Lean盲读及独立语义审计均已APPROVED. 工具库释放过程中发现K1新卡继承上游round4-recurrence的独立义务, 两条自身问题回执不能单独使其放行. 该继承义务随后另经隔离会话补审并释放, 最终满足全部当前复用义务; 全过程没有绕过检索门禁.


四个新问题先绑定旧版本并隔离. 修订三阶、Krein-Sobolev、K1状态和稳定性回执绑定; 四张数学内容未变的旧卡也复核其原修补, 因为旧共用回执绑定的K1卡已变. 每张新版须处理全部历史问题的释放义务, 不能只解除新问题. 稳定性本次主要续接精确证据绑定, 不冒称新数学发现. 已撤回的全阶稀疏多项式解释继续隔离.

本轮使用插件现有纠错、版本化批注、冻结审计和检索模块, 未修改插件源码或安装版本. 更新中英文首页、研究导航、问题图、项目理解、脚本导航及Lean状态. A6仍为PARTIAL: 非齐次源项和任意系数族仍开放. 原稀疏族3<s<7/2窗、M3/KP及其它问题不因此闭合, canonical未写入.

最终[逐路径保护检查](../../research/artifacts/proof-audit-round4-20260921/final-protection-result.json)通过: 原5609个跟踪文件中仅25个指定活动文件改变, 其余5584个及134个原未跟踪文件保持原字节; canonical、旧冻结证据和原44份Lean源码均在保留范围内. 原 `.gitattributes`、其它索引/活动状态及旧workspace未提交修改不纳入本轮提交. [受审源文件终检](../../research/artifacts/proof-audit-round4-20260921/reviewed-source-final-check.json)确认四份当前数学/程序/Lean源文件仍与批准输入相同. Git实际提交字节及origin/fork远端提交的最终核验由项目外 `F:/tools/math-audit-round4-20260921/DELIVERY.json` 记录; 云端交付版本以本报告所在提交为准.

最终默认检索实查: 78张可复用、1张撤回隔离. 八张本轮相关卡全部返回当前哈希, 原错误版本不进入默认复用. 当前登记98个历史版本、58条纠错事件, 新增一条绑定当前三阶卡的研究经验批注. 查询中的14条失效提示涉及7份不同的旧回执, 均已逐项确认为由本轮新回执替代的历史记录; 重复提示不计为新的问题, 也不伪装成零警告. [工具库结果](../../research/artifacts/proof-audit-round4-20260921/library-final.json)及[默认查询](../../research/artifacts/proof-audit-round4-20260921/default-query.json).
