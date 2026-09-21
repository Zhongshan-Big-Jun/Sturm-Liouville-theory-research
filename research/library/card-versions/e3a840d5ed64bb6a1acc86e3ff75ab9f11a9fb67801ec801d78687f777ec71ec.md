---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c2d0-78b9-7f73-be52-f9bb55841fcc", "01a0c2d0-7dec-77b3-894f-a0427000a837"], "evidence_status": "ROUND6_SCOPED_ANALYTIC_REPAIR; REUSE_REQUIRES_EXACT_CORRECTION_RECEIPT", "related": ["[[denseness-criteria]]", "[[moment-jump-completeness]]", "[[jump-stability]]"], "scope": "Complex Hilbert space with all polynomials included densely; exact projection and finite-tail-obstacle criteria. No arbitrary Krein-domain application or full historical branch recertification.", "slug": "constrained-denseness-runs", "source": "会话 106 (run R-20260814T070000Z-densbc-3F8A2C, 任务包 Q-20260814-densbc-3F8A2C)", "sources": [{"locator": "All current projection, finite-tail-obstacle and representer repair proofs", "path": "docs/SL_projection_moment_repairs.tex", "sha256": "be31a3d595342bbc752db7e5b61a39790daf32b7707dd8f5142484a0a0b1b389"}, {"locator": "Historical Theorem1 and Corollary1.1 corrected by round6", "path": "runs/rigorous-open-math-research/R-20260816T000000Z-densbc-o1/candidate_proof.md", "sha256": "d87bbda0e455ee3dfc6b682aa41e1625a5bbdbbaa89d198e8cae4692202b62ea"}, {"locator": "Historical F/G/H explanations corrected; other branches not globally reaudited", "path": "runs/rigorous-open-math-research/R-20260814T070000Z-densbc-3F8A2C/candidate_proof.md", "sha256": "c2b78e77b8f70bd1f3d67253fb813730f01d296023782f3c2faf0865ad669b31"}], "status": "第六轮F01-F03解析修订; 历史A-H不作整组复用; 一般非对角问题仍开放", "tags": ["稠密性", "矩刻画", "边界条件", "对角空间", "负结果"], "title": "受约束稀疏族: 投影、尾部障碍与矩条件", "tool_id": "constrained-denseness-runs"}
---
# 受约束稀疏族: 投影、尾部障碍与矩条件

本卡当前修订对应第六轮 F01-F03. 旧 run 的 A-H 全部 STRICT 标记不再作为整组复用依据. 本卡的当前状态由纠错回执决定; 历史证明和旧卡原字节保留.

设复 Hilbert 空间 H 包含全部多项式 Pi, 且 Pi 稠密; 内积对第一变量线性. 固定 p0=1, p1=x, p_(2m)=x^(2m)-m/(m-1)x^(2m-2), p_(2m+1)=x^(2m+1)-m/(m-1)x^(2m-1), m>=2. V 是闭子空间, P_V 是正交投影.

## 投影要补上缺失的两个方向

Pi=span({p_n} union {x²,x³}), 而 span{p_n}=Pi 与 Krein 两条多项式边界条件的交, 在 Pi 中余维2. 因此 P_V Pi 总在 V 中稠密, 但 {P_V p_n} 未必稠密. 令 M=closure_H span{p_n}, 则精确判据是

`closure_V span{P_V p_n}=V iff V intersect M^perp={0}`.

加入 P_V x²,P_V x³ 后总是稠密. 令 I={n:p_n in V}, S=closure_V span{p_n:n in I}. 有

`S=V iff {P_V p_n:n not in I} union {P_V x²,P_V x³} subset S`.

只有另证整个稀疏族在 H 中稠密时, 才可省去两个补充测试. 对角加权空间 H_beta 在 beta=2 的反例为 V=ker M0 和

`w=sum_(m>=1) m/(2m+1)^4 * x^(2m)`.

这里 <x^j,x^k>=delta_jk*(k+1)^4, ||w||²=sum m²/(2m+1)^4 有限且非零, M_(2m)=m, 所有奇矩和 M0 为零. w 属于 V 且正交于全部 P_V p_n. 只排除 p0, 其投影为0; 所以旧“只测试排除项”的判据也失败. 这个 H_beta 的参数2不表示第二左定空间.

## 有限矩条件应作用在尾部障碍上

原 F 同时要求 V 包含完整无限尾部, 又要求有限个矩测试在整个 V 上单射. 前者使 V 无限维, 后者不可能. 这是无适用实例的充分条件, 并非找到满足前提而结论错误的实例.

可用替代: 假设 ||x^k||_H<=C*(k+1)^beta, beta<1, m0>=2, L=2m0-2. 完整尾部 {p_(2m),p_(2m+1):m>=m0} 的正交补恰为

`Z_L={w in H:M_k(w)=0 for every k>=L}`, 且 `dim Z_L<=L`.

尾部矩递推给出 M_(2m)=m/(m0-1)*M_L, 奇侧同理; 次线性上界迫使两个尾部基矩为零. 低于 L 的矩在 Z_L 上是单射, 从而障碍有限维. 若 V 包含尾部, 保留的低指标集为 J, 则保留族在 V 中稠密当且仅当

`(V intersect Z_L) intersect (intersection_(n in J) ker <.,p_n>)={0}`.

非空实例: 对角 H_0, m0=2, V=H_0, 有 Z2=span{1,x}; p0,p1 恰好排除此二维障碍.

一般三角多项式尾部 q_n (每个 n>=N 恰为 n 次, 首项非零) 也有有限维尾部正交障碍, 维数至多 N. 低位矩在该障碍上单射, 其上保留测试的共同核为0才是相应判据. 不能以“证明与 F 相同”或仅凭增长系数断言每条三项递推解都增长; 最小解必须另计. 具体条件和证明见修订文稿.

## 检测不等于分别钉零

若 V=intersection ker <.,v_j>, j 有限, 则对所有 w in V 都有 M2(w)=M3(w)=0 当且仅当

`span{x²,x³} subset V^perp=span{v_j}`.

H_0 中 v=x²+x³ 同时与 x²,x³ 非正交, 但 w=x²-x³ 属于 v^perp 且 (M2,M3)=(1,-1). 单个约束只给出一个线性关系. 个别 w 的两个矩为零也不等价于整个 V 的两个矩恒零.

## 保留的范围与历史入口

一般正交补主判据 `closure span Q=V iff V intersect Q^perp={0}` 保留. 原 A-E 的其它独立矩刻画、条件性恢复结论、对角游程分类及其反例保留在旧 run, 本轮不把它们重标为全部复审通过. 真正 Krein 幂域通常不包含所有单项式, 不能直接套用本卡的 Pi subset H 假设; 具体族的分数阶结论见 [[spectral-domain-checks]], s=2余有限分类见 [[leftdef-o1pld-l2-structural]]. 一般非对角 O1'/O1'LD 仍未因此解决.

完整当前证明: [SL_projection_moment_repairs.tex](../docs/SL_projection_moment_repairs.tex). [第六轮报告](../reports/proof-audit-round6-20260921/REPORT.md)区分反例、解析证明、有限检查和局部 Lean. 原投影 run R-20260816T000000Z-densbc-o1 的 Theorem1“in particular”及 Corollary1.1, 原框架 run R-20260814T070000Z-densbc-3F8A2C 的 F/G/H 解释, 均按本修订限定使用; 冻结文件中的旧 PASS 是历史记录.
