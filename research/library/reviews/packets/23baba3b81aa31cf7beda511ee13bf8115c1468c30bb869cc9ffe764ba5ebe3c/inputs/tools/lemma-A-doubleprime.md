---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c4c7-52f9-71e3-bc0b-ef3e30abb78e", "01a0c4c7-595b-7a40-9740-ec99ceb721a6", "01a0c4cc-45bc-77e1-8ce3-f79b2f3d31aa"], "conditions": ["Dirichlet symmetric [R,1,R], R>=1500,0<u<1/2,w>=2"], "created": "2026-08-07", "dependencies": [{"location": "tools/cot-series-certificate.md", "sha256": "d759e4c41a800237671d575306a6eacd84a15102244109fd9c58f9f05b4e3c90"}, {"location": "tools/delta-bracketing.md", "sha256": "a4b382f79d39c092c9e2be61f1f39174132a7ac77567b351121d84eb5e74f20b"}], "evidence_status": "ROUND8_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT", "resources": [{"kind": "exact-computation", "locator": "Fraction/Machin/Taylor scalar certificate, no full spectral formalization", "path": "research/artifacts/proof-audit-round8-20260922/certificate/certificate.py", "sha256": "39cd4b13019fddfc7342e9c2d56131de01686504944b444af0e3bb92301833d6"}, {"kind": "author-execution", "locator": "Exact scalar outputs; independent review receipt required", "path": "research/artifacts/proof-audit-round8-20260922/certificate/results.json", "sha256": "15723e490e332b4b979a1641f86fed216cc4232964fb2e5c0d3c5bd642cb7166"}], "source": "自研 (会话 30, run R-20260806T200000Z-inflimit-5B2C7D)", "sources": [{"locator": "Round8 corrected phases, A doubleprime, continuous sliver, T1/T2/T3 and fixed-u rate", "path": "docs/SL_gap_n1_inf_limit_proof.tex", "sha256": "a41e919dccd9d28f876a6d0cccf65a70a31fe4ba8b906f1ea46935bfc64a6b00"}], "status": "第八轮范围明确的修订; 检索复用由当前精确版本纠错回执控制", "summary": "R>=1500,w>=2 时 G>Dbar+ell/(R*u^3); 初等差量 d1>4alpha,d2<3alpha. 不覆盖薄层, 不依赖旧浮点证书.", "tags": ["mathtool", "self-developed"], "title": "大 w 区域的 INF 比较引理 A''", "tool_id": "lemma-A-doubleprime", "updated": "2026-09-22"}
---
# 大 w 区域的 INF 极限比较引理 A''

对称阱族 [R,1,R], R>=1500, 0<u<1/2, w=u*sqrt(R)>=2. 记 ell=1/2-u, epsilon=R^(-1/2), mu_k=R*lambda_k, G=mu_2-mu_1, a in (pi/2,pi) 满足 tan(a)=-a*ell/u, Dbar=(a^2-pi^2/4)/u^2. 第八轮初等修订给出

    G(R,u)>Dbar(u)+ell/(R*u^3)>Dbar(u).

先由无极点匹配方程、半区间正性和 w>=2 确定 0<theta_1<pi/2<theta_2<pi, 见 [相位卡](delta-bracketing.md). 令 c=epsilon*ell/u, alpha=ell/(R*u), t=a, theta=theta_2, v=u/ell=-t*cot(t). 有 z_2<pi/8, theta<t, epsilon<1/38, alpha<1/152. 定义

    d_1=pi^2/4-theta_1^2, d_2=t^2-theta^2,
    G-Dbar=(d_1-d_2)/u^2.

由 delta_1<1/76, theta_1>7/5, delta_1>99*alpha*theta_1/100,

    d_1>(29/10)*(7/5)*(99/100)*alpha>4*alpha.

余切余项 r(z)=(sin(z)-z*cos(z))/(z*sin(z)) 用积分和 sin(z)>=z-z^3/6 给出 0<r(z)<(7/20)z (0<z<=pi/8). 连续三角界为

    B(t)=2*t^4/(t^2+v^2+v)<2*(t*sin(t))^2<=8.

t<=2 时显然; t>=2 时 q=t*sin(t) 严格凹, sin(2)<91/100, cos(2)<-2/5 的交错 Taylor 界给 q(t)<91/50+(11/100)*(8/7)=681/350<2. 这覆盖整个 (pi/2,pi).

写 psi=t-theta, A=v/t, B=epsilon*cot(c*theta). 由

    A-B=-v*psi/(t*theta)+epsilon*r(c*theta),
    tan(psi)=(A-B)/(1+A*B),

保留正分母 D0-d, D0=1+v*(v+1)/(t*theta)>=1, d=(7/20)*epsilon^2*theta/t<1/1000. 对 theta 的单调性给出

    d_2<(7/20)*(1000/999)*8*alpha=2800*alpha/999<3*alpha.

故 G-Dbar>alpha/u^2, 且 d_2/d_1<3/4. 全部步骤使用连续估计及精确有理比较. 完整分母检查和证明见 [当前 INF 极限证明](../docs/SL_gap_n1_inf_limit_proof.tex).

旧链的 Cz<0.337、B(t)<=9 与比例<0.8256 另由第八轮精确有理证书重新支持, 可作辅助标量工具; 它们不再是本引理主链的必要依赖. [余切卡](cot-series-certificate.md) 给出更细常数和正确的 Laurent 展开. 旧脚本19的定向区间认证地位撤回, 历史字节保留.

本引理覆盖 w>=2 (包括等号), 不承担 w<2 的薄层排除, 不推出非对称族、全盒类下确界、全 R 刚性或 n>=2 结论. 局部 Lean 仅验证报告列明的局部声明, 不等于本谱不等式已完整形式化. 精确版本检验与放行见 [第八轮报告](../reports/proof-audit-round8-20260922/REPORT.md).
