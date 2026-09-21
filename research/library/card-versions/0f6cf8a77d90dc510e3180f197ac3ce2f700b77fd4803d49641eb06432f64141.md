---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c4c7-52f9-71e3-bc0b-ef3e30abb78e", "01a0c4c7-595b-7a40-9740-ec99ceb721a6", "01a0c4cc-45bc-77e1-8ce3-f79b2f3d31aa"], "conditions": ["Dirichlet symmetric [R,1,R],0<u<1/2", "Global lower bound for R>=1500; fixed-u expansions are uniform only on interior compact intervals"], "created": "2026-08-07", "dependencies": [{"location": "tools/delta-bracketing.md", "sha256": "a4b382f79d39c092c9e2be61f1f39174132a7ac77567b351121d84eb5e74f20b"}, {"location": "tools/lemma-A-doubleprime.md", "sha256": "a9d4f744d0617717187e522c6d24a0a6bd019fe4d32e69515a456d7f8637e5a0"}], "evidence_status": "ROUND8_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT", "resources": [{"kind": "exact-computation", "locator": "Fraction/Machin/Taylor scalar certificate, no full spectral formalization", "path": "research/artifacts/proof-audit-round8-20260922/certificate/certificate.py", "sha256": "39cd4b13019fddfc7342e9c2d56131de01686504944b444af0e3bb92301833d6"}, {"kind": "author-execution", "locator": "Exact scalar outputs; independent review receipt required", "path": "research/artifacts/proof-audit-round8-20260922/certificate/results.json", "sha256": "15723e490e332b4b979a1641f86fed216cc4232964fb2e5c0d3c5bd642cb7166"}], "source": "自研 (会话 30, run R-20260806T200000Z-inflimit-5B2C7D)", "sources": [{"locator": "Round8 corrected phases, A doubleprime, continuous sliver, T1/T2/T3 and fixed-u rate", "path": "docs/SL_gap_n1_inf_limit_proof.tex", "sha256": "a41e919dccd9d28f876a6d0cccf65a70a31fe4ba8b906f1ea46935bfc64a6b00"}], "status": "第八轮范围明确的修订; 检索复用由当前精确版本纠错回执控制", "summary": "对称阱族 R*m_R->M, 误差O(1/R), R*eta_R->0近极小化子趋于u*. 连续相位覆盖全部薄层; T1不依赖T3数值. 固定内部u首项C(u)/R.", "tags": ["mathtool", "self-developed"], "title": "对称阱族 INF 极限与连续相位比较", "tool_id": "inf-limit-comparison", "updated": "2026-09-22"}
---
# 对称阱族的 INF 极限与连续相位比较

模型为 Dirichlet 弦 -y''=lambda*rho*y, rho=[R,1,R], 两端重层长度 u, 0<u<1/2. 令 D_R=lambda_2-lambda_1, G=R*D_R, m_R=inf_u D_R, ell=1/2-u, epsilon=R^(-1/2), w=u/epsilon. 极限根 a in (pi/2,pi) 满足 tan(a)=-a*ell/u, Dbar=(a^2-pi^2/4)/u^2.

T2 的解析符号链给出 Dbar 的唯一极小点 u*. 端点行为为 u*Dbar(u)->4 (u->0), Dbar(u)->3*pi^2 (u->1/2), 故 M=Dbar(u*)<3*pi^2. T3 用精确 Fraction 区间、Machin 公式和 Taylor 余项单独定位:

    u* in [0.32992250812006654958, 0.32992250812006654960],
    M in [24.9438661384324768968, 24.9438661384324769084].

根像传播使用下端的下界、上端的上界; 普通超越函数值再加一次 nextafter 不构成当前证书.

T1 的新证明覆盖 R>=1500 的整个参数域:

- w>=2: [引理 A''](lemma-A-doubleprime.md) 给 G>Dbar+ell/(R*u^3)>=M.
- 0<w<=2: 连续展开相位给出 G>15*pi^2/4>3*pi^2>M, 包括 w->0、原曲边漏区以及 R 无穷尾部.
- 固定 u* 的点态展开给 G(R,u*)=M+O(1/R), 因而 0<=R*m_R-M=O(1/R) 且 R*m_R->M.
- 若 R_j->infinity, D_(R_j)(u_j)<=m_(R_j)+eta_j, eta_j>=0, R_j*eta_j->0, 则 u_j->u*. 原 eta_j=R_j^(-2) 是特例.

这里 T1 使用 T2 的解析严格余量, 不再依赖 T3 的高精度数值或旧二维矩形覆盖. 近极小化子论证分别排除 Dbar->infinity 与 Dbar->3*pi^2 两端.

可复用的新工具是整个 R>=1,0<u<1/2 上的相位速度界:

    G(R,u)>=pi^2/[2*epsilon*(w+ell)*(w+epsilon*ell)].

对射击接口向量 (y',k*y)=(cos(w*k),epsilon*sin(w*k)), 取连续展开辐角 A_epsilon. 半区间相位 Phi(k)=ell*k+A_epsilon(w*k), Phi'>0 且 Phi'<=ell+w/epsilon. 实际偶/奇基态满足 Phi(k1)=pi/2,Phi(k2)=pi; 分别控制 k2-k1 和 k1 后得到该界. 这避免了对奇模强加全域 theta_2>pi/2.

固定内部 u 的展开为

    G=Dbar+C(u)/R+O_u(R^-2),
    C=pi^2*b/(2*u^2)-2*a^4*b^3/[3*u^2*(1+b+b^2*a^2)], b=ell/u,
    C(u*)=pi^2*(1/2-u*)/[3*(u*)^3]>0.

余项在内部紧区间上一致. 这没有证明全端点一致展开、最优值的精确首项系数或极小化参数收敛率; 非零 R^(-1/2) 首项的旧表述已撤回.

完整证明见 [当前正文](../docs/SL_gap_n1_inf_limit_proof.tex), 精确算术、隔离检验、局部 Lean、失败记录和放行见 [第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md). 历史05/16/19证书与旧点抽样保留溯源, 不继续作为当前连续域认证. 结果仅限所述对称阱族; 不据此授予一般非对称族、全盒类或高阶间距结论. 新相位方法向其它分层模型的推广只是研究线索, 尚无通用定理.
