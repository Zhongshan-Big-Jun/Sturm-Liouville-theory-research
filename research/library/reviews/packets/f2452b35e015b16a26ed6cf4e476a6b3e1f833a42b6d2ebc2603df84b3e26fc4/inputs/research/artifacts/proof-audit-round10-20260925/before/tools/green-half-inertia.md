---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c3da-1dd6-7e83-a355-61239cbfe206"], "canonical_key": "green-half-inertia (n>=2 gap Jacobian Green-kernel inertia reduction)", "created": "2026-08-13", "dependencies": [{"location": "tools/feynman-hellmann.md", "sha256": "da33642d9b86de9587760ffc635f9b4e655fc86c6610b75c1732dc0920095611"}], "evidence_status": "ROUND7_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT", "resources": [{"kind": "program", "locator": "Scoped finite exact and numerical checks; not complete Green audit", "path": "research/artifacts/proof-audit-round7-20260921/checks/checks.py", "sha256": "7dd9ef3f7b3b3544d9f69a6a355a32278fa2132622437624e16253c9fe5b911a"}, {"kind": "source-audit", "locator": "Confirmed direct propagation and untouched historical scope", "path": "research/artifacts/proof-audit-round7-20260921/checks/propagation.md", "sha256": "f9eae002f40576f74fd7d9a89f5de9c516f95b56c274f56f2c00087a33246a46"}], "scope": "Only explicit round7 determinant/inertia, normalization and coordinate corrections. Retained historical derivations are not newly certified.", "source": "自研 (R-205 历史记录; 第七轮修订入口 docs/SL_gap_nge2_symmetry_local_proof.tex 与 reports/proof-audit-round7-20260921/REPORT.md)", "sources": [{"locator": "Round7 local proof and explicitly scoped tail corrections", "path": "docs/SL_gap_nge2_symmetry_local_proof.tex", "sha256": "c71a98c666492b9b947378432533fa60ea44dfee3029e0d21711cdc6cafa61b1"}, {"locator": "Historical reconnaissance; round7 general-n supremum scope correction", "path": "docs/SL_gap_nge2_symmetry_recon.tex", "sha256": "dabfe0c359d75ab673f6f511ac0f72f8528e1313226c7e8219acc34301df100c"}], "status": "第七轮范围修订; 当前精确版本的可复用性由纠错回执控制; 历史 Green/M3/KP 与全 R 分支未获本轮整体认证", "summary": "对称密度才可使用镜像奇偶扇区. 有限点Green核惯性强化等式保留为待核验历史内容; 单凭detK>0不能推出定性. 奇扇区定性还不能替代另一扇区与完整G1义务. 第七轮范围修订按精确纠错回执检索, 不据历史STRICT标签宣布全局闭合.", "tags": ["mathtool", "self-developed", "green-function", "inertia", "oscillation", "gap-extremals", "nge2"], "title": "半问题 Green 与惯性: 对称支上的定性充分判据与奇偶性边界", "tool_id": "green-half-inertia", "updated": "2026-09-21"}
---

# 半问题 Green 惯性 (K_o 的 Green 函数化归)

## 第七轮修订范围

本卡是直接传播修订候选. 当前证明入口为
[局部对称性证明](../docs/SL_gap_nge2_symmetry_local_proof.tex),
修订和实际审查状态见 [第七轮 REPORT](../reports/proof-audit-round7-20260921/REPORT.md).
链接由协调器绑定最终版本, 不作验收凭据.
本轮区分 (G1') 的行列式条件与更强的 Hessian/扇区定性;
不全盘重审旧 Green、零点强化、M3/KP 或半问题表达式.
以下数值、原 STRICT 标记及运行说明是历史记录, 本轮未重跑或重新认证.

## 解析

### 奇偶性更正 (否证, EVIDENCE)
特征函数的反射奇偶性
$u_k(1-x)=(-1)^{k-1}u_k(x)$ 由 ODE 的反射不变性推出, 等价于
$\rho(1-x)=\rho(x)$ 作为函数成立, 即**宽度**回文
($w_i=w_{2n+2-i}$). 交替 bang-bang 图案只给出**高度**回文
($\sigma_i=\sigma_{2n+2-i}$); 宽度不对称时 $\rho(1-x)\ne\rho(x)$, 奇偶性
不成立. 随机 Dirichlet 宽度数值: 奇偶性与 $f$ 偶性误差 O(1)
(最坏 1.072 / 1.290), 对称支上为 1e-16. 因此镜像扇区分解、括号恒等式与
$H_e/H_o$ 的 Green 闭式**只在对称带自洽点成立**, 不能反过来证明对称性
(循环); 全局对称性结论仍走 (G1')+(G2) 的唯一性路线.

### 全局 ε 交错的历史输入 (原标记 STRICT, 本轮未重审)
见 [[switch-saturation-k-invariant]] 的 R-205 更新: 在 $f$ 的 $2n$ 个有序
简单零点处 $\varepsilon_j=(-1)^{j+1}$. 这是 $K$ 非对角闭式 (C1)/(C2) 在
一切带自洽点成立的正确全局输入.

### 半问题谱交错与有限点 Green 惯性边界
在对称支上把 $[0,1]$ 于 $x=1/2$ 对半: 偶特征函数 ($u'(1/2)=0$) 对应
Neumann 半问题, 奇特征函数 ($u(1/2)=0$) 对应 Dirichlet 半问题. 设
$\mu_k^N<\mu_k^D<\mu_{k+1}^N$ 为两半问题特征值, 则
\begin{equation*}
  n=2m:\ \lambda_n=\mu_m^D,\ \lambda_{n+1}=\mu_{m+1}^N;\qquad
  n=2m-1:\ \lambda_n=\mu_m^N,\ \lambda_{n+1}=\mu_m^D.
\end{equation*}
在 $n$ 个左半开关 $x_1<\cdots<x_n<1/2$ 上定义奇扇区约化预解核 (异奇偶类):
\begin{equation*}
  R_n^\bot=\sum_{l:\ \mathrm{par}(l)\ne\mathrm{par}(n)}
  \frac{u_l(x_i)u_l(x_j)}{\lambda_l-\lambda_n},\qquad
  R_{n+1}^\bot=\sum_{l:\ \mathrm{par}(l)\ne\mathrm{par}(n+1)}
  \frac{u_l(x_i)u_l(x_j)}{\lambda_l-\lambda_{n+1}}.
\end{equation*}
以下是历史记录声称的有限点核矩阵负指数等式, 本轮未核验:
\begin{equation*}
  n\ \text{偶}:\ \operatorname{neg} R_n^\bot=\operatorname{neg} R_{n+1}^\bot
  =\tfrac n2;\qquad
  n\ \text{奇}:\ \operatorname{neg} R_n^\bot=\tfrac{n-1}{2},\
  \operatorname{neg} R_{n+1}^\bot=\tfrac{n+1}{2}.
\end{equation*}
半问题算子的谱计数与其 Green 核在有限点集上的矩阵惯性是不同对象.
要在本卡点集上使用上述等号, 仍须核对点集条件及实现该负指数的论证;
仅引用 Gantmacher–Krein 名称或半问题谱交错不能在此替代这些义务.
原数值 (n=2: 各 1 负; n=3: $R_n^\bot$ 1 负, $R_{n+1}^\bot$ 2 负)
仅保留为历史 EVIDENCE, 不作为这些一般等式的认证.

### 奇扇区定性判据 (历史 Green 表达式保留)
在对称带自洽点, 历史括号恒等式与 $E_o$ 抵消给出以下奇扇区表达式;
本轮保留它的系数与归一化, 不以旧机器精度记录重新认证 Green 推导:
\begin{equation*}
  K_o=\operatorname{diag}(d)+\frac{4\lambda_n}{\lambda_{n+1}}
  \operatorname{diag}(u)\,M\,\operatorname{diag}(u),
\end{equation*}
\begin{equation*}
  M=\lambda_{n+1}\operatorname{diag}(\varepsilon)\,
  R_{n+1}^\bot\,\operatorname{diag}(\varepsilon)-\lambda_n R_n^\bot,\qquad
  d_j=\sigma\,\frac{2c|W(x_j)|}{R-1},
\end{equation*}
$\sigma=+1$ (SUP) / $-1$ (INF), $u_j=u_n(x_j)\ne0$, $\varepsilon_j=(-1)^{j+1}$.
在该表达式成立且 $u_j\ne0$ 的前提下, 可逆对角合同给出:
$K_o$ 的正定/负定等价于
$\operatorname{diag}(d/u^2)+\frac{4\lambda_n}{\lambda_{n+1}}M$ 的正定/负定.
这是奇扇区的定性判据, 不是 bare (G1') 的所谓 "奇扇区部分".
数值 (n=2,3, R=4, 两模式): $M$ 惯性混合 (n=2: 1+/1-; n=3: 1+/2-), 而 $K_o$
SUP 正定 / INF 负定; 这是历史观测. $\operatorname{diag}(d)$ 与 Green 组合 $M$
的惯性比较是更强定性路线的一项义务, 另一镜像扇区也需控制.
前节有限点核负指数等式不能在未核验时被当作已知输入.

在完整 $2n$ 接口坐标下, 取 $s_i=\rho(x_i+)-\rho(x_i-)$,
$F_i=f(x_i)/\lambda_{n+1}$, $J=D_xF$, $K=\operatorname{diag}(1/s)J$.
带自洽点满足
\begin{equation*}
 \det J=(-1)^n(R-1)^{2n}\det K,\qquad
 H_{\rm full}=-\lambda_{n+1}(R-1)^2K.
\end{equation*}
因此 (G1') 等价于在其所量化的解集上 $\det K>0$, 只保证非退化和行列式定号.
对称点另有 $\det K=\det K_e\det K_o$.
SUP 的 $K_e,K_o\succ0$ 或 INF 的 $K_e,K_o\prec0$ 是更强充分条件;
只核查 $K_o$ 的定性不足以推出完整 (G1').
一般矩阵 $\operatorname{diag}(1,1,-1,-1)$ 说明正行列式不能推出定性,
但不声称它能实现为实际 SL 矩阵.

若另知某起点 $R_*>1$ 的惯性, 待比较点经同一解分支的连续路径连接到该起点,
并且矩阵沿途连续实对称、全程非退化, 才可用惯性不变性继承起点定性.
单点 $\det K>0$ 不能替代沿途条件; 这些前提不自动建立全 R 分支或排除其它分支.
镜像参数需另用 $B_j=e_j-e_{2n+1-j}$ 作 $H_{\rm red}=B^TH_{\rm full}B$,
不能对 full-interface Hessian 统一乘 2. 上式 $d_j$ 已包含归一化除数,
不会因修正未归一化 $f'/s$ 而再乘 $\lambda_{n+1}$.

## 适用范围

- **适用**: 对称支上 $n\ge2$ 相邻谱隙问题的 Hessian 定性路线;
  将更强的 K 定性分解成两个 $n\times n$ 镜像扇区判据.
  使用历史 Green 闭式和有限点惯性计数前须核对各自前提及推导范围.
- **边界情形**: $x=1/2$ 处恰有一个相邻特征函数为零 (奇偶交错), $f(1/2)\ne0$;
  旧 INF 大 R 近简并和 detK 衰减描述在本卡仅属历史趋势,
  不证明全 R 分支或有限点惯性恒定; $R=1$ 为常数密度半问题,
  含 $1/(R-1)$ 的 K 表达式需取另行证明的缩放极限.
- **不适用 / 注意**: 奇偶性与括号恒等式**不**适用于非对称点 (本工具不声称
  全局奇偶性); 全局凹/凸性不成立 ($D_n$ 在随机 bang-bang 宽度处 Hess 惯性
  混合, EVIDENCE), 不能用整体凸性捷径替代 (G1'); 镜像分解要求回文高度且
  宽度对称, 非回文图案需另法.

## 验证与备注

- 来源: 自研 (R-205, 2026-08-13); 运行笔记
  runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/
  run_notes_addendum_2026-08-13b.md; 脚本
  scripts/_gapn2_parity_global_probe.py (奇偶性否证),
  scripts/_gapn2_green_inertia_probe.py (Green 惯性与 K_o 化归),
  scripts/_gapn2_bracket_identity_audit.py (括号恒等式 1e-15, docstring
  已限定为对称点).
- 诚实登记: (G1') 未由本卡关闭; 有限点 Green 惯性等式、历史全局 ε 输入
  和核组合推导未在本轮重审. 惯性比较是更强定性路线的一部分,
  不能以本卡的经典理论名称或数值记录宣称整个路线已获认证.
- 相关: [[band-selfconsistency-equivariance]] (镜像扇区与 (G1')/(G2) 框架),
  [[switch-saturation-k-invariant]] (ε 交错的胞腔来源),
  [[gap-band-extremals]] (带自洽判据), [[transfer-matrix-secular]] (数值
  射击), [[feynman-hellmann]] (一阶变分).
