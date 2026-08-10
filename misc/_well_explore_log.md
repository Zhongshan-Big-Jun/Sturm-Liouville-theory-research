# 阱族探索日志 (well-family exploration log)

状态: 2026-08-10 会话 52 (缺口 (a) 闭合)
用途: 登记阱族 INF 侧的全部**数值证据 (EVIDENCE)**。按项目纪律, 本文件所有条目
**不构成证明**; 结论依据只能是严格解析证明 (STRICT), 见
`docs/SL_gap_n1_well_rigidity_R32.pdf` (小 R 相位刚性定理), `docs/SL_gap_n1_symline_proof.pdf` (缺口 (a) 闭合, KEY LEMMA) 与
`docs/SL_gap_n1_O3a_phase_rigidity_proof.pdf` (垒族 O3a).
每条记录注明脚本、参数与精度。

---

## 1. 传输恒等式 y(b)^2/y(a)^2 = J~(B)/J~(A) (两个模态)

脚本: `misc/_well_explore1.py`; 精度: 相对误差 <= 6.3e-15.
配置 (a,b): (0.3,0.7), (0.25,0.62), (0.4,0.8), (0.3825,0.6175), R=4.
结论: 恒等式对模式 1 (相位 A,B) 与模式 2 (相位 tau*A,tau*B) 均成立至机器精度.
对应文档引理 lem:energy (STRICT 证明, 不依赖本条目).

## 2. 相位比 r~_tau 的单调性阈值

脚本: `scripts/_well_explore2.py`, `scripts/_well_verify_thm.py`,
`scripts/_well_verify_rc.py`.
- m=1.1 (R=1.21), tau in {1.2,2,4}: 单调性违规数 0 (递减).
- m=1.5 (R=2.25), m=2, m=3: 违规数 1 (非单调).
- R=1.4, 1.5: log r~_tau 最大步长 <= 4.4e-16 (递减至机器精度, 网格 40001).
- R=1.6, 1.7: 最大正步 1.8e-6, 4.6e-6 (非单调).
结论: 单调性阈值恰在 R=3/2. 对应文档引理 lem:rtau 的 R<=3/2 假设 (STRICT 证明)
与注 rem:threshold 的阈值精确性 (EVIDENCE).

## 3. Psi~'(x) 符号表与阈值

脚本: `scripts/_well_rigid_verify.py` (B1), `scripts/_well_psitilde.py`,
`scripts/_well_verify_rc.py`, `scripts/_well_H.py`.
- q = R-1 取 0, 0.25, 0.5: max Psi~' 于 (0,pi) 内部网格 = -6.7e-6, -2.7e-6,
  -6.9e-13 (均 < 0; q=0.5 的极小负值靠近边界 x->pi-).
- q = 0.5001, 0.55: max Psi~' = +4.4e-7, +4.7e-3 (出现正值).
- m 取 1.20, 1.2247 (=sqrt(1.5)), 1.23, 1.25: max Psi~' = -6e-6, -0.000000,
  +6.4e-4, +6.5e-3. 阈值 m = sqrt(1.5).
- 注: `scripts/_well_mc.py` 的 Psi 定义缺少 q 项, 输出无意义 (见第 10 节缺陷登记),
  以 `_well_psitilde.py`/`_well_verify_rc.py` 为准.

## 4. good root 数值表

脚本: `scripts/_well_rigid_verify.py` (B4), `scripts/_well_n1refine.py`,
`misc/_well_explore3.py`; 求解器: `scripts/_well_landscape2.py` (转移矩阵
secular, 网格 6000-12000, brentq xtol=1e-12), least_squares cost 判据 1e-16.
- R=1.5: 唯一 sign-consistent good root (6 种子收敛)
  (a,b) = (0.40879841, 0.59120159), a+b=1.0000000000 (误差 <= 1e-10),
  A=B=1.36620147 (|A-B| <= 4e-13), tau=1.891551, tau*A=2.584240 < pi,
  r~_tau(A)=r~_tau(B)=0.2189882504, D=19.19538813.
  符号: y2(a)=+0.08367 > 0, y2(b)=-0.08367 < 0, y2 零点 x=0.5000 in (a,b).
- R=4: `_well_explore3.py` 全参数三角形 Newton/least_squares 找到 7 个
  R1=R2=0 临界点; sign-consistent 的只有对称内点 (0.38259835, 0.61740165)
  (D=6.7844823391, R1=R2~1e-15) 与两个边界点 (0.2498,1.0), (0.0,0.7502)
  (D=15.6128); 其余 4 个 sign_ok=False.
  对称线 D 极小值 u*=0.38259826, D*=6.78448234.
- 粗网格下确界 (R=4): 6.7877 于 (0.3857,0.6091), 高于对称极小 6.7845
  (`_well_landscape2.py` 主程序).

## 5. 对称线单峰性与 f 零点

脚本: `scripts/_well_symline.py`, `scripts/_well_fzeros.py`,
`scripts/_well_fine.py`.
- R=1.05..400 (10 个值): 对称线 (0,1/2) 上 D(v) 每 R 恰 1 个局部极小,
  D* < 3pi^2/R 处处成立 (例: R=1.1: D*=28.1025 < 28.1989; R=4:
  D*=6.7845 < 7.4022; R=400: D*=0.0625 < 0.0740).
- v* 随 R 递减: 0.41813 (R=1.1) -> 0.33135 (R=400).
- f(v) = f_{v,1-v}(v) 零点数: R<=4 恰 1 (例 R=1.1: 0.4183; R=4: 0.3827);
  R=10, 100 时粗网格报 3 个密集零点 [0.3611,0.36125,0.36149] 等,
  经 `_well_fine.py` 细网格确认为数值伪影: 实际仅 1 个局部极小
  (R=10: v=0.361315, D=2.608915; R=100: v=0.33474, D=0.250933).
- 端点极限: D(v->0) = 3pi^2 (rho=1), D(v->1/2) = 3pi^2/R (rho=R), 均大于 D*.

## 6. Feynman-Hellmann 符号与公式

脚本: `misc/_well_fh2.py` (正确), `misc/_well_fh.py` (缺陷, 见第 10 节),
`scripts/_well_rigid_verify.py` fval.
- 单特征值 FH: d lambda_k/da = -lambda_k*(R-1)*y_k(a)^2/n, 数值验证到 1e-8
  (R=4, a=0.35: FD dlam1/da=-7.67251 vs 公式 -7.67251; dlam2/da=-10.09253
  vs -10.09254).
- 阱族 f = lambda2*y2^2/n2 - lambda1*y1^2/n1 (well 约定):
  dD/da = -(R-1) f(a), dD/db = +(R-1) f(b).
  R=4, (0.35,0.65): f(a)=f(b)=+0.8050, (R-1)f = 2.415 vs FD dD/da=-2.42,
  dD/db=+2.42.
- 带状自洽 (R=4 对称 good root): f(0.1)=+1.72, f(0.2)=+4.12, f(0.3)=+3.06
  (阱内 >0), f(0.45)=-1.85, f(0.5)=-2.28 (中区 <0), f(a)=f(b)=0.
  => {f>0} = 阱 = {rho = R}.

## 7. 范数方程 N1 与能量比 (R>3/2 候选路线)

脚本: `scripts/_well_n1curve.py`, `scripts/_well_n1refine.py`,
`scripts/_well_energy_ratio.py`.
- R=4 离轴 E=0 分支 (r~_tau(A)=r~_tau(B), A!=B, a in [0.015,0.16]):
  N1 = n2/n1 - sin^2(tau A)/sin^2 A 严格为负, 采样 6 点 N1 in [-2.76,-2.61].
- R=1.5 对称线: N1(v,1-v) = -1.858 (v=0.2), -0.794 (v=0.3),
  ~-1e-4 (v=v*=0.4088, 与积分精度同阶), +0.180 (v=0.45);
  零点在 v ~ v* (good root 处 N1 穿越 0, 数值支持 "good root 满足 N1=0" 的候选恒等式).
- 能量比: R=4 离轴分支 E2/E1 = int(y2')^2/int(y1')^2 <= 1.25,
  而 tau^2 sin^2(tau A)/sin^2 A >= 7.14.
  候选路线: 若证明 (i) good root 处 N1=0 (恒等式, 未证), (ii) 离轴 E=0 分支
  N1<0 对一切 R>3/2 (未证), 则刚性可推到一般 R. 两点均开放.

## 8. 离轴 E=0 分支出现阈值

脚本: `scripts/_well_branch_threshold.py`, `scripts/_well_verify_thm.py`.
- R=1.20, 1.50: 无离轴分支; R=1.52, 1.55, 1.60: 有;
  R=1.80, 2.00, 2.25, 2.50, 3.00, 4.00: 有.
结论: 分支出现阈值 ~ R=3/2, 与 r~_tau 单调性阈值一致.

## 9. 固定阱长非对称性 (EVIDENCE)

- 固定阱总长 1-2v 时 D 对 (a,b) 非对称: R=4 存在非对称临界点但 sign_ok=False
  (第 4 节), 粗网格下确界偏向对称线. 不存在被证实的非对称 sign-consistent
  good root (R=1.5 与 R=4 均如此).

## 10. 缺陷脚本登记 (E3 工具)

- `scripts/_well_mc.py`: Psi 定义缺 q 项, 输出 (min dPsi ~ -1.6e10) 无意义;
  被 `_well_psitilde.py` / `_well_verify_rc.py` 取代.
- `misc/_well_fh.py`: f1 定义为 lam1*y1^2/n1 - lam2*y2^2/n2 (垒族约定) 且
  数值与已验证的 fval/FH 公式不一致 (R=4 对称点报 R1=4.51, 正确为 0);
  被 `misc/_well_fh2.py` 与 `scripts/_well_rigid_verify.py` fval 取代.
- `scripts/_well_system_derive.py`: sec_value 中 X 项多 1/m 因子 (仅符号探索用);
  实际求解器 `_well_landscape2.py` 的 well_secular 与手推转移矩阵一致.
- `scripts/_well_landscape2.py` norm2_well 用梯形积分 (n<=1200), 绝对精度
  ~1e-4, 用于 N1 探针时以 n=2000..8000 交叉; N1 绝对值 ~1e-4 量级判定为
  积分精度噪声.

## 11. 文献判定: Sun 2022 (JMAA 516, 10.1016/j.jmaa.2022.126513)

- 全文不可达 (非 OA, ScienceDirect captcha, Sci-Hub 无 2022 后文献, 无 arXiv).
- 官方摘要 (colab.ws) 确认: 最优性条件 + 直接法刻画极值密度, 含极值特征函数
  与几何形状; zbMATH 评论 (评审 Erdogan Sen, Zbl 1506.34110) 确认密度类为
  "piecewise continuous with a bounded of jumps".
- 判定: 不能闭合我们的盒类 (1<=rho<=R 全可测) INF 侧; 潜在重叠需全文,
  作者主页/机构库不可达, 已登记. 文件: `research_cache/zb_review_1506.34110.txt`,
  `research_cache/lit_sun_qixie_notes.txt`, `research_cache/colabws_sun_jina.txt`,
  `misc/mardi_sun2022.html`, `misc/sd_sun2022.html`.
- 相关下载: `papers/ashbaugh1991_gaps.pdf` (Ashbaugh-Harrell-Svirsky 1991,
  Schrodinger L^p 势类 gap 极值, 机制相关但非同一问题, 不抢注).

## 12. 脚本索引 (本会话阱族工作)

`scripts/_well_landscape2.py` 阱道快速求解器 (secular + brentq)
`scripts/_well_rigid_verify.py` 本会话验证矩阵 (8 符号恒等式 + 5 数值探针)
`scripts/_well_signcheck.py` R=1.5 good root 符号/相位范围检查
`scripts/_well_n1refine.py` N1 高精度复算 + 离轴分支
`scripts/_well_crit.py` 临界点搜索 + Hessian (慢; R=1.5 全搜超时, 用种子版)
`scripts/_well_symline.py` 对称线 D(v) 多 R 扫描
`scripts/_well_fzeros.py` f(v) 零点计数
`scripts/_well_fine.py` 细网格局部极小确认
`scripts/_well_verify_thm.py` H'>=0 / r~_tau 阈值 / 离轴分支
`scripts/_well_verify_rc.py` Psi~' 阈值 + r~_tau@R=1.5
`scripts/_well_psitilde.py` Psi~' 扫描
`scripts/_well_psi_factor.py` Psi~' 因式分解 (sympy)
`scripts/_well_H.py` H 与 H' 结构
`scripts/_well_n1curve.py` 离轴 N1 符号
`scripts/_well_energy_ratio.py` 能量比探针
`scripts/_well_branch_threshold.py` 离轴分支阈值扫描
`scripts/_well_system_derive.py` good-root 系统符号推导 (含已知缺陷)
`misc/_well_explore1.py` 传输恒等式数值确认
`misc/_well_explore2.py` r~_tau 单调性扫描
`misc/_well_explore3.py` R=4 临界点全表 + 符号分类
`misc/_well_fh.py` FH 检查 (缺陷, 见第 10 节)
`misc/_well_fh2.py` 单特征值 FH 验证 (正确)
`misc/_well_norm.py` 范数探针
`misc/_well_phi.py` 相位探针

精度约定: 除注明外浮点 float64; 特征值 brentq xtol=1e-12..1e-13;
临界点 least_squares cost < 1e-16..1e-20; 积分梯形 n<=8000.
所有本文件条目均为 EVIDENCE, 不构成定理依据.

## 13. 缺口 (a) 闭合: 对称线 1D 分析 (KEY LEMMA 数值核验, EVIDENCE)

脚本: `scripts/_symline/master_verify.py`, `key_lemma_verify.py`,
`key_lemma_verify2.py`, `sym_endpoint_fixed.py`, `key_lemma_certificate.py`.
严格证明见 `docs/SL_gap_n1_symline_proof.pdf` (10 页零警告); 本文件所有条目
不构成证明.

- 相位分支 vs 直接 secular: 相对误差 <= 1e-51 (R=1.2,1.5,4.0; v=0.1..0.49).
- P1/P2 余量: max G1 ~ -2.4621 < -1.7394 = (6 sqrt6 - 6)/5; min G2 ~ -0.4000 >
  -1.2247 = -sqrt(3/2) > -4/3; max(G1-G2) ~ -2.2304 < 0 (网格 (0,1/2)x[q0,1],
  21x49 点).
- c*: 0.1821 (q~ = q0), 0.1917 (q~ = 1); max F~_e' 于 {F~_e >= 0} <= -7.58;
  易区 c in [1/2,50]: max F~_e <= -2.6e-7.
- 端点: F~_e(1e-6) ~ 3.0219 = pi^2/(4 q0); F~_e(1/2) < 0; alpha1(1/2)+alpha2(1/2)
  = pi 至 1e-31; tan(alpha1(1/2)/2) = 1/sqrt(2 q~ + 1) 至 1e-31;
  F~_e(1/2) 结构公式与直接值比值 = 1 至 1e-31.
- 导数闭式 (备查): F~_e''(q,1/2) 区间复算为正值 (+18..+27), 推翻交接摘要
  "F~_e'' < 0" 断言; F~_e'(q,1/2) = -2pi(1-cos x)^3 T(x)/sin^3 x, x = arccos(q/(1+q)),
  T > 0 于 [pi/3,pi/2], 数值验证至 1e-29.
- W0 引理: W0(Gamma) ~ 0.9500 < 1.0887 = (4/3) q0; W0 于 (0,Gamma] 递增;
  W0(0.001) ~ -6278 (负), W0(0.1) ~ -57.6, W0(0+) = 3-2pi < 0: W0 可负, P2 必须
  分情形. gamma <= Gamma 全过; W0 分情形样本 878 (W0<=0, 全 G2>=0) + 151
  (W0>0, 全 G2 >= -W0/q~).
- 降维恒等式: S_R(xi) = -8 q~^2 (c+q~)^3 F~_e(c) 相对误差 <= 1.3e-11
  (R=1.2,1.5; v=0.2..0.45); D_c 与 -F~_e 同号检验 0 违规.
- D(v) 结构: R=1.2: v* ~ 0.415, D* ~ 24.3622; R=1.5: v* ~ 0.409, D* ~ 19.1954;
  D(0.001) ~ 29.6088 = 3pi^2; D(0.499) -> 3pi^2/R; 递减/递增区间检验通过.
- 精确有理证书 (key_lemma_certificate.py): q0 > 2247/2753; q0/(1+q0) >
  2247/5000 > 8783/19683 > cos(10/9); cot(10/9) > 2121769/4288410;
  271586432/135084915 > 15789/8259; 全部 sympy True.

## 14. 缺陷脚本登记 (会话 52, 对称线)

- `scripts/_symline/master_verify.py`: mode-2 范数闭式与直接积分相对误差 ~0.5
  (KEY LEMMA 不依赖范数闭式, 不影响任何结论; 登记备用).
- `scripts/_symline/sym_endpoint.py` (未修正版): G2 第二项多乘因子 t (应为 pi-t),
  导致 c=1/2 闭式对 q<1 错误; 修正版 `sym_endpoint_fixed.py`.
- `scripts/_symline/key_lemma_verify.py` 初版: 3pi^2/R 对照值误打印为 3pi^2*m^2
  (数值本身正确; 已修正).

## 15. 脚本索引 (会话 52 对称线工作)

`scripts/_symline/master_verify.py` 相位分支 vs secular + 范数闭式 (含缺陷)
`scripts/_symline/key_lemma_verify.py` P1/P2/c*/端点/降维恒等式主核验
`scripts/_symline/key_lemma_verify2.py` gamma<=Gamma/W0 分情形/结构恒等式
`scripts/_symline/sym_endpoint_fixed.py` c=1/2 导数闭式与 W0/G2 修正版
`scripts/_symline/key_lemma_certificate.py` W0 精确有理证书 (sympy)
`scripts/_symline/fe_relations.py, fepp_full.py, fep_shape.py, g2_structure.py,
margin2.py, q_monotone.py, sym_dq*.py, threshold_scan.py, ...` 探索期脚本
(失败路线复算与 F~_e'' 符号判定, 详见 docs/SL_gap_n1_symline_summary.pdf 第 3 节)

精度约定: 除注明外 float64; 相位分支求根 xtol 1e-12..1e-13; 恒等式核验
mpmath 50 位 (key_lemma_verify2.py). 所有本文件条目均为 EVIDENCE, 不构成定理依据.
## 16. 缺口 (b) 闭合: 阱族全 R 相位刚性 (会话 55/56, 一切 R>1)

脚本: `scripts/_gapb_s55/` (会话 55 交接 + 本会话复核). 严格证明见
`docs/SL_gap_n1_well_rigidity_allR_proof.pdf` (14 页零警告) 与总结
`docs/SL_gap_n1_well_rigidity_allR_summary.pdf` (8 页零警告). 本文件所有条目
均为 EVIDENCE, 不构成证明.

- 复核 `_s55_full_verify.py` 全过: L0/BETA/引理 A/危险区/范数闭式; 中间区递减
  仅 tau>=2.5 失败 (证明前提 tau<2); alpha-反射网格仅精确边界 1-ulp 伪影取等.
- 区域 II 等值对 (R=100, tau=1.22): 867 对, 最小 x+y = 3.2159 > pi, 与 B' 一致.
- B' 全局最小值: 45 个 (R,tau) 配置, min x+y = 3.1421822, 最小余量 ~5.9e-4
  (R=10^4, tau=1.4).
- 危险区引理: 8 个 R 值、4 个 tau 值, 约 124 万样本, 0 违反.
- tau 上界: sign-consistent 890 配置 max tau = 1.99995184 (R=1.01, a=0.05,
  b=0.95), R->1+ 时 tau->2-; 一般配置反例 R=10^4, a=0.05, b=0.85 -> tau~4.70.
- D(x)=alpha(2x)-2alpha(x) >= 0: 6 个 R, 2000 点, min ~9.7e-13 > 0.
- 范数闭式: 三段直接积分 vs 闭式到 1e-40; C^2 = W(A)/W(B) 到 1e-40; sympy
  在切形式约束 (tan psi 公式) 下差为精确 0; 自由变量下非零 (约束必须代入).
- 细化对称 good root (R=4): v* = 0.3825982567998447..., A = B = 1.45756580
  in (x_mid, pi/tau); |R1| < 1e-50, Sigma2/Sigma1 = tau^2 r(A) = tau^2 r(B)
  到 1e-51. 8 位精度 v* 曾产生假非零残差 (教训: 残差恒等式需高精度根定位).
- 模态恒等式: 171 个 sign-consistent 配置失败数 0/0; P-和恒等式到 1.4e-40.
- 早期失败断言反例: (0,pi/tau) 全域 tau sin(tau x) > sin x 为假 (仅
  (0,x_mid)); r(y) > r(pi-y) 为假 (R=100, tau=1.22, y=1.64159: 0.0675 <
  0.1871); r_tau 于 (0,x_mid) 单调为假 (大 R 有鼓包, 但 L3 论证不依赖单调性).
- 交接 L0 逆式有抄写错误, 以差积公式重导出正确版本.

精度约定: mpmath 30-50 位; 特征值求根 bisect xtol 1e-12; 恒等式对照
1e-30..1e-40. 所有本文件条目均为 EVIDENCE, 不构成定理依据.
