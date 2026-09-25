---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c3c5-7f80-7623-862f-75dd78248a63", "01a0c3c5-83cf-7b72-a95f-694975ba511f"], "conditions": ["Dirichlet weighted string on (0,1), 1<=rho<=R, fixed n>=1", "Weighted normalization integral rho*u_k^2=1", "The doubled formula requires symmetric density and paired opposite interface velocities"], "created": "2026-08-05", "dependencies": [{"location": "tools/feynman-hellmann.md", "sha256": "da33642d9b86de9587760ffc635f9b4e655fc86c6610b75c1732dc0920095611"}], "evidence_status": "ROUND7_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT", "resources": [{"kind": "program", "locator": "Independent round7 finite checks", "path": "research/artifacts/proof-audit-round7-20260921/checks/checks.py", "sha256": "7dd9ef3f7b3b3544d9f69a6a355a32278fa2132622437624e16253c9fe5b911a"}, {"kind": "numerical-evidence", "locator": "Nonstationary mirror derivative and other scoped checks", "path": "research/artifacts/proof-audit-round7-20260921/checks/outputs.json", "sha256": "9b54ef988988f2117bda2d2e1cfcea66702bc45fa916e7375cbd7dbc3761f3a8"}], "scope": "Single and symmetric-pair shape derivatives; small-contrast local theorem; general-n supremum large-R limit. No all-R branch uniqueness or INF classification.", "source": "自研 (会话 13)", "sources": [{"locator": "Round7 Wronskian/endpoint/local symmetry and general supremum limit", "path": "docs/SL_gap_nge2_symmetry_local_proof.tex", "sha256": "c71a98c666492b9b947378432533fa60ea44dfee3029e0d21711cdc6cafa61b1"}, {"locator": "Historical n=1 large-R numerical evidence; not rerun as a full table", "path": "docs/SL_gap_extremals.tex", "sha256": "8e7a85ddb99cdc7cc395e0e855eebff9b8edec59e7e61c089cbabb7b97f5f070"}], "status": "第七轮修订; 可复用性由当前精确版本纠错回执控制", "summary": "Dirichlet变权弦采用积分rho*u_k²=1. 单接口谱隙导数为(rho_left-rho_right)f; 左右镜像反向移动时为2(rho_left-rho_right)f. 驻点方程不变. 弱反差局部唯一性以统一Volterra和根隔离修复; 固定n的盒类SUP极限为(n+1)²pi². 不提供有限R全局唯一性或INF分类.", "tags": ["mathtool", "self-developed"], "title": "带状自洽与谱隙的接口导数", "tool_id": "gap-band-extremals"}
---
# 带状自洽与谱隙的接口导数

考虑 Dirichlet 加权弦 -u''=lambda rho u, 无总质量约束的盒类 1<=rho<=R, R>1, 固定整数n>=1. 特征函数采用 integral rho*u_k²=1, f=lambda_n*u_n²-lambda_(n+1)*u_(n+1)², D_n=lambda_(n+1)-lambda_n.

## 密度方向与开关方向

对可微密度方向, delta D_n=integral delta_rho*f. 盒类极大子的必要饱和律是 rho=R 于f>0, rho=1 于f<0; 极小子反之. 这是极值必要条件, 单靠符号或数值残差不能证明全局极值性.

在固定交替图案的开关坐标x_1<...<x_m中, 设第j个接口左/右密度为rho_L,rho_R, 则

\[
\partial_{x_j}\lambda_k=-\lambda_k(\rho_L-\rho_R)u_k(x_j)^2,
\qquad \partial_{x_j}D_n=(\rho_L-\rho_R)f(x_j).
\]

形状导数的直接证明: 在各块上微分方程, 用Green恒等式配对未微分解, 将各块端点相加. u,u'在接口连续; 移动匹配条件给出 dot u 的连续性和 [dot u']=-[u''] dot x=lambda[rho]u dot x. 因而内部边界项为 -lambda*(rho_L-rho_R)*u(x_j)² dot x. 两个外端点固定, 分母为integral rho*u²=1. 这也可由解析转移矩阵的简单特征根微分得到; 不要求密度在L-infinity意义对接口可微.

因此在固定图案的内部参数空间, 驻点恰满足每个有效开关处f(x_j)=0. 带自洽还要求整块符号与图案相符, 不能从驻点方程单独推出.

## 镜像成对移动

假定rho关于1/2反射对称. 简单特征函数具有确定奇偶性, 故u_k(1-x)²=u_k(x)², f(1-x)=f(x). 同一个独立参数epsilon令左接口a变为a+epsilon, 右接口1-a变为1-a-epsilon. 镜像处密度跳跃和速度均反号, 两项相加:

\[
\frac{d\lambda_k}{d\epsilon}=-2\lambda_k(\rho_L-\rho_R)u_k(a)^2,
\qquad \frac{dD_n}{d\epsilon}=2(\rho_L-\rho_R)f(a).
\]

旧卡在第二式漏写2. 驻点条件f(a)=0保持不变, 因此只验证零点残差不能识别该错误. 梯度、步长或Hessian复用时须说明坐标: 完整接口坐标的单侧公式没有2; 对称独立坐标的两侧贡献须相加. 对线性嵌入x=Tt+b, 梯度为T^T grad_x D, Hessian为T^T Hess_x(D)T, 不可对任意坐标统一补乘2.

非驻点回归取n=1,R=4,rho=[1,4,1], a=1/4. 高精度射击、精确分块权归一化和中心差分应给 dD/da=53.88097216024057..., 旧式仅给一半. 新检查的实际结果见本轮绑定的可执行证据.

## 局部对称性与大反差极限

[当前局部证明](../docs/SL_gap_nge2_symmetry_local_proof.tex)的第七轮修订给出正确常密度Wronskian与端点系数, 以全区间Volterra估计替代错误的全局C3/首块宽度论证. 对每个固定n>=2及SUP/INF图案, R>1充分接近1时, 升序开关区域中的驻点唯一、反射对称且带自洽. 这不证明全部R的G1'/G2或全局唯一性.

令S_n(R)=sup_{1<=rho<=R}(lambda_(n+1)-lambda_n). 对每个固定n>=1, 一般上确界极限是(n+1)²pi², 4pi²是n=1特例. 证明以n个等距薄重块和min-max为依据, 同时适用于可测盒类及不限制有限块数的分块常值类; 不把这个上确界定理直接等同于某条未经全R存在/最优性证明的自洽分支. 沿可微且带自洽的SUP分支, 接口项为0, dD/dR=integral_{rho=R} f>0. 不据此预设分支全R存在、无折点或唯一. INF极限和M3/KP其它范围分别查看原来源.

## 历史证据与限制

早期R=4,n=1..12及额外块数的数值搜索、Hessian检查保存在 [数值报告](../docs/SL_gap_extremals.tex)和scripts/op03_gap_fixed.py等处. 这些历史数值不因本轮勘误自动重验或升级为全局证明. 旧R扫描中的SUP 4pi²及INF D*R=24.943866...均指n=1. 近简并问题或非常大R需另评估数值病态.

本卡不适用于未经调整的固定总质量或原子测度类. 原传播顺序错误(P*M而非M*P)、伪临界点和失败迭代仍作为历史经验保留. 本轮只纠正明确公式、归一化及其分析范围; 完整Volterra与谱极限尚未全部Lean形式化.
