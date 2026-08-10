---
canonical_key: key lemma decomposition G2-G1=(A-C)+(B-D) with exact corner limit 4*pi/(3*sqrt3)
title: KEY LEMMA 分解与逐项 q-单调性否证 (key-lemma-decomposition)
tags: [mathtool, self-developed, obstruction]
source: 自研 (coordinator, run R-20260805T000000Z-gapn1-a1b2c3)
status: 分解推导 + 精确角点极限 (已证) + B-D q-单调性否证 (反例已复现) + KEY LEMMA 已证 (独立审计 2026-08-06) + (LOG) 完全解析化 (thm:LOG, 2026-08-09)
created: 2026-08-05
---

# KEY LEMMA 分解与逐项 q-单调性否证 (key-lemma-decomposition)

## 解析
对对称垒 $[1,R,1]$, 记 $q=\sqrt R$, $\alpha_k(c)$ 为半问题 secular 曲线与 $\beta=c\alpha$
的交点. O2 的 KEY LEMMA 等价于 $G(\alpha_2(c);c)>G(\alpha_1(c);c)$, 其中
$$G(\alpha;c)=-\frac{\Phi(\alpha)W(\alpha)}{q+c\Phi(\alpha)}
+\frac{2c\alpha\Phi(\alpha)(q^2-1)\sin\alpha\cos\alpha}{(q+c\Phi(\alpha))^2},
\qquad W(\alpha)=3+2\alpha\cot\alpha.$$

**分解**: 令 $\alpha_2=\pi-\gamma$, 则
$$G_2-G_1=(A-C)+(B-D),$$
$$A-C=\frac{\Phi_1W_1}{q+c\Phi_1}-\frac{2c(q^2-1)\alpha_1\Phi_1\sin\alpha_1\cos\alpha_1}{(q+c\Phi_1)^2},
\qquad
B-D=-\frac{\Phi_2W_2}{q+c\Phi_2}
+\frac{2c(q^2-1)\alpha_2\Phi_2|\sin\alpha_2\cos\alpha_2|}{(q+c\Phi_2)^2}.$$

**q=1 基值闭式**: $\alpha_1=\pi/(2(1+c))$, $\alpha_2=\pi/(1+c)$, $\Phi\equiv1$,
$(q^2-1)=0$ 时
$$(A-C)|_{q=1}=\frac{W(\alpha_1)}{1+c},\qquad (B-D)|_{q=1}=-\frac{W(\alpha_2)}{1+c}.$$
由 $W'=2(\sin\alpha\cos\alpha-\alpha)/\sin^2\alpha<0$ 得
$$(G_2-G_1)|_{q=1}\ge\frac{W(\pi/3)-W(2\pi/3)}{3/2}=\frac{4\pi}{3\sqrt3}=2.41840\ldots>0.$$

**精确角点极限** ($q\to1^+$, $c\to1/2^-$): $A-C\to W(\pi/3)/(3/2)=2.80613\ldots$,
$B-D\to-W(2\pi/3)/(3/2)=-0.38773\ldots$, 和 $\to4\pi/(3\sqrt3)$.

## 否证 (逐项 q-单调性, 精确反例)
交接稿曾主张 $d(A-C)/dq\ge0$ 且 $d(B-D)/dq\ge0$ 在全网格成立, 据此闭环 KEY LEMMA.
独立复核 (细网格): **$A-C$ 对 $q$ 单调递增 (全采样通过), 但 $B-D$ 不单调**:
反例 $c=0.01$, $q\colon5000\to20000$ 时 $B-D\colon199.79\to193.99$ (递减);
$c\le0.1$ 均递减, $c\ge0.3$ 才递增. 因此``分解 + 逐项 q-单调''闭环作废.

## 适用范围
- 适用: 对称三块族相邻间距的驻点/单次穿零分析; KEY LEMMA 型对数导数不等式
  $d\log(M_1/M_2)/dc<0$ 的等价变换; 分解+基值+单调性的复合证明模板.
- 边界情形: $q\to1^+$ 角点需按 $c\to1/2^-$ 展开; 大 $q$ 小 $c$ 区是单调性最容易
  失效的区域 (B-D 大正但递减, 和仍稳健).
- 不适用: 当需要逐项单调性时, 必须逐项独立验证; 任何``数值全网格通过''的声明
  都要交代网格分辨率与极端区采样 (本工具即以反例说明此陷阱).
- 限制: 分解本身是恒等式, 精确角点极限已证; 但 KEY LEMMA 的整体证明仍开放.

## 验证与备注
- 来源: run R-20260805T000000Z-gapn1-a1b2c3 (Agent A 的 O2 报告 + coordinator 分解);
  独立复核脚本 misc/_verify_decomp.py, misc/_verify_bdmono.py, misc/_verify_acmono.py.
- 数值: 全网格 $q\in[1.00025,10^6]$, $c\in(0,1/2)$ 上 $G_2-G_1\ge2.41840$,
  最小值在角点; KEY LEMMA 余量 (对数导数形式) min 2.4481 (R=1.1) 至 19.45 (R=1e4).
- 经验: 交接数值表 (A-C min 2.8086, B-D min -0.3751, 和 2.4258) 为粗网格值,
  精确角点极限为 2.80613/-0.38773/2.41840, 以本文为准.


## 2026-08-06 更新: KEY LEMMA 归约到四引理 (run R-20260806T011500Z-keylemma-E58FB1)
独立 run 把 KEY LEMMA 归约到四个显式局部不等式, 全部数值验证带量化余量, 但解析证明开放:
- R1: G2 >= 0 for q >= 2, c in (0,1/2); 紧点 (2,1/2), 余量 0.069181 (精确角值).
- R2: G2 >= 0 for q > 1, c in (0,0.4]; 余量 0.415004.
- L4box: H' = G2'-G1' < 0 on (1,2]x[0.4,0.5]; 余量 7.7317.
- L5box: F~'' = M~1 J1 - M~2 J2 > 0 on (1,2]x[0.4,0.5]; 余量 14.167.
基座引理已证: L1 (G1<0 全域), L2 (G2>=0 => 两形式成立), B1-B3 (q=1 族), B4
(F~'(q,1/2)=2 pi (cos x-1)^3 P(x)/sin^3 x < 0, P(x)>(pi-3x)^2), B5 (H(q,1/2)=
2 pi q(q+1)/(2q+1)^{3/2} 严格递增, min 4 pi/(3 sqrt3)), B7 (G2(c;1)>0 for c<=0.4).
关键开放核心 Q1: dG2/dq >= 0 (全域数值成立, 衰减到 0) 可把 R1/R2 归约到一维边界 B6/B7.
审计发现 C1 (重要更正): (LOG) 形式 (d/dc)log(M1/M2)<0 与 (FP) 形式 F'(c)<0 并非逻辑等价;
源报告 T4 只消费 (FP) (F 在 (0,1/2) 严格递减); 两形式须分别证明.
四引理闭合后: R1^R2^L4box^L5box^B1-B5^B7 => (LOG)^(FP) => T1-T4 关闭 O2.

## 2026-08-06 更新: 四引理全部关闭 (run R-20260806T070000Z-keylemma2b-0A6D8F)
KEY LEMMA ((LOG) 与 (FP) 两形式) 已完成证明, 状态 CANDIDATE_COMPLETE_PROOF.
- R1, R2: 经由 (q,u) 换元 (u = q*tan(gamma) = tan(c*A)), 归结为 M2 (dIN/du < 0 on
  D) 与两个一维边界引理 CORNER (G2(1/2;q) >= 0, q >= 2, 闭式 + 初等 pi 证书) 与 C4
  (G2(0.4;q) >= 0, q >= 1, 曲线参数化 IN = A*K(v), 区间证书 + 精确有理数尾部下界
  T^3 K >= 178.85896 > 0).  M2 由 M2(1,u) = pi*h(u) < 0 (h 凹, 极值 < 0) 与
  dM2/dq < 0 (证书 [1,20]x[0,sqrt(41)] 含新增 strip 证书 + 初等尾部界 B(q)) 闭合.
- L4box, L5box: 128 叶向外舍入区间算术证书, 全部通过独立第二引擎 (mpmath.iv)
  复验 (worst -4.8416 / +8.3794, 0 失败).
- 四份证书 (dM2dq, C4, L4box, L5box) 均由两个独立引擎验证; 发现并修正 shipped
  verifier 中 C4 过期区域常数, 发现并补上 dM2/dq 证书未覆盖的 strip
  [1,20]x[y1,sqrt(41)] (新增 cert_dM2dq_strip_boxes.json, 独立复验通过).
- 工具要点: 证书生成引擎 riarith.iv_sqrt 并非严格向外舍入 (Decimal.sqrt 用最近舍入,
  下界可高出真值 ~1e-60); 所有符号结论由 sound 的 mpmath.iv 引擎独立重导, 不承重.
- 工件: runs/rigorous-open-math-research/R-20260806T070000Z-keylemma2b-0A6D8F/
  (candidate_proof.md, audit_report.md, 全套标准工件, reproducibility/ 脚本与捕获).

## 2026-08-06 更新: 独立审计通过, 状态升级 (run R-20260806T140000Z-keylemmaaudit-2F83B1)
KEY LEMMA 候选证明经第二独立实体审计, 状态 verbatim: INDEPENDENTLY_AUDITED_PROOF.
- 审计不信任产出 run 自审, 从第一性原理重导全部符号/解析/证书层: 符号 diff = 0
  覆盖 E1-E9, (q,u) 换元, IN = G2*POS, M2, dM2/dq, CORNER, IN = A*K(v) (用
  atan(tan v) = v 后 diff = 0, 产出 run 的 caveat 就此解除), T^3K 尾部, B4/B5.
- 证书层: 自建 80 位定向舍入 Decimal 区间引擎, 五份证书全部复验 (dM2dq 主盒
  -0.1902428, strip -448.7453, C4 +2.49716, L4 -4.8416038, L5 +8.3793828),
  (y1+1e-30)^2 > 41 精确成立, 精确有理数铺片 + 缝隙桥接, 复跑可复现.
- 确认 caveat: riarith.iv_sqrt 非严格性属实但审计引擎独立不受影响; C4 自带验证
  脚本区域常数过时, 审计改用证书自身端点 + 认证 pi 覆盖.
- 程序级结论: O2 义务 CLOSED; (LOG) 与 (FP) 两形式对一切 q>1, c in (0,1/2) 成立.
- 工件: runs/rigorous-open-math-research/R-20260806T140000Z-keylemmaaudit-2F83B1/
  (audit_report.md, candidate_proof.md 独立重建, reproducibility/audit_*.py).

## 2026-08-09 更新: 伴随命题 (LOG) 完全解析化 (thm:LOG), 128 叶盒证书退役
O3a 文档 (docs/SL_gap_n1_O3a_phase_rigidity_proof.tex, 32 页零警告) 中伴随命题
(LOG): d/dc log(M~f1/M~f2) = G1 - G2 < 0 由纯解析证明 (E1) 完成, 取代旧 128 叶盒
证书 (H' = (G2-G1)' < 0 于闭盒 Q 的叶盒覆盖路线).
- 第二相位恒等式: 令 gamma = pi - alpha2, A = pi - gamma, c = c2(gamma,q),
  Phi = cos^2 gamma + q^2 sin^2 gamma, D = q + c Phi,
  W0 = 3 - 2A cot gamma, P = c A Phi (q^2-1) sin gamma cos gamma / D^2, 则
  G2 = -Phi W0/D - 2P (sympy 精确验证 diff = 0).
- 三个估计 (盒 Q = [1,2] x [0.4,0.5], 0.655 <= gamma <= pi/3):
  (i)  Phi/D <= 65/66: u = Phi/q 关于 q 凸 (d^2u/dq^2 > 0), 端点 u(1) = 1,
       u(2) <= 13/8 (sin^2 gamma <= 3/4), c >= 0.4;
  (ii) W0 <= 3 - 4pi/(3 sqrt3) < 0.582: W0 在 [0.655, pi/3] 严格递增,
       pi > 3.1415, sqrt3 < 1.7321;
  (iii) P < 0.576: Phi(q^2-1)/D^2 <= 25/27 (f(Phi) 递增因 q - cPhi >= 0;
       h(q) = (q^2-1)/(1+0.4q)^2 递增, h(2) = 25/27), c sin gamma cos gamma
       <= 1/4, A <= pi - 0.655.
  组合: G2 >= -(65/66)(0.582) - 2(0.576) > -1.725 > -2.
- 定理 thm:LOG 证明: G2 >= 0 时由 lem:G1 (G1 < 0); G2 < 0 时 (q,c) 落入盒内,
  由 lem:G2m2 (G2 > -2) 与 thm:j1e1 第 (iii) 步 (G1 < -2) 得 G1 - G2 < 0.
- 验证: scripts/verify_o3a_LOG_analytic.py (mpmath 35 位): 盒上四界与
  G2 > -2 全 PASS (min G2 ≈ -0.3823, 下界 -1.725), 全域网格 min H = G2 - G1
  ≈ 2.472 > 0 (LOG). 该脚本是 E1 链的交叉检验 (E3 类), 不构成证明本身.
- 至此 O3a 文档四族证书 (J1 16 叶盒 / J2 67 叶盒 / C4 200 叶盒 / (LOG) 128
  叶盒) 全部解析化移除, 全文零证书: 证据分层为 E1 (严格解析) + E2 (单变量
  事实验证器, thm:j2e1 的 55 项事实) + E3 (数值扫描, 仅交叉检验).
