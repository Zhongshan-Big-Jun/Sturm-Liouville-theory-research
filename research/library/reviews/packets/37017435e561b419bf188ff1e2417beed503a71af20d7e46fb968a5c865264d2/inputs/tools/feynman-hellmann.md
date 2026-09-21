---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359"], "conditions": ["Differentiable simple eigenpair of symmetric forms on a common domain", "Use the denominator of the actual generalized eigenproblem"], "created": "2026-08-04", "evidence_status": "ROUND7_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT", "scope": "First derivative under explicit differentiability hypotheses; fixed L2 and variable-weight string normalization distinguished.", "source": "量子力学标准公式", "sources": [{"locator": "R7-P01 constant potential counterexample and generalized-eigenpair derivation", "path": "research/artifacts/proof-audit-round7-20260921/internal-normalization-finding.md", "sha256": "86459c7525f7384b7c08d1dc012baeabab9961734d441e9ba653e6e4efdc0bf8"}], "status": "第七轮修订; 可复用性由当前精确版本纠错回执控制", "summary": "广义特征对的一阶变分须使用真实分母: lambda_prime <u,Bu>=<u,A_prime u>-lambda<u,B_prime u>. 固定普通L2的势扰动与L2(rho)归一化的变权弦不能混用. 仅在可微简单特征对及共同形式域前提下使用; 二阶与谱可微性另证.", "tags": ["mathtool", "spectral"], "title": "Feynman-Hellmann公式: 固定空间与变权重", "tool_id": "feynman-hellmann"}
---
# Feynman-Hellmann 公式: 固定空间与变权重

## 共同形式及证明

设实 Hilbert 空间中的对称形式 A(t), B(t) 在共同形式域上可微, B(t) 正定. 假定有可微的简单特征分支 u(t), lambda(t), 满足 A(t)u=lambda(t)B(t)u; 下列配对及微分有意义. 则

\[
\lambda'\langle u,Bu\rangle
=\langle u,A'u\rangle-\lambda\langle u,B'u\rangle.
\]

证明: 微分特征方程并与 u 配对. 由对称性和 Au=lambda Bu, 含 u' 的两项相消, 剩下上述等式. 这一步假定分支可微, 不自行证明任意无界算子族的扰动正则性.

- 普通固定 Hilbert 空间的特征问题 Hu=lambda u: B=I. 采用该空间的范数 ||u||=1 后, lambda'=<u,H'u>. 未归一化时须除以 ||u||².
- 固定 L²(0,1) 中的 Dirichlet Schrödinger 算子 H(t)=-d²/dx²+t V(x), V 为有界实势: lambda'=integral V*u² / integral u². 归一化应是 integral u²=1.
- 加权 Dirichlet 弦 -u''=lambda rho(t,x)u, 权有严格正下界: A 的形式为 integral u'v', B 的形式为 integral rho*u*v. 在可微密度方向下, lambda'=-lambda*integral rho_dot*u² / integral rho*u². 采用 integral rho*u²=1 后分母才为1. 相邻谱隙的变分为 integral rho_dot*f, f=lambda_n*u_n²-lambda_(n+1)*u_(n+1)².

## 直接反例与适用边界

旧版混用两种归一化. 对 V=2, H(t)=-d²+2t, u=sin(pi*x) 满足 integral 2u²=1, 但 lambda_1(t)=pi²+2t, 导数为2. 旧版直接使用 integral 2u² 会误给1; 正确分母 integral u²=1/2 恢复2.

移动密度跳点并不是 L-infinity 中的可微方向, 不能直接把 delta 分布塞入上述有界方向公式作为证明. 有限分块权可由匹配解/弱形式的形状导数得到单接口公式; 对本项目的明确参数约定与推导见 [[gap-band-extremals]]. 重特征值须另处理子空间, 本卡不宣称二阶变分或全局极值性.

## 第七轮修订

R7-P01 修正了直接被谱隙文稿引用的归一化混淆. 上述微分推导和常势反例是当前使用依据; 旧卡及其历史引用保留在版本库. 数值检查仅验证选定实例, 局部 Lean 不覆盖算子可微性与无限维扰动理论.
