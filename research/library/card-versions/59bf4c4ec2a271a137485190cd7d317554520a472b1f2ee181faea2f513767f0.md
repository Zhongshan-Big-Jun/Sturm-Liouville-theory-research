---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359"], "canonical_key": "second-variation-weighted-eigenvalues (lambda'' formula + pitfalls + gap second variation Q)", "created": "2026-08-13", "dependencies": [], "evidence": [{"locator": "Both complete general analytic contracts; native isolated session /root/r16_final_analytic_review_v2", "path": "research/artifacts/proof-audit-round16-20261006/reviews/analytic-final-review-v2-result.md", "sha256": "906f3bd91c8287f5c18c40174a842019e444636ccb581d2ab59e16afa5cdffdf"}, {"locator": "Current 15-file software packet; actual ordinary/-O independent execution", "path": "research/artifacts/proof-audit-round16-20261006/reviews/software-review-v4-result.md", "sha256": "8ecd71b08980eed6ecefc0ef57d2f1b4c1b7f78840f933d7baa6f964a3b91e68"}], "evidence_status": "ROUND16_SCOPED_NATIVE_ANALYTIC_AND_SOFTWARE_APPROVED; LEGACY_GATES_REMAIN", "review_status": {"automatic_receipt": "UNRECEIVED_UNSUPPORTED_NATIVE_ADAPTER", "report": "research/artifacts/proof-audit-round16-20261006/reviews/analytic-final-review-v2-result.md", "reviewer_id": "/root/r16_final_analytic_review_v2", "scope": "Complete analytic contracts in the exact two current proofs; not Lean or canonical acceptance", "sha256": "906f3bd91c8287f5c18c40174a842019e444636ccb581d2ab59e16afa5cdffdf", "verdict": "APPROVED_FOR_SCOPED_ANALYTIC_INTEGRATION"}, "software_review_status": {"automatic_receipt": "UNRECEIVED_UNSUPPORTED_NATIVE_ADAPTER", "report": "research/artifacts/proof-audit-round16-20261006/reviews/software-review-v4-result.md", "reviewer_id": "/root/r16_software_review_v4", "scope": "Only the frozen current software input and actually executed finite tests", "sha256": "8ecd71b08980eed6ecefc0ef57d2f1b4c1b7f78840f933d7baa6f964a3b91e68", "verdict": "APPROVED_FOR_SCOPED_SOFTWARE_INTEGRATION"}, "source": "自研 (R-206, 2026-08-13; 承接 docs/SL_gap_nge2_symmetry_local_proof.tex 的 (G1')/(G2) 框架)", "sources": [{"locator": "V1-V4", "path": "research/artifacts/proof-audit-round9-20260923/analytic-repair.md", "sha256": "cb26b534c5a163d6409de3393db6c79bdb73fc6a5ea7a2036d52e44ea4bb9be0"}, {"locator": "S1-S4,R1-R2; independent analytic identities retain their prior scope", "path": "research/artifacts/proof-audit-round10-20260925/analytic-repair.md", "sha256": "1215c0f2291829a5fd40dd212f313e5ba07841bec9d70477d1dca4580bb0a066"}, {"locator": "J1-J5, finite-dimensional structure and finite-difference geometry with explicit limits", "path": "research/artifacts/proof-audit-round11-20260926/jacobian-repair.md", "sha256": "aabc1aa00e43ec64a1ef48e5f68dd39b349d57b6dfa3efd1da0cb1dd5e157824"}, {"locator": "Equations1-8, equality example and reliable-envelope premises", "path": "docs/SL_bounded_direction_spectral_tail.md", "sha256": "d5b0309d89650ec7322a45133d4c6794e7199a773b2bcebae7ffc99ee0d3868f"}, {"locator": "User-supplied tail appendix; independently derived rather than accepted by label", "path": "research/artifacts/proof-audit-round16-20261006/input/analytic_notes.md", "sha256": "c4e3eac6884ed2a387d14a92226e0c8e7b4a52a4a5279646f483af18dc283c31"}, {"locator": "BlockDirection, SpectralProbe.pairings, actual P1/P2/P2b/P3 calls", "path": "scripts/_gapn2_second_variation_probe.py", "sha256": "6410e71518c7e59ffd7f67342a809ab2dd827a5de66c2bc984172d68dd190f44"}], "status": "第十六轮有界方向尾界已证明并原生复审; 数值配对修复已独立执行; 旧精确纠错门禁未自动释放", "summary": "真实有界密度方向的二阶谱公式与Parseval两侧尾界. 分块方向按全部rho/h切点局部解析配对; 一般回调检查节点、模态分辨率和连续比较预算, 未决拒绝. 原始负浮点残余不截零, 浮点积分/特征值不是符号包络. 原归一化、接口与Jacobian范围保留.", "tags": ["mathtool", "self-developed", "perturbation-theory", "second-variation", "hessian", "gap-extremals", "nge2"], "title": "加权特征值二阶变分与归一化、切向及接口路径规范", "tool_id": "second-variation-weighted-eigenvalues", "updated": "2026-10-06"}
---
## 第十六轮: 有界方向的 Parseval 尾界与配对积分

真实 DD、0<m<=rho<=M、实 h in L-infinity, int rho u_k^2=1. 设 c_kl=int h u_k u_l, J_k=int(h^2/rho)u_k^2. 对真实完整一基模态,
E_(k,N)=J_k-sum_(l<=N)|c_kl|^2=sum_(l>N)|c_kl|^2>=0.
若 n>=1,N>=n+1, a=lambda_n,b=lambda_(n+1), Q_N 用前N模态,

 -b^2 E_(n+1,N)/(lambda_(N+1)-b) <= Q-Q_N
 <= a^2 E_(n,N)/(lambda_(N+1)-a).

rho=2,h=2 时配对为单位阵并精确零尾, Q=(2n+1)pi^2/2. rho=2,h=2cos(pi x), n>=2,N=n+1 达到左界. 欠分辨求积会在零尾例仍给错误Q, 所以积分误差与谱截断必须分开.

可靠的有限配对、J、特征值及Q_N包络才允许认证符号. E上端为负意味着输入预算矛盾并拒绝; 不能把普通负浮点剩余截零. 若d_lower>b_upper, 宽a包络先与真实谱序相交, aHat_upper=min(a_upper,b_upper), 再按完整证明式(8)取两侧包络. 分母未证明严格正或最终区间含0时未决.

活动分块常值方向用 BlockDirection 声明全部真实切点, 与rho断点取共同分割; 每个共同小段左端状态配合局部半宽积分, 避免全局中点舍失. 锚点以70位传播同一二进制频率/块长, 复用既有物理采样器的一个共同质量因子, 减少近节点相位舍入. 小相位乘积展开和按消去位数提高精度的sinc和/差回退维持数值可分辨; 正局部积分/相位下溢则拒绝. 不采用采样点的方向归属算薄段质量.

一般回调须声明已知断点, 拒绝折叠/端点节点, 检查模态相位分辨, 并在MaxOrder内完成两次连续比较. 误差仅为估计, 黑箱区间包络为None; 未决拒绝返回配对/Q. PairingResult保留原四数组兼容并携带diagnostics, CLI逐项写入; sign_certified=false. 解析三角浮点计算仍无舍入包络.

本尾界不适用于delta/delta'接口方向, 不建立脉冲宽度趋零的一致结论或ND/G1. 原Green、归一化、交叉Jacobian和raw K/SKS区别保持各自已修范围.

[完整尾界证明](../docs/SL_bounded_direction_spectral_tail.md)、[第十六轮实际交付](../reports/proof-audit-round16-20261006/REPORT.md). 原有纠错隔离和旧回执保持, 本段不构造自动放行.

## 第十一轮: Jacobian 分块与差分方向

对称点的残差 Jacobian 满足 JP=-PJ. 在反转偶/奇坐标下应取交叉块 C,D,
det J=(-1)^n det C det D. 旧诊断程序取到的是应为零的两个对角块, 撤回这种
数值分块解释. 输入反转奇方向保持物理反射, 反转偶方向破缺物理反射.
Hessian 或适当跳量对称化矩阵可以与 P 交换并块对角化, 不能统一交换分块位置.

旧 jac_fd 经裁剪和归一化可能改变差分路径. 当前版本直接构造独立接口的两侧端点,
检查实际坐标往返、中心方向和可分辨步长, 必要时缩步; 无法保持时明确拒绝.
P3 保存逐列几何回执. 这些浮点检查不是导数/谱尾项的区间认证.
本轮不否定正确的解析反对合、Green 或变分恒等式, 不宣称默认 R=4 历史数据全错,
也不认证所有旧调用者或全参数 G1'/Hessian 符号. 已核查范围见
[第十一轮推导](../research/artifacts/proof-audit-round11-20260926/jacobian-repair.md)
和[本轮报告](../reports/proof-audit-round11-20260926/REPORT.md).

# 加权特征值二阶变分与路径规范

## 第十轮: 数值谱序号与反射种子的适用边界

共享旧求根器存在漏掉成对低频根的真实反例. 根残差、正性和递增性不能确定谱序号;
旧数值输出保留为历史, 未经针对性重算不能继续作为已核实低模态证据.
这不否定本卡独立解析恒等式, 也不由反例推断默认R=4的旧数据全错.
当前引擎按连续提升的第n*pi相位定位, 高精度和有限差分仍限定同一指标.
浮点括区不是严格区间证书; 共用同一枚举器的两种计算不构成独立谱计数.

接口反射为 R(x)=1-Jx. 保持扇区 d=(v-Jv)/2 满足Jd=-d,
破缺扇区 d=(v+Jv)/2 满足Jd=d. 旧asym赋值仅是-Jv, 撤回其纯扇区解释.
旧(a,-a[::-1])及相同形式的网格平面保持几何反射, 不能提供离开该子空间的证据.
新种子检查零投影、严格可行步长及参数转换后实际位移; 标签只指初值而非完整优化轨迹.

算法推导、程序范围和历史传播见[第十轮修订](../research/artifacts/proof-audit-round10-20260925/analytic-repair.md).
最终重算/审查范围见[第十轮报告](../reports/proof-audit-round10-20260925/REPORT.md).
本轮不证明Hessian定性、G1'、全R分支或全局唯一性; 下列保留内容按其各自审查范围阅读.


设 `-u''=lambda rho u`, Dirichlet 区间 [0,1], 实 `0<m<=rho<=M<infinity`,
`int rho u_k^2=1`, 实有界方向 h, 线性密度路径 rho+t h 在零点附近保持正下界.
记 `a_k=int h u_k^2`, `B_kl=int h u_k u_l`. 在任意基点,

`lambda_k'=-lambda_k a_k`,

`lambda_k''=2lambda_k a_k^2-2lambda_k^2 sum_(l!=k) B_kl^2/(lambda_l-lambda_k)`.

所有 B_kl 配对均按 dx 积分. 分母有符号, 不能换为绝对值. 完整解析论证见
[本轮证明 V1-V4](../research/artifacts/proof-audit-round9-20260923/analytic-repair.md).
它从 Volterra 射击解构造解析分支, 再由加权正交展开与可求和性得到公式.

归一化导数必须包含核分量:

`v=-(a_k/2)u_k+lambda_k sum_(l!=k) B_kl/(lambda_l-lambda_k) u_l`.

若普通 L2(dx) 的正交约化逆给出
`v0=lambda_k R_perp[(h-a_k rho)u_k]`, 则
`v=v0-(a_k/2+int rho u_k v0)u_k`.
取 h=rho 有 v0=0, v=-u_k/2; 旧稿将两者直接相等的式子撤回.
谱 Green 有限部和普通 L2 正交约化逆也不是同一规范.

对 `D_n=lambda_(n+1)-lambda_n`, 定义
`f=lambda_n u_n^2-lambda_(n+1)u_(n+1)^2`, 则 `D_n'[h]=int f h`,
`Q(h)=(lambda_(n+1)''-lambda_n'')/2`. Q 在非驻点也有意义.
分块常值方向 b 的切向条件是 `dot(b,A)=0`, `A_i=int_(I_i) f`.
普通欧氏投影为 `b=b0-dot(b0,A)A/dot(A,A)`; A=0 时保留 b0.
若用真实 L2 系数度量 `sum L_i b_i c_i`, 则用
`b=b0-[sum L_i b0_i g_i/sum L_i g_i^2]g`, `g_i=A_i/L_i`.
旧脚本对未加权块平均值的投影不保证真实切向性; 常密度不等宽反例见 V2.
这些是局部正密度方向, 还不能自动作为饱和盒约束的可行方向.

一维正则问题的去简单极点 Green 核在闭正方形连续有界.
总变差一致有界的集中脉冲二次型因此一致有界. 还须支持集中到 a、
带符号总质量 int h_eta dx 趋于 q, 才有极限 q^2 u_k(a)^2 Gtilde_k(a,a).
总变差有界本身不保证带符号质量或二次型收敛. 特别在 rho=1,
单位质量脉冲集中到 1/2 时 `lambda_1''->6pi^2`, `lambda_2''->0`,
`Q->-3pi^2`. V3 给出完整谱和的控制收敛, 不依赖有限截断.
旧“bump 越窄必然 Green 对角发散”的理由撤回; 不推广到无界总质量、核导数或高维.

移动接口 a_i(t)=a_i+t d_i, 跳量 s_i=rho_right-rho_left 时,
`dot rho=-sum s_i d_i delta_(a_i)`, `ddot rho=sum s_i d_i^2 delta'_(a_i)`.
二阶路径链式法则中还应计入有限项 `-sum s_i d_i^2 f'(a_i)`
(这是完整二阶导数的项, 对 Q 需除以二). 驻点 f(a_i)=0 不使 f'(a_i) 消失.
本卡没有把任意分布路径的可微性当成已证前提, 没有据此证明 G1' 的定号.

历史 R-206 addendum 及旧 P1/P2/P3 输出按原字节保留.
F01 撤回其分块 P2 的“切向”解释, 不凭该错误否定任意方向 P1 二阶公式或实际积分的 P2b 分支.
随机同号样本不能证明切空间负定. 新脚本的方向残差、截断和有限差分结果按
[第九轮报告](../reports/proof-audit-round9-20260923/REPORT.md) 中真实重算范围阅读.
旧 P3 的稀网格窄脉冲和符号差异不能封死整条路线.

可继续研究: 在固定接口族中严格建立线性密度极限与有限加速度项的组合,
再研究完整宽度 Hessian 的符号. 此为重开的待证路线, 不是已解决的 G1'/O1/O2.
