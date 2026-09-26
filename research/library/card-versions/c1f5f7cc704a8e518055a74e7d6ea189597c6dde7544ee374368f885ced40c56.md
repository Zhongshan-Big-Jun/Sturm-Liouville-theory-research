---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c3da-1dd6-7e83-a355-61239cbfe206", "01a0dce3-b8a0-7d83-b359-03a8073d76d4"], "canonical_key": "half-problem-regularized-green (exact reduced resolvent without rho(y) factor + exact A1/A2 primitives + both mirror sectors of K)", "created": "2026-08-13", "dependencies": [{"location": "tools/feynman-hellmann.md", "sha256": "da33642d9b86de9587760ffc635f9b4e655fc86c6610b75c1732dc0920095611"}], "evidence_status": "ROUND12_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT", "resources": [{"kind": "program", "locator": "Scoped finite exact and numerical checks; not complete Green audit", "path": "research/artifacts/proof-audit-round7-20260921/checks/checks.py", "sha256": "7dd9ef3f7b3b3544d9f69a6a355a32278fa2132622437624e16253c9fe5b911a"}, {"kind": "source-audit", "locator": "Confirmed direct propagation and untouched historical scope", "path": "research/artifacts/proof-audit-round7-20260921/checks/propagation.md", "sha256": "f9eae002f40576f74fd7d9a89f5de9c516f95b56c274f56f2c00087a33246a46"}], "scope": "Current round12 statements and retained earlier scoped repairs. n2 normalized Green and general finite matrix/phase identities; no all-R signs, historical full scans or complete formalization.", "source": "自研 (R-207/R-208 历史记录; 第七轮修订入口 docs/SL_gap_nge2_symmetry_local_proof.tex 与 reports/proof-audit-round7-20260921/REPORT.md)", "sources": [{"locator": "Round7 local proof and explicitly scoped tail corrections", "path": "docs/SL_gap_nge2_symmetry_local_proof.tex", "sha256": "c71a98c666492b9b947378432533fa60ea44dfee3029e0d21711cdc6cafa61b1"}, {"locator": "Historical reconnaissance with round10 numerical-evidence and reflection-sector corrections", "path": "docs/SL_gap_nge2_symmetry_recon.tex", "sha256": "986262ff5379e2855f6e6cb9c907d6955da1a625ee31d5907f72314fd8e984bc"}, {"locator": "S1-S4,R1-R2; independent analytic identities retain their prior scope", "path": "research/artifacts/proof-audit-round10-20260925/analytic-repair.md", "sha256": "1215c0f2291829a5fd40dd212f313e5ba07841bec9d70477d1dca4580bb0a066"}, {"locator": "J1-J5, finite-dimensional structure and finite-difference geometry with explicit limits", "path": "research/artifacts/proof-audit-round11-20260926/jacobian-repair.md", "sha256": "aabc1aa00e43ec64a1ef48e5f68dd39b349d57b6dfa3efd1da0cb1dd5e157824"}, {"locator": "Sections 1-6: exact parity compression, indexed DD/DN phases, normalized n2 Green identities and explicit scope", "path": "research/artifacts/proof-audit-round12-20260926/analytic-repair.md", "sha256": "e133d8cc04484f44879af165f5022d2ce0ffc19af2e268c0748c5be973b6e571"}], "status": "第十二轮半谱身份与扇区对象修订; 可复用性以精确版本独立纠错回执为准", "summary": "半问题Green历史闭式及n=2镜像扇区研究入口. bare G1的行列式条件不等价于两扇区定性; 更强定性需另证. 半隙Hessian是B转置*H_full*B, 不是对完整Hessian一律加倍. 当前修订明确归一化、量词和历史边界; 未认证全R延拓或全部Green/M3/KP推导. 第十轮: 旧扫描不能认证谱序号, 旧asym非扇区投影; 新相位索引与可行扇区种子另审, 不据历史数值扩张解析结论. 第十一轮: 残差J取交叉块, 与Hessian块对角结构区分; 接口中心差分核对实际两侧位移, 失败明确拒绝, 不作全参数认证. 第十二轮: DD/DN相位按序号定位, 去极点绑定同一谱表; 交叉Green式为Kp奇块=E Ke E, 原Ko需自身约化核及秩一项. sector_data和负秩一判据原扇区标签已修正, 数值守卫不等于区间认证.", "tags": ["mathtool", "self-developed", "green-function", "reduced-resolvent", "sector-decomposition", "gap-extremals", "nge2"], "title": "半问题约化 Green 闭式: 无 rho(y) 因子的约化预解核与 K 的两个镜扇区闭式", "tool_id": "half-problem-regularized-green", "updated": "2026-09-26"}
---
## 第十二轮: 半谱身份、去极点与扇区对象

半区间的旧独立 mu 网格会漏掉成对低模态, 且请求 N 与 2N 时前缀会变.
旧求和只删除数组下标, 因而可能保留真正极点. 两个错误已用原完整源码复现.
当前 DD/DN 共用提升相位引擎, 第 j 阶目标分别为 j*pi、(j-1/2)*pi.
正坐标缩放保持这两类轴向目标. 共享谱表绑定几何、边界类型和一基模态序号;
去极点核对目标值, 截断覆盖和其余分母, 失配或不可分辨时拒绝计算.
这些是浮点诊断守卫, 不是区间证书; Richardson 也不认证尾项误差.

在 2n 维镜像基 Be/Bo 中, S=diag(1,-1,...,-1), E=S 的左半对角块.
对任意 K 均有 Bo^T SKS Bo=E Ke E、Be^T SKS Be=E Ko E.
压缩恒等式不需要 K 与反转 P 对易; 作为不变子空间分块则需要该条件.
因此交叉奇偶 Green 式代表 Kp=SKS 的奇块, 对应原 K 的偶块 Ke.
原 Ko 必须使用自身极点处的约化核及存留的秩一项.

直接传播还涉及 sector_data: 旧输出把 Kp 两块标为 raw Ke/Ko.
当前返回 Ke/Ko 及 He/Ho/Ee/Eo 均按原 K 命名, 另有显式 Kp* 字段;
历史 c_e/c_o 系数属于 KpEe/KpEo. 旧扫描文件不改写, 其单个扇区标签和
支配解释不能直接复用. 本轮 n=2 Green 恒等式有独立推导, n=2/3 R=4
程序对照是有限数值证据, 不关闭全参数符号、G1'、唯一性或历史全部路线.

精确条件与推导见[第十二轮解析修订](../research/artifacts/proof-audit-round12-20260926/analytic-repair.md),
执行与隔离检验范围见[本轮报告](../reports/proof-audit-round12-20260926/REPORT.md).
可复用性以本卡当前字节的原版纠错回执和实际查询为准.

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


# 半问题约化 Green 闭式

## 第七轮修订范围

本卡是直接传播修订候选, 不是验收回执. 当前证明入口为
[局部对称性证明](../docs/SL_gap_nge2_symmetry_local_proof.tex),
实际修订及审查状态见 [第七轮 REPORT](../reports/proof-audit-round7-20260921/REPORT.md).
最终版本及 exact hashes 由协调器绑定, 链接不表示已验收.
本轮只修 (G1')/定性逻辑和 full-interface 与镜像独立坐标的关系.
约化 Green、A1/A2、半问题展开、R-208 历史补证与 M3/KP 没有在此全盘重审;
旧数值和标题中的 STRICT 是原记录, 不构成本轮认证.
下文显式出现 $\mu_1^D,\mu_2^N$、两个左半开关的公式按 $n=2$ 阅读,
不由旧 "n 偶" 标题将这些固定索引推广到所有偶数 $n$.

## 解析

### 无 rho(y) 因子的约化预解核 (STRICT)

设定: 半问题 $-u''=\mu\rho u$ 于 $(0,L)$, $u(0)=0$, 右端 $u(L)=0$ (D) 或
$u'(L)=0$ (N), $\rho$ 分段常数. $u$ 为特征值 $\mu_k$ 处按 $\int\rho u^2=1$
归一化的特征函数, $v$ 为第二解, $W(u,v)=uv'-u'v=1$, 规范
$v(0)=-1/u'(0)$. 约化预解核
$Gt_k(x,y)=\sum_{l\ne k}v_l(x)v_l(y)/(\mu_l-\mu_k)$ 的闭式:

\begin{equation*}
  Gt_k(x,y)=B(x,y)-u(x)P(y),
\end{equation*}

\begin{equation*}
  B(x,y)=\bigl(u(x)v(y)-v(x)u(y)\bigr)\mathbf 1_{x>y}
  -u(x)u(y)\,I_1(x)+v(x)u(y)\,I_2(x),
\end{equation*}

\begin{equation*}
  I_1(x)=\int_0^x\rho uv\,dt,\qquad I_2(x)=\int_0^x\rho u^2\,dt,
\end{equation*}

\begin{equation*}
  P(y)=\langle\rho u,B(\cdot,y)\rangle
  =v(y)\bigl(1-I_2(y)\bigr)-u(y)\bigl[A_1-A_2+I_1(L)-I_1(y)\bigr],
\end{equation*}

\begin{equation*}
  A_1=\int_0^L\rho u^2I_1\,dx,\qquad A_2=\int_0^L\rho uv\,I_2\,dx.
\end{equation*}

证明要点 (参数变分法): 对 $L_x=-d^2/dx^2-\mu\rho(x)$ 配源
$h(x)=\delta(x-y)-\rho(x)u(x)u(y)$ 得 $L_xB=h$ ($B_x$ 在 $x=y$ 的跳量为
$u'v-v'u=-W=-1$, 故 $-B_{xx}$ 携带 $+\delta$; 光滑部分由 $u''=-\mu\rho u$,
$I_1'=\rho uv$, $I_2'=\rho u^2$ 直接求导验证). 边界条件成立
($B(0,y)=0$, D: $B(L,y)=0$, N: $B_x(L,y)=0$, 用 $I_2(L)=1$ 与 $u$ 的边界条件),
且 $\langle\rho u,Gt_k(\cdot,y)\rangle=P(y)-P(y)=0$. 三条性质唯一刻画约化预解.

精确 $A_1,A_2$: 每块上 $C^2/S^2/CS$ 乘 $iCC/iCS/iSS$ 的九个闭原函数
(初等三角反导数, scripts/_gapn2_half_problem_probe.py 的
`_prims_9`/`_fold3`/`_a1a2_exact`).

### 已登记的关键更正 (勿重犯)

- 旧稿在 $B$ 与 $P$ 中多乘了 $\rho(y)$: 该稿只解到 delta 的 $\rho(y)$ 因子
  (跳量错误), 且在密度跳点对 $y$ 不连续; 常数密度自检无法发现
  ($\rho(y)=1$ 时一致).
- 对 $A_1/A_2$ 求积精度的旧诊断撤回: 精确值与 20 万点梯形求积仅差约 2e-8,
  真正 bug 是 $\rho(y)$ 因子.

### eps 共轭扇区恒等式与约定 (STRICT)

采用一基指标 $1\le j\le n$, 镜像配对 $j\leftrightarrow2n+1-j$,
$B_e^{(j)}=(e_j+e_{2n+1-j})/\sqrt2$, $B_o^{(j)}=(e_j-e_{2n+1-j})/\sqrt2$.
记 $S=\operatorname{diag}((-1)^{j+1})_{j=1}^{2n}$, $E=S[:n,:n]$.
则 $SB_o=B_eE$, $SB_e=B_oE$, 对任意 K 有
\[
 B_o^TSKSB_o=E(B_e^TKB_e)E,\qquad B_e^TSKSB_e=E(B_o^TKB_o)E.
\]
当前 `sector_data['Ko']` 已修为原 $B_o^TKB_o$; 第十二轮前同名返回值实际上是
Kp 的奇块. 旧文档的接口描述与旧代码不符, 此处明确撤回该实现描述.
下文 $\operatorname{diag}(\beta)$ 统一取 E, 不混用零基和一基符号.

### n=2 原 K 的两个镜像扇区 (第十二轮重推, 条件见新解析稿)

$n=2$, $\lambda_2=\mu_1^D$ 为奇全模, $\lambda_3=\mu_2^N$ 为偶全模,
$c^2=\lambda_n/\lambda_{n+1}$, $e=\varepsilon[:n]$, $u=(u_n(x_j))_{j<n}$
取左半开关, $d=\sigma\,2c|W(x_j)|/(R-1)$. 由 R-206 塌缩恒等式
$Kp=\operatorname{diag}(d)+r\,vv^T+2\lambda_n\operatorname{diag}(u_n)
S\operatorname{diag}(u_n)$ ($v_j=u_n(x_j)^2$,
$r=2\lambda_nD/\lambda_{n+1}^2$,
$S=\varepsilon Gt_{n+1}\varepsilon-c^2Gt_n$) 与镜限制恒等式
$Be^T\varepsilon Gt_{n+1}\varepsilon Be=G_D(\mu_2^N)\circ ee^T$,
$Be^TGt_nBe=G_N(\mu_1^D)$, $Bo^Tv=0$,
$Bo^T(\varepsilon v)=\sqrt2(\varepsilon v)[:n]$ 得:

\begin{equation*}
  Kp_{\mathrm{odd}}:=\operatorname{diag}(\beta)Ke\operatorname{diag}(\beta)
  =\operatorname{diag}(d[:n])+2\lambda_n\operatorname{diag}(u)
  \bigl[G_D\circ ee^T-c^2G_N\bigr]\operatorname{diag}(u),
\end{equation*}

\begin{equation*}
  Ko:=Bo^TKBo=\operatorname{diag}(d[:n])+2r(\varepsilon v)(\varepsilon v)^T
  +2\lambda_n\operatorname{diag}(u)\bigl[Gt_N-c^2(Gt_D\circ ee^T)\bigr]
  \operatorname{diag}(u),
\end{equation*}

其中 $G_D=G_D(\mu_2^N)$, $G_N=G_N(\mu_1^D)$ 为交叉特征值处的全 Green,
$Gt_D,Gt_N$ 为自身极点处的约化 Green, 四个核均用第 1 节闭式在两个左半
开关处取值; $\det K=\det(Kp_{\mathrm{odd}})\det(Ko)$.

### 谱分裂与 PD 尾核 (STRICT, n=2)

由经典交错 $\mu_1^N<\mu_1^D<\mu_2^N<\mu_2^D$ (Gantmacher-Krein) 与半归一
特征函数 $v_m$ (D), $w_m$ (N):

\begin{equation*}
  G_D(\mu_2^N)|_2=-\alpha v_1v_1^T+Ph,\qquad \alpha=1/(\mu_2^N-\mu_1^D)>0,
\end{equation*}
\begin{equation*}
  G_N(\mu_1^D)|_2=-\beta w_1w_1^T+Qh,\qquad \beta=1/(\mu_1^D-\mu_1^N)>0,
\end{equation*}
\begin{equation*}
  Gt_D=\sum_{m\ge2}\frac{v_mv_m^T}{\mu_m^D-\mu_1^D}\ (PD),\qquad
  T_D=\sum_{m\ge2}\frac{v_mv_m^T}{(\mu_m^D-\mu_1^D)(\mu_m^D-\mu_2^N)}\ (PD),
\end{equation*}
\begin{equation*}
  Gt_N=-\alpha_N w_1w_1^T+Rh,\qquad \alpha_N=1/(\mu_2^N-\mu_1^N)>0,\qquad
  Rh=\sum_{m\ge3}\frac{w_mw_m^T}{\mu_m^N-\mu_2^N}\ (PD).
\end{equation*}

权重严格正 (交错性), 尾和的两点取值 PD (一维特征空间补在两点上取满
$\mathbb R^2$). 由带恒等式 $w_2(x_j)=\varepsilon_jc\,v_1(x_j)$:

\begin{equation*}
  Kp_{\mathrm{odd}}=B_1+2\lambda_2D\operatorname{diag}(u)\bigl[E\,T_DE\bigr]
  \operatorname{diag}(u),
\end{equation*}
\begin{equation*}
  B_1=\operatorname{diag}(d)+2\lambda_2\operatorname{diag}(u)
  \bigl[E\,Gt_DE-\alpha(Ev_1)(Ev_1)^T+c^2\beta w_1w_1^T-c^2Qh\bigr]
  \operatorname{diag}(u),
\end{equation*}
\begin{equation*}
  Ko=\operatorname{diag}(d)+2\lambda_2\operatorname{diag}(u)
  \bigl[Rh-c^2E\,Gt_DE\bigr]\operatorname{diag}(u)
  +2r(\varepsilon v)(\varepsilon v)^T
  -2\lambda_2\alpha_N\operatorname{diag}(u)w_1w_1^T\operatorname{diag}(u).
\end{equation*}

### 行列式条件与更强的扇区定性

(G1') 要求在指定解集上 $\det J\ne0$ 且 $\operatorname{sgn}\det J=(-1)^n$.
在 $R>1$ 时, 由 $\det J=(-1)^n(R-1)^{2n}\det K$, 它等价于每点 $\det K>0$.
在 $n=2$ 对称点, 上述块分解进一步给出
$\det(Kp_{\mathrm{odd}})\det(Ko)>0$; 这是行列式的非退化与定号条件.

另定义更强的定性判据: (I1) $Kp_{\mathrm{odd}}$ 负定 (INF) / 正定 (SUP),
(I2) $Ko$ 同号定性. 因 $Kp_{\mathrm{odd}}$ 与 $Ke$ 合同, (I1)+(I2)
等价于全矩阵 K 的相应定性, 从而蕴含 (G1'), 反向不无条件成立.
一般矩阵 $\operatorname{diag}(1,1,-1,-1)$ 有正行列式而不定;
这个例子只否定一般矩阵推理, 不声称是实际 SL 配置的实现.

沿支继承定性必须另给: 已知起点惯性, 从起点到目标点的连续解分支,
以及沿途矩阵连续实对称且全程非退化. 例如可取已核验的 $R_*>1$ 锚点;
若使用 $R\to1+$ 的缩放极限, 须先证明该极限及邻近分支.
在这些前提下惯性恒定; 仅知道终点 $\det K>0$ 不够, 也不能默认分支存在于全部 $R>1$.
只在对称分支核查上述条件, 还不能覆盖可能存在的非对称解.

历史计划包括 Cauchy/Binet 行列式展开、近 $R=1$ 锚点、沿支单调性和大 R 渐近.
以下保留其记录和公式, 不把计划或旧数值提升为全 R 证明.

### R→1+ 锚点记录 (R-208 原标记 STRICT, 本轮未重审该段证明)

局部结论的当前修订依据应绑定顶部第七轮证明入口, 特别是端点一致估计与整个 U 的唯一性.
这里保留 R-208 的论证与缩放式供溯源, 不以旧段落替代当前证明或独立审查.

引理 A (一切 n>=1): 常数弦处 $W_0=(u_{n+1}^0)'u_n^0-u_{n+1}^0(u_n^0)'$ 在
$f_0$ 的每个零点处非零. 证明: 设 $t=\pi x$, $p=\cos^2((n+1)t)$,
$q=\cos^2(nt)$, $c_0=n/(n+1)$; $f_0=0$ 给 $1-p=c_0^2(1-q)$; 若同时
$W_0=0$, 平方后代入得 $p=n^4q/(n+1)^4$, 联立得 $q=-(n+1)^2/n^2<0$, 矛盾
($\sin(nt)=0$ 情形由 $\gcd(n,n+1)=1$ 排除). 故 $f_0$ 在 $(0,1)$ 恰有 $2n$ 个
单零点且 $f_0'(x_j)=-2\lambda_{n+1}^0\varepsilon_jc_0W_0(x_j)\ne0$.

定理 B (锚点): 近 $R=1$ 的解集是唯一的光滑对称分支 (解的各坐标必是同一标量
函数 $f(\cdot;R)$ 的 $2n$ 个单零点; 对称子流形上 IFT 给存在性). 沿该分支

\begin{equation*}
  (R-1)K(R)\to\frac{\sigma}{\lambda_{n+1}^0}\operatorname{diag}(|f_0'(x_j)|)
\qquad(R\to1+),
\end{equation*}

严格定号 ($\sigma=+1$ SUP, $-1$ INF; 对角项 $2c|W(x_j)|/(R-1)$ 主导, 非对角
部分 $O(1)$: $r vv^T$ 与 $2\lambda_n\operatorname{diag}(u)S\operatorname{diag}(u)$ 在常数弦处有限).
于是 (G1') 对一切 n 在 $(1,1+\delta)$ 成立 (再现 $\operatorname{sgn}\det J(1,x*)=(-1)^n$),
且 n=2 时 (I1)/(I2) 在 $(1,1+\delta)$ 成立: $(R-1)Kp_{\mathrm{odd}}$ 与
$(R-1)Ko$ 均收敛到 $\operatorname{diag}(\sigma 2c_0|W_0(x_j)|)_{j<n}$.

### 半隙 Hessian 与完整接口 Hessian 的坐标关系 (第七轮更正)

固定 $n=2$, 全接口为 $x=(x_1,x_2,x_3,x_4)$, 对称参数为 $a=(a_1,a_2)$,
$x(a)=(a_1,a_2,1-a_2,1-a_1)$, $B=(e_1-e_4,e_2-e_3)=\sqrt2 Bo$.
这里 $Bo$ 是正交归一的镜像奇扇区基. 采用全区间归一化 $\int_0^1\rho u_k^2=1$,
$f=\lambda_2u_2^2-\lambda_3u_3^2$, $s_i=\rho(x_i+)-\rho(x_i-)$,
$F_i=f(x_i)/\lambda_3$, $J=D_xF$, $K=\operatorname{diag}(1/s)J$.
半隙函数 $g(a)=D_2(x(a))=\mu_2^N-\mu_1^D$ 满足
$\partial_{a_j}g=-2s_jf(a_j)$. 在带自洽点,

\begin{equation*}
 H_{\rm full}=-\lambda_3\operatorname{diag}(s)J=-\lambda_3(R-1)^2K,
 \qquad \nabla_a^2g=B^TH_{\rm full}B=-2\lambda_3(R-1)^2Ko.
\end{equation*}

full-interface 的 $H_{\rm full}$ 是 $4\times4$, $\nabla_a^2g$ 和 $Ko$ 是 $2\times2$.
因此不能将完整 Hessian 统一乘 2 或把 $K$ 与 $Ko$ 混写.
(I2) 等价于半隙 Hessian 的相应定性, 并充分保证半隙严格局部极值.
(I1) 另控制被对称约束省去的扇区, 两条件合起来充分保证全接口的严格局部极值.
半隙严格极值不反推 (I1), 无非退化前提的严格极值也不能反推 Hessian 定性.
历史 R=4 网格记录临界点外 Hessian 不定 (违例 11/15 与 12/15), 本轮未重跑;
本卡不声称全局凸/凹或全 R 临界点定性已证.

### 历史后续路线与未核验边界

当前局部证明的适用邻域之外, (G1') 仍未由本卡关闭. 历史 $n=2$ 定性路线为:
(M1) 在实际存在且可微的对称分支上证明
$\frac{d}{dR}\det Kp_{\mathrm{odd}}<0$ 与 $\frac{d}{dR}\det Ko<0$;
(M2) 证明迹符号 ($\operatorname{tr}<0$ INF, $>0$ SUP);
(M3) 建立所需的大 R 渐近与分支匹配. 对实对称 $2\times2$ 块,
正行列式加相应迹符号确实等价于正定/负定; 仅有两块行列式的正乘积不够.
若已另证分支延至任意大 R、每块行列式严格递减且趋于 0, 才可由该路线推出其正性.
本轮不验证这些全 R 前提, 不将 M1-M3 视作 bare (G1') 的等价分解,
也不重新评定其它 M3/KP 证明或有限 chart 的历史结论.
EVIDENCE: $\det$ 在 $[1.05,100]$ 严格递减 (双模式), 迹符号正确但非单调;
链式法则
$\frac{d}{dR}M=\partial M/\partial R|_x+\sum_j(\partial M/\partial x_j)(dx_j/dR)$,
$dx/dR=-J^{-1}\partial F/\partial R$ 在 R=1.5,2,4,10 验证到 4-5 位.

## 适用范围

- **适用**: 按历史来源核验后的分段常数半问题 (D/N 边界) 约化预解核公式;
  对称带自洽点处的镜扇区定性研究. 本卡显式半问题展开按 n=2 的索引使用;
  一般偶数 n 的完整表达式未在本轮核验.
- **边界情形**: 密度跳点处核连续 (6e-10), 对称性 1e-17; $R\to1+$ 时
  $d_j=O(1/(R-1))$ 对角占优; $R\to\infty$ 时 INF 余量退化
  ($\det K\to0+$), 闭式仍需键合-反键合渐近.
- **不适用 / 注意**: n 奇需另列半问题配对 ($\lambda_n=\mu_{(n+1)/2}^N$,
  $\lambda_{n+1}=\mu_{(n+1)/2}^D$); 非对称点镜恒等式不成立 (奇偶性需要
  $\rho(1-x)=\rho(x)$, 即宽度对称); 数值符号检验仅是 EVIDENCE, 不构成
  (I1)/(I2) 的证明; 本工具不提供全局极值性论证.
  近 R=1 的局部结果应读当前证明及其真实依赖; M1-M3 是历史定性证明路线,
  不是已知的全 R 延拓或等价闭合结论.

## 验证与备注

以下实验数值及 R-208 状态是历史记录, 本轮未重跑, 不替代新的独立审查.

- 来源: 自研 (R-207 第 2 段, 2026-08-13); 运行笔记
  runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/
  run_notes_addendum_2026-08-13d.md; 主脚本
  scripts/_gapn2_half_problem_probe.py (C0-C3, 修正后的
  `green_regularized` + 精确 `_a1a2_exact`), 调试链
  scripts/_gapn2_half_debug2/3/4.py, 分解脚本
  scripts/_gapn2_odd2x2_decompose.py, 原 K 奇扇区闭式脚本
  scripts/_gapn2_rawko_closed.py, R 扫描
  scripts/_gapn2_odd2x2_scan.py.
- 数值验证 (EVIDENCE): C2 闭式 vs Richardson 外推谱和 - INF R=4
  Gt_D 7.7e-6, Gt_N 5.8e-6, 全 GD 7.7e-6, GN 5.8e-6; SUP 2.3e-6/1.3e-6
  (残差为谱尾 $O(1/N^2)$, 闭式精确); 对称性 1.4e-17, 跳点连续性 6e-10,
  T_D 闭式 vs 谱 1.8e-11; C3 R-205 与塌缩装配一致 1.8e-15, Ko 闭式 vs FD
  4.6e-10 (INF) / 3.7e-10 (SUP), Kp_odd vs
  $\operatorname{diag}(1,-1)Ke_{fd}\operatorname{diag}(1,-1)$
  2.3e-9 / 8.6e-10; R 扫描 n=2: Kp_odd 与 Ko 在 R∈[1.05,100] (INF) /
  [1.05,10] (SUP) 全部定号, det J > 0.
- 诚实登记: 第 1-4 节原标记 STRICT, 本轮保留而未重审; 一切历史数值仅为 EVIDENCE.
  本轮没有完成 (I1)/(I2) 的全 R 证明或最终验收; (G1') 不能由本卡宣布闭合.
- R-208 验证 (EVIDENCE): n=2 R=1.00001 续延 (R-1)Kp_odd/Ko 与解析极限
  对角差 1.2e-4 (线性于 R-1), 开关收敛到 f0 零点 (3e-7), D->5pi^2;
  n=3 对角极限检查 3.8e-4/3.1e-3; det 单调递减双模式 [1.05,100];
  链式法则 4-5 位 (R=1.5..10); 全局凸性否证 (11/15, 12/15 违例).
  新脚本 scripts/_gapn2_r1_anchor_probe.py, _gapn2_r1_monotonicity_probe.py,
  _gapn2_gap_convexity_probe.py, _gapn2_r1_det_derivative_probe.py.
- 历史状态 (R-208): 原文将近 R=1 的 (G1') 与 n=2 的 (I1)/(I2) 标为 STRICT.
  本轮以当前局部证明为新入口, 不沿用 "全 R 只剩 M1-M3" 作为已核验结论.
- 相关: [[green-half-inertia]] (半问题 Green 惯性与 (G1') 化归),
  [[second-variation-weighted-eigenvalues]] (K 的全局恒等式),
  [[gap-band-extremals]] (带自洽极值判据), [[switch-saturation-k-invariant]]
  (块能量不变量与 eps 交错), [[feynman-hellmann]] (一阶导数).
