---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359"], "canonical_key": "second-variation-weighted-eigenvalues (lambda'' formula + pitfalls + gap second variation Q)", "created": "2026-08-13", "dependencies": [], "evidence_status": "ROUND10_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT", "source": "自研 (R-206, 2026-08-13; 承接 docs/SL_gap_nge2_symmetry_local_proof.tex 的 (G1')/(G2) 框架)", "sources": [{"locator": "V1-V4", "path": "research/artifacts/proof-audit-round9-20260923/analytic-repair.md", "sha256": "cb26b534c5a163d6409de3393db6c79bdb73fc6a5ea7a2036d52e44ea4bb9be0"}, {"locator": "S1-S4,R1-R2; independent analytic identities retain their prior scope", "path": "research/artifacts/proof-audit-round10-20260925/analytic-repair.md", "sha256": "175b8f4366f61498818f5eda1704d5a2a2972ddb9d9885f8dc2351b28a9637a7"}], "status": "第十轮数值依据/反射扇区纠错; 精确版本经独立纠错回执后方可复用", "summary": "正密度线性路径的二阶谱公式; 归一化导数含核分量. 分块切向使用块积分, Green核有界, 集中脉冲须总变差有界且有符号质量收敛才有点值极限; 移动接口另有有限加速度项. 不证明切空间负定或G1定号. 第十轮: 旧扫描不能认证谱序号, 旧asym非扇区投影; 新相位索引与可行扇区种子另审, 不据历史数值扩张解析结论.", "tags": ["mathtool", "self-developed", "perturbation-theory", "second-variation", "hessian", "gap-extremals", "nge2"], "title": "加权特征值二阶变分与归一化、切向及接口路径规范", "tool_id": "second-variation-weighted-eigenvalues", "updated": "2026-09-25"}
---
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
